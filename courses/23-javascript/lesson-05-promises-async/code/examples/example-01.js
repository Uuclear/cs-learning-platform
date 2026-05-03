// Promise基础与链式调用示例
console.log("=== Promise基础演示 ===");

// 模拟网络请求的函数
function fetchData(url, delay = 1000) {
  return new Promise((resolve, reject) => {
    console.log(`开始请求: ${url}`);
    setTimeout(() => {
      const success = Math.random() > 0.3; // 70%成功率
      if (success) {
        resolve({ url, data: `来自${url}的数据`, timestamp: Date.now() });
      } else {
        reject(new Error(`请求失败: ${url}`));
      }
    }, delay);
  });
}

// 基本使用 - 链式调用
fetchData("/api/users")
  .then(response => {
    console.log("✅ 用户数据:", response.data);
    return fetchData("/api/posts", 800); // 链式调用下一个请求
  })
  .then(response => {
    console.log("✅ 文章数据:", response.data);
    return fetchData("/api/comments", 600);
  })
  .then(response => {
    console.log("✅ 评论数据:", response.data);
    console.log("🎉 所有数据获取完成！");
  })
  .catch(error => {
    console.error("❌ 请求链中出现错误:", error.message);
  });

// 并发请求示例 - Promise.all
console.log("\n=== 并发请求演示 (Promise.all) ===");
Promise.all([
  fetchData("/api/users", 500),
  fetchData("/api/posts", 700),
  fetchData("/api/comments", 600)
])
  .then(results => {
    console.log("✅ 所有并发请求完成:");
    results.forEach((result, index) => {
      console.log(`  🔹 请求${index + 1}:`, result.data);
    });
  })
  .catch(error => {
    console.error("❌ 并发请求中有一个失败:", error.message);
  });

// Promise.race 示例 - 超时控制
console.log("\n=== Promise.race 演示 (超时控制) ===");
const timeoutPromise = new Promise((_, reject) => {
  setTimeout(() => reject(new Error("请求超时！")), 1200);
});

Promise.race([
  fetchData("/api/timeout-test", 1500), // 这个会超时
  timeoutPromise
])
  .then(result => {
    console.log("✅ 请求成功:", result.data);
  })
  .catch(error => {
    console.error("❌ 超时或请求失败:", error.message);
  });