#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <optional>
#include <algorithm>

// 安全的除法函数，使用 optional 处理除零错误
std::optional<double> safeDivide(double dividend, double divisor) {
    if (divisor == 0.0) {
        return std::nullopt; // 返回空值表示错误
    }
    return dividend / divisor;
}

// 查找学生最高分科目
std::optional<std::pair<std::string, double>> findBestSubject(
    const std::map<std::string, double>& grades) {
    if (grades.empty()) {
        return std::nullopt;
    }

    auto bestIt = std::max_element(grades.begin(), grades.end(),
        [](const auto& a, const auto& b) {
            return a.second < b.second;
        });

    return *bestIt;
}

int main() {
    std::cout << "=== 现代 C++ 实践解决方案 ===" << std::endl;

    // 1. 使用 optional 进行安全除法
    std::cout << "\n--- 安全除法测试 ---" << std::endl;
    auto result1 = safeDivide(10.0, 2.0);
    if (result1) {
        std::cout << "10.0 / 2.0 = " << *result1 << std::endl;
    }

    auto result2 = safeDivide(10.0, 0.0);
    if (result2) {
        std::cout << "10.0 / 0.0 = " << *result2 << std::endl;
    } else {
        std::cout << "10.0 / 0.0: 除零错误！" << std::endl;
    }

    // 2. 使用结构化绑定和 optional 查找最佳科目
    std::cout << "\n--- 学生成绩分析 ---" << std::endl;
    std::map<std::string, double> studentGrades = {
        {"数学", 85.5},
        {"英语", 92.0},
        {"物理", 78.5},
        {"化学", 88.0}
    };

    auto bestSubject = findBestSubject(studentGrades);
    if (bestSubject) {
        auto [subject, grade] = *bestSubject; // 结构化绑定
        std::cout << "最佳科目: " << subject << " (" << grade << " 分)" << std::endl;
    } else {
        std::cout << "没有成绩数据" << std::endl;
    }

    // 3. 使用 value_or 提供默认值
    std::cout << "\n--- 默认值处理 ---" << std::endl;
    std::optional<double> maybeScore;
    double finalScore = maybeScore.value_or(60.0); // 如果没有值，使用 60.0 作为默认及格分
    std::cout << "最终分数: " << finalScore << std::endl;

    // 4. 综合应用：计算加权平均分
    std::cout << "\n--- 加权平均分计算 ---" << std::endl;
    std::vector<std::pair<std::string, std::pair<double, double>>> weightedGrades = {
        {"数学", {85.5, 0.3}},   // 成绩, 权重
        {"英语", {92.0, 0.25}},
        {"物理", {78.5, 0.25}},
        {"化学", {88.0, 0.2}}
    };

    double weightedSum = 0.0;
    double totalWeight = 0.0;

    for (const auto& [subject, gradeWeightPair] : weightedGrades) {
        auto [grade, weight] = gradeWeightPair;
        weightedSum += grade * weight;
        totalWeight += weight;
    }

    if (totalWeight > 0) {
        double weightedAverage = weightedSum / totalWeight;
        std::cout << "加权平均分: " << weightedAverage << std::endl;
    }

    return 0;
}