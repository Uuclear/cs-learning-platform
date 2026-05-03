// 挑战1解决方案：图片加载器
console.log("=== 图片加载器解决方案 ===");

// 创建一个Promise来加载单张图片
function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(`无法加载图片: ${src}`));
    img.src = src;
  });
}

// 加载多张图片的函数
async function loadImages(imageUrls) {
  try {
    console.log(`开始加载 ${imageUrls.length} 张图片...`);

    // 使用Promise.all并发加载所有图片
    const images = await Promise.allSettled(
      imageUrls.map(url => loadImage(url))
    );

    // 分离成功和失败的结果
    const successfulImages = [];
    const failedImages = [];

    images.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        successfulImages.push(result.value);
        console.log(`✅ 图片 ${index + 1} 加载成功`);
      } else {
        failedImages.push({
          url: imageUrls[index],
          error: result.reason.message
        });
        console.log(`❌ 图片 ${index + 1} 加载失败:`, result.reason.message);
      }
    });

    console.log(`📊 总结: ${successfulImages.length} 张成功, ${failedImages.length} 张失败`);

    return {
      successful: successfulImages,
      failed: failedImages
    };

  } catch (error) {
    console.error("加载图片过程中发生意外错误:", error);
    throw error;
  }
}

// 使用示例（使用一些有效的图片URL进行测试）
const testImageUrls = [
  'https://via.placeholder.com/150',
  'https://via.placeholder.com/200',
  'https://invalid-url-that-will-fail.com/image.jpg', // 这个会失败
  'https://via.placeholder.com/100'
];

loadImages(testImageUrls)
  .then(results => {
    console.log("🎉 图片加载完成！");
    console.log(`成功加载: ${results.successful.length} 张`);
    console.log(`加载失败: ${results.failed.length} 张`);
  })
  .catch(error => {
    console.error("顶层错误:", error);
  });