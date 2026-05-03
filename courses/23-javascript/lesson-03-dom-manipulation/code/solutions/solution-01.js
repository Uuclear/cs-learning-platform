// solution-01.js - 示例1的解答：DOM选择器演示
// 完整的DOM选择器使用示例，包含错误处理和最佳实践

console.log('=== DOM选择器完整解决方案 ===');

// 安全的选择器函数，包含错误处理
function safeSelect(selector, method = 'querySelector') {
    try {
        let result;
        switch(method) {
            case 'getElementById':
                result = document.getElementById(selector);
                break;
            case 'getElementsByClassName':
                result = document.getElementsByClassName(selector);
                break;
            case 'getElementsByTagName':
                result = document.getElementsByTagName(selector);
                break;
            case 'querySelector':
                result = document.querySelector(selector);
                break;
            case 'querySelectorAll':
                result = document.querySelectorAll(selector);
                break;
            default:
                throw new Error('不支持的选择方法');
        }

        if (!result) {
            console.warn(`未找到匹配 "${selector}" 的元素`);
            return null;
        }

        return result;
    } catch (error) {
        console.error('选择器错误:', error.message);
        return null;
    }
}

// 1. 基础选择器演示
const header = safeSelect('main-header', 'getElementById');
if (header) {
    console.log('成功获取header元素:', header.tagName);
}

// 2. 类选择器演示
const buttons = safeSelect('btn', 'getElementsByClassName');
if (buttons) {
    console.log('找到按钮数量:', buttons.length);
    // 转换为数组以便使用数组方法
    const buttonsArray = Array.from(buttons);
    buttonsArray.forEach((btn, index) => {
        console.log(`按钮 ${index + 1}:`, btn.textContent.trim());
    });
}

// 3. 标签选择器演示
const paragraphs = safeSelect('p', 'getElementsByTagName');
console.log('段落数量:', paragraphs ? paragraphs.length : 0);

// 4. querySelector 系列演示
const firstButton = safeSelect('.btn', 'querySelector');
const navElement = safeSelect('#navigation', 'querySelector');
const allButtons = safeSelect('.btn', 'querySelectorAll');

if (allButtons) {
    console.log('querySelectorAll 结果类型:', Object.prototype.toString.call(allButtons));
    console.log('按钮总数:', allButtons.length);

    // NodeList 可以使用 forEach（现代浏览器）
    allButtons.forEach((btn, index) => {
        console.log(`按钮 ${index + 1} ID:`, btn.id || '无ID');
    });
}

// 5. 复杂选择器示例
const complexSelectors = [
    'ul li:first-child',
    'ul li:nth-child(even)',
    '[data-category="featured"]',
    '.btn.active',
    'div > p', // 直接子元素
    'div p'    // 后代元素
];

complexSelectors.forEach(selector => {
    const elements = safeSelect(selector, 'querySelectorAll');
    console.log(`选择器 "${selector}" 匹配元素数量:`, elements ? elements.length : 0);
});

// 6. 实用工具函数：检查元素是否存在
function elementExists(selector) {
    return document.querySelector(selector) !== null;
}

console.log('检查 #main-header 是否存在:', elementExists('#main-header'));
console.log('检查 .non-existent 是否存在:', elementExists('.non-existent'));

// 7. 性能提示：缓存选择结果
// 避免重复查询相同的选择器
const cachedElements = {
    headers: document.querySelectorAll('h1, h2, h3'),
    links: document.querySelectorAll('a[href]')
};

console.log('缓存的标题数量:', cachedElements.headers.length);
console.log('缓存的链接数量:', cachedElements.links.length);

console.log('=== DOM选择器解决方案完成 ===');