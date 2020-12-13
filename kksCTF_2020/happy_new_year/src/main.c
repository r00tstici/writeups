#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <netinet/in.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>

#include <sqlite3.h>

#include "lib/server.h"
#include "lib/md5.h"
#include "lib/sqlite_helper.h"

// Colors list
#define COLOR_RED     "\x1b[31m"
#define COLOR_GREEN   "\x1b[32m"
#define COLOR_YELLOW  "\x1b[33m"
#define COLOR_BLUE    "\x1b[34m"
#define COLOR_MAGENTA "\x1b[35m"
#define COLOR_CYAN    "\x1b[36m"
#define COLOR_RESET   "\x1b[0m"

// Some shit with buffering
__attribute__((constructor)) static void bufinit()
{
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);
}
// End shit with buffering

/*
    Start program logic
*/
// Welcome message...
void welcome(int sock)
{
    char *msg = COLOR_RED "Hi, this is secret Santa 🎅\n" COLOR_RESET;
    write(sock, msg, strlen(msg));
    msg = "You can send a " COLOR_RED "gift" COLOR_RESET " to a stranger and make him a pleasant " COLOR_GREEN "surprise" COLOR_RESET " for the new year 🎊.\n";
    write(sock, msg, strlen(msg));
}

// 
// Register and login function
// 
int show_login_menu(int sock)
{
    char options[2];
    char* message = COLOR_RED "\n====================\n" COLOR_RESET \
                    COLOR_GREEN "[1] " COLOR_RESET "Sign up\n"\
                    COLOR_GREEN "[2] " COLOR_RESET "Sign in\n"\
                    COLOR_GREEN "[3] " COLOR_RESET "Exit\n\n"\
                    COLOR_YELLOW "Option> " COLOR_RESET;
    write(sock, message, strlen(message));
    read(sock, options, 2);
    return options[0];
}

int reg_user(int sock, char* user)
{
    char username[100] = {0};
    char password[100] = {0};
    uint8_t result[16];
    char *hash = calloc(33, sizeof(char));
    char msg[256] = {0};

    write(sock, "Enter username: ", 17);
    read(sock, username, 99);
    write(sock, "Enter password: ", 17);
    read(sock, password, 99);
    username[strlen(username) - 1] = 0;
    password[strlen(password) - 1] = 0;

    // Check username
    // Very shitty check
    if(strstr(username, "`") ||strstr(username, "'") || strstr(username, "\"") || strstr(username, "(") || strstr(username, ")") || strstr(username, "#") || strstr(username, "--"))
    {
        char* msg = COLOR_RED "Bad username! Evil h4ck3r 👿\n" COLOR_RESET;
        write(sock, msg, strlen(msg));
        strcpy(user, "");
        return 1;
    }
    // Generate md5 from password and convert it to hex
    md5((uint8_t*)password, strlen(password), result);
    for(size_t i = 0; i < 16; i++)
        sprintf(hash + i*2, "%02x", result[i]);
    hash[32] = '\0';

    // Reg user in database
    int res = sql_reg_user(username, hash, msg);
    if(!res)
    {
        write(sock, msg, strlen(msg));
        strcpy(user, username);
    }else
    {
        write(sock, msg, strlen(msg));
        strcpy(user, "");
    }
    
    // Prevent use after free
    free(hash);
    hash = NULL;

    return 0;
}

int login_user(int sock, char* user)
{
    char username[100] = {0};
    char password[100] = {0};
    char msg[128] = {0};

    write(sock, "Enter username: ", 17);
    read(sock, username, 99);
    write(sock, "Enter password: ", 17);
    read(sock, password, 99);
    username[strlen(username) - 1] = 0;
    password[strlen(password) - 1] = 0;

    // Shitty check for "prevent" sql injection
    if(strstr(username, "`") ||strstr(username, "'") || strstr(username, "\"") || strstr(username, "(") || strstr(username, ")") || strstr(username, "#") || strstr(username, "--"))
    {
        char* msg = COLOR_RED "Bad username! Evil h4ck3r 👿\n" COLOR_RESET;
        write(sock, msg, strlen(msg));
        strcpy(user, "");
        return 1;
    }

    uint8_t result[16];
    char *hash = calloc(33, sizeof(char));
    md5((uint8_t*)password, strlen(password), result);
    for(size_t i = 0; i < 16; i++)
        sprintf(hash + i*2, "%02x", result[i]);
    hash[32] = '\0';

    int res = sql_login_user(username, hash, msg);

    write(sock, msg, strlen(msg));
    if(res)
        strcpy(user, username);

    return 0;
}

// 
// User cabinte
// 
int show_logged_menu(int sock)
{
    char options[2];
    char *message = COLOR_RED "\n====================\n" COLOR_RESET \
                    COLOR_GREEN "[1] " COLOR_RESET "Send a secret message, secret Santa will deliver it 🎅🎁🎅🎁\n"\
                    COLOR_GREEN "[2] " COLOR_RESET "Inbox\n"\
                    COLOR_GREEN "[3] " COLOR_RESET "Show participants\n"\
                    COLOR_GREEN "[4] "COLOR_RESET "Exit\n\n" \
                    COLOR_YELLOW "Option> " COLOR_RESET;
    write(sock, message, strlen(message));
    read(sock, options, 2);
    return options[0];
}

void show_participants(int sock)
{
    char *msg = COLOR_RED "\n====================\n" COLOR_RESET\
                "Participants:\n";
    char peoples[7168] = {0};
    write(sock, msg, strlen(msg));
    sql_show_participants(peoples);
    write(sock, peoples, strlen(peoples));
}

int send_message(int sock, char* fromuser)
{
    char *label = COLOR_RED "\n====================\n"COLOR_RESET \
                  "Yohohoho! Who will be honored with your letter?\nEnter username: ";
    char touser[100] = {0};
    char msg[2048] = {0};
    char response[256] = {0};

    write(sock, label, strlen(label));
    read(sock, touser, 99);
    touser[strlen(touser) - 1] = 0;

    write(sock, "What do you wish him in the coming year?\nInput message: ", 57);
    read(sock, msg, 2047);
    msg[strlen(msg) - 1] = 0;

    // Shitty check for "prevent" sql injection
    if(strstr(touser, "`") ||strstr(touser, "'") || strstr(touser, "\"") || strstr(touser, "(") || strstr(touser, ")") || strstr(touser, "#") || strstr(touser, "--"))
    {
        char* msg = COLOR_RED "Bad username! Evil h4ck3r 👿\n" COLOR_RESET;
        write(sock, msg, strlen(msg));
        return 1;
    }

    sql_send_message(touser, msg, response);
    write(sock, response, strlen(response));

    return 0;
}

void show_inbox(int sock, char* username)
{
    char messages[5120] = {0};
    char *label = COLOR_RED "\n====================\n"COLOR_RESET \
                  "Yohohoho!\nYour inbox:\n";
    write(sock, label, strlen(label));
    sql_show_inbox(username, messages);

    if (strcmp(messages, "") == 0)
        write(sock, "Sorry, but you haven't messsages 😔", 38);
    else
        write(sock, messages, strlen(messages));
}

int show_santa_menu(int sock, char* flag)
{
    char options[2];
    if(strcmp(flag, "") == 0)
        sql_get_flag(flag);

    char message[1024];
    sprintf(message, COLOR_RED "\n====================\n" COLOR_RESET "%s\nSanta Menu🎅\n" COLOR_GREEN "[1] " COLOR_RESET "Show all messages\n" COLOR_GREEN "[2] " COLOR_RESET "Inbox \n" COLOR_GREEN "[3] " COLOR_RESET "Send message\n" COLOR_GREEN "[4] " COLOR_RESET "Relax\n\n" COLOR_YELLOW "Option> " COLOR_RESET, flag);
    write(sock, message, strlen(message));
    read(sock, options, 2);
    return options[0];

}

void show_all_messages(int sock)
{
    char *msg = COLOR_YELLOW "Spying on others isn't good⛔, even though you're kks Santa🕵️\n" COLOR_RESET;
    write(sock, msg, strlen(msg));
}

void to_relax(int sock, int* drinks)
{
    char *msg = COLOR_RED "\n====================\n" COLOR_RESET \
                "Relax and have a beer🍻?\n"\
                "Yes\tYes\n";
    char info[32];

    (*drinks)++;
    sprintf(info, "Already drunk: %d!🍺\n", *drinks);
    write(sock, msg, strlen(msg));
    write(sock, info, strlen(info));

    if(*drinks == 4)
        write(sock, "This is just the beginning, isn't it 😉?\n", 44);
    else if (*drinks == 8)
        write(sock, "Is the holiday knocking on our door🎊?\n", 42);
    else if (*drinks == 16)
        write(sock, "Sure enough, he's already at the door🎉\n", 43);
    else if (*drinks == 32)
        write(sock, "Oh yeah, do you smell that tangerine smell on new year's eve🍊\n", 66);
    else if (*drinks == 64)
        write(sock, "Isn't it time to end the holiday, my friend😳?\n", 50);
    else if (*drinks == 128)
        write(sock, "Dude, you're a real beast, I can tell you were preparing for the New year!🤯🤯🤯🤯\n", 92);
}

void start_app(int sock)
{
    unsigned int drinks = 0;
    char flag[128] = {0};
    char username[100] = {0};
    welcome(sock);
    while(1)
    {
        if(!strcmp(username, ""))
        {
            char options = show_login_menu(sock); 
            switch (options)
            {
            case '1':
                reg_user(sock, username);
                break;
            case '2':
                login_user(sock, username);
                break;
            case '3':
                write(sock, "Goodbye!\n", 10);
                exit(1);
            default:
                break;
            }
        } else if(!strcmp(username, "kks_santa"))
        {
            char options = show_santa_menu(sock, flag);
            if (drinks == 128 && options == 'k')
            {
                write(sock, "\nYou are really kks santa!\n", 28);

                // Shitty shell, but why not?
                FILE *fp;
                while(1)
                {
                    char cmd[512] = {0};
                    write(sock, "$ ", 3);
                    read(sock, cmd, 127);
                    fp = popen(cmd, "r");
                    while(fgets(cmd, 512, fp) != NULL)
                        write(sock, cmd, strlen(cmd));
                }
            }
            switch (options)
            {
            case '1':
                show_all_messages(sock);
                break;
            case '2':
                show_inbox(sock, username);
                break;
            case '3': 
                send_message(sock, username);
                break;
            case '4':
                to_relax(sock, &drinks);
                break;
            default:
                break;
            }
        } else
        {
            char options = show_logged_menu(sock);
            switch (options)
            {
            case '1':
                send_message(sock, username);
                break;
            case '2':
                show_inbox(sock, username);
                break;
            case '3':
                show_participants(sock);
                break;
            case '4':
                write(sock, "Goodbye!\n", 10);
                exit(1);
            default:
                break;
            }
        }
    }
    exit(0);
}

// Main function for run program
int main(int argc, char** argv)
{
    if ( argc < 2 )
    {
        printf("Usage: %s <port>", argv[0]);
        exit(0);
    }

    run(atoi(argv[1]));
    return 0;
}
