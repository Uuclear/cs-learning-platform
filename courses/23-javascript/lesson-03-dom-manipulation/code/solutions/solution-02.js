// solution-02.js - 示例2的解答：元素内容、样式和属性修改
// 完整的DOM元素操作解决方案，包含安全实践

console.log('=== DOM元素操作完整解决方案 ===');

// 创建测试环境
function createTestEnvironment() {
    const testContainer = document.createElement('div');
    testContainer.id = 'test-environment';
    document.body.appendChild(testContainer);
    return testContainer;
}

const testEnv = createTestEnvironment();

// 1. 安全的内容修改函数
function updateContent(element, content, method = 'textContent') {
    if (!element) {
        console.warn('元素不存在，无法更新内容');
        return false;
    }

    try {
        switch(method) {
            case 'textContent':
                element.textContent = content;
                break;
            case 'innerHTML':
                // 安全警告：仅用于可信的静态内容，避免XSS风险
                console.warn('使用 innerHTML，请确保内容为可信的静态内容以避免XSS风险');
                element.innerHTML = content;
                break;
            case 'innerText':
                element.innerText = content;
                break;
            default:
                throw new Error('不支持的内容更新方法');
        }
        return true;
    } catch (error) {
        console.error('内容更新失败:', error.message);
        return false;
    }
}

// 测试内容修改
const contentElement = document.createElement('div');
testEnv.appendChild(contentElement);

updateContent(contentElement, '安全的文本内容', 'textContent');
console.log('textContent 结果:', contentElement.textContent);

updateContent(contentElement, '<strong>可信的静态HTML内容</strong>', 'innerHTML');
console.log('innerHTML 结果:', contentElement.innerHTML);

// 2. 样式操作工具函数
function updateStyles(element, styles) {
    if (!element || !styles) return false;

    try {
        Object.keys(styles).forEach(property => {
            element.style[property] = styles[property];
        });
        return true;
    } catch (error) {
        console.error('样式更新失败:', error.message);
        return false;
    }
}

// 测试样式修改
updateStyles(contentElement, {
    backgroundColor: 'lightgreen',
    padding: '15px',
    borderRadius: '5px',
    margin: '10px',
    fontSize: '16px'
});

console.log('样式已应用');

// 3. CSS类操作工具函数
const ClassManager = {
    add: (element, ...classes) => {
        if (!element) return false;
        classes.forEach(cls => element.classList.add(cls));
        return true;
    },

    remove: (element, ...classes) => {
        if (!element) return false;
        classes.forEach(cls => element.classList.remove(cls));
        return true;
    },

    toggle: (element, className) => {
        if (!element) return false;
        return element.classList.toggle(className);
    },

    has: (element, className) => {
        if (!element) return false;
        return element.classList.contains(className);
    },

    set: (element, className) => {
        if (!element) return false;
        element.className = className;
        return true;
    }
};

// 测试CSS类操作
ClassManager.set(contentElement, 'base-class');
ClassManager.add(contentElement, 'active', 'highlight', 'feature-enabled');
console.log('添加class后:', contentElement.className);

ClassManager.remove(contentElement, 'base-class');
console.log('移除class后:', contentElement.className);

const isHighlighted = ClassManager.has(contentElement, 'highlight');
console.log('是否包含 highlight class:', isHighlighted);

const toggled = ClassManager.toggle(contentElement, 'toggled-state');
console.log('切换 toggled-state:', toggled, '当前class:', contentElement.className);

// 4. 属性操作工具函数
const AttributeManager = {
    set: (element, attributes) => {
        if (!element || !attributes) return false;
        try {
            Object.keys(attributes).forEach(attr => {
                element.setAttribute(attr, attributes[attr]);
            });
            return true;
        } catch (error) {
            console.error('属性设置失败:', error.message);
            return false;
        }
    },

    get: (element, attribute) => {
        if (!element) return null;
        return element.getAttribute(attribute);
    },

    remove: (element, attribute) => {
        if (!element) return false;
        element.removeAttribute(attribute);
        return true;
    },

    has: (element, attribute) => {
        if (!element) return false;
        return element.hasAttribute(attribute);
    }
};

// 测试属性操作
AttributeManager.set(contentElement, {
    'data-role': 'content-block',
    'data-status': 'active',
    'title': '内容块标题',
    'aria-label': '主要内容区域'
});

console.log('data-role 属性值:', AttributeManager.get(contentElement, 'data-role'));
console.log('是否存在 title 属性:', AttributeManager.has(contentElement, 'title'));

AttributeManager.remove(contentElement, 'title');
console.log('移除 title 后是否存在:', AttributeManager.has(contentElement, 'title'));

// 5. 直接属性访问（标准属性）
contentElement.id = 'dynamic-content';
contentElement.tabIndex = 0;
console.log('直接设置的ID:', contentElement.id);
console.log('直接设置的tabIndex:', contentElement.tabIndex);

// 6. 综合示例：创建完整的UI组件
function createButton(config = {}) {
    const button = document.createElement('button');

    // 设置内容（使用textContent确保安全）
    updateContent(button, config.text || '按钮', 'textContent');

    // 设置样式
    updateStyles(button, {
        backgroundColor: config.color || '#007bff',
        color: 'white',
        border: 'none',
        padding: '8px 16px',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '14px'
    });

    // 设置类
    ClassManager.set(button, 'btn');
    if (config.variant) ClassManager.add(button, `btn-${config.variant}`);
    if (config.disabled) ClassManager.add(button, 'disabled');

    // 设置属性
    AttributeManager.set(button, {
        'type': config.type || 'button',
        'data-action': config.action || 'default'
    });

    if (config.disabled) {
        button.disabled = true;
    }

    return button;
}

// 创建测试按钮
const primaryBtn = createButton({
    text: '主要按钮',
    variant: 'primary',
    action: 'submit-form'
});

const disabledBtn = createButton({
    text: '禁用按钮',
    variant: 'secondary',
    disabled: true,
    action: 'inactive'
});

testEnv.appendChild(primaryBtn);
testEnv.appendChild(disabledBtn);

console.log('创建的按钮1 class:', primaryBtn.className);
console.log('创建的按钮2 disabled:', disabledBtn.disabled);

// 清理测试环境
document.body.removeChild(testEnv);
console.log('=== DOM元素操作解决方案完成 ===');