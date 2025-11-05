#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

char board[5][5];

void win() {
    puts("\nCongratulations!!");
    system("cat flag.txt");
    fflush(stdout);
    exit(0);
}

void initialize_board() {
    memset(board, '.', sizeof(board));
}

void print_board() {
    puts("\n  1 2 3 4 5  <- x");
    for (int i = 0; i < 5; i++) {
        printf("%d ", i + 1);
        for (int j = 0; j < 5; j++) {
            printf("%c ", board[i][j]);
        }
        puts("");
    }
    puts("^ y");
    fflush(stdout);
}

int check_winner(char player) {
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == player && board[i][j+1] == player && board[i][j+2] == player) return 1;
        }
    }
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 5; j++) {
            if (board[i][j] == player && board[i+1][j] == player && board[i+2][j] == player) return 1;
        }
    }
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == player && board[i+1][j+1] == player && board[i+2][j+2] == player) return 1;
        }
    }
    for (int i = 0; i < 3; i++) {
        for (int j = 2; j < 5; j++) {
            if (board[i][j] == player && board[i+1][j-1] == player && board[i+2][j-2] == player) return 1;
        }
    }
    return 0;
}

void player_turn(char player_piece) {
    char buf[64];
    int x, y;

    printf("\nYour turn ('%c'). Enter coordinate (x,y): ", player_piece);
    fflush(stdout);

    read(0, buf, 256);

    if (sscanf(buf, "(%d,%d)", &x, &y) == 2 && x >= 1 && x <= 5 && y >= 1 && y <= 5) {
        if (board[y - 1][x - 1] == '.') {
            board[y - 1][x - 1] = player_piece;
        } else {
            puts("That spot is already taken.");
            fflush(stdout);
        }
    } else {
        puts("Invalid format.");
        printf("Your input: ");
        printf(buf);
        fflush(stdout);
    }
}

void cpu_turn(char cpu_piece) {
    int x, y;
    int placed = 0;
    int is_full = 1;

    for(int i = 0; i < 5; ++i) {
        for(int j = 0; j < 5; ++j) {
            if(board[i][j] == '.') {
                is_full = 0;
                break;
            }
        }
        if(!is_full) break;
    }
    if(is_full) return;

    printf("\nCPU's turn ('%c')...", cpu_piece);
    fflush(stdout);

    do {
        x = rand() % 5;
        y = rand() % 5;
        if (x >= 1 && x <= 3 && y >= 1 && y <= 3) {
            continue;
        }
        if (board[y][x] == '.') {
            placed = 1;
        }
    } while (!placed);

    board[y][x] = cpu_piece;
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    srand(time(NULL));
    initialize_board();

    puts("Welcome to Vulnerable Gomoku!");
    puts("The first to get 3 in a row wins.");

    char player_piece, cpu_piece;
    if (rand() % 2 == 0) {
        player_piece = 'O';
        cpu_piece = 'X';
    } else {
        player_piece = 'X';
        cpu_piece = 'O';
    }
    printf("You are '%c'. CPU is '%c'.\n", player_piece, cpu_piece);

    while(1) {
        print_board();
        player_turn(player_piece);

        if (check_winner(player_piece)) {
            print_board();
            puts("\nYou win the game!");
            fflush(stdout);
            exit(0);
            break;
        }

        cpu_turn(cpu_piece);
        if (check_winner(cpu_piece)) {
            print_board();
            puts("\nCPU wins the game!");
            fflush(stdout);
            exit(0);
            break;
        }
    }

    return 0;
}