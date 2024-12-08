// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 256

int paper(char *config_file, char *key, char *value) {
    FILE *fp, *fp_temp;
    char line[MAX_LINE_LENGTH];
    char temp_file[] = "temp.ini";

    fp = fopen(config_file, "r");
    fp_temp = fopen(temp_file, "w");

    if (fp == NULL || fp_temp == NULL) {
        perror("Error opening file");
        return 1;
    }

    while (fgets(line, MAX_LINE_LENGTH, fp) != NULL) {
        if (strstr(line, key) != NULL) {
            fprintf(fp_temp, "%s=%s\n", key, value);
        } else {
            fprintf(fp_temp, "%s", line);
        }
    }

    fclose(fp);
    fclose(fp_temp);

    remove(config_file);
    rename(temp_file, config_file);

    return 0;
}