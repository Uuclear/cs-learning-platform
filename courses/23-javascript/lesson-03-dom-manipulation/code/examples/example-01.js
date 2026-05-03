// example-01.js - DOM选择器演示（querySelector/querySelectorAll）
// 演示各种DOM元素选择方法的使用

console.log('=== DOM选择器演示 ===');

// 1. 使用 getElementById 获取单个元素
const header = document.getElementById('main-header');
console.log('getElementById 结果:', header);

// 2. 使用 getElementsByClassName 获取元素集合
const buttons = document.getElementsByClassName('btn');
console.log('getElementsByClassName 结果 (长度):', buttons.length);

// 3. 使用 getElementsByTagName 获取所有段落
const paragraphs = document.getElementsByTagName('p');
console.log('getElementsByTagName 结果 (长度):', paragraphs.length);

// 4. 使用 querySelector 获取第一个匹配的元素
const firstButton = document.querySelector('.btn');
console.log('querySelector (.btn) 结果:', firstButton);

// 5. 使用 querySelector 获取ID元素（等同于 getElementById）
const navElement = document.querySelector('#navigation');
console.log('querySelector (#navigation) 结果:', navElement);

// 6. 使用 querySelectorAll 获取所有匹配的元素
const allButtons = document.querySelectorAll('.btn');
console.log('querySelectorAll (.btn) 结果 (长度):', allButtons.length);

// 7. 复杂CSS选择器示例
const firstListItem = document.querySelector('ul li:first-child');
console.log('复杂选择器 (第一个li):', firstListItem);

const evenListItems = document.querySelectorAll('ul li:nth-child(even)');
console.log('偶数位置的li元素数量:', evenListItems.length);

// 8. 属性选择器示例
const dataElements = document.querySelectorAll('[data-category="featured"]');
console.log('data-category="featured" 的元素数量:', dataElements.length);

// 9. 组合选择器示例
const activeButtons = document.querySelectorAll('.btn.active');
console.log('同时具有btn和active类的按钮数量:', activeButtons.length);

console.log('=== 选择器演示完成 ===');