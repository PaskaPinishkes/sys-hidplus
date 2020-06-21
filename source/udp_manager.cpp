// Most of the UDP code comes from hid-mitm: https://github.com/jakibaki/hid-mitm

#include "udp_manager.hpp"
#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

#define PORT 8000

static int sockfd = -1;

struct sockaddr_in servaddr, cliaddr;

void setup_socket()
{
    if (sockfd != -1)
        close(sockfd);
    
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0)
    {
        perror("failed to create the socket");
        exit(EXIT_FAILURE);
    }

    struct timeval read_timeout;
    read_timeout.tv_sec = 0;
    read_timeout.tv_usec = 100000;
    setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &read_timeout, sizeof read_timeout);

    memset(&servaddr, 0, sizeof(servaddr));
    memset(&cliaddr, 0, sizeof(cliaddr));

    servaddr.sin_family = AF_INET; // IPv4 address
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(PORT);

    bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr));
}

static u32 curIP = 0;
static int failed = 11;
static int counter = 0;
static input_message cached_message = {0};
u64 last_time;

int poll_udp_input(input_message *buf)
{
    // Just as mentioned before, most (if not all) of the code in the previous and current function comes from hid_mitm, so if you want to check how everything
    // works, I recommend you to check it out, it's pretty cool and well documented!
    if (++counter != 3)
    {
        if (failed > 10)
            return -1;
        *buf = cached_message;
        return 0;
    }
    counter = 0;

    u64 tmp_time = svcGetSystemTick();
    if (tmp_time - last_time > (19200000 / 10))
    {
        svcSleepThread(5e+8L);
        setup_socket();
        curIP = gethostid();
        tmp_time = svcGetSystemTick();
    }
    last_time = tmp_time;

    if (failed > 10 && failed % 10 != 0)
    {
        failed++;
        return -1;
    }

    if (curIP != gethostid())
    {
        setup_socket();
        curIP = gethostid();
    }

    socklen_t len;
    int n;
    input_message temp_message;
    n = recvfrom(sockfd, &temp_message, sizeof(input_message),
                 MSG_WAITALL, (struct sockaddr *)&cliaddr,
                 &len);
    if (n <= 0 || temp_message.magic != INPUT_MSG_MAGIC)
    {
        failed++;
    }
    else
    {
        failed = 0;
        cached_message = temp_message;
    }
    *buf = cached_message;

    if (failed >= 10)
    {
        return -1;
    }

    return 0;
}