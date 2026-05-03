// 父类
abstract class Animal {
    protected String name;
    protected int age;

    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // 抽象方法，子类必须实现
    public abstract void makeSound();

    // 具体方法，子类可以继承或重写
    public void sleep() {
        System.out.println(name + " is sleeping");
    }

    public void introduce() {
        System.out.println("I'm " + name + ", " + age + " years old");
    }
}

// 子类1
class Dog extends Animal {
    public Dog(String name, int age) {
        super(name, age); // 调用父类构造方法
    }

    @Override
    public void makeSound() {
        System.out.println(name + " says: Woof! Woof!");
    }

    public void wagTail() {
        System.out.println(name + " is wagging tail");
    }
}

// 子类2
class Cat extends Animal {
    public Cat(String name, int age) {
        super(name, age);
    }

    @Override
    public void makeSound() {
        System.out.println(name + " says: Meow! Meow!");
    }

    public void purr() {
        System.out.println(name + " is purring");
    }
}