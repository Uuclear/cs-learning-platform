#include <iostream>
#include <vector>
#include <memory>
#include <string>

// 抽象接口：可支付的
class Payable {
public:
    virtual ~Payable() = default;
    virtual double calculatePayment() const = 0;
    virtual std::string getPaymentDescription() const = 0;
};

// 抽象接口：可打印的
class Printable {
public:
    virtual ~Printable() = default;
    virtual void printDetails() const = 0;
};

// 员工基类（抽象类）
class Employee : public Payable, public Printable {
protected:
    std::string name;
    std::string id;
    double baseSalary;

public:
    Employee(const std::string& n, const std::string& empId, double salary)
        : name(n), id(empId), baseSalary(salary) {}

    virtual ~Employee() = default;

    // 实现Payable接口
    double calculatePayment() const override {
        return baseSalary;
    }

    std::string getName() const { return name; }
    std::string getId() const { return id; }
    double getBaseSalary() const { return baseSalary; }
};

// 经理类
class Manager : public Employee {
private:
    double bonus;
    int teamSize;

public:
    Manager(const std::string& n, const std::string& empId, double salary, double b, int team)
        : Employee(n, empId, salary), bonus(b), teamSize(team) {}

    // 重写计算薪资的方法
    double calculatePayment() const override {
        return baseSalary + bonus;
    }

    std::string getPaymentDescription() const override {
        return "Manager salary with bonus";
    }

    void printDetails() const override {
        std::cout << "Manager: " << name << " (ID: " << id << ")" << std::endl;
        std::cout << "  Base Salary: $" << baseSalary << std::endl;
        std::cout << "  Bonus: $" << bonus << std::endl;
        std::cout << "  Total Payment: $" << calculatePayment() << std::endl;
        std::cout << "  Team Size: " << teamSize << " employees" << std::endl;
    }

    int getTeamSize() const { return teamSize; }
    double getBonus() const { return bonus; }
};

// 开发者类
class Developer : public Employee {
private:
    std::string programmingLanguage;
    int experienceYears;

public:
    Developer(const std::string& n, const std::string& empId, double salary,
              const std::string& lang, int exp)
        : Employee(n, empId, salary), programmingLanguage(lang), experienceYears(exp) {}

    double calculatePayment() const override {
        // 经验丰富的开发者有额外津贴
        return baseSalary + (experienceYears * 1000);
    }

    std::string getPaymentDescription() const override {
        return "Developer salary with experience bonus";
    }

    void printDetails() const override {
        std::cout << "Developer: " << name << " (ID: " << id << ")" << std::endl;
        std::cout << "  Base Salary: $" << baseSalary << std::endl;
        std::cout << "  Experience Bonus: $" << (experienceYears * 1000) << std::endl;
        std::cout << "  Total Payment: $" << calculatePayment() << std::endl;
        std::cout << "  Language: " << programmingLanguage << std::endl;
        std::cout << "  Experience: " << experienceYears << " years" << std::endl;
    }

    std::string getProgrammingLanguage() const { return programmingLanguage; }
    int getExperienceYears() const { return experienceYears; }
};

// 设计师类
class Designer : public Employee {
private:
    std::string designTool;
    bool isSenior;

public:
    Designer(const std::string& n, const std::string& empId, double salary,
             const std::string& tool, bool senior)
        : Employee(n, empId, salary), designTool(tool), isSenior(senior) {}

    double calculatePayment() const override {
        return baseSalary + (isSenior ? 5000 : 2000);
    }

    std::string getPaymentDescription() const override {
        return isSenior ? "Senior designer salary" : "Junior designer salary";
    }

    void printDetails() const override {
        std::cout << "Designer: " << name << " (ID: " << id << ")" << std::endl;
        std::cout << "  Base Salary: $" << baseSalary << std::endl;
        std::cout << "  Level Bonus: $" << (isSenior ? 5000 : 2000) << std::endl;
        std::cout << "  Total Payment: $" << calculatePayment() << std::endl;
        std::cout << "  Design Tool: " << designTool << std::endl;
        std::cout << "  Level: " << (isSenior ? "Senior" : "Junior") << std::endl;
    }

    std::string getDesignTool() const { return designTool; }
    bool getIsSenior() const { return isSenior; }
};

// 处理可支付对象的通用函数
void processPayment(const Payable& payable) {
    std::cout << "Processing payment: $" << payable.calculatePayment()
              << " (" << payable.getPaymentDescription() << ")" << std::endl;
}

// 打印可打印对象的通用函数
void printItem(const Printable& printable) {
    printable.printDetails();
    std::cout << "---" << std::endl;
}

int main() {
    std::cout << "=== 抽象类与接口设计演示 ===" << std::endl;

    // 创建不同类型的员工
    Manager manager("Alice Johnson", "M001", 80000, 15000, 8);
    Developer developer("Bob Smith", "D001", 70000, "C++", 5);
    Designer designer("Carol Davis", "DS001", 65000, "Adobe Creative Suite", true);

    std::cout << "\n--- 使用具体类型 ---" << std::endl;
    manager.printDetails();
    std::cout << "---" << std::endl;
    developer.printDetails();
    std::cout << "---" << std::endl;
    designer.printDetails();

    std::cout << "\n--- 多态处理可支付对象 ---" << std::endl;
    processPayment(manager);
    processPayment(developer);
    processPayment(designer);

    std::cout << "\n--- 多态容器存储不同员工类型 ---" << std::endl;
    std::vector<std::unique_ptr<Employee>> employees;
    employees.push_back(std::make_unique<Manager>("David Wilson", "M002", 85000, 18000, 12));
    employees.push_back(std::make_unique<Developer>("Eva Brown", "D002", 75000, "Python", 3));
    employees.push_back(std::make_unique<Designer>("Frank Miller", "DS002", 60000, "Figma", false));

    double totalPayroll = 0.0;
    for (const auto& emp : employees) {
        emp->printDetails();
        totalPayroll += emp->calculatePayment();
        std::cout << "---" << std::endl;
    }

    std::cout << "Total payroll: $" << totalPayroll << std::endl;

    // 演示接口的灵活性
    std::cout << "\n=== 接口灵活性演示 ===" << std::endl;
    Printable* printableItems[] = {
        &manager,
        &developer,
        &designer
    };

    for (auto* item : printableItems) {
        item->printDetails();
        std::cout << "---" << std::endl;
    }

    return 0;
}