// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
#include <stdio.h>
#include <stdlib.h>

int isMac() {
    #ifdef __APPLE__
        return 0;
    #endif
    return 1;
}

int isWindows() {
    #ifdef _Win32
        return 0;
    #endif
    return 1;
}

int isLinux() {
    #ifdef __linux__
        return 0;
    #endif
    return 1;
}