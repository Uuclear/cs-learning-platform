#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME 50
#define MAX_PHONE 20
#define MAX_EMAIL 100
#define CONTACTS_FILE "contacts.dat"

typedef struct {
    int id;
    char name[MAX_NAME];
    char phone[MAX_PHONE];
    char email[MAX_EMAIL];
} Contact;

// 添加联系人
int add_contact() {
    FILE *fp = fopen(CONTACTS_FILE, "ab");
    if (fp == NULL) {
        perror("无法打开通讯录文件");
        return -1;
    }

    Contact new_contact;

    // 获取下一个ID
    FILE *read_fp = fopen(CONTACTS_FILE, "rb");
    if (read_fp == NULL) {
        new_contact.id = 1;
    } else {
        Contact temp;
        new_contact.id = 0;
        while (fread(&temp, sizeof(Contact), 1, read_fp) == 1) {
            if (temp.id > new_contact.id) {
                new_contact.id = temp.id;
            }
        }
        new_contact.id++;
        fclose(read_fp);
    }

    printf("请输入姓名: ");
    fgets(new_contact.name, MAX_NAME, stdin);
    new_contact.name[strcspn(new_contact.name, "\n")] = 0; // 移除换行符

    printf("请输入电话: ");
    fgets(new_contact.phone, MAX_PHONE, stdin);
    new_contact.phone[strcspn(new_contact.phone, "\n")] = 0;

    printf("请输入邮箱: ");
    fgets(new_contact.email, MAX_EMAIL, stdin);
    new_contact.email[strcspn(new_contact.email, "\n")] = 0;

    fwrite(&new_contact, sizeof(Contact), 1, fp);
    fclose(fp);
    printf("联系人添加成功！ID: %d\n", new_contact.id);
    return 0;
}

// 显示所有联系人
void show_all_contacts() {
    FILE *fp = fopen(CONTACTS_FILE, "rb");
    if (fp == NULL) {
        printf("通讯录为空或文件不存在。\n");
        return;
    }

    Contact contact;
    printf("\n=== 所有联系人 ===\n");
    while (fread(&contact, sizeof(Contact), 1, fp) == 1) {
        printf("ID: %d\n", contact.id);
        printf("姓名: %s\n", contact.name);
        printf("电话: %s\n", contact.phone);
        printf("邮箱: %s\n", contact.email);
        printf("-------------------\n");
    }
    fclose(fp);
}

// 查找联系人
void find_contact_by_name(const char *name) {
    FILE *fp = fopen(CONTACTS_FILE, "rb");
    if (fp == NULL) {
        printf("通讯录为空。\n");
        return;
    }

    Contact contact;
    int found = 0;
    printf("\n=== 搜索结果 ===\n");
    while (fread(&contact, sizeof(Contact), 1, fp) == 1) {
        if (strstr(contact.name, name) != NULL) {
            printf("ID: %d\n", contact.id);
            printf("姓名: %s\n", contact.name);
            printf("电话: %s\n", contact.phone);
            printf("邮箱: %s\n", contact.email);
            printf("-------------------\n");
            found = 1;
        }
    }

    if (!found) {
        printf("未找到匹配的联系人。\n");
    }
    fclose(fp);
}

int main() {
    int choice;
    char search_name[50];

    printf("=== C语言通讯录系统 ===\n");

    while (1) {
        printf("\n请选择操作:\n");
        printf("1. 添加联系人\n");
        printf("2. 显示所有联系人\n");
        printf("3. 按姓名查找联系人\n");
        printf("4. 退出\n");
        printf("请输入选择 (1-4): ");

        if (scanf("%d", &choice) != 1) {
            // 清空输入缓冲区
            while (getchar() != '\n');
            continue;
        }
        getchar(); // 消费换行符

        switch (choice) {
            case 1:
                add_contact();
                break;
            case 2:
                show_all_contacts();
                break;
            case 3:
                printf("请输入要查找的姓名: ");
                fgets(search_name, sizeof(search_name), stdin);
                search_name[strcspn(search_name, "\n")] = 0;
                find_contact_by_name(search_name);
                break;
            case 4:
                printf("再见！\n");
                return 0;
            default:
                printf("无效选择，请重试。\n");
        }
    }

    return 0;
}