// async/await语法和错误处理示例
console.log("=== async/await 基础演示 ===");

// 模拟异步操作的函数
function delay(ms, shouldFail = false) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) {
        reject(new Error("操作失败！"));
      } else {
        resolve(`延迟${ms}毫秒完成`);
      }
    }, ms);
  });
}

// 基本的async/await使用
async function basicAsyncAwait() {
  try {
    console.log("开始执行...");
    const result1 = await delay(1000);
    console.log("✅ 第一步:", result1);

    const result2 = await delay(800);
    console.log("✅ 第二步:", result2);

    const result3 = await delay(600);
    console.log("✅ 第三步:", result3);

    console.log("🎉 所有步骤完成！");
    return "全部成功";
  } catch (error) {
    console.error("❌ 执行过程中出错:", error.message);
    throw error; // 重新抛出错误
  }
}

// 错误处理示例
async function errorHandlingExample() {
  console.log("\n=== 错误处理演示 ===");

  try {
    console.log("尝试执行可能失败的操作...");
    await delay(500, true); // 这个会失败
    console.log("这行不会执行");
  } catch (error) {
    console.error("✅ 捕获到错误:", error.message);
    console.log("继续执行其他逻辑...");
  }

  // finally块的模拟（使用try-catch-finally）
  try {
    await delay(300);
    console.log("✅ 操作成功");
  } catch (error) {
    console.error("❌ 操作失败:", error.message);
  } finally {
    console.log("📌 无论成功还是失败，都会执行这里");
  }
}

// 并行执行 vs 串行执行
async function parallelVsSerial() {
  console.log("\n=== 并行 vs 串行演示 ===");

  // 串行执行（总时间约 1000+800+600 = 2400ms）
  console.log("串行执行开始...");
  const serialStart = Date.now();
  await delay(1000);
  await delay(800);
  await delay(600);
  const serialEnd = Date.now();
  console.log(`✅ 串行执行完成，耗时: ${serialEnd - serialStart}ms`);

  // 并行执行（总时间约 max(1000,800,600) = 1000ms）
  console.log("并行执行开始...");
  const parallelStart = Date.now();
  await Promise.all([
    delay(1000),
    delay(800),
    delay(600)
  ]);
  const parallelEnd = Date.now();
  console.log(`✅ 并行执行完成，耗时: ${parallelEnd - parallelStart}ms`);
}

// 调用所有示例
basicAsyncAwait()
  .then(result => console.log("最终结果:", result))
  .catch(error => console.error("顶层错误:", error.message));

errorHandlingExample();
parallelVsSerial();