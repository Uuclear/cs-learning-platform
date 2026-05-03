/**
 * 示例3：回调函数与回调地狱示例
 *
 * 这个例子演示了：
 * 1. 基本回调函数的使用
 * 2. 回调地狱（Callback Hell）的问题
 * 3. 错误处理在回调中的复杂性
 * 4. 简单的解决方案思路
 */

console.log('=== 示例3：回调函数与回调地狱 ===');

// 1. 基本回调函数示例
console.log('\n1. 基本回调函数：');

function fetchData(url, callback) {
  console.log(`开始获取数据: ${url}`);

  // 模拟异步操作
  setTimeout(() => {
    const data = `来自${url}的数据`;
    callback(null, data); // 第一个参数是错误，第二个是数据
  }, 500);
}

fetchData('https://api.example.com/users', (error, data) => {
  if (error) {
    console.error('获取数据失败:', error);
  } else {
    console.log('获取数据成功:', data);
  }
});

// 2. 回调地狱示例
console.log('\n2. 回调地狱演示：');

function getUser(id, callback) {
  console.log(`获取用户ID: ${id}`);
  setTimeout(() => {
    callback(null, { id, name: '张三', email: 'zhangsan@example.com' });
  }, 200);
}

function getPosts(userId, callback) {
  console.log(`获取用户${userId}的文章`);
  setTimeout(() => {
    callback(null, [
      { id: 1, title: 'JavaScript基础', authorId: userId },
      { id: 2, title: '事件处理', authorId: userId }
    ]);
  }, 200);
}

function getComments(postId, callback) {
  console.log(`获取文章${postId}的评论`);
  setTimeout(() => {
    callback(null, [
      { id: 1, content: '很好的文章！', postId: postId },
      { id: 2, content: '学到了很多', postId: postId }
    ]);
  }, 200);
}

// 回调地狱 - 多层嵌套
getUser(123, (error, user) => {
  if (error) {
    console.error('获取用户失败:', error);
    return;
  }

  getPosts(user.id, (error, posts) => {
    if (error) {
      console.error('获取文章失败:', error);
      return;
    }

    getComments(posts[0].id, (error, comments) => {
      if (error) {
        console.error('获取评论失败:', error);
        return;
      }

      console.log('最终结果:');
      console.log('用户:', user.name);
      console.log('文章:', posts[0].title);
      console.log('评论数量:', comments.length);

      // 如果还需要更多异步操作，嵌套会更深...
    });
  });
});

// 3. 错误处理的复杂性
console.log('\n3. 错误处理复杂性：');

function asyncOperation(name, shouldFail, callback) {
  console.log(`开始操作: ${name}`);
  setTimeout(() => {
    if (shouldFail) {
      callback(new Error(`操作${name}失败`));
    } else {
      callback(null, `${name}成功`);
    }
  }, 100);
}

// 在回调链中，每个步骤都需要单独处理错误
asyncOperation('A', false, (error, resultA) => {
  if (error) {
    console.error('A失败:', error.message);
    return;
  }

  asyncOperation('B', true, (error, resultB) => { // B会失败
    if (error) {
      console.error('B失败:', error.message);
      return;
    }

    asyncOperation('C', false, (error, resultC) => {
      if (error) {
        console.error('C失败:', error.message);
        return;
      }

      console.log('所有操作成功:', resultA, resultB, resultC);
    });
  });
});

// 4. 简单的改进思路（为后续Promise做铺垫）
console.log('\n4. 改进思路提示：');

// 理想情况下，我们希望这样写代码：
// const user = await getUser(123);
// const posts = await getPosts(user.id);
// const comments = await getComments(posts[0].id);
// console.log('结果:', user, posts, comments);

// 这就是为什么我们需要Promise和async/await！

console.log('\n=== 示例3结束 ===');
console.log('注意：回调地狱是传统异步编程的主要痛点之一');
console.log('现代JavaScript提供了更好的解决方案！');