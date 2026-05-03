# 挑战 2：字符串处理工具

## 要求

使用 STL 算法和 Lambda 表达式实现一个字符串处理工具，包含以下功能：

1. 使用 `std::transform` 将字符串向量中的所有字母转换为小写
2. 使用 `std::remove_if` 删除长度小于 3 的字符串
3. 使用 `std::sort` 按字符串长度排序，长度相同时按字典序排序
4. 使用 `std::unique` 去除重复字符串
5. 使用 `std::for_each` 打印处理后的所有字符串

## 提示

- 字符串转小写可以使用 `std::tolower`
- `std::unique` 需要容器先排序，它只删除相邻的重复元素
- 记住 erase-remove idiom 的正确用法

## 解答

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cctype>

int main() {
    std::vector<std::string> words = {
        "Hello", "C++", "a", "hello", "STL", "world", "b",
        "Algorithm", "Hello", "c", "Lambda", "C++"
    };

    // 步骤1：转换为小写
    std::transform(words.begin(), words.end(), words.begin(),
        [](std::string s) {
            std::transform(s.begin(), s.end(), s.begin(),
                [](unsigned char c) { return std::tolower(c); });
            return s;
        });

    // 步骤2：删除长度小于3的字符串
    words.erase(
        std::remove_if(words.begin(), words.end(),
            [](const std::string& s) { return s.length() < 3; }),
        words.end()
    );

    // 步骤3：排序（先去重需要排序）
    std::sort(words.begin(), words.end());

    // 步骤4：去除重复
    words.erase(std::unique(words.begin(), words.end()), words.end());

    // 步骤5：按长度排序
    std::stable_sort(words.begin(), words.end(),
        [](const std::string& a, const std::string& b) {
            if (a.length() != b.length()) return a.length() < b.length();
            return a < b;
        });

    // 步骤6：打印结果
    std::cout << "处理后的字符串:\n";
    std::for_each(words.begin(), words.end(),
        [](const std::string& s) { std::cout << "  " << s << "\n"; });

    return 0;
}
```
