# 挑战 1：创建一个完整的数学工具库

## 目标
创建一个功能完整的数学工具库 crate，包含基本运算、安全操作、统计函数，并正确配置 Cargo.toml。

## 要求

### 1. 项目结构
- 使用 `cargo new math-toolbox --lib` 创建新项目
- 在 `src/lib.rs` 中实现所有功能
- 在 `tests/` 目录下创建集成测试

### 2. 功能实现
实现以下函数：

**基本运算：**
- `add(a: i32, b: i32) -> i32`
- `subtract(a: i32, b: i32) -> i32`
- `multiply(a: i32, b: i32) -> Option<i32>`（带溢出检查）
- `safe_divide(dividend: f64, divisor: f64) -> Option<f64>`

**高级功能：**
- `factorial(n: u32) -> Option<u64>`（带溢出检查）
- `is_prime(n: u32) -> bool`
- `gcd(a: u32, b: u32) -> u32`（最大公约数）

**统计函数：**
- `mean(numbers: &[f64]) -> Option<f64>`
- `median(numbers: Vec<f64>) -> Option<f64>`

### 3. Cargo.toml 配置
- 设置正确的包信息（name, version, description, license, authors）
- 添加可选特性：
  - `statistics`：启用统计函数（默认启用）
  - `advanced`：启用高级数学函数
- 添加开发依赖：`anyhow = "1.0"` 用于错误处理

### 4. 文档和测试
- 为所有公共函数添加详细的文档注释（使用 `///`）
- 编写全面的单元测试，覆盖正常情况和边界情况
- 编写集成测试，测试多个函数的组合使用
- 确保所有测试通过：`cargo test`

### 5. 文档生成
- 运行 `cargo doc --open` 验证文档生成正确
- 确保文档包含使用示例和参数说明

## 提交要求
提交完整的项目目录，包括：
- `Cargo.toml`
- `src/lib.rs`
- `tests/integration_tests.rs`
- 确保 `cargo test` 和 `cargo doc` 都能正常工作

## 评分标准
- 功能完整性（30%）
- 代码质量与错误处理（25%）
- Cargo.toml 配置正确性（20%）
- 文档质量（15%）
- 测试覆盖率（10%）