# 挑战 2：构建完整的前端工具链配置 ⭐⭐⭐⭐

## 背景
你的团队正在启动一个新的 React 项目，需要配置一个完整的、生产就绪的前端工具链。项目要求支持 TypeScript、CSS Modules、代码分割、性能优化和开发体验。

## 要求
创建一个完整的构建配置，可以选择 Webpack 或 Vite，并实现以下功能：

### 核心功能
1. **TypeScript 支持**：编译 `.ts` 和 `.tsx` 文件
2. **CSS 处理**：支持 CSS Modules、PostCSS（自动添加 vendor 前缀）
3. **资源处理**：正确处理图片、字体等静态资源
4. **开发服务器**：支持 HMR、代理 API 请求
5. **生产优化**：代码分割、压缩、缓存策略

### 高级功能
6. **性能分析**：集成 Webpack Bundle Analyzer 或类似工具
7. **环境配置**：区分开发、测试、生产环境
8. **Linting & Formatting**：集成 ESLint 和 Prettier
9. **测试支持**：配置 Jest 测试环境

## 具体任务

### 方案 A：Webpack 配置
- 创建 `webpack.config.js`（或分离的配置文件）
- 实现上述所有功能
- 提供 npm scripts：`dev`、`build`、`analyze`、`test`

### 方案 B：Vite 配置  
- 创建 `vite.config.ts`
- 实现相同的功能集
- 利用 Vite 的原生 ES 模块优势

## 评估标准
- **功能性**：所有要求的功能都正确实现
- **性能**：开发服务器启动快，HMR 响应迅速
- **可维护性**：配置清晰、模块化、有注释
- **最佳实践**：遵循当前社区的最佳实践
- **错误处理**：有适当的错误边界和调试信息

## 提交内容
1. 完整的配置文件
2. `package.json` 中的相关脚本和依赖
3. 简短的 README 说明配置的关键决策和使用方法
4. 性能基准测试结果（可选但推荐）

## 扩展挑战
- 实现自定义插件来自动化某个重复任务
- 配置微前端架构支持
- 添加 Docker 容器化支持
- 集成 CI/CD 流水线配置

## 参考资源
- Webpack 官方文档的高级配置指南
- Vite 插件生态系统
- Create React App 的配置作为参考
- 当前流行的 starter templates