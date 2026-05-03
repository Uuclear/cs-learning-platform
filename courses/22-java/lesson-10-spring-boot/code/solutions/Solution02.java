package com.example.userapi;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.List;
import java.util.Optional;

/**
 * 用户服务实现 - 业务逻辑层
 */
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EmailService emailService;

    public List<User> findAllUsers() {
        return userRepository.findAll();
    }

    public User findUserById(Long id) {
        Optional<User> user = userRepository.findById(id);
        return user.orElse(null);
    }

    public User createUser(String username, String email) {
        // 验证用户名唯一性
        if (userRepository.findByUsername(username) != null) {
            throw new RuntimeException("用户名已存在: " + username);
        }

        User user = new User();
        user.setUsername(username);
        user.setEmail(email);

        User savedUser = userRepository.save(user);

        // 发送欢迎邮件
        emailService.sendWelcomeEmail(email);

        return savedUser;
    }

    public User updateUser(Long id, String username, String email) {
        User existingUser = findUserById(id);
        if (existingUser == null) {
            return null;
        }

        // 检查用户名是否被其他用户使用
        User existingByUsername = userRepository.findByUsername(username);
        if (existingByUsername != null && !existingByUsername.getId().equals(id)) {
            throw new RuntimeException("用户名已被其他用户使用: " + username);
        }

        existingUser.setUsername(username);
        existingUser.setEmail(email);
        return userRepository.save(existingUser);
    }

    public boolean deleteUser(Long id) {
        User user = findUserById(id);
        if (user != null) {
            userRepository.delete(user);
            return true;
        }
        return false;
    }
}

/**
 * 邮件服务
 */
@Service
class EmailService {

    public void sendWelcomeEmail(String email) {
        System.out.println("发送欢迎邮件到: " + email);
        // 实际应用中这里会调用邮件发送服务
    }

    public void sendUpdateNotification(String email, String username) {
        System.out.println("发送更新通知到: " + email + "，用户: " + username);
    }
}