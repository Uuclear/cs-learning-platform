#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <optional>
#include <tuple>

// 模拟一个可能失败的函数，返回 optional
std::optional<int> findValue(const std::map<std::string, int>& data, const std::string& key) {
    auto it = data.find(key);
    if (it != data.end()) {
        return it->second;
    }
    return std::nullopt; // 表示没有找到
}

// 返回多个值的函数
std::tuple<std::string, int, double> getUserInfo() {
    return std::make_tuple("Alice", 25, 3.85);
}

int main() {
    // 1. 结构化绑定 - 解构 tuple、pair、数组等
    std::cout << "=== 结构化绑定 ===" << std::endl;

    // 解构 tuple
    auto [name, age, gpa] = getUserInfo();
    std::cout << "用户信息: 姓名=" << name << ", 年龄=" << age << ", GPA=" << gpa << std::endl;

    // 解构 pair (map 的元素是 pair)
    std::map<std::string, int> scores{{"数学", 95}, {"英语", 87}, {"物理", 92}};
    std::cout << "成绩单: ";
    for (const auto& [subject, score] : scores) {
        std::cout << subject << ":" << score << " ";
    }
    std::cout << std::endl;

    // 解构数组
    int arr[3] = {10, 20, 30};
    auto [x, y, z] = arr;
    std::cout << "数组解构: x=" << x << ", y=" << y << ", z=" << z << std::endl;

    // 2. std::optional - 安全处理可能不存在的值
    std::cout << "\n=== std::optional 使用 ===" << std::endl;

    // 查找存在的键
    auto mathScore = findValue(scores, "数学");
    if (mathScore.has_value()) {
        std::cout << "数学成绩: " << mathScore.value() << std::endl;
        // 或者直接使用 *mathScore
        std::cout << "数学成绩(解引用): " << *mathScore << std::endl;
    }

    // 查找不存在的键
    auto chemistryScore = findValue(scores, "化学");
    if (chemistryScore) { // 可以直接用作布尔值
        std::cout << "化学成绩: " << *chemistryScore << std::endl;
    } else {
        std::cout << "未找到化学成绩!" << std::endl;
    }

    // 使用 value_or 提供默认值
    int defaultScore = chemistryScore.value_or(0);
    std::cout << "化学成绩(默认值): " << defaultScore << std::endl;

    // 创建 optional 值
    std::optional<std::string> maybeName = "Bob";
    std::cout << "名字: " << maybeName.value_or("未知") << std::endl;

    // 空的 optional
    std::optional<std::string> emptyName;
    std::cout << "空名字: " << emptyName.value_or("无名氏") << std::endl;

    return 0;
}