#include <iostream>
#include <vector>
#include <algorithm>

// 练习1解决方案：实现一个函数，找出vector中的最大值和最小值
std::pair<int, int> findMinMax(const std::vector<int>& vec) {
    if (vec.empty()) {
        throw std::invalid_argument("Vector is empty");
    }

    // 使用STL算法
    auto minMax = std::minmax_element(vec.begin(), vec.end());
    return {*minMax.first, *minMax.second};
}

// 练习2解决方案：实现一个函数，将vector中的偶数移动到前面，奇数移动到后面
void separateEvenOdd(std::vector<int>& vec) {
    std::stable_partition(vec.begin(), vec.end(),
                         [](int n) { return n % 2 == 0; });
}

// 练习3解决方案：实现一个函数，删除vector中的重复元素（保持原有顺序）
std::vector<int> removeDuplicates(const std::vector<int>& vec) {
    std::vector<int> result;
    std::set<int> seen;

    for (const auto& element : vec) {
        if (seen.find(element) == seen.end()) {
            seen.insert(element);
            result.push_back(element);
        }
    }

    return result;
}

int main() {
    // 测试练习1
    std::vector<int> numbers = {3, 7, 1, 9, 4, 6, 2, 8, 5};
    auto [minVal, maxVal] = findMinMax(numbers);
    std::cout << "最小值: " << minVal << ", 最大值: " << maxVal << std::endl;

    // 测试练习2
    std::vector<int> evenOddTest = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    std::cout << "分离前: ";
    for (const auto& n : evenOddTest) std::cout << n << " ";
    std::cout << std::endl;

    separateEvenOdd(evenOddTest);
    std::cout << "分离后: ";
    for (const auto& n : evenOddTest) std::cout << n << " ";
    std::cout << std::endl;

    // 测试练习3
    std::vector<int> duplicates = {1, 2, 3, 2, 4, 1, 5, 3, 6};
    std::cout << "去重前: ";
    for (const auto& n : duplicates) std::cout << n << " ";
    std::cout << std::endl;

    auto uniqueVec = removeDuplicates(duplicates);
    std::cout << "去重后: ";
    for (const auto& n : uniqueVec) std::cout << n << " ";
    std::cout << std::endl;

    return 0;
}