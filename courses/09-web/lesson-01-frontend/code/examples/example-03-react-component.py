#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3: React 组件模式演示
这个脚本生成一个HTML文件，展示React-like组件模式的概念，
使用原生JavaScript模拟React的组件化思想和状态管理。
"""

def generate_react_pattern_html():
    """生成包含React组件模式演示的HTML内容"""
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>React 组件模式演示</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
            color: #333;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }

        .demo-section {
            margin-bottom: 40px;
            padding: 25px;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            background-color: #f8f9fa;
        }

        .demo-title {
            margin-top: 0;
            color: #495057;
            border-bottom: 1px solid #dee2e6;
            padding-bottom: 15px;
            font-size: 20px;
        }

        .component-container {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        .component-card {
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            min-width: 250px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .component-header {
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }

        .component-header h3 {
            margin: 0;
            color: #495057;
        }

        .counter-value {
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
            text-align: center;
            margin: 15px 0;
        }

        .button-group {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 15px;
        }

        button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #0056b3;
        }

        button.secondary {
            background-color: #6c757d;
        }

        button.success {
            background-color: #28a745;
        }

        button.danger {
            background-color: #dc3545;
        }

        .user-profile {
            text-align: center;
        }

        .avatar-placeholder {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(45deg, #3498db, #9b59b6);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            margin: 0 auto 15px;
            font-size: 20px;
        }

        .todo-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .todo-item {
            display: flex;
            align-items: center;
            padding: 10px;
            margin: 5px 0;
            background-color: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #dee2e6;
        }

        .todo-item.completed {
            background-color: #d4edda;
            color: #155724;
            text-decoration: line-through;
        }

        .todo-checkbox {
            margin-right: 10px;
        }

        .todo-text {
            flex: 1;
        }

        .todo-actions button {
            padding: 5px 10px;
            font-size: 12px;
            margin-left: 5px;
        }

        input[type="text"] {
            padding: 8px 12px;
            border: 1px solid #ced4da;
            border-radius: 5px;
            width: 200px;
            margin-right: 10px;
        }

        .state-info {
            background-color: #e9ecef;
            padding: 10px;
            border-radius: 5px;
            margin-top: 15px;
            font-family: monospace;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚛️ React 组件模式演示</h1>

        <!-- 概念说明 -->
        <div class="demo-section">
            <h2 class="demo-title">React 组件化思想</h2>
            <p>React 的核心思想是将UI拆分成独立、可复用的<strong>组件</strong>。每个组件都有自己的：</p>
            <ul>
                <li><strong>状态 (State)</strong>: 组件内部的数据，变化时会触发重新渲染</li>
                <li><strong>属性 (Props)</strong>: 从父组件传递给子组件的数据</li>
                <li><strong>生命周期</strong>: 组件从创建到销毁的过程</li>
            </ul>
            <p>下面的示例使用原生JavaScript模拟这些概念：</p>
        </div>

        <!-- 示例 1: 计数器组件 -->
        <div class="demo-section">
            <h2 class="demo-title">示例 1: 计数器组件</h2>
            <div class="component-container">
                <div class="component-card" id="counter-component-1">
                    <div class="component-header">
                        <h3>计数器 A</h3>
                    </div>
                    <div class="counter-value" id="counter-value-1">0</div>
                    <div class="button-group">
                        <button onclick="counterComponents[0].increment()">+</button>
                        <button onclick="counterComponents[0].decrement()" class="secondary">-</button>
                        <button onclick="counterComponents[0].reset()" class="danger">重置</button>
                    </div>
                    <div class="state-info" id="counter-state-1"></div>
                </div>
                <div class="component-card" id="counter-component-2">
                    <div class="component-header">
                        <h3>计数器 B</h3>
                    </div>
                    <div class="counter-value" id="counter-value-2">0</div>
                    <div class="button-group">
                        <button onclick="counterComponents[1].increment()">+</button>
                        <button onclick="counterComponents[1].decrement()" class="secondary">-</button>
                        <button onclick="counterComponents[1].reset()" class="danger">重置</button>
                    </div>
                    <div class="state-info" id="counter-state-2"></div>
                </div>
            </div>
        </div>

        <!-- 示例 2: 用户资料组件 -->
        <div class="demo-section">
            <h2 class="demo-title">示例 2: 用户资料组件</h2>
            <div class="component-container">
                <div class="component-card" id="profile-component">
                    <div class="component-header">
                        <h3>用户资料</h3>
                    </div>
                    <div class="user-profile">
                        <div class="avatar-placeholder" id="avatar-placeholder">👤</div>
                        <h4 id="user-name">张小明</h4>
                        <p id="user-status">在线</p>
                        <div class="button-group">
                            <button onclick="toggleUserStatus()">切换状态</button>
                            <button onclick="changeUserName()" class="secondary">修改姓名</button>
                        </div>
                    </div>
                    <div class="state-info" id="profile-state"></div>
                </div>
            </div>
        </div>

        <!-- 示例 3: 待办事项组件 -->
        <div class="demo-section">
            <h2 class="demo-title">示例 3: 待办事项组件</h2>
            <div class="component-container">
                <div class="component-card" id="todo-component">
                    <div class="component-header">
                        <h3>我的待办事项</h3>
                    </div>
                    <div>
                        <input type="text" id="todo-input" placeholder="添加新任务...">
                        <button onclick="addTodoItem()">添加</button>
                    </div>
                    <ul class="todo-list" id="todo-list">
                        <!-- 动态待办事项将在这里显示 -->
                    </ul>
                    <div class="button-group">
                        <button onclick="clearCompletedTodos()" class="danger">清除已完成</button>
                    </div>
                    <div class="state-info" id="todo-state"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // ========== 模拟React组件系统 ==========

        // 基础组件类
        class Component {
            constructor(initialState) {
                this.state = initialState;
                this.render(); // 初始渲染
            }

            setState(newState) {
                // 合并新状态
                this.state = { ...this.state, ...newState };
                // 重新渲染
                this.render();
            }

            render() {
                // 子类需要实现具体的render方法
                console.log('Component render called');
            }
        }

        // ========== 计数器组件 ==========
        class CounterComponent extends Component {
            constructor(containerId, valueId, stateId, initialValue = 0) {
                super({ count: initialValue });
                this.containerId = containerId;
                this.valueId = valueId;
                this.stateId = stateId;
                this.render();
            }

            increment() {
                this.setState({ count: this.state.count + 1 });
            }

            decrement() {
                this.setState({ count: this.state.count - 1 });
            }

            reset() {
                this.setState({ count: 0 });
            }

            render() {
                // 更新UI
                document.getElementById(this.valueId).textContent = this.state.count;

                // 安全地更新状态信息（避免innerHTML）
                const stateElement = document.getElementById(this.stateId);
                stateElement.textContent = '';
                const stateText = document.createTextNode(`状态: { count: ${this.state.count} }`);
                stateElement.appendChild(stateText);
            }
        }

        // ========== 用户资料组件 ==========
        class ProfileComponent extends Component {
            constructor(containerId, stateId) {
                super({
                    name: "张小明",
                    status: "online",
                    avatar: "👤"
                });
                this.containerId = containerId;
                this.stateId = stateId;
                this.render();
            }

            toggleStatus() {
                const newStatus = this.state.status === "online" ? "offline" : "online";
                this.setState({ status: newStatus });
            }

            changeName(newName) {
                if (newName) {
                    this.setState({ name: newName });
                }
            }

            render() {
                document.getElementById('user-name').textContent = this.state.name;
                document.getElementById('user-status').textContent =
                    this.state.status === "online" ? "在线" : "离线";

                // 安全地更新状态信息
                const stateElement = document.getElementById('profile-state');
                stateElement.textContent = '';
                const stateText = document.createTextNode(
                    `状态: { name: "${this.state.name}", status: "${this.state.status}" }`
                );
                stateElement.appendChild(stateText);
            }
        }

        // ========== 待办事项组件 ==========
        class TodoComponent extends Component {
            constructor(containerId, stateId) {
                super({
                    todos: [
                        { id: 1, text: "学习前端基础知识", completed: false },
                        { id: 2, text: "练习DOM操作", completed: true }
                    ],
                    nextId: 3
                });
                this.containerId = containerId;
                this.stateId = stateId;
                this.render();
            }

            addTodo(text) {
                if (text.trim()) {
                    const newTodo = {
                        id: this.state.nextId,
                        text: text.trim(),
                        completed: false
                    };
                    this.setState({
                        todos: [...this.state.todos, newTodo],
                        nextId: this.state.nextId + 1
                    });
                }
            }

            toggleTodo(id) {
                const updatedTodos = this.state.todos.map(todo =>
                    todo.id === id ? { ...todo, completed: !todo.completed } : todo
                );
                this.setState({ todos: updatedTodos });
            }

            deleteTodo(id) {
                const updatedTodos = this.state.todos.filter(todo => todo.id !== id);
                this.setState({ todos: updatedTodos });
            }

            clearCompleted() {
                const activeTodos = this.state.todos.filter(todo => !todo.completed);
                this.setState({ todos: activeTodos });
            }

            render() {
                const todoList = document.getElementById('todo-list');
                todoList.innerHTML = '';

                this.state.todos.forEach(todo => {
                    const todoItem = document.createElement('li');
                    todoItem.className = `todo-item ${todo.completed ? 'completed' : ''}`;

                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.className = 'todo-checkbox';
                    checkbox.checked = todo.completed;
                    checkbox.onchange = () => this.toggleTodo(todo.id);

                    const todoText = document.createElement('span');
                    todoText.className = 'todo-text';
                    todoText.textContent = todo.text;

                    const actions = document.createElement('div');
                    actions.className = 'todo-actions';

                    const deleteBtn = document.createElement('button');
                    deleteBtn.className = 'danger';
                    deleteBtn.textContent = '删除';
                    deleteBtn.onclick = () => this.deleteTodo(todo.id);

                    actions.appendChild(deleteBtn);
                    todoItem.appendChild(checkbox);
                    todoItem.appendChild(todoText);
                    todoItem.appendChild(actions);
                    todoList.appendChild(todoItem);
                });

                // 安全地更新状态信息
                const stateElement = document.getElementById('todo-state');
                stateElement.textContent = '';
                const stateText = document.createTextNode(
                    `状态: { todos: [${this.state.todos.length} items] }`
                );
                stateElement.appendChild(stateText);
            }
        }

        // ========== 初始化组件实例 ==========
        const counterComponents = [
            new CounterComponent('counter-component-1', 'counter-value-1', 'counter-state-1', 0),
            new CounterComponent('counter-component-2', 'counter-value-2', 'counter-state-2', 5)
        ];

        const profileComponent = new ProfileComponent('profile-component', 'profile-state');

        const todoComponent = new TodoComponent('todo-component', 'todo-state');

        // ========== 全局函数（用于HTML中的onclick） ==========
        function toggleUserStatus() {
            profileComponent.toggleStatus();
        }

        function changeUserName() {
            const newName = prompt("请输入新的姓名:", profileComponent.state.name);
            if (newName !== null) {
                profileComponent.changeName(newName);
            }
        }

        function addTodoItem() {
            const input = document.getElementById('todo-input');
            const text = input.value;
            if (text.trim()) {
                todoComponent.addTodo(text);
                input.value = '';
            }
        }

        function clearCompletedTodos() {
            todoComponent.clearCompleted();
        }

        // 监听回车键添加待办事项
        document.getElementById('todo-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addTodoItem();
            }
        });

        console.log("✅ React组件模式演示已初始化完成！");
        console.log("组件实例:", { counterComponents, profileComponent, todoComponent });
    </script>
</body>
</html>"""
    return html_content

def save_html_file(content, filename="react-pattern-demo.html"):
    """将HTML内容保存到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已生成React模式演示文件: {filename}")
    print(f"💡 请在浏览器中打开 {filename} 查看组件化效果")

def main():
    """主函数"""
    print("🚀 开始生成React组件模式演示...")

    # 生成HTML内容
    html_content = generate_react_pattern_html()

    # 保存HTML文件
    save_html_file(html_content, "code/examples/react-pattern-demo.html")

    print("\n🎯 React组件模式演示已生成完成！")
    print("主要演示了以下概念：")
    print("1. 组件类继承和状态管理")
    print("2. 独立的计数器组件（多个实例）")
    print("3. 用户资料组件（状态切换）")
    print("4. 待办事项组件（列表管理和CRUD操作）")
    print("5. 组件间的状态隔离")

if __name__ == "__main__":
    main()