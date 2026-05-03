# 挑战 1：图书馆管理系统

## 背景
你是一家小型图书馆的管理员，需要开发一个简单的图书管理系统。

## 需求
1. 创建 `Book` 类，包含以下属性：
   - `title`（书名）
   - `author`（作者）
   - `isbn`（ISBN号）
   - `isAvailable`（是否可借阅）

2. 创建 `LibraryMember` 类，包含以下属性：
   - `memberId`（会员ID）
   - `name`（姓名）
   - `borrowedBooks`（已借阅的书籍列表）

3. 实现以下功能：
   - `borrowBook(Book book)`：借书功能，检查书籍是否可用
   - `returnBook(Book book)`：还书功能
   - `listAvailableBooks()`：列出所有可借阅的书籍

4. 使用继承创建特殊类型的书籍：
   - `ReferenceBook`（参考书）：不能外借，重写相关方法
   - `FictionBook`（小说）：可以外借，但有特殊的逾期规则

5. **额外挑战**：实现 `Searchable` 接口，允许按作者或标题搜索书籍

## 提示
- 使用封装原则，将属性设为私有，提供公共的getter/setter方法
- 考虑异常处理（如尝试借阅不可用的书籍）
- 使用 `@Override` 注解标记重写的方法