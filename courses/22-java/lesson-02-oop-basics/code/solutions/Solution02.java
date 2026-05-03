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

// 新增鸟类 - 实现 Flyable 接口
interface Flyable {
    void fly();
}

class Bird extends Animal implements Flyable {
    private double wingspan;

    public Bird(String name, int age, double wingspan) {
        super(name, age);
        this.wingspan = wingspan;
    }

    @Override
    public void makeSound() {
        System.out.println(name + " chirps melodiously!");
    }

    @Override
    public void fly() {
        System.out.println(name + " soars through the sky with " + wingspan + "m wingspan");
    }
}

// 新增鱼类 - 实现 Swimmable 接口
interface Swimmable {
    void swim();
}

class Fish extends Animal implements Swimmable {
    private String habitat;

    public Fish(String name, int age, String habitat) {
        super(name, age);
        this.habitat = habitat;
    }

    @Override
    public void makeSound() {
        System.out.println(name + " makes bubbling sounds");
    }

    @Override
    public void swim() {
        System.out.println(name + " swims gracefully in " + habitat);
    }
}

// 动物园管理系统
class Zoo {
    private java.util.List<Animal> animals;

    public Zoo() {
        this.animals = new java.util.ArrayList<>();
    }

    public void addAnimal(Animal animal) {
        animals.add(animal);
    }

    public void feedAllAnimals() {
        for (Animal animal : animals) {
            animal.makeSound();
            System.out.println("Feeding " + animal.name);
        }
    }

    public void demonstrateAbilities() {
        for (Animal animal : animals) {
            if (animal instanceof Flyable) {
                ((Flyable) animal).fly();
            }
            if (animal instanceof Swimmable) {
                ((Swimmable) animal).swim();
            }
        }
    }
}