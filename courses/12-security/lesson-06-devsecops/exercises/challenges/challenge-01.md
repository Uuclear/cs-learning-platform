# 挑战 1: 构建安全的CI/CD管道

## 背景
你正在为一个Python Web应用程序构建CI/CD管道。该应用使用Flask框架，依赖多个第三方库，并需要访问外部API。

## 任务
设计一个完整的GitHub Actions工作流文件（`.github/workflows/security.yml`），包含以下安全扫描步骤：

1. **SAST扫描**：使用Bandit工具扫描Python代码中的安全漏洞
2. **依赖项扫描**：使用pip-audit检查requirements.txt中的漏洞
3. **密钥扫描**：使用gitleaks检测意外提交的敏感信息
4. **容器扫描**：如果项目包含Dockerfile，扫描构建的镜像

## 要求
- 所有扫描步骤都应该在测试步骤之后、部署步骤之前运行
- 任何安全扫描发现高危或严重漏洞时，应该使整个工作流失败
- 为每个扫描工具提供适当的配置和忽略规则（如果有）
- 工作流应该在每次pull request到main分支时触发

## 提交内容
创建完整的`security.yml`文件，包含所有必要的步骤和配置。

## 提示
- Bandit配置文件可以放在`.bandit`文件中
- pip-audit可以直接运行而无需额外配置
- gitleaks需要安装并配置适当的规则
- 考虑使用Docker的buildx来构建和扫描镜像