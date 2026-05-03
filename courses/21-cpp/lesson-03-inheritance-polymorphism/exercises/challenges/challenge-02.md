# 挑战 2：实现一个图形绘制系统

## 背景
你需要为一个简单的绘图应用程序实现图形对象系统。系统需要支持多种基本形状，并能够统一处理它们。

## 任务要求

### 1. 设计抽象基类 `Drawable`
- 包含纯虚函数：
  - `draw()` - 绘制图形到控制台
  - `getArea()` - 计算并返回面积
  - `getPerimeter()` - 计算并返回周长
  - `moveTo(double x, double y)` - 移动图形到新位置
- 包含受保护的成员变量：
  - `x`, `y` (double) - 图形的位置坐标
  - `color` (std::string) - 图形的颜色

### 2. 实现具体的图形类

**Circle 类**
- 额外属性：`radius` (double)
- 面积公式：π × radius²
- 周长公式：2 × π × radius
- `draw()` 输出格式："Drawing [color] circle at ([x], [y]) with radius [radius]"

**Rectangle 类**
- 额外属性：`width`, `height` (double)
- 面积公式：width × height
- 周长公式：2 × (width + height)
- `draw()` 输出格式："Drawing [color] rectangle at ([x], [y]) with size [width]x[height]"

**Triangle 类**
- 额外属性：三个顶点坐标 `(x1,y1)`, `(x2,y2)`, `(x3,y3)`
- 使用海伦公式计算面积
- 周长是三边长度之和
- `draw()` 输出格式："Drawing [color] triangle with vertices at ([x1],[y1]), ([x2],[y2]), ([x3],[y3])"

### 3. 实现图形管理器
创建 `DrawingManager` 类：
- `std::vector<std::unique_ptr<Drawable>> shapes`
- `void addShape(std::unique_ptr<Drawable> shape)`
- `void renderAll()` - 绘制所有图形
- `double getTotalArea()` - 返回所有图形的总面积
- `void moveAll(double dx, double dy)` - 将所有图形移动指定的偏移量

### 4. 实现高级功能

**颜色过滤**
- 添加 `std::vector<Drawable*> getShapesByColor(const std::string& color)` 方法
- 返回指定颜色的所有图形指针

**面积排序**
- 添加 `void sortShapesByArea()` 方法
- 按面积从小到大对图形进行排序

### 5. 测试你的实现
在 `main()` 函数中：
- 创建各种图形对象（圆形、矩形、三角形）
- 设置不同的位置和颜色
- 将它们添加到图形管理器中
- 测试所有功能：渲染、计算总面积、移动、颜色过滤、排序
- 验证输出是否正确

## 额外挑战（可选）
- 添加更多图形类型（如椭圆、多边形）
- 实现图形的旋转功能
- 添加边界检测（检查图形是否在画布范围内）
- 实现图形的缩放功能

## 提交要求
- 所有代码放在一个 `.cpp` 文件中
- 使用 const 正确性（const 成员函数）
- 确保有 virtual 析构函数
- 使用智能指针管理内存
- 包含必要的数学计算（使用 `<cmath>`）
- 使用适当的错误处理