// solution-03.cpp - STL 综合实战：数据处理管道
// 结合 transform、sort、find_if 等算法构建数据处理管道

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>
#include <sstream>

struct Product {
    std::string name;
    double price;
    int stock;
    std::string category;
};

// 辅助函数：打印产品信息
void printProduct(const Product& p) {
    std::cout << p.name << " | ¥" << p.price
              << " | 库存:" << p.stock << " | " << p.category << "\n";
}

int main() {
    std::vector<Product> products = {
        {"MacBook Pro", 14999.0, 50, "electronics"},
        {"iPhone 15", 7999.0, 200, "electronics"},
        {"Rust Programming", 89.0, 500, "books"},
        {"C++ Primer", 109.0, 300, "books"},
        {"Mechanical Keyboard", 499.0, 0, "electronics"},
        {"Clean Code", 79.0, 150, "books"},
        {"USB-C Cable", 29.0, 1000, "accessories"},
        {"Monitor 27inch", 2499.0, 80, "electronics"}
    };

    // 步骤1：筛选有库存的商品（erase-remove idiom）
    products.erase(
        std::remove_if(products.begin(), products.end(),
            [](const Product& p) { return p.stock == 0; }),
        products.end()
    );
    std::cout << "=== 有库存的商品 ===\n";

    // 步骤2：按价格降序排序
    std::sort(products.begin(), products.end(),
        [](const Product& a, const Product& b) {
            return a.price > b.price;
        });

    // 步骤3：找出第一个价格低于100的商品
    auto it = std::find_if(products.begin(), products.end(),
        [](const Product& p) { return p.price < 100.0; });
    if (it != products.end()) {
        std::cout << "\n第一个低于100元的商品: " << it->name << " (¥" << it->price << ")\n";
    }

    // 步骤4：统计各分类商品数量
    std::map<std::string, int> categoryCount;
    for (const auto& p : products) {
        categoryCount[p.category]++;
    }
    std::cout << "\n=== 各分类商品数量 ===\n";
    for (const auto& [cat, count] : categoryCount) {
        std::cout << cat << ": " << count << " 件\n";
    }

    // 步骤5：计算所有商品总价
    double totalPrice = std::accumulate(products.begin(), products.end(), 0.0,
        [](double sum, const Product& p) { return sum + p.price; });
    std::cout << "\n所有商品总价: ¥" << totalPrice << "\n";

    // 步骤6：提取所有商品名称
    std::vector<std::string> names(products.size());
    std::transform(products.begin(), products.end(), names.begin(),
        [](const Product& p) { return p.name; });

    std::cout << "\n=== 商品名称列表 ===\n";
    for (const auto& name : names) {
        std::cout << "  - " << name << "\n";
    }

    return 0;
}
