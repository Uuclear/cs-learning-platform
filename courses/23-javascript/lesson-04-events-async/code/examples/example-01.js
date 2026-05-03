/**
 * 示例1：事件监听、冒泡与委托
 *
 * 这个例子演示了：
 * 1. 基本的事件监听器添加
 * 2. 事件冒泡的实际效果
 * 3. 事件委托的实现方式
 */

console.log('=== 示例1：事件监听、冒泡与委托 ===');

// 创建HTML结构（模拟）- 使用安全的方式
const container = document.createElement('div');
container.id = 'container';

const parent = document.createElement('div');
parent.className = 'parent';
parent.id = 'parent';

// 创建按钮元素
for (let i = 1; i <= 3; i++) {
  const button = document.createElement('button');
  button.className = 'child';
  button.id = `child${i}`;
  button.textContent = `按钮${i}`;
  parent.appendChild(button);
}

container.appendChild(parent);

// 添加到文档（如果在浏览器环境中）
if (typeof document !== 'undefined') {
  document.body.appendChild(container);
}

// 1. 基本事件监听
console.log('\n1. 基本事件监听：');
document.getElementById('child1').addEventListener('click', function(event) {
  console.log('按钮1被点击了！事件阶段：', event.eventPhase);
  // event.eventPhase: 1=捕获, 2=目标, 3=冒泡
});

// 2. 演示事件冒泡
console.log('\n2. 事件冒泡演示：');
document.getElementById('parent').addEventListener('click', function(event) {
  console.log('父容器收到了冒泡事件！触发元素：', event.target.id);
});

// 3. 事件委托
console.log('\n3. 事件委托：');
document.getElementById('container').addEventListener('click', function(event) {
  // 检查是否点击的是子按钮
  if (event.target.classList.contains('child')) {
    console.log('通过事件委托处理：', event.target.id, '被点击了！');

    // 阻止事件继续冒泡（可选）
    // event.stopPropagation();
  }
});

// 4. 捕获阶段的事件监听
console.log('\n4. 捕获阶段监听：');
document.addEventListener('click', function(event) {
  console.log('document在捕获阶段收到了点击事件！');
}, true); // 第三个参数true表示在捕获阶段监听

// 模拟点击事件（用于Node.js环境测试）
console.log('\n模拟点击按钮1：');
const clickEvent = new Event('click');
document.getElementById('child1').dispatchEvent(clickEvent);

console.log('\n=== 示例1结束 ===');