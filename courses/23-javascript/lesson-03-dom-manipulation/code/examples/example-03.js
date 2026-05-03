// example-03.js - 动态创建和删除DOM节点
// 演示如何动态创建、插入、删除和替换DOM元素

console.log('=== 动态创建和删除DOM节点演示 ===');

// 1. 创建新的DOM元素
const newDiv = document.createElement('div');
newDiv.className = 'dynamic-element';
newDiv.textContent = '这是动态创建的元素';

const newParagraph = document.createElement('p');
newParagraph.textContent = '这是动态创建的段落';

const newText = document.createTextNode('这是纯文本节点');

// 2. 创建容器元素用于演示
const container = document.createElement('div');
container.id = 'demo-container';
document.body.appendChild(container);

// 3. 使用 appendChild() 插入元素
container.appendChild(newDiv);
console.log('使用 appendChild() 插入元素完成');

// 4. 使用 insertBefore() 在指定位置插入
const referenceElement = document.createElement('span');
referenceElement.textContent = '参考元素';
container.appendChild(referenceElement);

const insertBeforeElement = document.createElement('em');
insertBeforeElement.textContent = '插入到参考元素之前 ';
container.insertBefore(insertBeforeElement, referenceElement);
console.log('使用 insertBefore() 插入元素完成');

// 5. 现代插入方法演示 (ES6+)
const modernContainer = document.createElement('div');
modernContainer.id = 'modern-demo';
document.body.appendChild(modernContainer);

// append() - 在容器末尾插入
modernContainer.append('文本内容 ', newParagraph.cloneNode(true));

// prepend() - 在容器开头插入
const prependedDiv = document.createElement('div');
prependingDiv.textContent = '开头插入的内容';
modernContainer.prepend(prependedDiv);
console.log('使用 append() 和 prepend() 完成');

// before() 和 after() - 在元素前后插入
const siblingElement = document.createElement('div');
siblingElement.textContent = '兄弟元素';
modernContainer.appendChild(siblingElement);

const beforeElement = document.createElement('span');
beforeElement.textContent = '在兄弟元素之前 ';
siblingElement.before(beforeElement);

const afterElement = document.createElement('span');
afterElement.textContent = ' 在兄弟元素之后';
siblingElement.after(afterElement);
console.log('使用 before() 和 after() 完成');

// 6. 删除元素演示
const elementToDelete = document.createElement('div');
elementToDelete.id = 'delete-me';
elementToDelete.textContent = '这个元素将被删除';
document.body.appendChild(elementToDelete);

console.log('删除前，元素存在:', !!document.getElementById('delete-me'));

// 传统删除方法
if (elementToDelete.parentNode) {
    elementToDelete.parentNode.removeChild(elementToDelete);
}
console.log('使用 removeChild() 删除后:', !!document.getElementById('delete-me'));

// 重新添加用于现代方法演示
document.body.appendChild(elementToDelete);
console.log('重新添加后，元素存在:', !!document.getElementById('delete-me'));

// 现代删除方法 (ES6+)
elementToDelete.remove();
console.log('使用 remove() 删除后:', !!document.getElementById('delete-me'));

// 7. 替换元素演示
const oldElement = document.createElement('div');
oldElement.id = 'old-element';
oldElement.textContent = '旧元素';
document.body.appendChild(oldElement);

const newElement = document.createElement('div');
newElement.textContent = '新元素（替换了旧元素）';

// 传统替换方法
if (oldElement.parentNode) {
    oldElement.parentNode.replaceChild(newElement, oldElement);
}
console.log('使用 replaceChild() 替换完成');

// 重新添加旧元素用于现代方法演示
document.body.appendChild(oldElement);

// 现代替换方法 (ES6+)
oldElement.replaceWith(newElement.cloneNode(true));
console.log('使用 replaceWith() 替换完成');

// 8. 性能优化：使用 DocumentFragment
console.log('=== DocumentFragment 性能优化演示 ===');

const performanceContainer = document.createElement('ul');
performanceContainer.id = 'performance-test';
document.body.appendChild(performanceContainer);

// 使用 DocumentFragment 批量添加元素
const fragment = document.createDocumentFragment();
for (let i = 0; i < 5; i++) {
    const li = document.createElement('li');
    li.textContent = `列表项 ${i + 1}`;
    fragment.appendChild(li);
}
performanceContainer.appendChild(fragment);
console.log('使用 DocumentFragment 批量添加完成');

// 清理所有测试元素
document.body.removeChild(container);
document.body.removeChild(modernContainer);
document.body.removeChild(performanceContainer);
document.body.removeChild(newElement);
document.body.removeChild(newElement.cloneNode(true));

console.log('=== 动态创建和删除DOM节点演示完成 ===');