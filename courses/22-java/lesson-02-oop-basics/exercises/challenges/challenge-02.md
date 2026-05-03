# 挑战 2：几何图形计算器增强版

## 背景
基于课程中的 `Drawable` 接口示例，创建一个功能更强大的几何图形计算器。

## 需求
1. 扩展 `Drawable` 接口，添加以下方法：
   - `double calculatePerimeter()`：计算周长
   - `boolean containsPoint(double x, double y)`：检查是否包含某点

2. 实现更多图形类：
   - `Square`（正方形）：继承自 `Rectangle`
   - `RegularPolygon`（正多边形）：接受边数和边长参数
   - `Ellipse`（椭圆）：接受长轴和短轴参数

3. 创建 `ShapeComparator` 类，实现以下排序功能：
   - 按面积升序/降序排序
   - 按周长排序
   - 按类型分组

4. 实现 `SerializableShape` 接口，允许将图形对象序列化到文件：
   ```java
   interface SerializableShape {
       void saveToFile(String filename);
       static Drawable loadFromFile(String filename);
   }
   ```

5. **高级挑战**：创建 `CompositeShape` 类，可以包含多个子图形，整体作为一个图形处理

## 设计要求
- 使用组合优于继承的原则
- 所有图形类必须正确实现 `Drawable` 接口的所有方法
- 考虑浮点数精度问题（使用适当的比较方法）
- 提供完整的异常处理和输入验证

## 测试用例
创建一个测试类，验证以下场景：
- 不同图形的面积和周长计算是否正确
- 排序功能是否按预期工作
- 序列化和反序列化是否保持数据完整性
- 复合图形的总面积是否等于各子图形面积之和