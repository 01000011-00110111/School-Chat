// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
#include <iostream>
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

    for (int i = 0; i < argc; i++) {

        if (argv[i] == std::string("-debug")) {
            paper("./core/config/keys.conf", "debug", "True");
            std::print("Debug: true");
        } 
        // else if (argv[i] == std::string("-nodebug")) {
        //     paper("./core/config/keys.conf", "debug", "False");
        //     std::print("Debug: false");
        // }

        if (argv[i] == std::string("--run")) {
            start_backend();
            start_frontend();
            paper("./core/config/keys.conf", "debug", "False");
            std::print("Debug: false");
        }

    }

    return 0;
}