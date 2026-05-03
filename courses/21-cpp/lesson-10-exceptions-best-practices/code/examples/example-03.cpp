#include <iostream>
#include <vector>
#include <memory>
#include <stdexcept>

// noexcept 演示
class NoExceptExample {
private:
    int value;
    
public:
    // 默认构造函数 - noexcept
    NoExceptExample() noexcept : value(0) {
        std::cout << "默认构造函数 (noexcept)" << std::endl;
    }
    
    // 拷贝构造函数 - noexcept
    NoExceptExample(const NoExceptExample& other) noexcept : value(other.value) {
        std::cout << "拷贝构造函数 (noexcept)" << std::endl;
    }
    
    // 移动构造函数 - noexcept（重要！）
    NoExceptExample(NoExceptExample&& other) noexcept : value(other.value) {
        other.value = 0;
        std::cout << "移动构造函数 (noexcept)" << std::endl;
    }
    
    // 赋值操作符 - noexcept
    NoExceptExample& operator=(const NoExceptExample& other) noexcept {
        if (this != &other) {
            value = other.value;
        }
        std::cout << "拷贝赋值 (noexcept)" << std::endl;
        return *this;
    }
    
    // 移动赋值 - noexcept（重要！）
    NoExceptExample& operator=(NoExceptExample&& other) noexcept {
        if (this != &other) {
            value = other.value;
            other.value = 0;
        }
        std::cout << "移动赋值 (noexcept)" << std::endl;
        return *this;
    }
    
    // 可能抛出异常的函数
    void setValue(int new_value) {
        if (new_value < 0) {
            throw std::invalid_argument("值不能为负数");
        }
        value = new_value;
        std::cout << "设置值: " << value << std::endl;
    }
    
    // noexcept 函数 - 承诺不抛出异常
    int getValue() const noexcept {
        return value;
    }
    
    // 析构函数总是 noexcept
    ~NoExceptExample() noexcept {
        std::cout << "析构函数 (隐式 noexcept)" << std::endl;
    }
};

// 异常安全级别演示
class ExceptionSafetyDemo {
private:
    std::unique_ptr<int[]> data;
    size_t size;
    
public:
    explicit ExceptionSafetyDemo(size_t s) : size(s) {
        data = std::make_unique<int[]>(size);
        std::cout << "创建大小为 " << size << " 的数组" << std::endl;
    }
    
    // 基本异常安全保证 (Basic Guarantee)
    void basicGuaranteeOperation() {
        // 如果这里抛出异常，对象仍然处于有效状态
        // 但可能不是原来的状态
        if (size == 0) {
            throw std::runtime_error("数组大小为零");
        }
        
        // 修改数据
        for (size_t i = 0; i < size; ++i) {
            data[i] = static_cast<int>(i);
        }
        std::cout << "基本异常安全操作完成" << std::endl;
    }
    
    // 强异常安全保证 (Strong Guarantee) - 提供提交/回滚语义
    void strongGuaranteeOperation() {
        // 创建临时副本
        auto temp_data = std::make_unique<int[]>(size);
        
        // 在临时副本上进行所有可能失败的操作
        for (size_t i = 0; i < size; ++i) {
            if (i == size / 2 && size > 10) {
                // 模拟在中间抛出异常
                throw std::runtime_error("模拟操作失败");
            }
            temp_data[i] = static_cast<int>(i * 2);
        }
        
        // 只有在所有操作成功后才交换
        data.swap(temp_data);
        std::cout << "强异常安全操作完成" << std::endl;
    }
    
    // 不抛出异常保证 (No-throw Guarantee)
    size_t getSize() const noexcept {
        return size;
    }
    
    int getDataAt(size_t index) const noexcept {
        // 注意：这里没有边界检查，因为要保证不抛出异常
        // 实际代码中应该确保调用者已经验证了索引
        return data[index];
    }
};

// noexcept 操作符演示
template<typename T>
void demonstrateNoexceptOperator() {
    std::cout << "std::is_nothrow_constructible_v<T>: " 
              << std::is_nothrow_constructible_v<T> << std::endl;
    std::cout << "noexcept(T{}): " 
              << noexcept(T{}) << std::endl;
}

// 容器操作中的 noexcept 重要性
void demonstrateVectorOperations() {
    std::cout << "\n=== vector 操作中的 noexcept ===" << std::endl;
    
    std::vector<NoExceptExample> vec;
    
    // 添加元素
    vec.emplace_back();
    
    try {
        vec.at(0).setValue(-1); // 这会抛出异常
    } catch (const std::exception& e) {
        std::cout << "捕获异常: " << e.what() << std::endl;
    }
    
    // vector 的 resize 操作依赖于移动构造函数的 noexcept
    // 如果移动构造函数不是 noexcept，vector 会使用拷贝而不是移动
    std::cout << "vector 大小: " << vec.size() << std::endl;
}

// RAII 和异常安全
class FileHandle {
private:
    FILE* file;
    
public:
    explicit FileHandle(const char* filename) {
        file = fopen(filename, "w");
        if (!file) {
            throw std::runtime_error("无法打开文件");
        }
        std::cout << "文件已打开: " << filename << std::endl;
    }
    
    ~FileHandle() noexcept {
        if (file) {
            fclose(file);
            std::cout << "文件已关闭" << std::endl;
        }
    }
    
    // 禁止拷贝
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    
    // 允许移动（noexcept 很重要）
    FileHandle(FileHandle&& other) noexcept : file(other.file) {
        other.file = nullptr;
        std::cout << "文件句柄已移动" << std::endl;
    }
    
    FileHandle& operator=(FileHandle&& other) noexcept {
        if (this != &other) {
            if (file) fclose(file);
            file = other.file;
            other.file = nullptr;
        }
        return *this;
    }
    
    void write(const char* data) {
        if (!file) {
            throw std::runtime_error("文件句柄无效");
        }
        if (fwrite(data, 1, strlen(data), file) != strlen(data)) {
            throw std::runtime_error("写入失败");
        }
    }
};

int main() {
    std::cout << "=== noexcept 和异常安全保证演示 ===" << std::endl;
    
    // 演示 noexcept 操作符
    demonstrateNoexceptOperator<NoExceptExample>();
    
    // 演示异常安全级别
    try {
        ExceptionSafetyDemo demo(5);
        demo.basicGuaranteeOperation();
        
        ExceptionSafetyDemo demo2(15);
        demo2.strongGuaranteeOperation(); // 这会抛出异常
    } catch (const std::exception& e) {
        std::cout << "异常安全演示捕获异常: " << e.what() << std::endl;
    }
    
    // 演示 vector 操作
    demonstrateVectorOperations();
    
    // 演示 RAII
    try {
        FileHandle handle("test.txt");
        handle.write("Hello, World!");
        // 即使这里抛出异常，文件也会被正确关闭
    } catch (const std::exception& e) {
        std::cout << "文件操作异常: " << e.what() << std::endl;
    }
    
    std::cout << "\n程序正常结束！" << std::endl;
    return 0;
}
