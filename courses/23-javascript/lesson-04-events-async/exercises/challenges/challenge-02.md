# 编程挑战 2：异步操作模拟器

## 任务描述

创建一个异步操作模拟器，演示JavaScript事件循环的工作机制，并实现防抖（debounce）和节流（throttle）函数。

## 功能要求

### 第一部分：事件循环可视化

1. **创建控制面板**，包含以下按钮：
   - "执行同步阻塞"：执行3秒的同步阻塞操作
   - "设置setTimeout"：设置一个1秒后的setTimeout回调
   - "添加Promise微任务"：添加一个Promise微任务
   - "清除所有定时器"：清理所有活动的定时器

2. **显示执行日志**：在页面上实时显示每个操作的执行时间和类型

3. **演示执行顺序**：通过按钮组合展示微任务优先于宏任务的特性

### 第二部分：防抖和节流实现

1. **防抖函数（debounce）**：
   - 实现一个`debounce(func, delay)`函数
   - 创建一个输入框，用户输入时触发防抖函数
   - 显示"用户停止输入X秒后执行"

2. **节流函数（throttle）**：
   - 实现一个`throttle(func, delay)`函数  
   - 创建一个按钮，连续点击时使用节流限制执行频率
   - 显示"每X秒最多执行一次"

## JavaScript要求

### 防抖函数实现
```javascript
function debounce(func, delay) {
  // 你的实现
}
```

### 节流函数实现
```javascript
function throttle(func, delay) {
  // 你的实现
}
```

### 事件循环演示要求
- 使用`console.log`和页面元素同时显示执行信息
- 在同步阻塞期间，其他异步操作应该被推迟
- 清晰展示微任务和宏任务的执行顺序差异

## HTML结构建议

```html
<div id="async-simulator">
  <h2>异步操作模拟器</h2>
  
  <div class="controls">
    <button id="sync-block">执行同步阻塞 (3秒)</button>
    <button id="set-timeout">设置setTimeout (1秒)</button>
    <button id="add-microtask">添加Promise微任务</button>
    <button id="clear-all">清除所有定时器</button>
  </div>
  
  <div class="debounce-section">
    <h3>防抖演示</h3>
    <input type="text" id="debounce-input" placeholder="输入内容...">
    <div id="debounce-output"></div>
  </div>
  
  <div class="throttle-section">
    <h3>节流演示</h3>
    <button id="throttle-btn">快速点击我</button>
    <div id="throttle-output"></div>
  </div>
  
  <div class="log-section">
    <h3>执行日志</h3>
    <div id="execution-log"></div>
  </div>
</div>
```

## 额外挑战（可选）

- 添加性能监控，显示每个操作的实际执行时间
- 实现取消功能，允许取消待执行的防抖/节流操作
- 添加可视化的时间轴，显示任务队列状态

## 提交要求

将完整的HTML、CSS和JavaScript代码保存在一个文件中，确保可以在浏览器中正常运行。

## 评估标准

- ✅ 正确实现防抖和节流函数
- ✅ 准确演示事件循环机制
- ✅ 代码结构良好，有清晰注释
- ✅ 用户界面友好，功能完整
- ✅ 处理各种边界情况和错误状态