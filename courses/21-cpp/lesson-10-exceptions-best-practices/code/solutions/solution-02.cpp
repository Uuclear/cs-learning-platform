#include <iostream>
#include <stdexcept>
#include <string>
#include <memory>

// 改进的自定义异常层次结构
class ApplicationException : public std::exception {
protected:
    std::string message;
    std::string component;
    
public:
    explicit ApplicationException(const std::string& comp, const std::string& msg) 
        : component(comp), message(comp + ": " + msg) {}
    
    const char* what() const noexcept override {
        return message.c_str();
    }
    
    const std::string& getComponent() const noexcept {
        return component;
    }
};

// 客户端异常
class ClientException : public ApplicationException {
public:
    explicit ClientException(const std::string& msg) 
        : ApplicationException("Client", msg) {}
};

// 服务器异常
class ServerException : public ApplicationException {
public:
    explicit ServerException(const std::string& msg) 
        : ApplicationException("Server", msg) {}
};

// 验证异常
class ValidationException : public ClientException {
private:
    std::string field_name;
    
public:
    ValidationException(const std::string& field, const std::string& msg)
        : ClientException("验证失败 - 字段: " + field + ", " + msg), field_name(field) {}
        
    const std::string& getFieldName() const noexcept {
        return field_name;
    }
};

// 认证异常
class AuthenticationException : public ClientException {
public:
    explicit AuthenticationException(const std::string& reason)
        : ClientException("认证失败 - " + reason) {}
};

// 授权异常
class AuthorizationException : public ClientException {
public:
    explicit AuthorizationException(const std::string& resource, const std::string& action)
        : ClientException("授权失败 - 无权执行 " + action + " 操作于 " + resource) {}
};

// 数据库异常
class DatabaseException : public ServerException {
public:
    explicit DatabaseException(const std::string& msg)
        : ServerException("数据库错误 - " + msg) {}
};

// 网络异常
class NetworkException : public ServerException {
public:
    explicit NetworkException(const std::string& msg)
        : ServerException("网络错误 - " + msg) {}
};

// 配置异常
class ConfigurationException : public ServerException {
public:
    explicit ConfigurationException(const std::string& msg)
        : ServerException("配置错误 - " + msg) {}
};

// 异常工厂模式
class ExceptionFactory {
public:
    static std::unique_ptr<ValidationException> createValidationException(
        const std::string& field, const std::string& msg) {
        return std::make_unique<ValidationException>(field, msg);
    }
    
    static std::unique_ptr<AuthenticationException> createAuthenticationException(
        const std::string& reason) {
        return std::make_unique<AuthenticationException>(reason);
    }
    
    static std::unique_ptr<AuthorizationException> createAuthorizationException(
        const std::string& resource, const std::string& action) {
        return std::make_unique<AuthorizationException>(resource, action);
    }
};

// 用户验证服务
class UserService {
public:
    static void validateUser(const std::string& username, const std::string& email) {
        if (username.empty()) {
            throw *ExceptionFactory::createValidationException("username", "用户名不能为空");
        }
        if (username.length() < 3) {
            throw *ExceptionFactory::createValidationException("username", "用户名长度至少为3个字符");
        }
        if (email.empty() || email.find('@') == std::string::npos) {
            throw *ExceptionFactory::createValidationException("email", "邮箱格式无效");
        }
        std::cout << "用户验证通过: " << username << " (" << email << ")" << std::endl;
    }
    
    static void authenticateUser(const std::string& username, const std::string& password) {
        if (password.length() < 8) {
            throw *ExceptionFactory::createAuthenticationException("密码长度不足8位");
        }
        if (username == "admin" && password != "secure_password") {
            throw *ExceptionFactory::createAuthenticationException("管理员密码错误");
        }
        std::cout << "用户认证成功: " << username << std::endl;
    }
    
    static void authorizeAction(const std::string& username, const std::string& resource, const std::string& action) {
        if (username == "guest" && (action == "delete" || action == "modify")) {
            throw *ExceptionFactory::createAuthorizationException(resource, action);
        }
        std::cout << "授权成功: " << username << " 可以 " << action << " " << resource << std::endl;
    }
};

// 异常处理策略
void handleApplicationException(const ApplicationException& e) {
    std::cout << "应用异常处理 [" << e.getComponent() << "]: " << e.what() << std::endl;
    
    // 根据组件类型进行不同处理
    if (e.getComponent() == "Client") {
        std::cout << "客户端错误 - 向用户显示友好消息" << std::endl;
    } else if (e.getComponent() == "Server") {
        std::cout << "服务器错误 - 记录日志并通知管理员" << std::endl;
    }
}

// 综合演示
void demonstrateExceptionHierarchy() {
    std::cout << "=== 改进的异常层次结构演示 ===" << std::endl;

    // 用户验证测试
    try {
        UserService::validateUser("", "test@example.com");
    } catch (const ValidationException& e) {
        std::cout << "验证异常 - 字段: " << e.getFieldName() << ", 消息: " << e.what() << std::endl;
    } catch (const ClientException& e) {
        handleApplicationException(e);
    }

    // 认证测试
    try {
        UserService::authenticateUser("admin", "weak");
    } catch (const AuthenticationException& e) {
        std::cout << "认证异常: " << e.what() << std::endl;
    } catch (const ClientException& e) {
        handleApplicationException(e);
    }

    // 授权测试
    try {
        UserService::authorizeAction("guest", "user_profile", "delete");
    } catch (const AuthorizationException& e) {
        std::cout << "授权异常: " << e.what() << std::endl;
    } catch (const ClientException& e) {
        handleApplicationException(e);
    }

    // 通用异常处理
    try {
        throw ConfigurationException("数据库连接字符串缺失");
    } catch (const ServerException& e) {
        handleApplicationException(e);
    } catch (const ApplicationException& e) {
        handleApplicationException(e);
    } catch (const std::exception& e) {
        std::cout << "未预期的异常: " << e.what() << std::endl;
    }
}

// 异常安全的资源管理
class DatabaseConnection {
private:
    std::string connection_string;
    bool connected;
    
public:
    explicit DatabaseConnection(const std::string& conn_str) 
        : connection_string(conn_str), connected(false) {
        if (conn_str.empty()) {
            throw ConfigurationException("连接字符串为空");
        }
        std::cout << "创建数据库连接对象" << std::endl;
    }
    
    void connect() {
        if (connection_string.find("invalid") != std::string::npos) {
            throw DatabaseException("无法连接到数据库服务器");
        }
        connected = true;
        std::cout << "数据库连接成功" << std::endl;
    }
    
    ~DatabaseConnection() noexcept {
        if (connected) {
            std::cout << "关闭数据库连接" << std::endl;
        }
    }
    
    // 禁止拷贝，允许移动
    DatabaseConnection(const DatabaseConnection&) = delete;
    DatabaseConnection& operator=(const DatabaseConnection&) = delete;
    
    DatabaseConnection(DatabaseConnection&& other) noexcept 
        : connection_string(std::move(other.connection_string)), connected(other.connected) {
        other.connected = false;
        std::cout << "移动数据库连接" << std::endl;
    }
};

void testDatabaseConnection() {
    std::cout << "\n=== 异常安全的数据库连接 ===" << std::endl;
    
    try {
        DatabaseConnection conn("valid_connection_string");
        conn.connect();
        // 正常使用...
    } catch (const DatabaseException& e) {
        std::cout << "数据库连接异常: " << e.what() << std::endl;
    } catch (const ConfigurationException& e) {
        std::cout << "配置异常: " << e.what() << std::endl;
    }
    // 即使抛出异常，析构函数也会被调用
    
    try {
        DatabaseConnection conn("invalid_connection");
        conn.connect(); // 这会抛出异常
    } catch (const std::exception& e) {
        std::cout << "连接异常: " << e.what() << std::endl;
    }
}

int main() {
    demonstrateExceptionHierarchy();
    testDatabaseConnection();
    
    std::cout << "\n程序正常结束！" << std::endl;
    return 0;
}
