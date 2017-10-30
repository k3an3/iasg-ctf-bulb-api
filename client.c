#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>

const char flag[] = "flag{lol}";
struct sockaddr_in remote_addr, listen_addr;

int main()
{
	/* Struct to hold host info after resolving */
	struct addrinfo* ai;
	/* Buffer for received data */
	char buff[2048];
	/* Temp integer vars */
	int n, sock, listen_sock, s, remote_addr_len = sizeof(remote_addr);

	/* Create the socket descriptor */
	sock = socket(AF_INET, SOCK_STREAM, 0);
	/* Set socket options */
	setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, (void *)1, sizeof(int));

	/* Get addr info from the given hostname/addr, save
	 * to addrinfo struct. Replace 6010 with port. */
	if (getaddrinfo("199.100.16.99", "6010", NULL, &ai)) {
		perror("Could not resolve host");
		exit(1);
	}

	/* Attempt to connect to the server */
	if(connect(sock, ai->ai_addr, ai->ai_addrlen) < 0) {
		 perror("Could not connect");
		 exit(1);
	}

	send(sock, flag, strlen(flag), 0);

	close(s);
}
