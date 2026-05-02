# CS知识学习网站 - 第一阶段实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** 搭建CS知识学习网站的基础框架，开发第一门示例课程，建立Agent协作流程

**Architecture:** 采用模块化课程系统，每节课独立开发。主Agent负责框架搭建和任务分配，子Agent负责具体课程开发。

**Tech Stack:** Next.js 14, React 18, TypeScript, Tailwind CSS, MDX

---

## 阶段目标

第一阶段（MVP验证）：
1. 搭建网站平台框架
2. 开发1门示例课程（01-01 冯诺依曼架构）
3. 验证Agent协作流程

---

## 任务清单

### Task 1: 初始化Next.js项目

**Files:**
- Create: `platform/package.json`
- Create: `platform/tsconfig.json`
- Create: `platform/tailwind.config.ts`
- Create: `platform/postcss.config.js`
- Create: `platform/next.config.js`
- Create: `platform/app/globals.css`
- Create: `platform/app/layout.tsx`
- Create: `platform/app/page.tsx`

- [ ] **Step 1: 创建package.json**
- [ ] **Step 2: 安装依赖**
- [ ] **Step 3: 配置TypeScript**
- [ ] **Step 4: 配置Tailwind CSS**
- [ ] **Step 5: 配置Next.js**
- [ ] **Step 6: 创建全局样式**
- [ ] **Step 7: 创建布局组件**
- [ ] **Step 8: 创建首页**
- [ ] **Step 9: 测试开发服务器**
- [ ] **Step 10: 提交**

### Task 2: 创建共享组件库

**Files:**
- Create: `platform/lib/utils.ts`
- Create: `platform/components/ui/Button.tsx`
- Create: `platform/components/ui/Card.tsx`
- Create: `platform/components/ui/Badge.tsx`

- [ ] **Step 1: 创建工具函数**
- [ ] **Step 2: 创建Button组件**
- [ ] **Step 3: 创建Card组件**
- [ ] **Step 4: 创建Badge组件**
- [ ] **Step 5: 提交**

### Task 3: 创建课程数据结构

**Files:**
- Create: `platform/types/course.ts`
- Create: `platform/lib/courses.ts`

- [ ] **Step 1: 创建类型定义**
- [ ] **Step 2: 创建课程数据**
- [ ] **Step 3: 提交**

### Task 4: 创建导航组件

**Files:**
- Create: `platform/components/layout/Header.tsx`
- Create: `platform/components/layout/Sidebar.tsx`
- Modify: `platform/app/layout.tsx`

- [ ] **Step 1: 创建Header组件**
- [ ] **Step 2: 创建Sidebar组件**
- [ ] **Step 3: 更新布局**
- [ ] **Step 4: 提交**

### Task 5: 创建课程列表页面

**Files:**
- Create: `platform/app/courses/page.tsx`
- Modify: `platform/app/page.tsx`

- [ ] **Step 1: 创建课程列表页**
- [ ] **Step 2: 更新首页**
- [ ] **Step 3: 提交**

### Task 6: 创建示例课程内容

**Files:**
- Create: `courses/01-computer-basics/lesson-01-von-neumann-architecture/index.mdx`
- Create: `courses/01-computer-basics/lesson-01-von-neumann-architecture/metadata.json`
- Create: `courses/01-computer-basics/lesson-01-von-neumann-architecture/code/examples/example-01-cpu-simulation.py`

- [ ] **Step 1: 创建课程目录结构**
- [ ] **Step 2: 创建示例课程元数据**
- [ ] **Step 3: 创建示例代码**
- [ ] **Step 4: 创建课程MDX内容**
- [ ] **Step 5: 提交**

### Task 7: 创建课程详情页面

**Files:**
- Create: `platform/app/courses/[slug]/page.tsx`
- Create: `platform/components/course/CourseContent.tsx`
- Create: `platform/components/course/CodeBlock.tsx`

- [ ] **Step 1: 创建代码块组件**
- [ ] **Step 2: 创建课程内容组件**
- [ ] **Step 3: 创建课程详情页**
- [ ] **Step 4: 提交**

### Task 8: 配置MDX渲染

**Files:**
- Create: `platform/mdx-components.tsx`
- Modify: `platform/next.config.js`
- Modify: `platform/app/courses/[slug]/page.tsx`

- [ ] **Step 1: 创建MDX组件映射**
- [ ] **Step 2: 更新Next.js配置**
- [ ] **Step 3: 更新课程详情页**
- [ ] **Step 4: 提交**

### Task 9: 更新进度文档

**Files:**
- Modify: `claude-progress.txt`

- [ ] **Step 1: 更新进度**
- [ ] **Step 2: 提交**

---

## 阶段完成标准

第一阶段完成时，应该能够：

- [ ] 运行 `npm run dev` 启动开发服务器
- [ ] 访问首页看到课程介绍
- [ ] 访问 `/courses` 看到课程列表
- [ ] 访问 `/courses/lesson-01-von-neumann-architecture` 看到示例课程内容
- [ ] 代码块能够正确渲染
- [ ] 导航栏和侧边栏正常工作

---

## 下一阶段计划

第二阶段将：
1. 并行开发多个子Agent创建剩余49门课程
2. 完善平台功能（搜索、进度跟踪、用户系统）
3. 添加交互式代码运行环境
4. 部署到Vercel

---

*计划创建时间: 2026-05-03*
*计划版本: v1.0*
