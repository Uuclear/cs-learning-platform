package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * 示例2: Spring Boot 依赖注入演示
 * 展示 @Service 和 @Autowired 注解的使用
 */
@Service
public class UserService {

    private final EmailService emailService;
    private final NotificationService notificationService;

    // 构造器注入（推荐方式）
    public UserService(EmailService emailService, NotificationService notificationService) {
        this.emailService = emailService;
        this.notificationService = notificationService;
    }

    // 也可以使用字段注入（不推荐但常见）
    // @Autowired
    // private EmailService emailService;

    public void registerUser(String username, String email) {
        // 业务逻辑：注册用户
        System.out.println("注册用户: " + username);

        // 使用注入的服务
        emailService.sendWelcomeEmail(email);
        notificationService.sendRegistrationNotification(username);
    }

    public String getUserProfile(String username) {
        return "用户 " + username + " 的个人资料";
    }
}

// 模拟邮件服务
@Service
class EmailService {
    public void sendWelcomeEmail(String email) {
        System.out.println("发送欢迎邮件到: " + email);
    }
}

// 模拟通知服务
@Service
class NotificationService {
    public void sendRegistrationNotification(String username) {
        System.out.println("发送注册通知给用户: " + username);
    }
}