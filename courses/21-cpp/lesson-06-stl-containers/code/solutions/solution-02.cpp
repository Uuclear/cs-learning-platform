#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>

// 练习1：学生成绩管理系统
class StudentGradeManager {
private:
    std::map<std::string, std::vector<int>> studentGrades;

public:
    void addGrade(const std::string& name, int grade) {
        studentGrades[name].push_back(grade);
    }

    double calculateAverage(const std::string& name) const {
        auto it = studentGrades.find(name);
        if (it == studentGrades.end() || it->second.empty()) {
            return 0.0;
        }

        int sum = 0;
        for (int grade : it->second) {
            sum += grade;
        }
        return static_cast<double>(sum) / it->second.size();
    }

    std::string findTopStudent() const {
        if (studentGrades.empty()) {
            return "";
        }

        std::string topStudent;
        double highestAverage = -1.0;

        for (const auto& [name, grades] : studentGrades) {
            if (!grades.empty()) {
                double avg = calculateAverage(name);
                if (avg > highestAverage) {
                    highestAverage = avg;
                    topStudent = name;
                }
            }
        }

        return topStudent;
    }

    void displayAllStudents() const {
        for (const auto& [name, grades] : studentGrades) {
            std::cout << "学生: " << name << ", 成绩: ";
            for (size_t i = 0; i < grades.size(); ++i) {
                std::cout << grades[i];
                if (i < grades.size() - 1) std::cout << ", ";
            }
            std::cout << ", 平均分: " << calculateAverage(name) << std::endl;
        }
    }
};

// 练习2：购物车实现
class ShoppingCart {
private:
    std::map<std::string, int> items;
    // 商品价格表（简化版）
    std::map<std::string, double> prices = {
        {"苹果", 5.0}, {"香蕉", 3.5}, {"橙子", 4.0},
        {"牛奶", 12.0}, {"面包", 8.0}, {"鸡蛋", 15.0}
    };

public:
    void addItem(const std::string& item, int quantity = 1) {
        if (prices.find(item) != prices.end()) {
            items[item] += quantity;
            std::cout << "已添加 " << quantity << " 个 " << item << " 到购物车" << std::endl;
        } else {
            std::cout << "商品 " << item << " 不存在" << std::endl;
        }
    }

    void removeItem(const std::string& item, int quantity = -1) {
        auto it = items.find(item);
        if (it == items.end()) {
            std::cout << "购物车中没有 " << item << std::endl;
            return;
        }

        if (quantity == -1 || quantity >= it->second) {
            items.erase(it);
            std::cout << "已从购物车移除所有 " << item << std::endl;
        } else {
            it->second -= quantity;
            std::cout << "已从购物车移除 " << quantity << " 个 " << item << std::endl;
        }
    }

    double getTotalPrice() const {
        double total = 0.0;
        for (const auto& [item, quantity] : items) {
            total += prices.at(item) * quantity;
        }
        return total;
    }

    void displayCart() const {
        if (items.empty()) {
            std::cout << "购物车为空" << std::endl;
            return;
        }

        std::cout << "=== 购物车内容 ===" << std::endl;
        for (const auto& [item, quantity] : items) {
            double itemTotal = prices.at(item) * quantity;
            std::cout << item << " x " << quantity
                      << " = " << itemTotal << " 元" << std::endl;
        }
        std::cout << "总计: " << getTotalPrice() << " 元" << std::endl;
    }
};

int main() {
    std::cout << "=== 学生成绩管理系统 ===" << std::endl;
    StudentGradeManager gradeManager;

    // 添加成绩
    gradeManager.addGrade("张三", 85);
    gradeManager.addGrade("张三", 92);
    gradeManager.addGrade("张三", 78);

    gradeManager.addGrade("李四", 90);
    gradeManager.addGrade("李四", 88);
    gradeManager.addGrade("李四", 95);

    gradeManager.addGrade("王五", 76);
    gradeManager.addGrade("王五", 82);

    gradeManager.displayAllStudents();
    std::cout << "最高分学生: " << gradeManager.findTopStudent() << std::endl;

    std::cout << "\n=== 购物车示例 ===" << std::endl;
    ShoppingCart cart;
    cart.addItem("苹果", 3);
    cart.addItem("牛奶", 2);
    cart.addItem("面包", 1);
    cart.displayCart();

    cart.removeItem("苹果", 1);
    cart.displayCart();

    return 0;
}