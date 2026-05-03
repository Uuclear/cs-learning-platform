// 综合Promise工具函数解决方案
console.log("=== 综合Promise工具函数解决方案 ===");

// 1. 超时控制函数
function withTimeout(promise, timeoutMs) {
  const timeout = new Promise((_, reject) => {
    setTimeout(() => reject(new Error(`操作超时 (${timeoutMs}ms)`)), timeoutMs);
  });

  return Promise.race([promise, timeout]);
}

// 2. 并发限制函数（限制同时进行的Promise数量）
async function limitConcurrency(tasks, limit) {
  const results = [];
  const executing = [];

  for (const [index, task] of tasks.entries()) {
    // 如果达到并发限制，等待其中一个完成
    if (executing.length >= limit) {
      await Promise.race(executing);
    }

    const promise = Promise.resolve().then(() => task()).then(
      result => ({ index, result }),
      error => ({ index, error })
    );

    executing.push(promise);

    // 清理已完成的Promise
    promise.then(() => {
      const idx = executing.indexOf(promise);
      if (idx !== -1) executing.splice(idx, 1);
    });
  }

  // 等待所有剩余的Promise完成
  const remaining = await Promise.all(executing);
  for (const { index, result, error } of remaining) {
    if (error) {
      results[index] = { status: 'rejected', reason: error };
    } else {
      results[index] = { status: 'fulfilled', value: result };
    }
  }

  return results;
}

// 3. 优雅的错误处理包装器
function safePromise(promiseFn) {
  return (...args) => {
    return Promise.resolve()
      .then(() => promiseFn(...args))
      .then(result => ({ success: true, data: result }))
      .catch(error => ({ success: false, error: error.message }));
  };
}

// 使用示例
async function demonstrateUtils() {
  console.log("=== 超时控制演示 ===");
  try {
    // 这个会超时
    await withTimeout(new Promise(resolve => setTimeout(resolve, 2000)), 1000);
  } catch (error) {
    console.log("✅ 超时控制工作正常:", error.message);
  }

  console.log("\n=== 并发限制演示 ===");
  const tasks = Array.from({ length: 6 }, (_, i) =>
    () => new Promise(resolve => {
      const delay = Math.random() * 1000 + 500;
      console.log(`开始任务 ${i + 1}，延迟 ${delay.toFixed(0)}ms`);
      setTimeout(() => {
        console.log(`✅ 任务 ${i + 1} 完成`);
        resolve(`结果${i + 1}`);
      }, delay);
    })
  );

  // 限制同时只运行2个任务
  const limitedResults = await limitConcurrency(tasks, 2);
  console.log("并发限制结果:", limitedResults.map(r => r.status === 'fulfilled' ? r.value : `错误:${r.reason.message}`));

  console.log("\n=== 安全Promise包装器演示 ===");
  const safeFetch = safePromise(async (url, shouldFail) => {
    if (shouldFail) throw new Error("模拟失败");
    return `成功获取${url}`;
  });

  const [successResult, failResult] = await Promise.all([
    safeFetch("/api/good", false),
    safeFetch("/api/bad", true)
  ]);

  console.log("安全调用结果:");
  console.log("  成功:", successResult);
  console.log("  失败:", failResult);
}

demonstrateUtils();