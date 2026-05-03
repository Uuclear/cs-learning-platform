#include <iostream>
#include <string>

// 完整的字符串类实现，展示各种运算符重载
class MyString {
private:
    char* data;
    size_t length;

    // 辅助函数：复制字符串
    void copyFrom(const char* str) {
        if (str == nullptr) {
            data = new char[1];
            data[0] = '\0';
            length = 0;
        } else {
            length = std::strlen(str);
            data = new char[length + 1];
            std::strcpy(data, str);
        }
    }

public:
    // 默认构造函数
    MyString() : data(new char[1]), length(0) {
        data[0] = '\0';
    }

    // C字符串构造函数
    MyString(const char* str) {
        copyFrom(str);
    }

    // 拷贝构造函数
    MyString(const MyString& other) {
        copyFrom(other.data);
    }

    // 析构函数
    ~MyString() {
        delete[] data;
    }

    // 赋值运算符重载
    MyString& operator=(const MyString& other) {
        if (this != &other) {
            delete[] data;
            copyFrom(other.data);
        }
        return *this;
    }

    // 成员函数重载 + 运算符（连接）
    MyString operator+(const MyString& other) const {
        char* newData = new char[length + other.length + 1];
        std::strcpy(newData, data);
        std::strcat(newData, other.data);
        MyString result(newData);
        delete[] newData;
        return result;
    }

    // 成员函数重载 += 运算符
    MyString& operator+=(const MyString& other) {
        char* newData = new char[length + other.length + 1];
        std::strcpy(newData, data);
        std::strcat(newData, other.data);
        delete[] data;
        data = newData;
        length = length + other.length;
        return *this;
    }

    // 成员函数重载 [] 运算符（可修改版本）
    char& operator[](size_t index) {
        if (index >= length) {
            throw std::out_of_range("Index out of range");
        }
        return data[index];
    }

    // 成员函数重载 [] 运算符（只读版本）
    char operator[](size_t index) const {
        if (index >= length) {
            throw std::out_of_range("Index out of range");
        }
        return data[index];
    }

    // 成员函数重载 == 运算符
    bool operator==(const MyString& other) const {
        return std::strcmp(data, other.data) == 0;
    }

    // 成员函数重载 != 运算符
    bool operator!=(const MyString& other) const {
        return !(*this == other);
    }

    // 成员函数重载 < 运算符
    bool operator<(const MyString& other) const {
        return std::strcmp(data, other.data) < 0;
    }

    // 获取长度
    size_t getLength() const { return length; }

    // 获取C字符串
    const char* c_str() const { return data; }
};

// 友元函数重载 << 运算符
std::ostream& operator<<(std::ostream& os, const MyString& str) {
    os << str.c_str();
    return os;
}

// 友元函数重载 >> 运算符
std::istream& operator>>(std::istream& is, MyString& str) {
    std::string temp;
    is >> temp;
    delete[] str.data;
    str.copyFrom(temp.c_str());
    return is;
}

// 非成员函数重载 + 运算符（C字符串 + MyString）
MyString operator+(const char* lhs, const MyString& rhs) {
    MyString result(lhs);
    return result + rhs;
}

// 非成员函数重载 + 运算符（MyString + C字符串）
MyString operator+(const MyString& lhs, const char* rhs) {
    MyString result(rhs);
    return lhs + result;
}

int main() {
    MyString s1("Hello");
    MyString s2(" World");

    std::cout << "s1 = " << s1 << "\n";
    std::cout << "s2 = " << s2 << "\n\n";

    // 测试字符串连接
    MyString s3 = s1 + s2;
    std::cout << "s1 + s2 = " << s3 << "\n";

    MyString s4 = "Goodbye" + s2;
    std::cout << "\"Goodbye\" + s2 = " << s4 << "\n";

    MyString s5 = s1 + "!";
    std::cout << "s1 + \"!\" = " << s5 << "\n\n";

    // 测试 += 运算符
    s1 += s2;
    std::cout << "s1 after += s2: " << s1 << "\n\n";

    // 测试比较运算符
    std::cout << "s3 == s1: " << (s3 == s1 ? "true" : "false") << "\n";
    std::cout << "s3 != s4: " << (s3 != s4 ? "true" : "false") << "\n";
    std::cout << "s3 < s4: " << (s3 < s4 ? "true" : "false") << "\n\n";

    // 测试索引运算符
    std::cout << "First character of s3: " << s3[0] << "\n";
    s3[0] = 'J';
    std::cout << "After changing first char: " << s3 << "\n\n";

    // 测试输入
    std::cout << "请输入一个字符串: ";
    MyString inputStr;
    std::cin >> inputStr;
    std::cout << "你输入的字符串是: " << inputStr << "\n";

    return 0;
}