/**
 * 示例2：setTimeout/setInterval与事件循环
 *
 * 这个例子演示了：
 * 1. setTimeout的基本用法和延迟机制
 * 2. setInterval的使用和清理
 * 3. 事件循环中宏任务和微任务的执行顺序
 * 4. 阻塞主线程对定时器的影响
 */

console.log('=== 示例2：setTimeout/setInterval与事件循环 ===');

// 1. 基本的setTimeout使用
console.log('\n1. 基本setTimeout演示：');
console.log('开始执行');

setTimeout(() => {
  console.log('setTimeout回调执行（延迟0ms）');
}, 0);

console.log('同步代码执行完毕');

// 2. 微任务 vs 宏任务
console.log('\n2. 微任务和宏任务执行顺序：');

// Promise是微任务
Promise.resolve().then(() => {
  console.log('Promise微任务执行');
});

// setTimeout是宏任务
setTimeout(() => {
  console.log('setTimeout宏任务执行');
}, 0);

console.log('同步代码结束');

// 3. setInterval示例
console.log('\n3. setInterval演示：');

let count = 0;
const intervalId = setInterval(() => {
  count++;
  console.log(`Interval执行第${count}次`);

  if (count >= 3) {
    clearInterval(intervalId);
    console.log('Interval已停止');
  }
}, 1000);

// 4. 阻塞主线程的影响
console.log('\n4. 阻塞主线程对定时器的影响：');

setTimeout(() => {
  console.log('这个setTimeout应该在2秒后执行');
}, 2000);

// 模拟长时间运行的同步操作（阻塞主线程）
console.log('开始阻塞操作...');
const startTime = Date.now();
while (Date.now() - startTime < 3000) {
  // 空循环，阻塞3秒
}
console.log('阻塞操作结束，实际耗时约3秒');

// 注意：上面的setTimeout会被推迟到阻塞结束后才执行

// 5. 嵌套setTimeout的行为
console.log('\n5. 嵌套setTimeout：');

setTimeout(() => {
  console.log('外层setTimeout');

  setTimeout(() => {
    console.log('内层setTimeout');
  }, 0);

  Promise.resolve().then(() => {
    console.log('外层中的Promise微任务');
  });
}, 0);

console.log('\n=== 示例2结束 ===');

// 注意：在Node.js环境中，某些行为可能与浏览器略有不同
// 但核心的事件循环机制是一致的