// Promise.all并发控制和fetch API示例
console.log("=== Promise.all 并发控制演示 ===");

// 模拟fetch API的函数
async function mockFetch(url, delay = 1000, shouldFail = false) {
  console.log(`📡 发起请求: ${url}`);

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) {
        reject(new Error(`网络错误: ${url}`));
      } else {
        const mockData = {
          url: url,
          data: `成功获取${url}的数据`,
          timestamp: new Date().toISOString()
        };
        resolve(mockData);
      }
    }, delay);
  });
}

// 使用Promise.all进行并发请求
async function concurrentRequests() {
  try {
    console.log("开始并发请求...");

    // 同时发起多个请求
    const results = await Promise.all([
      mockFetch("/api/users", 800),
      mockFetch("/api/posts", 1200),
      mockFetch("/api/comments", 600),
      mockFetch("/api/profile", 1000)
    ]);

    console.log("✅ 所有请求完成！");
    results.forEach((result, index) => {
      console.log(`  🔹 结果${index + 1}:`, result.data);
    });

    return results;
  } catch (error) {
    console.error("❌ 其中一个请求失败:", error.message);
    throw error;
  }
}

// 使用Promise.allSettled处理部分失败的情况
async function allSettledExample() {
  console.log("\n=== Promise.allSettled 演示 ===");

  const results = await Promise.allSettled([
    mockFetch("/api/good-endpoint", 500, false),
    mockFetch("/api/bad-endpoint", 700, true), // 这个会失败
    mockFetch("/api/another-good", 600, false)
  ]);

  console.log("✅ 所有请求都已完成（无论成功或失败）:");
  results.forEach((result, index) => {
    if (result.status === "fulfilled") {
      console.log(`  ✅ 请求${index + 1} 成功:`, result.value.data);
    } else {
      console.log(`  ❌ 请求${index + 1} 失败:`, result.reason.message);
    }
  });
}

// 实际的fetch API使用示例（注释版本，因为实际环境可能没有网络）
async function realFetchExample() {
  console.log("\n=== 实际fetch API使用模式 ===");
  console.log("以下是在真实环境中使用fetch的模式:");

  // 检查响应状态
  // const response = await fetch('/api/data');
  // if (!response.ok) {
  //   throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  // }
  // const data = await response.json();

  // 超时控制
  // const controller = new AbortController();
  // const timeoutId = setTimeout(() => controller.abort(), 5000);
  // try {
  //   const response = await fetch('/api/data', { signal: controller.signal });
  //   clearTimeout(timeoutId);
  //   const data = await response.json();
  // } catch (error) {
  //   if (error.name === 'AbortError') {
  //     console.error('请求超时');
  //   } else {
  //     console.error('请求失败:', error);
  //   }
  // }

  console.log("💡 提示: 在实际项目中，记得处理网络错误和超时情况！");
}

// 调用所有示例
concurrentRequests()
  .then(results => console.log("\n📌 并发请求示例完成"))
  .catch(error => console.error("并发请求顶层错误:", error));

allSettledExample()
  .then(() => console.log("\n📌 allSettled示例完成"));

realFetchExample();