#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2: 待办事项列表应用
这个脚本生成一个完整的待办事项列表应用，使用DOM操作实现所有功能。
用户可以运行此脚本生成HTML文件，然后在浏览器中打开使用。
"""

def generate_todo_app():
    """生成待办事项应用的完整HTML内容"""
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>待办事项列表 - Todo List</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }

        .app-content {
            padding: 30px;
        }

        /* 输入区域 */
        .input-section {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }

        #todo-input {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            font-family: inherit;
            transition: border-color 0.3s ease;
        }

        #todo-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        }

        #add-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0 25px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s ease;
        }

        #add-btn:hover {
            transform: translateY(-2px);
        }

        #add-btn:active {
            transform: translateY(0);
        }

        /* 统计信息 */
        .stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 8px;
            font-size: 14px;
            color: #666;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
            display: block;
        }

        /* 过滤按钮 */
        .filters {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 20px;
        }

        .filter-btn {
            padding: 8px 16px;
            border: 2px solid #e0e0e0;
            background: white;
            color: #666;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
        }

        .filter-btn.active,
        .filter-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }

        /* 待办事项列表 */
        .todo-list {
            list-style: none;
        }

        .todo-item {
            display: flex;
            align-items: center;
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s ease;
            border-left: 4px solid #667eea;
        }

        .todo-item.completed {
            background: #e8f5e8;
            border-left-color: #28a745;
            opacity: 0.8;
        }

        .todo-item:hover {
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .todo-checkbox {
            margin-right: 15px;
            width: 20px;
            height: 20px;
            cursor: pointer;
        }

        .todo-text {
            flex: 1;
            font-size: 16px;
            color: #333;
        }

        .todo-item.completed .todo-text {
            text-decoration: line-through;
            color: #666;
        }

        .todo-actions {
            display: flex;
            gap: 8px;
        }

        .todo-btn {
            padding: 6px 12px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            transition: background-color 0.2s ease;
        }

        .edit-btn {
            background: #ffc107;
            color: #212529;
        }

        .edit-btn:hover {
            background: #e0a800;
        }

        .delete-btn {
            background: #dc3545;
            color: white;
        }

        .delete-btn:hover {
            background: #c82333;
        }

        /* 空状态 */
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #666;
        }

        .empty-state h3 {
            margin-bottom: 10px;
            color: #667eea;
        }

        .empty-state p {
            font-size: 14px;
        }

        /* 编辑输入框 */
        .edit-input {
            flex: 1;
            padding: 8px 12px;
            border: 2px solid #667eea;
            border-radius: 4px;
            font-size: 16px;
            font-family: inherit;
        }

        /* 响应式设计 */
        @media (max-width: 600px) {
            .input-section {
                flex-direction: column;
            }

            #add-btn {
                padding: 15px;
            }

            .stats {
                flex-direction: column;
                gap: 10px;
            }

            .header h1 {
                font-size: 2rem;
            }
        }

        /* 动画效果 */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .todo-item {
            animation: fadeIn 0.3s ease-out;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 待办事项</h1>
            <p>管理您的任务，提高工作效率</p>
        </div>

        <div class="app-content">
            <!-- 输入区域 -->
            <div class="input-section">
                <input type="text" id="todo-input" placeholder="添加新的待办事项...">
                <button id="add-btn">添加</button>
            </div>

            <!-- 统计信息 -->
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number" id="total-count">0</span>
                    <span>总计</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number" id="completed-count">0</span>
                    <span>已完成</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number" id="pending-count">0</span>
                    <span>待完成</span>
                </div>
            </div>

            <!-- 过滤按钮 -->
            <div class="filters">
                <button class="filter-btn active" data-filter="all">全部</button>
                <button class="filter-btn" data-filter="active">待完成</button>
                <button class="filter-btn" data-filter="completed">已完成</button>
            </div>

            <!-- 待办事项列表 -->
            <ul class="todo-list" id="todo-list">
                <!-- 动态待办事项将在这里显示 -->
                <div class="empty-state" id="empty-state">
                    <h3>🎉 没有待办事项！</h3>
                    <p>添加您的第一个任务开始吧</p>
                </div>
            </ul>
        </div>
    </div>

    <script>
        // ========== 待办事项应用类 ==========
        class TodoApp {
            constructor() {
                this.todos = JSON.parse(localStorage.getItem('todos')) || [];
                this.currentFilter = 'all';
                this.nextId = this.todos.length > 0 ? Math.max(...this.todos.map(t => t.id)) + 1 : 1;

                this.initializeElements();
                this.bindEvents();
                this.render();
                this.updateStats();
            }

            initializeElements() {
                this.todoInput = document.getElementById('todo-input');
                this.addBtn = document.getElementById('add-btn');
                this.todoList = document.getElementById('todo-list');
                this.emptyState = document.getElementById('empty-state');
                this.filterButtons = document.querySelectorAll('.filter-btn');
                this.totalCount = document.getElementById('total-count');
                this.completedCount = document.getElementById('completed-count');
                this.pendingCount = document.getElementById('pending-count');
            }

            bindEvents() {
                // 添加新任务
                this.addBtn.addEventListener('click', () => this.addTodo());
                this.todoInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') this.addTodo();
                });

                // 过滤按钮
                this.filterButtons.forEach(btn => {
                    btn.addEventListener('click', () => {
                        this.setFilter(btn.dataset.filter);
                    });
                });

                // 删除本地存储数据的监听（用于多标签页同步）
                window.addEventListener('storage', () => {
                    this.todos = JSON.parse(localStorage.getItem('todos')) || [];
                    this.render();
                    this.updateStats();
                });
            }

            addTodo() {
                const text = this.todoInput.value.trim();
                if (!text) {
                    this.showNotification('请输入待办事项内容！', 'error');
                    return;
                }

                const newTodo = {
                    id: this.nextId++,
                    text: text,
                    completed: false,
                    createdAt: new Date().toISOString()
                };

                this.todos.push(newTodo);
                this.saveToStorage();
                this.render();
                this.updateStats();

                // 清空输入框
                this.todoInput.value = '';
                this.todoInput.focus();

                this.showNotification('✅ 任务已添加！');
            }

            toggleTodo(id) {
                const todo = this.todos.find(t => t.id === id);
                if (todo) {
                    todo.completed = !todo.completed;
                    this.saveToStorage();
                    this.render();
                    this.updateStats();

                    const action = todo.completed ? '完成' : '取消完成';
                    this.showNotification(`✅ 任务已${action}！`);
                }
            }

            editTodo(id, newText) {
                const todo = this.todos.find(t => t.id === id);
                if (todo && newText.trim()) {
                    todo.text = newText.trim();
                    this.saveToStorage();
                    this.render();
                    this.showNotification('✅ 任务已更新！');
                }
            }

            deleteTodo(id) {
                if (confirm('确定要删除这个任务吗？')) {
                    this.todos = this.todos.filter(t => t.id !== id);
                    this.saveToStorage();
                    this.render();
                    this.updateStats();
                    this.showNotification('🗑️ 任务已删除！');
                }
            }

            clearCompleted() {
                const completedCount = this.todos.filter(t => t.completed).length;
                if (completedCount === 0) {
                    this.showNotification('没有已完成的任务可以清理！');
                    return;
                }

                if (confirm(`确定要清理 ${completedCount} 个已完成的任务吗？`)) {
                    this.todos = this.todos.filter(t => !t.completed);
                    this.saveToStorage();
                    this.render();
                    this.updateStats();
                    this.showNotification(`🗑️ 已清理 ${completedCount} 个已完成的任务！`);
                }
            }

            setFilter(filter) {
                this.currentFilter = filter;

                // 更新过滤按钮样式
                this.filterButtons.forEach(btn => {
                    if (btn.dataset.filter === filter) {
                        btn.classList.add('active');
                    } else {
                        btn.classList.remove('active');
                    }
                });

                this.render();
            }

            getFilteredTodos() {
                switch (this.currentFilter) {
                    case 'active':
                        return this.todos.filter(todo => !todo.completed);
                    case 'completed':
                        return this.todos.filter(todo => todo.completed);
                    default:
                        return this.todos;
                }
            }

            saveToStorage() {
                localStorage.setItem('todos', JSON.stringify(this.todos));
            }

            updateStats() {
                const total = this.todos.length;
                const completed = this.todos.filter(t => t.completed).length;
                const pending = total - completed;

                this.totalCount.textContent = total;
                this.completedCount.textContent = completed;
                this.pendingCount.textContent = pending;
            }

            render() {
                const filteredTodos = this.getFilteredTodos();
                const hasTodos = filteredTodos.length > 0;

                // 显示/隐藏空状态
                this.emptyState.style.display = hasTodos ? 'none' : 'block';

                // 清空列表（安全方式）
                while (this.todoList.firstChild) {
                    this.todoList.removeChild(this.todoList.firstChild);
                }

                if (hasTodos) {
                    filteredTodos.forEach(todo => {
                        const todoItem = this.createTodoElement(todo);
                        this.todoList.appendChild(todoItem);
                    });
                } else {
                    // 添加空状态元素
                    this.todoList.appendChild(this.emptyState);
                }
            }

            createTodoElement(todo) {
                const todoItem = document.createElement('li');
                todoItem.className = `todo-item ${todo.completed ? 'completed' : ''}`;
                todoItem.dataset.id = todo.id;

                // 复选框
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.className = 'todo-checkbox';
                checkbox.checked = todo.completed;
                checkbox.addEventListener('change', () => this.toggleTodo(todo.id));

                // 文本内容
                const todoText = document.createElement('span');
                todoText.className = 'todo-text';
                todoText.textContent = todo.text;

                // 操作按钮
                const actions = document.createElement('div');
                actions.className = 'todo-actions';

                const editBtn = document.createElement('button');
                editBtn.className = 'todo-btn edit-btn';
                editBtn.textContent = '编辑';
                editBtn.addEventListener('click', () => this.startEdit(todo.id, todo.text));

                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'todo-btn delete-btn';
                deleteBtn.textContent = '删除';
                deleteBtn.addEventListener('click', () => this.deleteTodo(todo.id));

                actions.appendChild(editBtn);
                actions.appendChild(deleteBtn);

                todoItem.appendChild(checkbox);
                todoItem.appendChild(todoText);
                todoItem.appendChild(actions);

                return todoItem;
            }

            startEdit(id, currentText) {
                const todoItem = document.querySelector(`.todo-item[data-id="${id}"]`);
                const todoText = todoItem.querySelector('.todo-text');
                const actions = todoItem.querySelector('.todo-actions');

                // 创建编辑输入框
                const editInput = document.createElement('input');
                editInput.type = 'text';
                editInput.className = 'edit-input';
                editInput.value = currentText;

                // 替换文本为输入框
                todoText.replaceWith(editInput);
                editInput.focus();

                // 保存编辑的函数
                const saveEdit = () => {
                    this.editTodo(id, editInput.value);
                    // 重新渲染整个列表以恢复原始状态
                    this.render();
                };

                // 取消编辑的函数
                const cancelEdit = () => {
                    this.render();
                };

                // 绑定事件
                editInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        saveEdit();
                    } else if (e.key === 'Escape') {
                        cancelEdit();
                    }
                });

                // 修改操作按钮为保存/取消
                // 清空操作按钮
                while (actions.firstChild) {
                    actions.removeChild(actions.firstChild);
                }

                const saveBtn = document.createElement('button');
                saveBtn.className = 'todo-btn edit-btn';
                saveBtn.textContent = '保存';
                saveBtn.addEventListener('click', saveEdit);

                const cancelBtn = document.createElement('button');
                cancelBtn.className = 'todo-btn delete-btn';
                cancelBtn.textContent = '取消';
                cancelBtn.addEventListener('click', cancelEdit);

                actions.appendChild(saveBtn);
                actions.appendChild(cancelBtn);
            }

            showNotification(message, type = 'success') {
                // 创建通知元素（安全方式）
                const notification = document.createElement('div');
                notification.textContent = message;
                notification.style.position = 'fixed';
                notification.style.top = '20px';
                notification.style.right = '20px';
                notification.style.padding = '15px 20px';
                notification.style.borderRadius = '8px';
                notification.style.color = 'white';
                notification.style.fontWeight = 'bold';
                notification.style.zIndex = '10000';
                notification.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';

                if (type === 'error') {
                    notification.style.backgroundColor = '#dc3545';
                } else {
                    notification.style.backgroundColor = '#28a745';
                }

                document.body.appendChild(notification);

                // 3秒后自动移除
                setTimeout(() => {
                    notification.style.opacity = '0';
                    notification.style.transition = 'opacity 0.5s ease';
                    setTimeout(() => {
                        document.body.removeChild(notification);
                    }, 500);
                }, 3000);
            }
        }

        // 初始化应用
        document.addEventListener('DOMContentLoaded', function() {
            const app = new TodoApp();

            // 添加清理已完成任务的功能（通过右键菜单或额外按钮）
            const clearCompletedBtn = document.createElement('button');
            clearCompletedBtn.textContent = '清理已完成';
            clearCompletedBtn.style.marginTop = '15px';
            clearCompletedBtn.style.padding = '8px 16px';
            clearCompletedBtn.style.backgroundColor = '#6c757d';
            clearCompletedBtn.style.color = 'white';
            clearCompletedBtn.style.border = 'none';
            clearCompletedBtn.style.borderRadius = '4px';
            clearCompletedBtn.style.cursor = 'pointer';

            clearCompletedBtn.addEventListener('click', () => app.clearCompleted());

            document.querySelector('.app-content').appendChild(clearCompletedBtn);

            console.log('✅ 待办事项应用已初始化完成！');
            console.log('💡 提示：数据已保存到本地存储，刷新页面不会丢失');
        });
    </script>
</body>
</html>"""
    return html_content

def save_html_file(content, filename="todo-app.html"):
    """将HTML内容保存到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已生成待办事项应用文件: {filename}")
    print(f"💡 请在浏览器中打开 {filename} 使用应用")

def main():
    """主函数"""
    print("🚀 开始构建待办事项列表应用...")

    # 生成HTML内容
    html_content = generate_todo_app()

    # 保存HTML文件
    save_html_file(html_content, "code/solutions/todo-app.html")

    print("\n🎯 待办事项应用已构建完成！")
    print("主要功能包括：")
    print("1. 添加、编辑、删除待办事项")
    print("2. 标记完成/未完成状态")
    print("3. 数据持久化（本地存储）")
    print("4. 任务统计和过滤功能")
    print("5. 响应式设计和交互反馈")

if __name__ == "__main__":
    main()