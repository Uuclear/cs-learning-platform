#include <iostream>
#include <stdexcept>
#include <string>

// 自定义异常基类
class CustomException : public std::exception {
protected:
    std::string message;
    
public:
    explicit CustomException(const std::string& msg) : message(msg) {}
    
    const char* what() const noexcept override {
        return message.c_str();
    }
};

// 数据库异常
class DatabaseException : public CustomException {
public:
    explicit DatabaseException(const std::string& msg) 
        : CustomException("数据库错误: " + msg) {}
};

// 网络异常
class NetworkException : public CustomException {
public:
    explicit NetworkException(const std::string& msg) 
        : CustomException("网络错误: " + msg) {}
};

// 配置异常
class ConfigurationException : public CustomException {
public:
    explicit ConfigurationException(const std::string& msg) 
        : CustomException("配置错误: " + msg) {}
};

// 具体的数据库异常
class ConnectionFailedException : public DatabaseException {
public:
    explicit ConnectionFailedException(const std::string& host, int port)
        : DatabaseException("连接失败 - 主机: " + host + ", 端口: " + std::to_string(port)) {}
};

class QueryExecutionException : public DatabaseException {
private:
    std::string query;
    
public:
    explicit QueryExecutionException(const std::string& query, const std::string& reason)
        : DatabaseException("查询执行失败 - 原因: " + reason), query(query) {}
        
    const std::string& getQuery() const {
        return query;
    }
};

// 模拟数据库操作函数
void connectToDatabase(const std::string& host, int port) {
    if (host.empty() || port <= 0 || port > 65535) {
        throw ConnectionFailedException(host, port);
    }
    std::cout << "成功连接到数据库: " << host << ":" << port << std::endl;
}

void executeQuery(const std::string& query) {
    if (query.empty()) {
        throw QueryExecutionException(query, "查询语句为空");
    }
    if (query.find("DROP") != std::string::npos) {
        throw QueryExecutionException(query, "不允许执行危险操作");
    }
    std::cout << "成功执行查询: " << query << std::endl;
}

// 异常处理演示
void demonstrateCustomExceptions() {
    std::cout << "=== 自定义异常类层次演示 ===" << std::endl;

    // 测试数据库连接异常
    try {
        connectToDatabase("", -1);
    } catch (const ConnectionFailedException& e) {
        std::cout << "捕获到连接失败异常: " << e.what() << std::endl;
    } catch (const DatabaseException& e) {
        std::cout << "捕获到数据库异常: " << e.what() << std::endl;
    } catch (const CustomException& e) {
        std::cout << "捕获到自定义异常: " << e.what() << std::endl;
    }

    // 测试查询执行异常
    try {
        executeQuery("DROP TABLE users");
    } catch (const QueryExecutionException& e) {
        std::cout << "捕获到查询执行异常: " << e.what() << std::endl;
        std::cout << "有问题的查询: " << e.getQuery() << std::endl;
    } catch (const DatabaseException& e) {
        std::cout << "捕获到数据库异常: " << e.what() << std::endl;
    }

    // 测试通用异常处理
    try {
        throw NetworkException("网络超时");
    } catch (const CustomException& e) {
        std::cout << "捕获到自定义异常: " << e.what() << std::endl;
    } catch (const std::exception& e) {
        std::cout << "捕获到标准异常: " << e.what() << std::endl;
    }
}

// 异常安全的资源管理示例
class ResourceManager {
private:
    std::string resource_name;
    bool acquired;
    
public:
    explicit ResourceManager(const std::string& name) 
        : resource_name(name), acquired(false) {
        std::cout << "创建资源管理器: " << resource_name << std::endl;
    }
    
    void acquire() {
        if (resource_name == "invalid") {
            throw ConfigurationException("无效的资源配置");
        }
        acquired = true;
        std::cout << "成功获取资源: " << resource_name << std::endl;
    }
    
    ~ResourceManager() {
        if (acquired) {
            std::cout << "释放资源: " << resource_name << std::endl;
        }
    }
};

void testResourceManager() {
    std::cout << "\n=== 异常安全的资源管理 ===" << std::endl;
    
    try {
        ResourceManager rm("database_connection");
        rm.acquire();
        // 正常使用资源...
        std::cout << "正常使用资源..." << std::endl;
    } catch (const std::exception& e) {
        std::cout << "资源管理异常: " << e.what() << std::endl;
    }
    
    try {
        ResourceManager rm("invalid");
        rm.acquire(); // 这会抛出异常
    } catch (const ConfigurationException& e) {
        std::cout << "配置异常: " << e.what() << std::endl;
        // 注意：即使抛出异常，析构函数也会被调用，确保资源清理
    }
}

int main() {
    demonstrateCustomExceptions();
    testResourceManager();
    
    std::cout << "\n程序正常结束！" << std::endl;
    return 0;
}
