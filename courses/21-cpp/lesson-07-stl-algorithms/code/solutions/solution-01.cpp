#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

// 定义员工结构体
struct Employee {
    std::string name;
    double salary;
    int departmentId;

    Employee(const std::string& n, double s, int dept)
        : name(n), salary(s), departmentId(dept) {}
};

int main() {
    std::vector<Employee> employees = {
        {"Alice", 75000.0, 1},
        {"Bob", 65000.0, 2},
        {"Charlie", 85000.0, 1},
        {"Diana", 70000.0, 3},
        {"Eve", 90000.0, 2},
        {"Frank", 60000.0, 1}
    };

    // 1. 按薪资从高到低排序
    std::sort(employees.begin(), employees.end(),
        [](const Employee& a, const Employee& b) {
            return a.salary > b.salary;
        });

    std::cout << "按薪资从高到低排序:" << std::endl;
    for (const auto& emp : employees) {
        std::cout << emp.name << ": $" << emp.salary
                  << " (部门 " << emp.departmentId << ")" << std::endl;
    }

    // 2. 按部门ID排序，同部门内按姓名排序
    std::sort(employees.begin(), employees.end(),
        [](const Employee& a, const Employee& b) {
            if (a.departmentId != b.departmentId) {
                return a.departmentId < b.departmentId;
            }
            return a.name < b.name;
        });

    std::cout << "\n按部门和姓名排序:" << std::endl;
    for (const auto& emp : employees) {
        std::cout << "部门 " << emp.departmentId << " - "
                  << emp.name << ": $" << emp.salary << std::endl;
    }

    // 3. 找出薪资最高的员工
    auto highestPaid = std::max_element(employees.begin(), employees.end(),
        [](const Employee& a, const Employee& b) {
            return a.salary < b.salary;
        });

    if (highestPaid != employees.end()) {
        std::cout << "\n薪资最高的员工: " << highestPaid->name
                  << " ($" << highestPaid->salary << ")" << std::endl;
    }

    // 4. 找出薪资低于平均值的员工
    double totalSalary = std::accumulate(employees.begin(), employees.end(), 0.0,
        [](double sum, const Employee& emp) { return sum + emp.salary; });
    double averageSalary = totalSalary / employees.size();

    std::cout << "\n平均薪资: $" << averageSalary << std::endl;
    std::cout << "薪资低于平均值的员工:" << std::endl;
    std::for_each(employees.begin(), employees.end(),
        [averageSalary](const Employee& emp) {
            if (emp.salary < averageSalary) {
                std::cout << emp.name << ": $" << emp.salary << std::endl;
            }
        });

    return 0;
}