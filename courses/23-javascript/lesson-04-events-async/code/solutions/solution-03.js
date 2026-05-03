/**
 * 解决方案3：回调函数与回调地狱的完整解决方案
 *
 * 这是示例3的完整解决方案，展示了如何正确处理回调并提供改进思路
 */

console.log('=== 解决方案3：回调函数与回调地狱 ===');

// 1. 正确的回调函数模式
console.log('\n1️⃣ 正确的回调函数模式（错误优先）：');

function fetchDataWithErrorFirst(url, callback) {
  console.log(`🔍 开始获取: ${url}`);

  // 模拟网络请求
  setTimeout(() => {
    const success = Math.random() > 0.2; // 80%成功率

    if (success) {
      callback(null, { data: `来自${url}的数据`, status: 200 });
    } else {
      callback(new Error(`请求失败: ${url}`), null);
    }
  }, 300);
}

// 使用正确的错误处理
fetchDataWithErrorFirst('https://api.example.com/users', (error, result) => {
  if (error) {
    console.error('❌ 获取用户失败:', error.message);
    return;
  }
  console.log('✅ 获取用户成功:', result.data);
});

// 2. 回调地狱的结构化解决方案
console.log('\n2️⃣ 回调地狱的结构化处理：');

// 将每个异步操作封装为独立函数
function getUserAsync(id, callback) {
  console.log(`👤 获取用户: ${id}`);
  setTimeout(() => {
    callback(null, { id, name: '李四', email: 'lisi@example.com' });
  }, 200);
}

function getUserPostsAsync(userId, callback) {
  console.log(`📝 获取用户文章: ${userId}`);
  setTimeout(() => {
    callback(null, [
      { id: 101, title: 'JavaScript事件循环', authorId: userId },
      { id: 102, title: '异步编程最佳实践', authorId: userId }
    ]);
  }, 200);
}

function getPostCommentsAsync(postId, callback) {
  console.log(`💬 获取文章评论: ${postId}`);
  setTimeout(() => {
    callback(null, [
      { id: 201, content: '深入浅出，很好理解！', postId: postId },
      { id: 202, content: '期待更多相关内容', postId: postId },
      { id: 203, content: '实际项目中很有用', postId: postId }
    ]);
  }, 200);
}

// 使用命名函数减少嵌套深度
function handleComments(error, comments) {
  if (error) {
    console.error('❌ 获取评论失败:', error.message);
    return;
  }

  console.log('✅ 最终结果:');
  console.log(`   评论数量: ${comments.length}`);
  console.log(`   第一条评论: "${comments[0].content}"`);
}

function handlePosts(error, posts) {
  if (error) {
    console.error('❌ 获取文章失败:', error.message);
    return;
  }

  console.log(`✅ 获取到 ${posts.length} 篇文章`);
  getPostCommentsAsync(posts[0].id, handleComments);
}

function handleUser(error, user) {
  if (error) {
    console.error('❌ 获取用户失败:', error.message);
    return;
  }

  console.log(`✅ 用户: ${user.name} (${user.email})`);
  getUserPostsAsync(user.id, handlePosts);
}

// 启动链式调用
getUserAsync(456, handleUser);

// 3. 错误处理的最佳实践
console.log('\n3️⃣ 错误处理最佳实践：');

function safeAsyncOperation(name, shouldFail, callback) {
  // 立即验证参数
  if (typeof callback !== 'function') {
    throw new TypeError('回调必须是函数');
  }

  console.log(`⚙️  开始安全操作: ${name}`);

  setTimeout(() => {
    try {
      if (shouldFail) {
        // 创建有意义的错误对象
        const error = new Error(`操作失败: ${name}`);
        error.operation = name;
        error.timestamp = Date.now();
        callback(error);
      } else {
        callback(null, `${name}执行成功`);
      }
    } catch (unexpectedError) {
      // 捕获意外错误
      callback(unexpectedError);
    }
  }, 100);
}

// 使用示例
safeAsyncOperation('数据库连接', false, (error, result) => {
  if (error) {
    console.error('❌ 数据库连接失败:', error.message);
    // 可以在这里添加重试逻辑或降级处理
  } else {
    console.log('✅', result);
  }
});

// 4. 向Promise过渡的桥梁函数
console.log('\n4️⃣ 向现代异步模式过渡：');

// 将回调函数转换为Promise的通用函数
function promisify(callbackBasedFunction) {
  return function(...args) {
    return new Promise((resolve, reject) => {
      callbackBasedFunction(...args, (error, result) => {
        if (error) {
          reject(error);
        } else {
          resolve(result);
        }
      });
    });
  };
}

// 使用promisify转换现有函数
const getUserPromise = promisify(getUserAsync);
const getPostsPromise = promisify(getUserPostsAsync);

// 现在可以这样使用（虽然本课程不深入Promise，但这是发展方向）
getUserPromise(789)
  .then(user => {
    console.log('🔄 Promise方式获取用户:', user.name);
    return getPostsPromise(user.id);
  })
  .then(posts => {
    console.log('🔄 Promise方式获取文章数量:', posts.length);
  })
  .catch(error => {
    console.error('🔄 Promise错误处理:', error.message);
  });

console.log('\n💡 回调函数关键要点：');
console.log('- 始终使用错误优先回调模式');
console.log('- 尽量减少嵌套深度');
console.log('- 提供有意义的错误信息');
console.log('- 考虑向Promise/async-await迁移');

console.log('\n=== 解决方案3结束 ===');
console.log('记住：回调是JavaScript异步编程的基础，但现代开发更推荐Promise和async/await！');