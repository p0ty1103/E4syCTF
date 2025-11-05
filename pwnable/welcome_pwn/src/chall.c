#include <stdio.h>
#include <stdlib.h>

void win() {
    system("cat flag.txt");
}

void vuln() {
    char buffer[32];
    puts("What's your name?");
    gets(buffer);
    printf("Hello, %s!\n", buffer);
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    vuln();

    return 0;
}