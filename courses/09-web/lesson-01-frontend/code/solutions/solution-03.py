#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3: 计数器组件模式（React-like状态管理）
这个脚本演示如何使用Python模拟React的状态管理概念，
创建一个简单的计数器组件系统，展示组件化和状态管理的核心思想。
"""

def generate_counter_component_demo():
    """生成计数器组件演示的HTML内容"""
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>计数器组件 - React状态管理模拟</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }

        .header h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 15px;
        }

        .header p {
            color: #666;
            font-size: 1.1rem;
            line-height: 1.6;
        }

        .concept-explanation {
            background: #e3f2fd;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 4px solid #2196f3;
        }

        .concept-explanation h3 {
            color: #0d47a1;
            margin-bottom: 10px;
        }

        /* 组件容器 */
        .components-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }

        .component-card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .component-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }

        .component-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }

        .component-header h3 {
            font-size: 1.5rem;
            margin: 0;
        }

        .component-body {
            padding: 30px;
            text-align: center;
        }

        .counter-display {
            font-size: 3rem;
            font-weight: bold;
            color: #667eea;
            margin: 20px 0;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .counter-buttons {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        .counter-btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            min-width: 80px;
        }

        .increment-btn {
            background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
            color: white;
        }

        .decrement-btn {
            background: linear-gradient(135deg, #f44336 0%, #da190b 100%);
            color: white;
        }

        .reset-btn {
            background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
            color: white;
        }

        .step-btn {
            background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
            color: white;
        }

        .counter-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        .counter-btn:active {
            transform: translateY(0);
        }

        .state-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-family: monospace;
            font-size: 14px;
            color: #495057;
            border: 1px solid #e9ecef;
        }

        /* 共享状态示例 */
        .shared-state-demo {
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            padding: 30px;
            margin-bottom: 40px;
        }

        .shared-state-demo h2 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }

        .shared-counters {
            display: flex;
            justify-content: center;
            gap: 50px;
            flex-wrap: wrap;
            margin-bottom: 30px;
        }

        .shared-counter {
            text-align: center;
        }

        .shared-counter-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #e91e63;
            margin: 15px 0;
        }

        /* 步长控制 */
        .step-control {
            text-align: center;
            margin: 20px 0;
        }

        .step-input {
            padding: 10px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            width: 100px;
            text-align: center;
            margin: 0 10px;
        }

        /* 响应式设计 */
        @media (max-width: 768px) {
            .components-grid {
                grid-template-columns: 1fr;
            }

            .shared-counters {
                gap: 20px;
            }

            .header h1 {
                font-size: 2rem;
            }

            .counter-display {
                font-size: 2.5rem;
            }
        }

        @media (max-width: 480px) {
            .counter-buttons {
                flex-direction: column;
                gap: 10px;
            }

            .counter-btn {
                width: 100%;
            }
        }

        /* 动画效果 */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .counter-display.updated {
            animation: pulse 0.3s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚛️ React状态管理模拟</h1>
            <p>使用原生JavaScript模拟React的组件化思想和状态管理机制</p>

            <div class="concept-explanation">
                <h3>核心概念说明</h3>
                <p><strong>状态 (State)</strong>: 组件内部的数据，当状态改变时，组件会自动重新渲染</p>
                <p><strong>单向数据流</strong>: 状态只能通过特定的方法修改，确保数据变化的可预测性</p>
                <p><strong>组件隔离</strong>: 每个组件都有独立的状态，互不影响</p>
                <p><strong>状态提升</strong>: 多个组件需要共享状态时，将状态提升到共同的父组件</p>
            </div>
        </div>

        <!-- 独立计数器组件 -->
        <h2 style="text-align: center; color: #2c3e50; margin-bottom: 30px;">独立计数器组件</h2>
        <div class="components-grid">
            <div class="component-card">
                <div class="component-header">
                    <h3>计数器 A</h3>
                </div>
                <div class="component-body">
                    <div class="counter-display" id="counter-a-display">0</div>
                    <div class="counter-buttons">
                        <button class="counter-btn increment-btn" onclick="counterA.increment()">+</button>
                        <button class="counter-btn decrement-btn" onclick="counterA.decrement()">-</button>
                        <button class="counter-btn reset-btn" onclick="counterA.reset()">重置</button>
                    </div>
                    <div class="state-info" id="counter-a-state">状态: { count: 0 }</div>
                </div>
            </div>

            <div class="component-card">
                <div class="component-header">
                    <h3>计数器 B</h3>
                </div>
                <div class="component-body">
                    <div class="counter-display" id="counter-b-display">0</div>
                    <div class="counter-buttons">
                        <button class="counter-btn increment-btn" onclick="counterB.increment()">+</button>
                        <button class="counter-btn decrement-btn" onclick="counterB.decrement()">-</button>
                        <button class="counter-btn reset-btn" onclick="counterB.reset()">重置</button>
                    </div>
                    <div class="state-info" id="counter-b-state">状态: { count: 0 }</div>
                </div>
            </div>

            <div class="component-card">
                <div class="component-header">
                    <h3>计数器 C (带步长)</h3>
                </div>
                <div class="component-body">
                    <div class="counter-display" id="counter-c-display">0</div>
                    <div class="counter-buttons">
                        <button class="counter-btn increment-btn" onclick="counterC.increment()">+1</button>
                        <button class="counter-btn decrement-btn" onclick="counterC.decrement()">-1</button>
                        <button class="counter-btn step-btn" onclick="counterC.incrementByStep()">+步长</button>
                        <button class="counter-btn reset-btn" onclick="counterC.reset()">重置</button>
                    </div>
                    <div class="step-control">
                        <label for="step-input">步长:</label>
                        <input type="number" id="step-input" class="step-input" value="5" min="1" onchange="counterC.setStep(this.value)">
                    </div>
                    <div class="state-info" id="counter-c-state">状态: { count: 0, step: 5 }</div>
                </div>
            </div>
        </div>

        <!-- 共享状态示例 -->
        <div class="shared-state-demo">
            <h2>共享状态示例</h2>
            <p style="text-align: center; margin-bottom: 20px; color: #666;">
                这两个计数器共享同一个状态，体现了<strong>状态提升</strong>的概念
            </p>

            <div class="shared-counters">
                <div class="shared-counter">
                    <h3>显示组件</h3>
                    <div class="shared-counter-value" id="shared-counter-display">0</div>
                    <div class="state-info" id="shared-counter-state">状态: { count: 0 }</div>
                </div>

                <div class="shared-counter">
                    <h3>控制组件</h3>
                    <div class="counter-buttons">
                        <button class="counter-btn increment-btn" onclick="sharedCounter.increment()">增加</button>
                        <button class="counter-btn decrement-btn" onclick="sharedCounter.decrement()">减少</button>
                        <button class="counter-btn reset-btn" onclick="sharedCounter.reset()">重置</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // ========== 基础组件类 ==========
        class Component {
            constructor(initialState) {
                this.state = { ...initialState };
                this.render(); // 初始渲染
            }

            setState(newState) {
                // 合并新状态（浅拷贝）
                this.state = { ...this.state, ...newState };
                // 触发重新渲染
                this.render();
            }

            render() {
                // 子类必须实现具体的render方法
                console.log('Base Component render called');
            }
        }

        // ========== 基础计数器组件 ==========
        class CounterComponent extends Component {
            constructor(displayId, stateId, initialValue = 0) {
                super({ count: initialValue });
                this.displayId = displayId;
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
                // 更新显示值
                const displayElement = document.getElementById(this.displayId);
                displayElement.textContent = this.state.count;

                // 添加更新动画
                displayElement.classList.add('updated');
                setTimeout(() => {
                    displayElement.classList.remove('updated');
                }, 300);

                // 安全地更新状态信息
                const stateElement = document.getElementById(this.stateId);
                stateElement.textContent = '';
                const stateText = document.createTextNode(
                    `状态: { count: ${this.state.count} }`
                );
                stateElement.appendChild(stateText);
            }
        }

        // ========== 带步长的计数器组件 ==========
        class StepCounterComponent extends Component {
            constructor(displayId, stateId, initialValue = 0, initialStep = 1) {
                super({
                    count: initialValue,
                    step: initialStep
                });
                this.displayId = displayId;
                this.stateId = stateId;
                this.render();
            }

            increment() {
                this.setState({ count: this.state.count + 1 });
            }

            decrement() {
                this.setState({ count: this.state.count - 1 });
            }

            incrementByStep() {
                this.setState({ count: this.state.count + this.state.step });
            }

            setStep(newStep) {
                const stepValue = parseInt(newStep) || 1;
                this.setState({ step: Math.max(1, stepValue) });
            }

            reset() {
                this.setState({ count: 0 });
            }

            render() {
                // 更新显示值
                const displayElement = document.getElementById(this.displayId);
                displayElement.textContent = this.state.count;

                // 添加更新动画
                displayElement.classList.add('updated');
                setTimeout(() => {
                    displayElement.classList.remove('updated');
                }, 300);

                // 更新步长输入框
                const stepInput = document.getElementById('step-input');
                if (stepInput) {
                    stepInput.value = this.state.step;
                }

                // 安全地更新状态信息
                const stateElement = document.getElementById(this.stateId);
                stateElement.textContent = '';
                const stateText = document.createTextNode(
                    `状态: { count: ${this.state.count}, step: ${this.state.step} }`
                );
                stateElement.appendChild(stateText);
            }
        }

        // ========== 共享状态计数器 ==========
        class SharedCounter {
            constructor(displayId, stateId) {
                this.count = 0;
                this.displayId = displayId;
                this.stateId = stateId;
                this.render();
            }

            increment() {
                this.count++;
                this.render();
            }

            decrement() {
                this.count--;
                this.render();
            }

            reset() {
                this.count = 0;
                this.render();
            }

            render() {
                // 更新显示值
                const displayElement = document.getElementById(this.displayId);
                displayElement.textContent = this.count;

                // 添加更新动画
                displayElement.classList.add('updated');
                setTimeout(() => {
                    displayElement.classList.remove('updated');
                }, 300);

                // 安全地更新状态信息
                const stateElement = document.getElementById(this.stateId);
                stateElement.textContent = '';
                const stateText = document.createTextNode(
                    `状态: { count: ${this.count} }`
                );
                stateElement.appendChild(stateText);
            }
        }

        // ========== 初始化所有组件实例 ==========
        // 独立计数器
        const counterA = new CounterComponent('counter-a-display', 'counter-a-state', 0);
        const counterB = new CounterComponent('counter-b-display', 'counter-b-state', 10);
        const counterC = new StepCounterComponent('counter-c-display', 'counter-c-state', 0, 5);

        // 共享状态计数器
        const sharedCounter = new SharedCounter('shared-counter-display', 'shared-counter-state');

        // ========== 全局函数（用于HTML中的onclick） ==========
        // 这些函数只是简单地调用对应的组件方法
        // 实际上可以直接在HTML中使用组件实例的方法

        console.log('✅ 计数器组件系统已初始化完成！');
        console.log('💡 提示：每个计数器都有独立的状态，互不影响');
        console.log('📊 共享计数器展示了状态提升的概念');
    </script>
</body>
</html>"""
    return html_content

def save_html_file(content, filename="counter-component-demo.html"):
    """将HTML内容保存到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已生成计数器组件演示文件: {filename}")
    print(f"💡 请在浏览器中打开 {filename} 查看状态管理效果")

def main():
    """主函数"""
    print("🚀 开始构建计数器组件模式演示...")

    # 生成HTML内容
    html_content = generate_counter_component_demo()

    # 保存HTML文件
    save_html_file(html_content, "code/solutions/counter-component-demo.html")

    print("\n🎯 计数器组件模式演示已构建完成！")
    print("主要演示了以下概念：")
    print("1. 组件基类和继承")
    print("2. 独立状态管理（每个组件有自己的状态）")
    print("3. 状态更新触发重新渲染")
    print("4. 共享状态和状态提升")
    print("5. 组件间的隔离性")

if __name__ == "__main__":
    main()