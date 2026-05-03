# 挑战 2：发布你的第一个 crate 到 crates.io

## 目标
将你在挑战 1 中创建的数学工具库发布到 crates.io，让全世界的 Rust 开发者都能使用。

## 要求

### 1. 准备工作
- 在 [crates.io](https://crates.io) 注册账户（如果还没有）
- 获取 API token：登录后点击账户名 → Account Settings → API Tokens → New Token
- 在本地运行 `cargo login your-api-token`

### 2. 完善 crate 元数据
在 `Cargo.toml` 中确保包含以下字段：

```toml
[package]
name = "your-unique-crate-name"  # 必须是全局唯一的！
version = "0.1.0"
edition = "2021"
description = "A comprehensive math toolbox for Rust"
license = "MIT"  # 或其他开源许可证
repository = "https://github.com/your-username/your-repo"
documentation = "https://docs.rs/your-crate-name"
readme = "README.md"
keywords = ["math", "utilities", "calculator"]
categories = ["algorithms", "science"]
```

### 3. 创建 README.md
在项目根目录创建 `README.md`，包含：

- **项目标题和简短描述**
- **安装说明**（如何在 Cargo.toml 中添加依赖）
- **使用示例**（代码示例展示主要功能）
- **特性说明**（可选特性的使用方法）
- **许可证信息**

### 4. 文档优化
- 确保所有公共 API 都有完整的文档注释
- 在 crate 根级别添加模块级文档（使用 `//!`）
- 包含详细的使用示例，这些示例会被自动测试
- 使用 `cargo doc --no-deps --open` 预览文档

### 5. 版本验证
- 运行 `cargo publish --dry-run` 验证所有配置正确
- 修复任何出现的错误或警告
- 确保所有依赖都使用兼容的版本约束

### 6. 正式发布
- 运行 `cargo publish` 发布你的 crate
- 验证发布成功：访问 `https://crates.io/crates/your-crate-name`
- 验证文档生成：访问 `https://docs.rs/your-crate-name`

### 7. 后续维护计划
创建一个 `RELEASES.md` 文件，规划未来的版本：

- **v0.1.0**：初始版本（当前）
- **v0.2.0**：添加更多数学函数（三角函数、对数等）
- **v1.0.0**：稳定 API，承诺向后兼容

## 注意事项

### 命名规则
- crate 名称必须是小写字母、数字、连字符的组合
- 名称在 crates.io 上必须是全局唯一的
- 建议使用描述性的名称，如 `math-toolbox-rs` 或 `rust-math-utils`

### 许可证选择
- 必须指定有效的开源许可证
- 推荐使用 MIT、Apache-2.0 或双许可证
- 确保你了解所选许可证的要求

### 质量保证
- 确保所有代码都有相应的测试
- 文档示例必须能够编译和运行
- 避免不必要的依赖，保持 crate 轻量

## 提交要求
提交以下文件：
- 完整的项目目录（包括 README.md 和 RELEASES.md）
- crates.io 发布成功的截图或链接
- docs.rs 文档页面的截图或链接

## 扩展挑战（可选）
- 实现 Serde 序列化支持作为可选特性
- 添加工作空间支持，将不同功能拆分为多个子 crate
- 配置 GitHub Actions 自动运行测试和检查

## 评分标准
- 发布成功（40%）
- 文档质量（25%）
- README 完整性（20%）
- 维护计划合理性（15%）