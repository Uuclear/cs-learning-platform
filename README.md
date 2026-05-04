# CS 知识学习平台

一个通俗易懂、幽默风趣的计算机科学学习平台。用生活化的比喻解释复杂的计算机概念，让学习变得生动有趣。

## 在线演示

> 部署后请访问: `https://<your-domain>` (或本地 `http://localhost:3000`)

## 功能特性

- **系统课程**: 覆盖 15+ 核心模块，50+ 精心设计的课程，从基础到进阶
- **通俗易懂**: 用生活化的比喻和类比，让抽象的 CS 概念变得具体可感
- **实战代码**: 每节课都配有可运行的代码示例，均有中文注释
- **多选测验**: 每节课后配有互动测验，即时检验学习效果
- **进度追踪**: 本地存储学习进度，支持跨标签页同步
- **主题切换**: 支持 Light / Dark 模式，自动保存偏好设置
- **全文搜索**: 支持课程标题、描述、正文内容的全局搜索
- **书签收藏**: 收藏感兴趣的课程，快速回顾
- **最近浏览**: 自动记录最近访问的课程
- **打印输出**: 课程页面支持打印，自动隐藏导航等交互元素
- **移动端适配**: 响应式布局，侧栏抽屉式导航
- **上下课导航**: 课程底部提供上/下一课按钮，支持键盘快捷键 ← →

## 课程模块

| 模块 | 课程数 | 难度 |
|------|--------|------|
| 计算机基础 | 5 | 入门 |
| 数据结构 | 10 | 入门-中等 |
| 算法 | 10 | 中等 |
| 操作系统 | 10 | 中等-困难 |
| 数据库 | 10 | 入门-中等 |
| 计算机网络 | 8 | 中等 |
| 编程语言 | 6 | 入门-中等 |
| 计算机组成原理 | 6 | 中等 |
| 微机原理 | 6 | 困难 |
| 汇编语言 | 5 | 困难 |
| C++ | 5 | 中等 |
| C 语言 | 5 | 入门 |
| Java | 5 | 入门 |
| JavaScript | 5 | 入门 |
| Rust | 5 | 困难 |
| 机器学习 | 6 | 中等 |
| 深度学习 | 5 | 困难 |
| 强化学习 | 5 | 专家 |

## 技术栈

- **框架**: [Next.js 14](https://nextjs.org/) (App Router, SSG)
- **语言**: TypeScript (strict mode)
- **样式**: [Tailwind CSS](https://tailwindcss.com/) + CSS Variables
- **图标**: [Lucide React](https://lucide.dev/)
- **MDX 渲染**: Marked + Sanitize-HTML
- **状态管理**: LocalStorage (无后端)
- **字体**: Geist Sans / Geist Mono

## 快速开始

### 环境要求

- Node.js >= 18
- npm >= 9

### 安装依赖

```bash
cd platform
npm install
```

### 开发模式

```bash
cd platform
npm run dev
```

访问 `http://localhost:3000`

### 构建生产版本

```bash
cd platform
npm run build
npm run start
```

## 部署

### GitHub Pages (推荐，免费)

**CI 自动部署**: 推送到 `main` 分支后，GitHub Actions 会自动构建并部署到 GitHub Pages。

**手动部署**:
```bash
./deploy.sh --gh-pages
```

> 需在 GitHub 仓库设置 → Pages → Build and deployment → Source: GitHub Actions

### Vercel (一键部署)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2F<your-username>%2Fcs-learning-platform&project-name=cs-learning-platform&repository-name=cs-learning-platform&root-directory=platform)

### 手动部署 (Node.js 服务器)

```bash
cd platform
npm run build
npm run start
```

或使用一键部署脚本:

```bash
./deploy.sh
```

## 项目结构

```
.
├── platform/                    # Next.js 应用
│   ├── app/                     # App Router 页面
│   │   ├── page.tsx             # 首页
│   │   ├── courses/             # 课程页面
│   │   │   ├── page.tsx         # 课程列表
│   │   │   ├── client.tsx       # 客户端课程列表
│   │   │   └── [slug]/page.tsx  # 课程详情
│   │   └── api/search/route.ts  # 全文搜索 API
│   ├── components/              # React 组件
│   │   ├── layout/              # 布局组件 (Header, Sidebar, ThemeToggle)
│   │   ├── course/              # 课程组件 (SearchBar, Quiz, Navigation)
│   │   └── ui/                  # UI 基础组件 (Button, Card, Badge)
│   ├── lib/                     # 工具函数
│   │   ├── courses.ts           # 课程数据加载
│   │   ├── progress.ts          # 学习进度管理
│   │   ├── mdx-renderer.ts      # MDX → HTML 渲染
│   │   └── search.ts            # 全文搜索索引
│   ├── types/                   # TypeScript 类型定义
│   └── styles/                  # 全局样式
├── courses/                     # 课程内容 (MDX + 代码 + 测验)
│   ├── 01-computer-basics/      # 模块目录
│   │   ├── lesson-01-*/         # 课程目录
│   │   │   ├── index.mdx        # 课程正文
│   │   │   ├── metadata.json    # 课程元数据
│   │   │   ├── code/            # 代码示例
│   │   │   └── exercises/       # 测验题目
│   │   └── ...
│   └── ...
├── deploy.sh                    # 一键部署脚本
└── .github/workflows/           # GitHub Actions CI/CD
    └── deploy.yml               # GitHub Pages 自动部署
```

## 添加新课程

每门课程需要三个文件：

1. `courses/<module>/<lesson>/metadata.json` — 课程元数据
2. `courses/<module>/<lesson>/index.mdx` — 课程内容 (Markdown)
3. `courses/<module>/<lesson>/exercises/quiz.json` — 测验题目 (可选)

## 开源协议

MIT
