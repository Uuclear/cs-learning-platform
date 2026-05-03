#include <iostream>
#include <vector>
#include <memory>
#include <algorithm>
#include <stdexcept>

// 改进的 noexcept 实现
class ImprovedNoExceptExample {
private:
    std::unique_ptr<int[]> data;
    size_t size;
    
public:
    // 默认构造函数 - noexcept
    ImprovedNoExceptExample() noexcept : size(0) {
        std::cout << "默认构造 (noexcept)" << std::endl;
    }
    
    // 带大小的构造函数 - 可能抛出异常
    explicit ImprovedNoExceptExample(size_t s) : size(s) {
        if (s > 1000000) {
            throw std::invalid_argument("数组大小过大");
        }
        data = std::make_unique<int[]>(size);
        std::cout << "带参构造，大小: " << size << std::endl;
    }
    
    // 拷贝构造函数 - noexcept（使用智能指针）
    ImprovedNoExceptExample(const ImprovedNoExceptExample& other) noexcept 
        : size(other.size), data(std::make_unique<int[]>(other.size)) {
        std::copy(other.data.get(), other.data.get() + other.size, data.get());
        std::cout << "拷贝构造 (noexcept)" << std::endl;
    }
    
    // 移动构造函数 - noexcept（关键！）
    ImprovedNoExceptExample(ImprovedNoExceptExample&& other) noexcept 
        : data(std::move(other.data)), size(other.size) {
        other.size = 0;
        std::cout << "移动构造 (noexcept)" << std::endl;
    }
    
    // 拷贝赋值 - noexcept
    ImprovedNoExceptExample& operator=(const ImprovedNoExceptExample& other) noexcept {
        if (this != &other) {
            size = other.size;
            data = std::make_unique<int[]>(size);
            std::copy(other.data.get(), other.data.get() + size, data.get());
        }
        std::cout << "拷贝赋值 (noexcept)" << std::endl;
        return *this;
    }
    
    // 移动赋值 - noexcept（关键！）
    ImprovedNoExceptExample& operator=(ImprovedNoExceptExample&& other) noexcept {
        if (this != &other) {
            data = std::move(other.data);
            size = other.size;
            other.size = 0;
        }
        std::cout << "移动赋值 (noexcept)" << std::endl;
        return *this;
    }
    
    // noexcept 访问器
    size_t getSize() const noexcept {
        return size;
    }
    
    int getValue(size_t index) const {
        if (index >= size) {
            throw std::out_of_range("索引超出范围");
        }
        return data[index];
    }
    
    void setValue(size_t index, int value) {
        if (index >= size) {
            throw std::out_of_range("索引超出范围");
        }
        data[index] = value;
    }
    
    // noexcept 析构函数
    ~ImprovedNoExceptExample() noexcept {
        std::cout << "析构函数" << std::endl;
    }
};

// 强异常安全保证的实现
class StrongGuaranteeContainer {
private:
    std::vector<int> data;
    
public:
    explicit StrongGuaranteeContainer(const std::vector<int>& initial) : data(initial) {}
    
    // 强异常安全的赋值操作
    StrongGuaranteeContainer& operator=(const StrongGuaranteeContainer& other) {
        // 创建临时副本
        StrongGuaranteeContainer temp(other);
        // 交换 - noexcept 操作
        swap(temp);
        return *this;
    }
    
    // noexcept 交换函数
    void swap(StrongGuaranteeContainer& other) noexcept {
        data.swap(other.data);
    }
    
    // 强异常安全的修改操作
    void modifyWithStrongGuarantee(int multiplier) {
        // 在临时对象上进行所有可能失败的操作
        auto temp_data = data;
        for (auto& value : temp_data) {
            // 模拟可能失败的操作
            if (multiplier == 0) {
                throw std::invalid_argument("乘数不能为零");
            }
            value *= multiplier;
        }
        // 只有成功后才提交更改
        data = std::move(temp_data);
    }
    
    const std::vector<int>& getData() const noexcept {
        return data;
    }
};

// noexcept 工具函数
template<typename T>
constexpr bool is_nothrow_swappable_v = noexcept(std::declval<T&>().swap(std::declval<T&>()));

// 异常安全的算法实现
template<typename Container, typename UnaryOperation>
Container transformWithStrongGuarantee(const Container& input, UnaryOperation op) {
    Container result;
    result.reserve(input.size()); // 预分配空间
    
    // 在临时容器中执行转换
    for (const auto& element : input) {
        result.push_back(op(element)); // 如果op抛出异常，result会被正确销毁
    }
    
    return result; // 移动语义，如果移动是noexcept则高效
}

// RAII 文件管理器
class SafeFile {
private:
    FILE* file;
    
public:
    explicit SafeFile(const char* filename, const char* mode = "r") {
        file = fopen(filename, mode);
        if (!file) {
            throw std::runtime_error(std::string("无法打开文件: ") + filename);
        }
    }
    
    ~SafeFile() noexcept {
        if (file) {
            fclose(file);
        }
    }
    
    // 禁止拷贝
    SafeFile(const SafeFile&) = delete;
    SafeFile& operator=(const SafeFile&) = delete;
    
    // noexcept 移动
    SafeFile(SafeFile&& other) noexcept : file(other.file) {
        other.file = nullptr;
    }
    
    SafeFile& operator=(SafeFile&& other) noexcept {
        if (this != &other) {
            if (file) fclose(file);
            file = other.file;
            other.file = nullptr;
        }
        return *this;
    }
    
    template<typename T>
    void write(const T& data) {
        if (!file) {
            throw std::runtime_error("文件未打开");
        }
        // 写入操作可能失败
        if (fwrite(&data, sizeof(T), 1, file) != 1) {
            throw std::runtime_error("写入失败");
        }
    }
    
    bool isValid() const noexcept {
        return file != nullptr;
    }
};

// 演示 noexcept 的重要性
void demonstrateNoexceptImportance() {
    std::cout << "=== noexcept 重要性演示 ===" << std::endl;
    
    // 检查类型特性
    std::cout << "ImprovedNoExceptExample is nothrow move constructible: " 
              << std::is_nothrow_move_constructible_v<ImprovedNoExceptExample> << std::endl;
    std::cout << "ImprovedNoExceptExample is nothrow move assignable: " 
              << std::is_nothrow_move_assignable_v<ImprovedNoExceptExample> << std::endl;
    std::cout << "std::vector uses move for ImprovedNoExceptExample: " 
              << std::is_nothrow_move_constructible_v<ImprovedNoExceptExample> << std::endl;
    
    // vector 操作演示
    std::vector<ImprovedNoExceptExample> vec;
    vec.emplace_back(5);
    
    try {
        // 这会触发 vector 的重新分配
        for (int i = 0; i < 100; ++i) {
            vec.emplace_back(i + 1);
        }
        std::cout << "vector 扩展成功，大小: " << vec.size() << std::endl;
    } catch (const std::exception& e) {
        std::cout << "vector 操作异常: " << e.what() << std::endl;
    }
}

// 异常安全级别演示
void demonstrateExceptionSafetyLevels() {
    std::cout << "\n=== 异常安全级别演示 ===" << std::endl;
    
    // 基本保证
    try {
        ImprovedNoExceptExample obj(10);
        obj.setValue(5, 42);
        // 即使后续操作失败，obj仍然有效
    } catch (const std::exception& e) {
        std::cout << "基本保证异常: " << e.what() << std::endl;
    }
    
    // 强保证
    try {
        StrongGuaranteeContainer container({1, 2, 3, 4, 5});
        auto original_data = container.getData();
        
        container.modifyWithStrongGuarantee(2); // 成功
        std::cout << "强保证操作成功" << std::endl;
        
        container.modifyWithStrongGuarantee(0); // 失败，但container保持原状态
    } catch (const std::exception& e) {
        std::cout << "强保证异常（状态已回滚）: " << e.what() << std::endl;
    }
    
    // 不抛出保证
    StrongGuaranteeContainer container2({10, 20, 30});
    auto size_before = container2.getData().size();
    // getSize() 是 noexcept，不会改变状态
    auto size_after = container2.getData().size();
    std::cout << "不抛出保证：大小 " << size_before << " -> " << size_after << std::endl;
}

// RAII 和异常安全
void demonstrateRAII() {
    std::cout << "\n=== RAII 和异常安全演示 ===" << std::endl;
    
    try {
        SafeFile file("output.txt", "w");
        int data = 42;
        file.write(data);
        std::cout << "文件写入成功" << std::endl;
        // 即使这里抛出异常，文件也会被正确关闭
    } catch (const std::exception& e) {
        std::cout << "文件操作异常: " << e.what() << std::endl;
    }
    
    // 使用智能指针确保异常安全
    auto ptr = std::make_unique<ImprovedNoExceptExample>(3);
    ptr->setValue(0, 100);
    ptr->setValue(1, 200);
    ptr->setValue(2, 300);
    std::cout << "智能指针资源管理成功" << std::endl;
    // 即使抛出异常，ptr也会被正确销毁
}

int main() {
    demonstrateNoexceptImportance();
    demonstrateExceptionSafetyLevels();
    demonstrateRAII();
    
    std::cout << "\n程序正常结束！" << std::endl;
    return 0;
}
