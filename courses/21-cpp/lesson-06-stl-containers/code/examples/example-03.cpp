#include <iostream>
#include <set>
#include <vector>
#include <algorithm>

int main() {
    // 创建一个包含重复元素的vector
    std::vector<int> numbersWithDuplicates = {5, 2, 8, 2, 1, 5, 9, 1, 3, 8, 4};

    std::cout << "=== 原始数据（含重复） ===" << std::endl;
    std::cout << "原始vector: ";
    for (const auto& num : numbersWithDuplicates) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    // 使用set自动去重和排序
    std::set<int> uniqueNumbers(numbersWithDuplicates.begin(),
                               numbersWithDuplicates.end());

    std::cout << "\n=== Set去重排序结果 ===" << std::endl;
    std::cout << "set中的元素: ";
    for (const auto& num : uniqueNumbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    std::cout << "去重后元素个数: " << uniqueNumbers.size() << std::endl;
    std::cout << "原始元素个数: " << numbersWithDuplicates.size() << std::endl;

    // 检查元素是否存在
    std::cout << "\n=== 元素查找 ===" << std::endl;
    int searchValue = 5;
    if (uniqueNumbers.find(searchValue) != uniqueNumbers.end()) {
        std::cout << "找到了 " << searchValue << std::endl;
    } else {
        std::cout << "没有找到 " << searchValue << std::endl;
    }

    searchValue = 10;
    if (uniqueNumbers.find(searchValue) != uniqueNumbers.end()) {
        std::cout << "找到了 " << searchValue << std::endl;
    } else {
        std::cout << "没有找到 " << searchValue << std::endl;
    }

    // set的插入操作
    std::cout << "\n=== 插入新元素 ===" << std::endl;
    uniqueNumbers.insert(7);
    uniqueNumbers.insert(0);
    uniqueNumbers.insert(5); // 重复插入，会被忽略

    std::cout << "插入新元素后: ";
    for (const auto& num : uniqueNumbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    // 使用反向迭代器
    std::cout << "反向遍历: ";
    for (auto rit = uniqueNumbers.rbegin(); rit != uniqueNumbers.rend(); ++rit) {
        std::cout << *rit << " ";
    }
    std::cout << std::endl;

    return 0;
}