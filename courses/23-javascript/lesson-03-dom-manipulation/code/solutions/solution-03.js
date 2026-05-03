// solution-03.js - 示例3的解答：动态创建和删除DOM节点
// 完整的DOM节点管理解决方案，包含性能优化

console.log('=== DOM节点管理完整解决方案 ===');

// 1. 节点创建工厂函数
const NodeFactory = {
    // 创建元素节点
    element: (tagName, config = {}) => {
        const element = document.createElement(tagName);

        // 设置文本内容
        if (config.text) {
            element.textContent = config.text;
        }

        // 设置HTML内容（仅用于可信的静态内容）
        if (config.html) {
            console.warn('使用 innerHTML，请确保内容为可信的静态内容以避免XSS风险');
            element.innerHTML = config.html;
        }

        // 设置类名
        if (config.className) {
            element.className = config.className;
        }

        // 设置ID
        if (config.id) {
            element.id = config.id;
        }

        // 设置属性
        if (config.attributes) {
            Object.keys(config.attributes).forEach(attr => {
                element.setAttribute(attr, config.attributes[attr]);
            });
        }

        // 设置样式
        if (config.styles) {
            Object.keys(config.styles).forEach(style => {
                element.style[style] = config.styles[style];
            });
        }

        return element;
    },

    // 创建文本节点
    text: (text) => {
        return document.createTextNode(text);
    },

    // 创建文档片段
    fragment: () => {
        return document.createDocumentFragment();
    }
};

// 2. 节点插入管理器
const InsertManager = {
    // 在末尾插入
    append: (parent, ...children) => {
        if (!parent) return false;
        children.forEach(child => {
            if (child) parent.appendChild(child);
        });
        return true;
    },

    // 在开头插入
    prepend: (parent, ...children) => {
        if (!parent) return false;
        // 现代浏览器支持 prepend
        if (parent.prepend) {
            parent.prepend(...children.filter(Boolean));
        } else {
            // 降级方案：使用 insertBefore
            const firstChild = parent.firstChild;
            children.filter(Boolean).reverse().forEach(child => {
                parent.insertBefore(child, firstChild);
            });
        }
        return true;
    },

    // 在指定元素前插入
    before: (reference, ...elements) => {
        if (!reference || !reference.parentNode) return false;
        elements.filter(Boolean).forEach(element => {
            reference.parentNode.insertBefore(element, reference);
        });
        return true;
    },

    // 在指定元素后插入
    after: (reference, ...elements) => {
        if (!reference || !reference.parentNode) return false;
        const nextSibling = reference.nextSibling;
        if (nextSibling) {
            elements.filter(Boolean).forEach(element => {
                reference.parentNode.insertBefore(element, nextSibling);
            });
        } else {
            // 如果没有下一个兄弟，直接append到父元素
            elements.filter(Boolean).forEach(element => {
                reference.parentNode.appendChild(element);
            });
        }
        return true;
    },

    // 批量插入（使用DocumentFragment优化性能）
    batchInsert: (parent, createElementsFn) => {
        if (!parent || typeof createElementsFn !== 'function') return false;

        const fragment = NodeFactory.fragment();
        const elements = createElementsFn(fragment);

        if (Array.isArray(elements)) {
            elements.forEach(el => fragment.appendChild(el));
        }

        parent.appendChild(fragment);
        return true;
    }
};

// 3. 节点删除管理器
const DeleteManager = {
    // 删除单个元素
    remove: (element) => {
        if (!element) return false;
        if (element.remove) {
            element.remove();
        } else if (element.parentNode) {
            element.parentNode.removeChild(element);
        }
        return true;
    },

    // 批量删除
    removeAll: (elements) => {
        if (!Array.isArray(elements)) return false;
        elements.forEach(el => DeleteManager.remove(el));
        return true;
    },

    // 清空容器
    empty: (container) => {
        if (!container) return false;
        while (container.firstChild) {
            container.removeChild(container.firstChild);
        }
        return true;
    }
};

// 4. 节点替换管理器
const ReplaceManager = {
    // 替换元素
    replace: (oldElement, newElement) => {
        if (!oldElement || !newElement) return false;
        if (oldElement.replaceWith) {
            oldElement.replaceWith(newElement);
        } else if (oldElement.parentNode) {
            oldElement.parentNode.replaceChild(newElement, oldElement);
        }
        return true;
    },

    // 替换所有匹配的元素
    replaceAll: (selector, createNewElementFn) => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(oldElement => {
            const newElement = createNewElementFn(oldElement);
            if (newElement) {
                ReplaceManager.replace(oldElement, newElement);
            }
        });
    }
};

// 5. 实际应用示例：动态待办事项列表
function createTodoApp() {
    // 创建容器
    const todoContainer = NodeFactory.element('div', {
        className: 'todo-app',
        id: 'todo-app'
    });

    // 创建标题
    const title = NodeFactory.element('h2', {
        text: '待办事项列表',
        className: 'todo-title'
    });

    // 创建输入框
    const input = NodeFactory.element('input', {
        attributes: {
            type: 'text',
            placeholder: '添加新任务...',
            id: 'todo-input'
        },
        className: 'todo-input'
    });

    // 创建添加按钮
    const addButton = NodeFactory.element('button', {
        text: '添加',
        className: 'todo-add-btn'
    });

    // 创建列表容器
    const list = NodeFactory.element('ul', {
        className: 'todo-list',
        id: 'todo-list'
    });

    // 组装UI
    InsertManager.append(todoContainer, title, input, addButton, list);

    // 添加事件处理（简化版）
    addButton.addEventListener('click', () => {
        const text = input.value.trim();
        if (text) {
            addTodoItem(list, text);
            input.value = '';
        }
    });

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const text = input.value.trim();
            if (text) {
                addTodoItem(list, text);
                input.value = '';
            }
        }
    });

    return todoContainer;
}

// 添加待办事项项
function addTodoItem(list, text) {
    const item = NodeFactory.element('li', {
        className: 'todo-item'
    });

    const itemText = NodeFactory.element('span', {
        text: text,
        className: 'todo-text'
    });

    const deleteBtn = NodeFactory.element('button', {
        text: '删除',
        className: 'todo-delete-btn'
    });

    // 删除功能
    deleteBtn.addEventListener('click', () => {
        DeleteManager.remove(item);
    });

    // 完成功能
    itemText.addEventListener('click', () => {
        itemText.classList.toggle('completed');
    });

    InsertManager.append(item, itemText, deleteBtn);
    InsertManager.append(list, item);
}

// 6. 性能测试：批量操作 vs 单个操作
function performanceTest() {
    console.log('=== 性能测试开始 ===');

    // 测试容器
    const testContainer = NodeFactory.element('div', { id: 'performance-test' });
    document.body.appendChild(testContainer);

    // 方法1：逐个添加（性能较差）
    console.time('逐个添加');
    const slowList = NodeFactory.element('ul');
    for (let i = 0; i < 100; i++) {
        const li = NodeFactory.element('li', { text: `项目 ${i + 1}` });
        slowList.appendChild(li);
    }
    testContainer.appendChild(slowList);
    console.timeEnd('逐个添加');

    // 方法2：批量添加（性能较好）
    console.time('批量添加');
    const fastList = NodeFactory.element('ul');
    InsertManager.batchInsert(fastList, (fragment) => {
        const items = [];
        for (let i = 0; i < 100; i++) {
            const li = NodeFactory.element('li', { text: `项目 ${i + 101}` });
            items.push(li);
        }
        return items;
    });
    testContainer.appendChild(fastList);
    console.timeEnd('批量添加');

    // 清理测试
    DeleteManager.remove(testContainer);
    console.log('=== 性能测试完成 ===');
}

// 7. 演示完整的节点操作流程
function demonstrateFullWorkflow() {
    console.log('=== 完整工作流演示 ===');

    // 创建主容器
    const mainContainer = NodeFactory.element('div', { id: 'demo-container' });
    document.body.appendChild(mainContainer);

    // 创建初始内容
    const initialContent = NodeFactory.element('div', {
        text: '初始内容',
        className: 'initial'
    });
    InsertManager.append(mainContainer, initialContent);

    // 更新内容
    setTimeout(() => {
        const updatedContent = NodeFactory.element('div', {
            html: '<strong>更新后的静态内容</strong>',
            className: 'updated'
        });
        ReplaceManager.replace(initialContent, updatedContent);
        console.log('内容已更新');

        // 添加更多内容
        const additionalContent = NodeFactory.element('p', {
            text: '额外添加的内容',
            className: 'additional'
        });
        InsertManager.after(updatedContent, additionalContent);
        console.log('额外内容已添加');

        // 删除操作
        setTimeout(() => {
            DeleteManager.remove(additionalContent);
            console.log('额外内容已删除');

            // 清空容器
            setTimeout(() => {
                DeleteManager.empty(mainContainer);
                console.log('容器已清空');

                // 重新填充
                const newContent = NodeFactory.element('div', {
                    text: '全新内容',
                    className: 'new'
                });
                InsertManager.append(mainContainer, newContent);
                console.log('全新内容已添加');

                // 最终清理
                setTimeout(() => {
                    DeleteManager.remove(mainContainer);
                    console.log('演示完成，所有元素已清理');
                }, 500);
            }, 500);
        }, 500);
    }, 500);
}

// 运行演示
performanceTest();
demonstrateFullWorkflow();

// 创建并添加待办事项应用（注释掉以避免实际DOM污染）
// const todoApp = createTodoApp();
// document.body.appendChild(todoApp);

console.log('=== DOM节点管理解决方案完成 ===');