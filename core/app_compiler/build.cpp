// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
#include <iostream>
#include <vector>
#include "platform.h"

using namespace std;

void build(char device[]) {
    print("Built for {}", device);
}

int compile_sass(char *input_file, char *output_file) {
    const char *path = "./frontend/src";
    char command[256];
    snprintf(command, sizeof(command), "cd %s && sass --watch sass/%s compiled_css/%s", path, input_file, output_file);
    system(command);
    return 0;
}

int check_file_exist(char *__FILENAME__, char *__FILEPATH__) {
    FILE *file;
    char buf[0x100];
    snprintf(buf, sizeof(buf), "%s%s", __FILEPATH__, __FILENAME__);

    file = fopen(buf, "r");
    print("{} \n", buf);
    if (file) {
        print("File exists \n");
        return 0;
    } else {
        print("File does not exist \n");
        return 1;
    }
}

int build_app_files() {
    const char *af_path = "core/app_compiler/";
    char *required_compiled_files[] = {"server.cpp", "build.cpp"};
    char *compiled_files_name[] = {"server", "sc-build"};
    int length = sizeof(required_compiled_files) / sizeof(required_compiled_files[0]);
    char command[0x100];
    // snprintf(command, sizeof(command), "gcc %sserver.c -o server", af_path);
    snprintf(command, sizeof(command), "clang++ -Wall -std=c++23 %sserver.cpp -o server", af_path);
    system(command);

    print("These files have been compiled:\n");
    for (int i = 0; i < length; i++) {
        print("[{}] -> {} \n", required_compiled_files[i], compiled_files_name[i]);
    }
    return 0;
}

int main(int argc, char *argv[]) {
    char device_type[20] = "";

    if (isMac() == 0) {
        print("is mac device \n");
        strcpy(device_type, "Mac");
    }

    if (isWindows() == 0) {
        print("is windows device \n");
        strcpy(device_type, "Windows");
    }

    if (isLinux() == 0) {
        print("is linux device \n");
        strcpy(device_type, "Linux");
    }
    
    if (argv[1] == std::string("-c")) {
        if (check_file_exist(argv[2], "./frontend/src/sass/")==0 && check_file_exist(argv[3], "./frontend/src/compiled_css/")==0) {
            compile_sass(argv[2], argv[3]);
            print("\nFinished compiling {} -> {}", argv[2], argv[3]);
        }
    }

    if (argv[1] == std::string("-cb")) {
        build_app_files();
    }
    return 0;
}