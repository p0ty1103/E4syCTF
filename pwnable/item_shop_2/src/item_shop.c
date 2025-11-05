#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <seccomp.h>
#include <linux/seccomp.h>

void *items[10];
int item_count = 0;

void initialize_seccomp() {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    if (ctx == NULL) {
        perror("seccomp_init");
        exit(1);
    }
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(brk), 0);

    if (seccomp_load(ctx) < 0) {
        perror("seccomp_load");
        exit(1);
    }
    seccomp_release(ctx);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    puts("========================================");
    puts("    Welcome to the Secret Item Shop!");
    puts("========================================");
}

void menu() {
    puts("\nWhat would you like to do?");
    puts("1. Buy an item");
    puts("2. Discard an item");
    puts("3. Enhance an item");
    puts("4. Check inventory");
    puts("5. Leave the shop");
    printf("> ");
}

void buy_item() {
    if (item_count >= 10) {
        puts("You can't carry any more items!");
        return;
    }
    printf("Choose the size of your item (16-128): ");
    int size;
    scanf("%d", &size);
    if (size < 16 || size > 128) {
        puts("We don't sell items of that size.");
        return;
    }

    items[item_count] = malloc(size);
    if (!items[item_count]) {
        puts("Error: Failed to create item.");
        exit(1);
    }
    printf("You got item %d! Please write something in it.\n> ", item_count);
    read(0, items[item_count], size);
    puts("Thank you for your purchase!");
    item_count++;
}

void discard_item() {
    printf("Which item do you want to discard? (0-%d): ", item_count - 1);
    int idx;
    scanf("%d", &idx);
    if (idx < 0 || idx >= item_count) {
        puts("You don't have such an item.");
        return;
    }

    free(items[idx]);
    puts("Item discarded.");
    // items[idx] = NULL;
}

void enhance_item() {
    printf("Which item do you want to enhance? (0-%d): ", item_count - 1);
    int idx;
    scanf("%d", &idx);
    if (idx < 0 || idx >= item_count || items[idx] == NULL) {
        puts("You don't have such an item.");
        return;
    }

    printf("Imbuing the item with new power...\n> ");
    read(0, items[idx], 8);
    puts("Enhancement complete!");
}

void check_items() {
    puts("--- Inventory List ---");
    for (int i = 0; i < item_count; i++) {
        if (items[i] != NULL) {
            printf("Item %d: ", i);
            write(1, items[i], 8);
            puts("");
        }
    }
    puts("----------------------");
}

int main() {
    initialize_seccomp();
    setup();
    int choice;
    while (1) {
        menu();
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                buy_item();
                break;
            case 2:
                discard_item();
                break;
            case 3:
                enhance_item();
                break;
            case 4:
                check_items();
                break;
            case 5:
                puts("Please come again!");
                return 0;
            default:
                puts("Invalid menu option.");
                break;
        }
    }
    return 0;
}