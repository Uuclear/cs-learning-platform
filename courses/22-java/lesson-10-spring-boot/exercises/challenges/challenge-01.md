# 挑战任务 1：构建图书管理 API

## 任务描述
使用 Spring Boot 创建一个完整的图书管理 REST API，包含以下功能：

### 功能要求
1. **实体类设计**：
   - `Book` 实体类，包含字段：id、title（书名）、author（作者）、isbn（ISBN号）、publishedYear（出版年份）
   - 使用 JPA 注解正确配置实体关系

2. **数据访问层**：
   - 创建 `BookRepository` 接口，继承 `JpaRepository<Book, Long>`
   - 添加自定义查询方法：按作者查找、按出版年份范围查找

3. **服务层**：
   - 创建 `BookService` 类，使用 `@Service` 注解
   - 实现完整的 CRUD 操作（创建、读取、更新、删除）
   - 在创建和更新图书时进行数据验证（如 ISBN 格式验证）

4. **控制器层**：
   - 创建 `BookController` 类，使用 `@RestController` 注解
   - 实现以下 REST 端点：
     - `GET /api/books` - 获取所有图书
     - `GET /api/books/{id}` - 根据 ID 获取单本图书
     - `POST /api/books` - 创建新图书
     - `PUT /api/books/{id}` - 更新图书信息
     - `DELETE /api/books/{id}` - 删除图书
     - `GET /api/books/search?author={author}` - 按作者搜索

### 技术要求
- 使用构造器注入而非字段注入
- 正确处理异常情况（如图书不存在）
- 返回适当的 HTTP 状态码
- 使用 DTO（数据传输对象）进行请求/响应

### 提示
- 参考课程中的用户管理示例
- 记住 Spring Boot 的约定优于配置原则
- 考虑使用 `ResponseEntity` 来控制 HTTP 响应

### 验收标准
- 所有端点都能正常工作
- 数据验证逻辑正确
- 代码结构清晰，符合 Spring Boot 最佳实践
- 包含适当的错误处理