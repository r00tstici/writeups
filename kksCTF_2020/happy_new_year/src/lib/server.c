#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>

extern void start_app(int);

// Run server
// Function accept ip and port value from argc
int run(int port)
{
   int sockfd, newsockfd, clilen;
   struct sockaddr_in serv_addr;
   struct sockaddr_in cli_addr;
   int pid;
   
   /* First call to socket() function */
   sockfd = socket(AF_INET, SOCK_STREAM, 0);
   
   if (sockfd < 0) {
        perror("ERROR opening socket");
        exit(1);
   } else{
       printf("Server started on port %d!\n", port);
   }
   
   /* Initialize socket structure */
   bzero((char *) &serv_addr, sizeof(serv_addr));
   
   serv_addr.sin_family = AF_INET;
   serv_addr.sin_addr.s_addr = INADDR_ANY;
   serv_addr.sin_port = htons(port);
   
   /* Now bind the host address using bind() call.*/
   if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {
      perror("ERROR on binding");
      exit(1);
   }
   
   /* Now start listening for the clients, here
      * process will go in sleep mode and will wait
      * for the incoming connection
   */
   
   listen(sockfd,300);
   clilen = sizeof(cli_addr);
   
   while (1) {
      newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
		
      if (newsockfd < 0) {
        perror("ERROR on accept");
        exit(1);
      } else {
          printf("Client %s:%d connected!\n", inet_ntoa(cli_addr.sin_addr), (int)htons(cli_addr.sin_port));
      }
      
      /* Create child process */
      pid = fork();
		
      if (pid < 0) {
         perror("ERROR on fork");
         exit(1);
      }
      
      if (pid == 0) {
         /* This is the client process */
         close(sockfd);
         start_app(newsockfd);
         exit(0);
      }
      else {
        close(newsockfd);
      }
		
   } /* end of while */
}
