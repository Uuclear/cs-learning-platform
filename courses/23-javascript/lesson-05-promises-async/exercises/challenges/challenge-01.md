# 编程挑战 1：实现图片加载器

## 要求

创建一个函数 `loadImages(imageUrls)`，能够：

1. **并发加载**多张图片（使用Promise.all或Promise.allSettled）
2. **优雅处理错误**：如果某些图片加载失败，不应该影响其他图片的加载
3. **返回详细结果**：包含成功加载的图片和失败的图片信息
4. **使用Image对象**：通过创建`new Image()`来加载图片，并监听`onload`和`onerror`事件

## 具体实现要求

- 函数应该返回一个Promise，resolve时包含：
  - `successful`: 成功加载的图片数组（Image对象）
  - `failed`: 失败的图片信息数组，包含URL和错误信息
- 使用`Promise.allSettled()`而不是`Promise.all()`，以确保所有图片都尝试加载完成
- 每个图片的加载都应该包装在一个Promise中

## 测试用例

```javascript
const imageUrls = [
  'https://via.placeholder.com/150',
  'https://via.placeholder.com/200', 
  'https://invalid-url-example.com/image.jpg', // 这个应该失败
  'https://via.placeholder.com/100'
];

loadImages(imageUrls)
  .then(results => {
    console.log(`成功: ${results.successful.length} 张`);
    console.log(`失败: ${results.failed.length} 张`);
  });
```

## 提示

- 使用`new Image()`创建图片对象
- 设置`img.src = url`开始加载
- 监听`onload`事件表示成功，`onerror`事件表示失败
- 记得在Promise中正确调用`resolve`和`reject`

完成这个挑战后，你将更好地理解如何在实际应用中处理异步资源加载！