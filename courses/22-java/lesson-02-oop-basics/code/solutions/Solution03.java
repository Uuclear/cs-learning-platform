// 定义 Drawable 接口
interface Drawable {
    void draw();
    double calculateArea();
}

// 圆形实现
class Circle implements Drawable {
    private double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public void draw() {
        System.out.println("Drawing a circle with radius " + radius);
    }

    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}

// 矩形实现
class Rectangle implements Drawable {
    private double width;
    private double height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public void draw() {
        System.out.println("Drawing a rectangle " + width + "x" + height);
    }

    @Override
    public double calculateArea() {
        return width * height;
    }
}

// 三角形实现
class Triangle implements Drawable {
    private double base;
    private double height;

    public Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }

    @Override
    public void draw() {
        System.out.println("Drawing a triangle with base " + base + " and height " + height);
    }

    @Override
    public double calculateArea() {
        return 0.5 * base * height;
    }
}

// 新增椭圆实现
class Ellipse implements Drawable {
    private double majorAxis;
    private double minorAxis;

    public Ellipse(double majorAxis, double minorAxis) {
        this.majorAxis = majorAxis;
        this.minorAxis = minorAxis;
    }

    @Override
    public void draw() {
        System.out.println("Drawing an ellipse with major axis " + majorAxis + " and minor axis " + minorAxis);
    }

    @Override
    public double calculateArea() {
        return Math.PI * majorAxis * minorAxis;
    }
}

// 实现 Comparable 接口按面积排序
class ComparableCircle extends Circle implements Comparable<ComparableCircle> {
    public ComparableCircle(double radius) {
        super(radius);
    }

    @Override
    public int compareTo(ComparableCircle other) {
        return Double.compare(this.calculateArea(), other.calculateArea());
    }
}

// 画布类管理多个图形
class Canvas {
    private java.util.List<Drawable> shapes;

    public Canvas() {
        this.shapes = new java.util.ArrayList<>();
    }

    public void addShape(Drawable shape) {
        shapes.add(shape);
    }

    public void drawAll() {
        for (Drawable shape : shapes) {
            shape.draw();
        }
    }

    public double getTotalArea() {
        return shapes.stream().mapToDouble(Drawable::calculateArea).sum();
    }

    public void sortShapesByArea() {
        // 创建可比较的包装器来排序
        java.util.List<java.util.Map.Entry<Drawable, Double>> shapeAreas = new java.util.ArrayList<>();
        for (Drawable shape : shapes) {
            shapeAreas.add(new java.util.AbstractMap.SimpleEntry<>(shape, shape.calculateArea()));
        }

        shapeAreas.sort(java.util.Map.Entry.comparingByValue());

        // 重新构建列表
        shapes.clear();
        for (java.util.Map.Entry<Drawable, Double> entry : shapeAreas) {
            shapes.add(entry.getKey());
        }
    }
}