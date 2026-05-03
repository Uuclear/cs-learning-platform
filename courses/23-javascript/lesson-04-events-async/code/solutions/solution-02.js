/**
 * 解决方案2：setTimeout/setInterval与事件循环的完整演示
 *
 * 这是示例2的完整解决方案，清晰展示了事件循环的工作机制
 */

console.log('=== 解决方案2：setTimeout/setInterval与事件循环 ===');

// 1. 基本setTimeout行为
console.log('\n1️⃣ 基本setTimeout行为：');
console.log('同步代码开始执行');

setTimeout(() => {
  console.log('✅ setTimeout回调（延迟0ms） - 宏任务');
}, 0);

console.log('同步代码执行完毕');

// 2. 微任务 vs 宏任务执行顺序
console.log('\n2️⃣ 微任务和宏任务执行顺序：');

Promise.resolve().then(() => {
  console.log('✅ Promise微任务 - 优先执行');
});

setTimeout(() => {
  console.log('✅ setTimeout宏任务 - 后执行');
}, 0);

queueMicrotask(() => {
  console.log('✅ queueMicrotask - 也是微任务');
});

console.log('同步代码结束');

// 3. setInterval完整示例
console.log('\n3️⃣ setInterval完整示例：');

let intervalCount = 0;
const maxIntervals = 3;

const intervalId = setInterval(() => {
  intervalCount++;
  console.log(`✅ Interval ${intervalCount}/${maxIntervals} 执行`);

  if (intervalCount >= maxIntervals) {
    clearInterval(intervalId);
    console.log('✅ Interval已清理并停止');
  }
}, 500);

// 4. 主线程阻塞对定时器的影响
console.log('\n4️⃣ 主线程阻塞影响：');

setTimeout(() => {
  console.log('✅ 这个setTimeout设置为2秒后执行');
}, 2000);

console.log('⏳ 开始3秒阻塞操作...');
const blockStart = Date.now();
while (Date.now() - blockStart < 3000) {
  // 阻塞主线程3秒
}
console.log('✅ 阻塞操作结束（实际耗时3秒）');
console.log('💡 注意：上面的setTimeout会被推迟到阻塞结束后执行');

// 5. 复杂的事件循环演示
console.log('\n5️⃣ 复杂事件循环演示：');

console.log('同步代码：开始');

setTimeout(() => {
  console.log('宏任务1：setTimeout外层');

  Promise.resolve().then(() => {
    console.log('微任务1：Promise在外层setTimeout中');
  });

  setTimeout(() => {
    console.log('宏任务2：嵌套setTimeout');
  }, 0);
}, 0);

Promise.resolve().then(() => {
  console.log('微任务2：顶层Promise');

  setTimeout(() => {
    console.log('宏任务3：setTimeout在顶层Promise中');
  }, 0);
});

console.log('同步代码：结束');

// 6. 实际应用：防抖函数实现
console.log('\n6️⃣ 实际应用：防抖函数');

function debounce(func, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}

const debouncedLog = debounce((msg) => {
  console.log('✅ 防抖函数执行:', msg);
}, 1000);

console.log('调用防抖函数多次...');
debouncedLog('第一次调用');
debouncedLog('第二次调用');
debouncedLog('第三次调用');
// 只有最后一次会执行

console.log('\n💡 事件循环关键点：');
console.log('- JavaScript是单线程的');
console.log('- 微任务优先于宏任务执行');
console.log('- setTimeout不能保证精确延迟');
console.log('- 长时间同步操作会阻塞所有异步回调');

console.log('\n=== 解决方案2结束 ===');