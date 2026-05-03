package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 示例1: Spring Boot REST API 基础
 * 使用 @RestController 注解创建简单的 REST 控制器
 */
@RestController
@RequestMapping("/api")
public class HelloController {

    @GetMapping("/hello")
    public String sayHello() {
        return "Hello, Spring Boot!";
    }

    @GetMapping("/welcome")
    public Greeting welcome() {
        return new Greeting("欢迎来到 Spring Boot 世界！", "这是一个自动生成的问候");
    }

    // 内部类用于返回 JSON 对象
    public static class Greeting {
        private String message;
        private String description;

        public Greeting(String message, String description) {
            this.message = message;
            this.description = description;
        }

        // Getter 方法（Spring Boot 会自动序列化为 JSON）
        public String getMessage() {
            return message;
        }

        public String getDescription() {
            return description;
        }
    }
}