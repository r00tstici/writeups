#include <sqlite3.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int callback(void *NotUsed, int argc, char **argv, char **azColName)
{
    for(int i=0; i < argc; i++)
        printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
    return 0;
}

static int callback_for_login(void *data, int argc, char **argv, char **azColName)
{
    strcpy((char*)data, argv[0]);
    return 0;
}

static int callback_for_show_inbox(void *data, int argc, char **argv, char **azColName)
{
    char tmp[2048] = {0};
    sprintf(tmp, "Letter: %s\n", argv[1] ? argv[1] : "No messsages 😔");
    strcat((char*)data, tmp);
    return 0;
}

static int callback_for_get_flag(void *data, int argc, char **argv, char **azColName)
{
    strcpy((char*)data, argv[0]);
    return 0;
}

static int callback_for_show_participants(void *data, int argc, char **argv, char **azColName)
{
    char tmp[100] = {0};
    sprintf(tmp, "* %s\n", argv[0] ? argv[0] : "No user 😔");
    strcat((char*)data, tmp);
    return 0;
}

// Reg user in database
int sql_reg_user(char* user, char* hash, char* msg)
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc; 

    rc = sqlite3_open("db/profiles.db", &db);

    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        exit(1);
    }

    char query[1024];
    sprintf(query, "INSERT INTO users VALUES ('%s', '%s');", user, hash);

    rc = sqlite3_exec(db, query, callback, 0, &zErrMsg);
    if( rc != SQLITE_OK )
    {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
        strcpy(msg, "A user with this name already exists 😔\n");
        sqlite3_close(db);
        return 1;
    }else
    {
        strcpy(msg, "You have successfully registered 😉\n");
        fprintf(stdout, "User %s created successfully\n", user);
        sqlite3_close(db);
        return 0;
    }
}

// Login user...
int sql_login_user(char* user, char* hash, char* msg)
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc; 
    char hash_from_db[32];

    rc = sqlite3_open("db/profiles.db", &db);

    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        exit(1);
    }

    char sql[256];
    sprintf(sql, "SELECT password from users where username == '%s';", user);
    rc = sqlite3_exec(db, sql, callback_for_login, (void*) hash_from_db, &zErrMsg);

    if( rc != SQLITE_OK )
    {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
        strcpy(msg, "Oops, some error!\n");
    }else
    {
        if(strcmp(hash, hash_from_db) == 0)
        {
            strcpy(msg, "Logged in!\n");
            sqlite3_close(db);
            return 1;
        }else{
            strcpy(msg, "Failed login 🗿\n");
            sqlite3_close(db);
            return 0;
        }
    }
}

// Send message from user
void sql_send_message(char* touser, char* msg, char* response)
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc; 
    char *hash_from_db;

    rc = sqlite3_open("db/profiles.db", &db);

    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        exit(1);
    }

    // "||(SELECT group_concat(password, ':') from users)||" -- payload
    char query[4096];
    sprintf(query, "INSERT INTO messages (to_user, letter) VALUES (\"%s\",\"%s\");", touser, msg);

    rc = sqlite3_exec(db, query, callback, 0, &zErrMsg);
    if( rc != SQLITE_OK )
    {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
        strcpy(response, "Something wrong!\n");
    }else
        strcpy(response, "Congratulations, your letter has already been delivered!\nHappy new year to you! Yohohoho🎅\n");

    sqlite3_close(db);
}

void sql_show_inbox(char* username, char* msg)
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc; 
    char *hash_from_db;

    rc = sqlite3_open("db/profiles.db", &db);

    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        exit(1);
    }

    char sql[256];
    sprintf(sql, "SELECT * from messages WHERE to_user == '%s';", username) ;

    rc = sqlite3_exec(db, sql, callback_for_show_inbox, msg, &zErrMsg);
    if( rc != SQLITE_OK )
    {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    }

    sqlite3_close(db);
}

void sql_get_flag(char* key)
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc; 
    char *hash_from_db;

    rc = sqlite3_open("db/profiles.db", &db);

    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        exit(1);
    }

    char sql[1024];
    sprintf(sql, "SELECT key from key;");
    rc = sqlite3_exec(db, sql, callback_for_get_flag, (void*)key, &zErrMsg);
    if( rc != SQLITE_OK )
    {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    }
    sqlite3_close(db);
}

void sql_show_participants(char *peoples)
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc; 
    char *hash_from_db;

    rc = sqlite3_open("db/profiles.db", &db);

    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        exit(1);
    }

    char sql[64] = "SELECT username from users where username != 'kks_santa';";

    rc = sqlite3_exec(db, sql, callback_for_show_participants, (void*)peoples, &zErrMsg);
    if( rc != SQLITE_OK )
    {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    }
    sqlite3_close(db);
}
