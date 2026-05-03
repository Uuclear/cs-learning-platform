# 编程挑战 1：动态图片画廊

## 任务描述
创建一个动态图片画廊，包含以下功能：

1. 显示一张主图片和多个缩略图
2. 点击任意缩略图时，主图片切换为对应的完整图片
3. 当前选中的缩略图应该有特殊的高亮样式
4. 支持动态添加新的图片到画廊中

## 具体要求

### HTML结构
- 主容器：`<div class="gallery">`
- 主图片显示区域：`<div class="main-image"><img id="main-img" src="" alt=""></div>`
- 缩略图容器：`<div class="thumbnails"></div>`
- 添加按钮：`<button id="add-image-btn">添加图片</button>`

### 功能实现
1. **初始化画廊**：使用JavaScript动态创建上述HTML结构
2. **图片数据**：使用以下图片数组作为初始数据：
   ```javascript
   const images = [
     { thumb: 'thumb1.jpg', full: 'full1.jpg', alt: '风景1' },
     { thumb: 'thumb2.jpg', full: 'full2.jpg', alt: '风景2' },
     { thumb: 'thumb3.jpg', full: 'full3.jpg', alt: '风景3' }
   ];
   ```
3. **缩略图点击事件**：点击缩略图时更新主图片的 `src` 和 `alt` 属性，并给当前缩略图添加 `active` 类
4. **添加图片功能**：点击"添加图片"按钮时，弹出对话框让用户输入新图片信息，然后动态添加到画廊中

### 样式要求
- 主图片：宽度 400px，高度自适应
- 缩略图：宽度 80px，高度 60px，边框 2px solid #ccc
- 激活的缩略图：边框颜色变为 #007bff
- 缩略图容器：flex布局，横向排列

## 完整解决方案

```javascript
// 图片画廊完整实现
class ImageGallery {
  constructor(containerId, initialImages = []) {
    this.container = document.getElementById(containerId);
    this.images = initialImages;
    this.currentIndex = 0;
    
    if (this.container) {
      this.init();
    }
  }

  // 初始化画廊结构
  init() {
    // 创建主图片区域
    const mainImageDiv = document.createElement('div');
    mainImageDiv.className = 'main-image';
    
    const mainImg = document.createElement('img');
    mainImg.id = 'main-img';
    mainImg.alt = '';
    mainImageDiv.appendChild(mainImg);

    // 创建缩略图容器
    const thumbnailsDiv = document.createElement('div');
    thumbnailsDiv.className = 'thumbnails';
    thumbnailsDiv.id = 'thumbnails-container';

    // 创建添加按钮
    const addButton = document.createElement('button');
    addButton.id = 'add-image-btn';
    addButton.textContent = '添加图片';

    // 组装结构
    this.container.appendChild(mainImageDiv);
    this.container.appendChild(thumbnailsDiv);
    this.container.appendChild(addButton);

    // 应用基础样式
    this.applyBaseStyles();

    // 加载初始图片
    this.loadImages();

    // 绑定事件
    this.bindEvents();
  }

  // 应用基础CSS样式
  applyBaseStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .main-image img {
        width: 400px;
        height: auto;
        border: 1px solid #ddd;
      }
      .thumbnails {
        display: flex;
        gap: 10px;
        margin: 10px 0;
        flex-wrap: wrap;
      }
      .thumbnail {
        width: 80px;
        height: 60px;
        object-fit: cover;
        border: 2px solid #ccc;
        cursor: pointer;
        transition: border-color 0.2s;
      }
      .thumbnail.active {
        border-color: #007bff;
      }
      #add-image-btn {
        margin-top: 10px;
        padding: 8px 16px;
        background-color: #28a745;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }
      #add-image-btn:hover {
        background-color: #218838;
      }
    `;
    document.head.appendChild(style);
  }

  // 加载并显示图片
  loadImages() {
    const thumbnailsContainer = document.getElementById('thumbnails-container');
    const mainImg = document.getElementById('main-img');

    // 清空现有缩略图（使用安全的方法）
    while (thumbnailsContainer.firstChild) {
      thumbnailsContainer.removeChild(thumbnailsContainer.firstChild);
    }

    this.images.forEach((image, index) => {
      const thumbImg = document.createElement('img');
      thumbImg.src = image.thumb;
      thumbImg.alt = image.alt;
      thumbImg.className = 'thumbnail';
      thumbImg.dataset.index = index;

      if (index === this.currentIndex) {
        thumbImg.classList.add('active');
        mainImg.src = image.full;
        mainImg.alt = image.alt;
      }

      thumbImg.addEventListener('click', () => this.selectImage(index));
      thumbnailsContainer.appendChild(thumbImg);
    });
  }

  // 选择图片
  selectImage(index) {
    if (index < 0 || index >= this.images.length) return;

    this.currentIndex = index;
    
    // 更新主图片
    const mainImg = document.getElementById('main-img');
    mainImg.src = this.images[index].full;
    mainImg.alt = this.images[index].alt;

    // 更新缩略图激活状态
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach((thumb, i) => {
      if (i === index) {
        thumb.classList.add('active');
      } else {
        thumb.classList.remove('active');
      }
    });
  }

  // 添加新图片
  addImage() {
    const url = prompt('请输入完整图片URL:');
    const thumbUrl = prompt('请输入缩略图URL:');
    const altText = prompt('请输入图片描述:', '新图片');

    if (url && thumbUrl) {
      this.images.push({
        full: url,
        thumb: thumbUrl,
        alt: altText
      });
      this.loadImages();
    }
  }

  // 绑定事件
  bindEvents() {
    const addButton = document.getElementById('add-image-btn');
    addButton.addEventListener('click', () => this.addImage());
  }
}

// 使用示例
const initialImages = [
  { 
    thumb: 'https://via.placeholder.com/80x60/4CAF50/white?text=Thumb1', 
    full: 'https://via.placeholder.com/400x300/4CAF50/white?text=Full1', 
    alt: '风景1' 
  },
  { 
    thumb: 'https://via.placeholder.com/80x60/2196F3/white?text=Thumb2', 
    full: 'https://via.placeholder.com/400x300/2196F3/white?text=Full2', 
    alt: '风景2' 
  },
  { 
    thumb: 'https://via.placeholder.com/80x60/FF9800/white?text=Thumb3', 
    full: 'https://via.placeholder.com/400x300/FF9800/white?text=Full3', 
    alt: '风景3' 
  }
];

// 创建画廊（需要在HTML中有 <div id="gallery-container"></div>）
// const gallery = new ImageGallery('gallery-container', initialImages);
```

## 测试说明
1. 在HTML文件中创建一个 `<div id="gallery-container"></div>`
2. 引入上述JavaScript代码
3. 调用 `new ImageGallery('gallery-container', initialImages)`
4. 验证所有功能是否正常工作

## 扩展思考
- 如何添加图片删除功能？
- 如何支持键盘导航（左右箭头切换图片）？
- 如何实现图片预加载以提高用户体验？