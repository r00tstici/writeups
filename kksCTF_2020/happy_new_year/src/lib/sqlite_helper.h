#ifndef SQLITE_HELPER_H
#define SQLITE_HELPER_H

static int callback(void *NotUsed, int argc, char **argv, char **azColName);
int sql_reg_user(char* user, char* hash, char* msg);
void sql_send_message(char* touser, char* msg, char* response);

int sql_login_user(char* user, char* hash, char* msg);
static int callback_for_login(void *data, int argc, char **argv, char **azColName);

void sql_show_inbox(char* username, char* msg);
static int callback_for_show_inbox(void *data, int argc, char **argv, char **azColName);

void sql_get_flag(char* key);
static int callback_for_get_flag(void *data, int argc, char **argv, char **azColName);

void sql_show_participants(char *peoples);
static int callback_for_show_participants(void *data, int argc, char **argv, char **azColName);

#endif
