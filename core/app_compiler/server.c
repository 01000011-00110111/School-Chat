// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
#include <stdio.h>
#include <stdlib.h>
#include "parser.h"

int start_frontend() {
    const char *path = "./frontend";
    char command[256];
    snprintf(command, sizeof(command), "cd %s && npm start", path);
    system(command);
    return 0;
}

int start_backend() {
    FILE *find_backend;
    find_backend = popen("python3 app.py", "w");
    return 0;
}

int main(int argc, char *argv[]) {
    if (strcmp(argv[1], "-df")==0) {
        paper("./core/config/keys.conf", "debug", "False");
        start_backend();
        start_frontend();
    }
    else if (strcmp(argv[1], "-dt")==0) {
        paper("./core/config/keys.conf", "debug", "True");
        start_backend();
        start_frontend();
    }
}