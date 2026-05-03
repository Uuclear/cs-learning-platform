package com.example.demo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

/**
 * 示例3: Spring Boot 实体类与数据访问
 * 展示 @Entity, @Repository 和 JPA Repository 的使用
 */

// 实体类 - 对应数据库表
@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String username;
    private String email;
    private int age;

    // 无参构造器（JPA 要求）
    public User() {}

    public User(String username, String email, int age) {
        this.username = username;
        this.email = email;
        this.age = age;
    }

    // Getter 和 Setter 方法
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    @Override
    public String toString() {
        return "User{id=" + id + ", username='" + username + "', email='" + email + "', age=" + age + "}";
    }
}

// 数据访问接口 - Spring Data JPA 会自动实现
@Repository
interface UserRepository extends JpaRepository<User, Long> {
    // Spring Data JPA 提供了基本的 CRUD 操作
    // 还可以添加自定义查询方法

    User findByUsername(String username);

    java.util.List<User> findByAgeGreaterThan(int age);
}