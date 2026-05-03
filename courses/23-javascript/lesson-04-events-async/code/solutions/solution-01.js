/**
 * 解决方案1：事件监听、冒泡与委托的完整实现
 *
 * 这是示例1的完整解决方案，包含了所有功能的正确实现
 */

console.log('=== 解决方案1：事件监听、冒泡与委托 ===');

// 创建安全的DOM结构
function createDOMStructure() {
  const container = document.createElement('div');
  container.id = 'container';

  const parent = document.createElement('div');
  parent.className = 'parent';
  parent.id = 'parent';

  // 创建3个按钮
  for (let i = 1; i <= 3; i++) {
    const button = document.createElement('button');
    button.className = 'child';
    button.id = `child${i}`;
    button.textContent = `按钮${i}`;
    parent.appendChild(button);
  }

  container.appendChild(parent);
  return container;
}

// 初始化DOM
const container = createDOMStructure();
if (typeof document !== 'undefined') {
  document.body.appendChild(container);
}

// 1. 基本事件监听 - 在目标阶段触发
document.getElementById('child1').addEventListener('click', function(event) {
  console.log('✅ 按钮1被点击了！事件阶段：',
    event.eventPhase === 1 ? '捕获阶段' :
    event.eventPhase === 2 ? '目标阶段' : '冒泡阶段'
  );
});

// 2. 事件冒泡演示
document.getElementById('parent').addEventListener('click', function(event) {
  console.log('✅ 父容器收到了冒泡事件！触发元素：', event.target.id);
});

// 3. 事件委托实现
document.getElementById('container').addEventListener('click', function(event) {
  if (event.target.classList.contains('child')) {
    console.log('✅ 通过事件委托处理：', event.target.id, '被点击了！');

    // 可以在这里添加具体的处理逻辑
    // 例如：删除元素、更新状态等
  }
});

// 4. 捕获阶段监听
document.addEventListener('click', function(event) {
  console.log('✅ document在捕获阶段收到了点击事件！');
}, true);

// 测试函数
function testEvents() {
  console.log('\n🧪 开始测试事件传播...');

  // 创建并触发点击事件
  const clickEvent = new MouseEvent('click', {
    bubbles: true,
    cancelable: true,
    view: window
  });

  document.getElementById('child2').dispatchEvent(clickEvent);

  console.log('✅ 测试完成！观察控制台输出了解事件传播顺序');
}

// 自动运行测试（如果在浏览器环境中）
if (typeof window !== 'undefined') {
  setTimeout(testEvents, 1000);
}

console.log('\n💡 关键知识点：');
console.log('- 事件传播：捕获 → 目标 → 冒泡');
console.log('- 事件委托利用冒泡特性，提高性能');
console.log('- addEventListener第三个参数控制捕获/冒泡阶段');

console.log('\n=== 解决方案1结束 ===');