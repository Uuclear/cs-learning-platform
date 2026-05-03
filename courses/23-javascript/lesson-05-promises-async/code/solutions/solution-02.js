// 挑战2解决方案：API请求重试机制
console.log("=== API请求重试机制解决方案 ===");

// 模拟可能失败的API调用
function mockApiCall(url, attempt) {
  console.log(`📡 尝试请求 ${url} (第${attempt}次尝试)`);

  return new Promise((resolve, reject) => {
    // 模拟网络延迟
    const delay = Math.random() * 1000 + 500;

    setTimeout(() => {
      // 前两次尝试有较高失败率，第三次成功率更高
      const shouldFail = attempt < 3 && Math.random() > 0.6;

      if (shouldFail) {
        reject(new Error(`API调用失败 (尝试${attempt}): 网络错误`));
      } else {
        resolve({
          url: url,
          data: `成功获取数据 (尝试${attempt})`,
          timestamp: Date.now()
        });
      }
    }, delay);
  });
}

// 带重试机制的API调用函数
async function fetchWithRetry(url, maxRetries = 3, baseDelay = 1000) {
  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await mockApiCall(url, attempt);
      console.log(`✅ 请求成功:`, result.data);
      return result;

    } catch (error) {
      lastError = error;
      console.error(`❌ 第${attempt}次尝试失败:`, error.message);

      // 如果不是最后一次尝试，等待后重试
      if (attempt < maxRetries) {
        // 使用指数退避策略：delay = baseDelay * 2^(attempt-1)
        const delay = baseDelay * Math.pow(2, attempt - 1);
        console.log(`⏳ 等待 ${delay}ms 后进行第${attempt + 1}次尝试...`);

        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  // 所有重试都失败了
  console.error(`🔥 所有 ${maxRetries} 次尝试都失败了`);
  throw lastError;
}

// 高级重试机制，支持自定义条件
async function advancedFetchWithRetry(url, options = {}) {
  const {
    maxRetries = 3,
    baseDelay = 1000,
    shouldRetry = (error, attempt) => attempt < maxRetries,
    onRetry = (error, attempt, delay) => {
      console.log(`🔄 重试 #${attempt}，延迟 ${delay}ms`);
    }
  } = options;

  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await mockApiCall(url, attempt);
      return result;
    } catch (error) {
      lastError = error;

      if (shouldRetry(error, attempt)) {
        const delay = baseDelay * Math.pow(2, attempt - 1);
        onRetry(error, attempt, delay);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        break;
      }
    }
  }

  throw lastError;
}

// 测试基本重试机制
console.log("=== 测试基本重试机制 ===");
fetchWithRetry("/api/data")
  .then(result => console.log("🎉 基本重试成功:", result.data))
  .catch(error => console.error("💥 基本重试最终失败:", error.message));

// 测试高级重试机制
console.log("\n=== 测试高级重试机制 ===");
advancedFetchWithRetry("/api/advanced-data", {
  maxRetries: 4,
  baseDelay: 500,
  shouldRetry: (error, attempt) => {
    // 只在特定错误类型时重试
    return attempt < 4 && error.message.includes("网络错误");
  },
  onRetry: (error, attempt, delay) => {
    console.log(`🎯 高级重试 #${attempt} - 错误: ${error.message}`);
  }
})
  .then(result => console.log("🎉 高级重试成功:", result.data))
  .catch(error => console.error("💥 高级重试最终失败:", error.message));