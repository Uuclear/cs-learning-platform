#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

// 定义书籍结构体
struct Book {
    std::string title;
    std::string author;
    int year;
    double price;
    bool isHardcover;

    Book(const std::string& t, const std::string& a, int y, double p, bool hc)
        : title(t), author(a), year(y), price(p), isHardcover(hc) {}
};

int main() {
    std::vector<Book> library = {
        {"C++ Primer", "Stanley Lippman", 2012, 89.99, true},
        {"Effective C++", "Scott Meyers", 2005, 79.99, false},
        {"The C++ Programming Language", "Bjarne Stroustrup", 2013, 99.99, true},
        {"Programming: Principles and Practice Using C++", "Bjarne Stroustrup", 2014, 84.99, false},
        {"C++ Concurrency in Action", "Anthony Williams", 2012, 69.99, true},
        {"Modern C++ Design", "Andrei Alexandrescu", 2001, 59.99, false}
    };

    // 1. 找出所有精装书
    std::cout << "=== 精装书列表 ===" << std::endl;
    auto hardcoverBooks = std::partition(library.begin(), library.end(),
        [](const Book& book) { return book.isHardcover; });

    for (auto it = library.begin(); it != hardcoverBooks; ++it) {
        std::cout << it->title << " by " << it->author << std::endl;
    }

    // 2. 统计2010年以后出版的书籍数量
    int recentBooks = std::count_if(library.begin(), library.end(),
        [](const Book& book) { return book.year > 2010; });
    std::cout << "\n2010年以后出版的书籍数量: " << recentBooks << std::endl;

    // 3. 找出价格最便宜的平装书
    auto cheapestPaperback = std::find_if(library.begin(), library.end(),
        [](const Book& book) { return !book.isHardcover; });

    if (cheapestPaperback != library.end()) {
        double minPrice = cheapestPaperback->price;
        auto result = std::min_element(cheapestPaperback, library.end(),
            [](const Book& a, const Book& b) {
                // 只比较平装书
                if (!a.isHardcover && !b.isHardcover) {
                    return a.price < b.price;
                }
                // 如果a是平装而b不是，a更小
                if (!a.isHardcover && b.isHardcover) return true;
                // 如果b是平装而a不是，b更小
                if (a.isHardcover && !b.isHardcover) return false;
                // 都是精装，相等
                return false;
            });

        if (result != library.end() && !result->isHardcover) {
            std::cout << "\n最便宜的平装书: " << result->title
                      << " - $" << result->price << std::endl;
        }
    }

    // 4. 检查是否有任何书籍价格超过$90
    bool hasExpensiveBook = std::any_of(library.begin(), library.end(),
        [](const Book& book) { return book.price > 90.0; });
    std::cout << "\n有价格超过$90的书籍: " << (hasExpensiveBook ? "是" : "否") << std::endl;

    // 5. 找出所有Scott Meyers的书籍
    std::cout << "\n=== Scott Meyers 的书籍 ===" << std::endl;
    std::for_each(library.begin(), library.end(),
        [](const Book& book) {
            if (book.author == "Scott Meyers") {
                std::cout << book.title << " (" << book.year << ")" << std::endl;
            }
        });

    // 6. 使用 equal_range 找出特定年份的书籍（需要先按年份排序）
    std::sort(library.begin(), library.end(),
        [](const Book& a, const Book& b) { return a.year < b.year; });

    auto yearRange = std::equal_range(library.begin(), library.end(), 2012,
        [](const Book& book, int year) { return book.year < year; },
        [](int year, const Book& book) { return year < book.year; });

    std::cout << "\n=== 2012年出版的书籍 ===" << std::endl;
    for (auto it = yearRange.first; it != yearRange.second; ++it) {
        std::cout << it->title << " by " << it->author << std::endl;
    }

    return 0;
}