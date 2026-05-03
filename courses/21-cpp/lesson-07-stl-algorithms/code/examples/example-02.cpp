#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

// 定义产品结构体
struct Product {
    std::string name;
    double price;
    bool inStock;

    Product(const std::string& n, double p, bool stock)
        : name(n), price(p), inStock(stock) {}
};

int main() {
    std::vector<Product> products = {
        {"笔记本电脑", 5999.99, true},
        {"手机", 3999.50, true},
        {"耳机", 299.99, false},
        {"键盘", 199.99, true},
        {"鼠标", 89.99, true},
        {"显示器", 1299.99, false}
    };

    std::cout << "=== 所有产品列表 ===" << std::endl;
    for (const auto& product : products) {
        std::cout << product.name << " - ¥" << product.price
                  << " (" << (product.inStock ? "有货" : "缺货") << ")" << std::endl;
    }

    // 使用 find_if 查找第一个价格超过 1000 元的产品
    auto expensiveProduct = std::find_if(products.begin(), products.end(),
        [](const Product& p) { return p.price > 1000.0; });

    if (expensiveProduct != products.end()) {
        std::cout << "\n=== 第一个价格超过 1000 元的产品 ===" << std::endl;
        std::cout << expensiveProduct->name << " - ¥" << expensiveProduct->price << std::endl;
    }

    // 使用 find_if 查找第一个缺货的产品
    auto outOfStock = std::find_if(products.begin(), products.end(),
        [](const Product& p) { return !p.inStock; });

    if (outOfStock != products.end()) {
        std::cout << "\n=== 第一个缺货的产品 ===" << std::endl;
        std::cout << outOfStock->name << " - 缺货" << std::endl;
    }

    // 使用 count_if 统计价格低于 200 元的产品数量
    int cheapCount = std::count_if(products.begin(), products.end(),
        [](const Product& p) { return p.price < 200.0; });
    std::cout << "\n=== 价格低于 200 元的产品数量: " << cheapCount << " 个" << std::endl;

    // 使用 count_if 统计有货的产品数量
    int inStockCount = std::count_if(products.begin(), products.end(),
        [](const Product& p) { return p.inStock; });
    std::cout << "有货的产品数量: " << inStockCount << " 个" << std::endl;

    // 使用 Lambda 表达式进行更复杂的查找
    double targetPrice = 4000.0;
    auto nearTarget = std::find_if(products.begin(), products.end(),
        [targetPrice](const Product& p) {
            return std::abs(p.price - targetPrice) < 100.0;
        });

    if (nearTarget != products.end()) {
        std::cout << "\n=== 价格接近 " << targetPrice << " 元的产品 ===" << std::endl;
        std::cout << nearTarget->name << " - ¥" << nearTarget->price << std::endl;
    }

    // 使用 all_of、any_of、none_of
    bool allExpensive = std::all_of(products.begin(), products.end(),
        [](const Product& p) { return p.price > 50.0; });
    std::cout << "\n所有产品都超过 50 元: " << (allExpensive ? "是" : "否") << std::endl;

    bool anyOutOfStock = std::any_of(products.begin(), products.end(),
        [](const Product& p) { return !p.inStock; });
    std::cout << "有任何产品缺货: " << (anyOutOfStock ? "是" : "否") << std::endl;

    bool noneCheap = std::none_of(products.begin(), products.end(),
        [](const Product& p) { return p.price < 50.0; });
    std::cout << "没有任何产品低于 50 元: " << (noneCheap ? "是" : "否") << std::endl;

    return 0;
}