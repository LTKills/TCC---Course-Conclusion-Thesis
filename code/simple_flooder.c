#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>

#include <mqtt.h>
#include "templates/posix_sockets.h"


/**
 * @brief The function that would be called whenever a PUBLISH is received.
 *
 * @note This function is not used in this example.
 */
void publish_callback(void** unused, struct mqtt_response_publish *published);

/**
 * @brief The client's refresher. This function triggers back-end routines to
 *        handle ingress/egress traffic to the broker.
 *
 * @note All this function needs to do is call \ref __mqtt_recv and
 *       \ref __mqtt_send every so often. I've picked 100 ms meaning that
 *       client ingress/egress traffic will be handled every 100 ms.
 */
void* client_refresher(void* client);

/**
 * @brief Safelty closes the \p sockfd and cancels the \p client_daemon before \c exit.
 */
void exit_example(int status, int sockfd, pthread_t *client_daemon);


// Variable and function used when checking for Ctrl-D (stop) signal
volatile sig_atomic_t keepFlooding = 1;
void stopFlooding(int signum) {
    keepFlooding = 0;
}

/**
 * A simple program that publishes trash with QoS 2 (highest) to flood the specified topic.
 */

int main(int argc, const char *argv[]) {
    const char* addr = "localhost";
    const char* port;
    const char* topic;

    if(argc != 2 && argc != 3) {
        printf("usage: %s topic [port]\n", argv[0]);
        return 1;
    }

    // get port number (argv[2] if present)
    if(argc == 3)
        port = argv[2];
    else
        port = "1883";

    // get the topic name to publish
    topic = argv[1];

    /* open the non-blocking TCP socket (connecting to the broker) */
    int sockfd = open_nb_socket(addr, port);

    if (sockfd == -1) {
        perror("Failed to open socket: ");
        exit_example(EXIT_FAILURE, sockfd, NULL);
    }

    /* setup a client */
    struct mqtt_client client;
    uint8_t sendbuf[2048]; /* sendbuf should be large enough to hold multiple whole mqtt messages */
    uint8_t recvbuf[1024]; /* recvbuf should be large enough any whole mqtt message expected to be received */
    mqtt_init(&client, sockfd, sendbuf, sizeof(sendbuf), recvbuf, sizeof(recvbuf), publish_callback);
    mqtt_connect(&client, "publishing_client", NULL, NULL, 0, NULL, NULL, 0, 400);

    /* check that we don't have any errors */
    if (client.error != MQTT_OK) {
        fprintf(stderr, "error: %s\n", mqtt_error_str(client.error));
        exit_example(EXIT_FAILURE, sockfd, NULL);
    }

    /* start a thread to refresh the client (handle egress and ingree client traffic) */
    pthread_t client_daemon;
    if(pthread_create(&client_daemon, NULL, client_refresher, &client)) {
        fprintf(stderr, "Failed to start client daemon.\n");
        exit_example(EXIT_FAILURE, sockfd, NULL);

    }

    /* start publishing the time */
    printf("%s is ready to begin flooding.\n", argv[0]);
    printf("Press CTRL-C to exit.\n\n");

    /* build flood message */
    char application_message[256] = "This is a flood message\n";
    snprintf(application_message, sizeof(application_message), "This is a flood message\n");

    // Check for Ctrl-C, stop running
    signal(SIGINT, stopFlooding);

    for(unsigned long long int i = 0; keepFlooding; i++) {

        // Print number of published messages from time to time
        if(i % 1000 == 0)
            printf("%s: published %llu messages\n", argv[0], i);

        // publish flood message with QoS 2 (highest)
        mqtt_publish(&client, topic, application_message, strlen(application_message) + 1, MQTT_PUBLISH_QOS_2);

        /* check for errors */
        if (client.error != MQTT_OK) {
            fprintf(stderr, "error: %s\n", mqtt_error_str(client.error));
            exit_example(EXIT_FAILURE, sockfd, &client_daemon);
        }
    }

    /* disconnect */
    printf("\n%s disconnecting from %s\n", argv[0], addr);
    sleep(1);

    /* exit */
    exit_example(EXIT_SUCCESS, sockfd, &client_daemon);
}

void exit_example(int status, int sockfd, pthread_t *client_daemon) {
    if (sockfd != -1) close(sockfd);
    if (client_daemon != NULL) pthread_cancel(*client_daemon);
    exit(status);
}



void publish_callback(void** unused, struct mqtt_response_publish *published) {
    /* not used in this example */
}

void* client_refresher(void* client) {
    while(1)
    {
        mqtt_sync((struct mqtt_client*) client);
        usleep(100000U);
    }
    return NULL;
}