# 编程挑战 1：事件委托实现待办事项列表

## 任务描述

创建一个简单的待办事项（Todo）列表应用，要求使用**事件委托**来处理用户交互。

## 功能要求

1. **添加任务**：用户可以在输入框中输入任务内容，点击"添加"按钮或按回车键添加新任务
2. **删除任务**：每个任务项右侧有一个"删除"按钮，点击后删除对应任务
3. **标记完成**：点击任务文本可以切换完成状态（添加删除线样式）
4. **使用事件委托**：所有交互必须通过在父容器上绑定一个事件监听器来处理

## HTML结构要求

```html
<div id="todo-app">
  <h2>我的待办事项</h2>
  <div class="input-section">
    <input type="text" id="task-input" placeholder="输入新任务...">
    <button id="add-task">添加</button>
  </div>
  <ul id="task-list">
    <!-- 任务项将在这里动态添加 -->
  </ul>
</div>
```

## 任务项结构

每个任务项应该具有以下结构：
```html
<li class="task-item" data-task-id="1">
  <span class="task-text">任务内容</span>
  <button class="delete-btn">删除</button>
</li>
```

## JavaScript要求

- 使用`document.getElementById('todo-app')`作为事件委托的容器
- 在同一个事件监听器中处理：
  - 添加按钮点击
  - 输入框回车键
  - 任务文本点击（切换完成状态）
  - 删除按钮点击
- 使用`event.target`和`event.target.classList.contains()`来判断触发元素
- 为每个任务生成唯一的ID（可以使用时间戳或计数器）

## 额外挑战（可选）

- 实现任务计数显示（总任务数和已完成任务数）
- 添加本地存储支持，刷新页面后任务不丢失

## 提交要求

将你的完整代码保存在单独的HTML文件中，确保可以在现代浏览器中正常运行。

## 评估标准

- ✅ 正确使用事件委托
- ✅ 所有功能正常工作
- ✅ 代码结构清晰，有适当的注释
- ✅ 处理边界情况（如空输入）