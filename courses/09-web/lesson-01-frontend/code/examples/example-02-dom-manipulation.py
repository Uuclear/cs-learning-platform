#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2: DOM 操作演示
这个脚本生成一个HTML文件，其中包含JavaScript代码来演示DOM操作的基本概念。
用户可以运行此脚本生成HTML文件，然后在浏览器中打开查看交互效果。
"""

import os

def generate_dom_demo_html():
    """生成包含DOM操作演示的HTML内容"""
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DOM 操作演示</title>
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
            max-width: 800px;
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
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            background-color: #f8f9fa;
        }

        .demo-title {
            margin-top: 0;
            color: #495057;
            border-bottom: 1px solid #dee2e6;
            padding-bottom: 10px;
        }

        button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #0056b3;
        }

        button.success {
            background-color: #28a745;
        }

        button.danger {
            background-color: #dc3545;
        }

        .dynamic-content {
            margin-top: 15px;
            padding: 15px;
            background-color: #e9ecef;
            border-radius: 5px;
            min-height: 20px;
        }

        .task-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin: 5px 0;
            background-color: #fff;
            border: 1px solid #dee2e6;
            border-radius: 5px;
        }

        .task-text {
            flex: 1;
        }

        .task-actions button {
            padding: 5px 10px;
            font-size: 12px;
            margin: 0 2px;
        }

        input[type="text"] {
            padding: 10px;
            border: 1px solid #ced4da;
            border-radius: 5px;
            width: 200px;
            margin-right: 10px;
        }

        .counter-display {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 DOM 操作演示</h1>

        <!-- 示例 1: 基础元素操作 -->
        <div class="demo-section">
            <h3 class="demo-title">示例 1: 基础DOM操作</h3>
            <button id="change-text-btn">修改文本</button>
            <button id="change-style-btn">修改样式</button>
            <button id="toggle-visibility-btn">切换显示/隐藏</button>
            <div id="demo-text" class="dynamic-content">
                这是原始文本内容
            </div>
        </div>

        <!-- 示例 2: 动态创建和删除元素 -->
        <div class="demo-section">
            <h3 class="demo-title">示例 2: 动态元素管理</h3>
            <input type="text" id="new-item-input" placeholder="输入新项目">
            <button id="add-item-btn">添加项目</button>
            <button id="clear-all-btn" class="danger">清空所有</button>
            <div id="items-container" class="dynamic-content">
                <!-- 动态项目将在这里显示 -->
            </div>
        </div>

        <!-- 示例 3: 事件委托 -->
        <div class="demo-section">
            <h3 class="demo-title">示例 3: 事件委托</h3>
            <p>点击下面的按钮来增加或减少计数器：</p>
            <div class="counter-display" id="counter-display">计数: 0</div>
            <div id="counter-buttons">
                <button data-action="increment">+</button>
                <button data-action="decrement">-</button>
                <button data-action="reset" class="danger">重置</button>
            </div>
        </div>

        <!-- 示例 4: 表单处理 -->
        <div class="demo-section">
            <h3 class="demo-title">示例 4: 表单事件处理</h3>
            <form id="demo-form">
                <input type="text" id="name-input" placeholder="输入姓名" required>
                <input type="email" id="email-input" placeholder="输入邮箱" required>
                <button type="submit">提交表单</button>
            </form>
            <div id="form-result" class="dynamic-content"></div>
        </div>
    </div>

    <script>
        // ========== 示例 1: 基础DOM操作 ==========
        document.addEventListener('DOMContentLoaded', function() {
            // 获取按钮和目标元素
            const changeTextBtn = document.getElementById('change-text-btn');
            const changeStyleBtn = document.getElementById('change-style-btn');
            const toggleVisibilityBtn = document.getElementById('toggle-visibility-btn');
            const demoText = document.getElementById('demo-text');

            // 修改文本内容
            changeTextBtn.addEventListener('click', function() {
                demoText.textContent = '🎉 文本已被JavaScript修改！';
            });

            // 修改样式
            changeStyleBtn.addEventListener('click', function() {
                demoText.style.backgroundColor = '#d4edda';
                demoText.style.color = '#155724';
                demoText.style.border = '2px solid #28a745';
                demoText.style.padding = '10px';
                demoText.style.borderRadius = '5px';
            });

            // 切换显示/隐藏
            toggleVisibilityBtn.addEventListener('click', function() {
                if (demoText.style.display === 'none') {
                    demoText.style.display = 'block';
                    toggleVisibilityBtn.textContent = '切换显示/隐藏';
                } else {
                    demoText.style.display = 'none';
                    toggleVisibilityBtn.textContent = '显示内容';
                }
            });

            // ========== 示例 2: 动态创建和删除元素 ==========
            const addItemBtn = document.getElementById('add-item-btn');
            const clearAllBtn = document.getElementById('clear-all-btn');
            const newItemInput = document.getElementById('new-item-input');
            const itemsContainer = document.getElementById('items-container');

            // 添加新项目
            addItemBtn.addEventListener('click', function() {
                const itemText = newItemInput.value.trim();
                if (itemText) {
                    // 创建新的任务项元素
                    const taskItem = document.createElement('div');
                    taskItem.className = 'task-item';

                    const taskText = document.createElement('span');
                    taskText.className = 'task-text';
                    taskText.textContent = itemText;

                    const taskActions = document.createElement('div');
                    taskActions.className = 'task-actions';

                    const deleteBtn = document.createElement('button');
                    deleteBtn.className = 'danger';
                    deleteBtn.textContent = '删除';
                    deleteBtn.onclick = function() {
                        taskItem.remove();
                    };

                    taskActions.appendChild(deleteBtn);
                    taskItem.appendChild(taskText);
                    taskItem.appendChild(taskActions);

                    // 添加到容器中
                    itemsContainer.appendChild(taskItem);

                    // 清空输入框
                    newItemInput.value = '';
                    newItemInput.focus();
                } else {
                    alert('请输入项目内容！');
                }
            });

            // 清空所有项目
            clearAllBtn.addEventListener('click', function() {
                if (confirm('确定要清空所有项目吗？')) {
                    itemsContainer.innerHTML = '';
                }
            });

            // ========== 示例 3: 事件委托 ==========
            const counterDisplay = document.getElementById('counter-display');
            const counterButtons = document.getElementById('counter-buttons');
            let counter = 0;

            counterButtons.addEventListener('click', function(event) {
                const action = event.target.dataset.action;

                if (action === 'increment') {
                    counter++;
                } else if (action === 'decrement') {
                    counter--;
                } else if (action === 'reset') {
                    counter = 0;
                }

                counterDisplay.textContent = `计数: ${counter}`;
            });

            // ========== 示例 4: 表单处理 ==========
            const demoForm = document.getElementById('demo-form');
            const formResult = document.getElementById('form-result');

            demoForm.addEventListener('submit', function(event) {
                // 阻止表单默认提交行为
                event.preventDefault();

                // 获取表单数据
                const name = document.getElementById('name-input').value;
                const email = document.getElementById('email-input').value;

                // 安全地显示结果（使用createElement而不是innerHTML）
                formResult.innerHTML = ''; // 先清空

                const resultTitle = document.createElement('h4');
                resultTitle.textContent = '✅ 表单提交成功！';
                formResult.appendChild(resultTitle);

                const namePara = document.createElement('p');
                namePara.innerHTML = '<strong>姓名:</strong> ' + name;
                formResult.appendChild(namePara);

                const emailPara = document.createElement('p');
                emailPara.innerHTML = '<strong>邮箱:</strong> ' + email;
                formResult.appendChild(emailPara);

                const notePara = document.createElement('p');
                notePara.innerHTML = '<em>数据已通过JavaScript处理，没有实际发送到服务器</em>';
                formResult.appendChild(notePara);
            });
        });
    </script>
</body>
</html>"""
    return html_content

def save_html_file(content, filename="dom-demo.html"):
    """将HTML内容保存到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已生成DOM演示文件: {filename}")
    print(f"💡 请在浏览器中打开 {filename} 查看交互效果")

def main():
    """主函数"""
    print("🚀 开始生成DOM操作演示...")

    # 生成HTML内容
    html_content = generate_dom_demo_html()

    # 保存HTML文件
    save_html_file(html_content, "code/examples/dom-demo.html")

    print("\n🎯 DOM操作演示已生成完成！")
    print("主要演示了以下概念：")
    print("1. 基础DOM元素获取和修改")
    print("2. 动态创建和删除元素")
    print("3. 事件委托（Event Delegation）")
    print("4. 表单事件处理")

if __name__ == "__main__":
    main()