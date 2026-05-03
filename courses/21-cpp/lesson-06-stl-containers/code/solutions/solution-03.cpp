#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>

// 练习3：电话簿实现
class PhoneBook {
private:
    std::map<std::string, std::string> contacts;

public:
    // 添加联系人
    void addContact(const std::string& name, const std::string& phone) {
        contacts[name] = phone;
        std::cout << "已添加联系人: " << name << " - " << phone << std::endl;
    }

    // 查找联系人电话
    std::string findPhone(const std::string& name) const {
        auto it = contacts.find(name);
        if (it != contacts.end()) {
            return it->second;
        }
        return ""; // 未找到
    }

    // 列出所有联系人（按姓名排序）
    void listAllContacts() const {
        if (contacts.empty()) {
            std::cout << "电话簿为空" << std::endl;
            return;
        }

        std::cout << "=== 电话簿联系人 ===" << std::endl;
        for (const auto& [name, phone] : contacts) {
            std::cout << name << ": " << phone << std::endl;
        }
    }

    // 删除联系人
    bool removeContact(const std::string& name) {
        return contacts.erase(name) > 0;
    }

    // 检查联系人是否存在
    bool hasContact(const std::string& name) const {
        return contacts.find(name) != contacts.end();
    }

    // 获取联系人数量
    size_t getContactCount() const {
        return contacts.size();
    }
};

// 额外挑战：实现一个函数，找出文本中最常用的前N个单词
std::vector<std::pair<std::string, int>> getTopNWords(
    const std::string& text, size_t n) {

    // 统计词频
    std::map<std::string, int> wordCount;
    std::istringstream iss(text);
    std::string word;

    while (iss >> word) {
        // 简单清理
        std::string cleanWord;
        for (char c : word) {
            if (std::isalpha(c)) {
                cleanWord += std::tolower(c);
            }
        }
        if (!cleanWord.empty()) {
            wordCount[cleanWord]++;
        }
    }

    // 转换为vector以便排序
    std::vector<std::pair<std::string, int>> wordVec(
        wordCount.begin(), wordCount.end());

    // 按频率降序排序
    std::sort(wordVec.begin(), wordVec.end(),
              [](const auto& a, const auto& b) {
                  return a.second > b.second;
              });

    // 返回前N个
    if (n >= wordVec.size()) {
        return wordVec;
    }
    return std::vector<std::pair<std::string, int>>(
        wordVec.begin(), wordVec.begin() + n);
}

int main() {
    std::cout << "=== 电话簿示例 ===" << std::endl;
    PhoneBook phoneBook;

    // 添加联系人
    phoneBook.addContact("张三", "13800138001");
    phoneBook.addContact("李四", "13900139002");
    phoneBook.addContact("王五", "13700137003");
    phoneBook.addContact("赵六", "13600136004");

    // 列出所有联系人
    phoneBook.listAllContacts();

    // 查找特定联系人
    std::string name = "李四";
    std::string phone = phoneBook.findPhone(name);
    if (!phone.empty()) {
        std::cout << "\n找到 " << name << " 的电话: " << phone << std::endl;
    } else {
        std::cout << "\n未找到 " << name << " 的联系信息" << std::endl;
    }

    // 删除联系人
    if (phoneBook.removeContact("王五")) {
        std::cout << "\n已删除王五的联系信息" << std::endl;
    }

    std::cout << "\n删除后的电话簿:" << std::endl;
    phoneBook.listAllContacts();

    std::cout << "\n=== 词频统计挑战 ===" << std::endl;
    std::string sampleText = "the quick brown fox jumps over the lazy dog "
                           "the dog was really lazy and the fox was quick";

    auto topWords = getTopNWords(sampleText, 5);
    std::cout << "前5个最常用单词:" << std::endl;
    for (const auto& [word, count] : topWords) {
        std::cout << word << ": " << count << " 次" << std::endl;
    }

    return 0;
}