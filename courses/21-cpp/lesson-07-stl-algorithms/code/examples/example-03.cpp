#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>

int main() {
    // 原始数据：温度（摄氏度）
    std::vector<double> celsiusTemps = {0.0, 25.0, 37.0, 100.0, -10.0, 15.5};

    std::cout << "=== 原始温度（摄氏度） ===" << std::endl;
    for (double temp : celsiusTemps) {
        std::cout << temp << "°C ";
    }
    std::cout << std::endl;

    // 使用 transform 将摄氏度转换为华氏度
    std::vector<double> fahrenheitTemps(celsiusTemps.size());
    std::transform(celsiusTemps.begin(), celsiusTemps.end(), fahrenheitTemps.begin(),
        [](double celsius) { return celsius * 9.0 / 5.0 + 32.0; });

    std::cout << "\n=== 转换后的温度（华氏度） ===" << std::endl;
    for (double temp : fahrenheitTemps) {
        std::cout << temp << "°F ";
    }
    std::cout << std::endl;

    // 使用 transform 进行平方运算
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    std::vector<int> squares(numbers.size());
    std::transform(numbers.begin(), numbers.end(), squares.begin(),
        [](int x) { return x * x; });

    std::cout << "\n=== 原始数字和它们的平方 ===" << std::endl;
    for (size_t i = 0; i < numbers.size(); ++i) {
        std::cout << numbers[i] << "^2 = " << squares[i] << std::endl;
    }

    // 使用 accumulate 计算总和
    int sum = std::accumulate(numbers.begin(), numbers.end(), 0);
    std::cout << "\n=== 数字总和: " << sum << std::endl;

    // 使用 accumulate 计算乘积
    int product = std::accumulate(numbers.begin(), numbers.end(), 1,
        [](int acc, int val) { return acc * val; });
    std::cout << "数字乘积: " << product << std::endl;

    // 使用 accumulate 计算平方和
    int sumOfSquares = std::accumulate(squares.begin(), squares.end(), 0);
    std::cout << "平方和: " << sumOfSquares << std::endl;

    // 使用 accumulate 和 Lambda 计算字符串长度总和
    std::vector<std::string> words = {"Hello", "World", "STL", "Algorithms", "C++"};
    int totalLength = std::accumulate(words.begin(), words.end(), 0,
        [](int acc, const std::string& word) { return acc + word.length(); });
    std::cout << "\n=== 字符串总长度: " << totalLength << std::endl;

    // 使用 transform 处理两个容器（向量加法）
    std::vector<int> vec1 = {1, 2, 3, 4, 5};
    std::vector<int> vec2 = {10, 20, 30, 40, 50};
    std::vector<int> result(vec1.size());

    std::transform(vec1.begin(), vec1.end(), vec2.begin(), result.begin(),
        [](int a, int b) { return a + b; });

    std::cout << "\n=== 向量加法结果 ===" << std::endl;
    for (size_t i = 0; i < result.size(); ++i) {
        std::cout << vec1[i] << " + " << vec2[i] << " = " << result[i] << std::endl;
    }

    // 使用 accumulate 计算平均值
    double average = static_cast<double>(sum) / numbers.size();
    std::cout << "\n=== 平均值: " << average << std::endl;

    // 使用 accumulate 计算标准差
    double variance = std::accumulate(numbers.begin(), numbers.end(), 0.0,
        [average](double acc, int val) {
            return acc + (val - average) * (val - average);
        }) / numbers.size();
    double stdDev = std::sqrt(variance);
    std::cout << "标准差: " << stdDev << std::endl;

    return 0;
}