// example-02.js - 元素内容、样式和属性修改
// 演示如何修改DOM元素的内容、样式和属性

console.log('=== DOM元素内容、样式和属性修改演示 ===');

// 假设我们有一个测试元素
const testElement = document.createElement('div');
testElement.id = 'test-element';
testElement.className = 'initial-class';
document.body.appendChild(testElement);

// 1. 修改文本内容 (textContent)
testElement.textContent = '这是通过 textContent 设置的文本';
console.log('textContent 设置后:', testElement.textContent);

// 2. 修改HTML内容 (innerHTML) - 注意：仅用于可信的静态内容，避免XSS风险
testElement.innerHTML = '<strong>这是粗体文本</strong> 和 <em>斜体文本</em>';
console.log('innerHTML 设置后 (仅用于可信内容):', testElement.innerHTML);

// 3. 修改样式 (style 属性)
testElement.style.backgroundColor = 'lightblue';
testElement.style.padding = '20px';
testElement.style.borderRadius = '8px';
testElement.style.margin = '10px';
console.log('样式修改完成');

// 4. 修改CSS类 (className)
testElement.className = 'updated-class highlight';
console.log('className 修改后:', testElement.className);

// 5. 使用 classList API (推荐方式)
testElement.classList.add('active');
testElement.classList.add('new-feature');
console.log('添加class后:', testElement.className);

testElement.classList.remove('initial-class');
console.log('移除class后:', testElement.className);

// 切换class（如果存在就移除，不存在就添加）
testElement.classList.toggle('toggled-class');
console.log('切换class后 (第一次):', testElement.className);

testElement.classList.toggle('toggled-class');
console.log('切换class后 (第二次):', testElement.className);

// 检查是否包含某个class
const hasActive = testElement.classList.contains('active');
console.log('是否包含 "active" class:', hasActive);

// 6. 修改属性 (setAttribute/getAttribute)
testElement.setAttribute('data-status', 'completed');
testElement.setAttribute('title', '这是一个测试元素');
console.log('设置属性后 data-status:', testElement.getAttribute('data-status'));
console.log('设置属性后 title:', testElement.getAttribute('title'));

// 7. 直接访问标准属性
testElement.id = 'modified-id';
console.log('直接修改id后:', testElement.id);

// 8. 移除属性
testElement.removeAttribute('title');
console.log('移除title属性后:', testElement.getAttribute('title')); // null

// 清理测试元素
document.body.removeChild(testElement);
console.log('=== 内容、样式和属性修改演示完成 ===');