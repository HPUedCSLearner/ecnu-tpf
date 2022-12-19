#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h> 

sqlite3 *db;
char *zErrMsg = 0;

static int callback(void *NotUsed, int argc, char **argv, char **azColName);

int __sqlite3_open(const char *filename) {
    /* Open database */
   int rc = sqlite3_open(filename, &db);
   if( rc ){
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
   }else{
        fprintf(stdout, "Opened database successfully\n");
   }
   return rc;
}

int __sqlite3_exec(const char *sqlstr) {
    /* Execute SQL statement */
   int rc = sqlite3_exec(db, sqlstr, callback, 0, &zErrMsg);
   if( rc != SQLITE_OK ){
   fprintf(stderr, "SQL error: %s\n", zErrMsg);
      sqlite3_free(zErrMsg);
   }else{
      fprintf(stdout, "Table created successfully\n");
   }
   sqlite3_close(db);
   return rc;
}

void __sqlite3_close() {
    sqlite3_close(db);
}



static int callback(void *NotUsed, int argc, char **argv, char **azColName){
   int i;
   for(i=0; i<argc; i++){
      printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
   }
   printf("\n");
   return 0;
}

