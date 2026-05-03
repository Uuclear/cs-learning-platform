#include <iostream>
#include <string>

// 基类：交通工具
class Vehicle {
protected:
    std::string brand;
    std::string model;
    int year;

public:
    Vehicle(const std::string& b, const std::string& m, int y)
        : brand(b), model(m), year(y) {}

    virtual ~Vehicle() = default;

    // 纯虚函数 - 必须在派生类中实现
    virtual void start() = 0;
    virtual void stop() = 0;
    virtual double getSpeed() const = 0;

    // 普通函数
    void displayInfo() const {
        std::cout << brand << " " << model << " (" << year << ")" << std::endl;
    }

    std::string getBrand() const { return brand; }
    std::string getModel() const { return model; }
    int getYear() const { return year; }
};

// 汽车类
class Car : public Vehicle {
private:
    int doors;
    double currentSpeed;

public:
    Car(const std::string& b, const std::string& m, int y, int d)
        : Vehicle(b, m, y), doors(d), currentSpeed(0.0) {}

    void start() override {
        std::cout << "Starting car engine..." << std::endl;
        currentSpeed = 0.0;
    }

    void stop() override {
        std::cout << "Stopping car..." << std::endl;
        currentSpeed = 0.0;
    }

    double getSpeed() const override {
        return currentSpeed;
    }

    void accelerate(double speed) {
        currentSpeed += speed;
        if (currentSpeed < 0) currentSpeed = 0;
    }

    int getDoors() const { return doors; }
};

// 自行车类
class Bicycle : public Vehicle {
private:
    bool hasGears;
    double currentSpeed;

public:
    Bicycle(const std::string& b, const std::string& m, int y, bool gears)
        : Vehicle(b, m, y), hasGears(gears), currentSpeed(0.0) {}

    void start() override {
        std::cout << "Starting to pedal the bicycle..." << std::endl;
        currentSpeed = 0.0;
    }

    void stop() override {
        std::cout << "Stopping bicycle by braking..." << std::endl;
        currentSpeed = 0.0;
    }

    double getSpeed() const override {
        return currentSpeed;
    }

    void pedal(double speed) {
        currentSpeed += speed;
        if (currentSpeed < 0) currentSpeed = 0;
    }

    bool getHasGears() const { return hasGears; }
};

// 飞机类
class Airplane : public Vehicle {
private:
    int maxAltitude;
    double currentSpeed;
    int currentAltitude;

public:
    Airplane(const std::string& b, const std::string& m, int y, int maxAlt)
        : Vehicle(b, m, y), maxAltitude(maxAlt), currentSpeed(0.0), currentAltitude(0) {}

    void start() override {
        std::cout << "Starting airplane engines and preparing for takeoff..." << std::endl;
        currentSpeed = 0.0;
        currentAltitude = 0;
    }

    void stop() override {
        std::cout << "Landing airplane and shutting down engines..." << std::endl;
        currentSpeed = 0.0;
        currentAltitude = 0;
    }

    double getSpeed() const override {
        return currentSpeed;
    }

    void takeOff() {
        if (currentSpeed > 200) {
            currentAltitude = 1000;
            std::cout << "Airplane is now airborne!" << std::endl;
        } else {
            std::cout << "Need more speed for takeoff!" << std::endl;
        }
    }

    void climb(int altitude) {
        if (currentAltitude + altitude <= maxAltitude) {
            currentAltitude += altitude;
        } else {
            currentAltitude = maxAltitude;
            std::cout << "Reached maximum altitude!" << std::endl;
        }
    }

    int getCurrentAltitude() const { return currentAltitude; }
    int getMaxAltitude() const { return maxAltitude; }
};

int main() {
    std::cout << "=== 交通工具继承体系解决方案 ===" << std::endl;

    // 创建不同类型的交通工具
    Car myCar("Toyota", "Camry", 2023, 4);
    Bicycle myBike("Trek", "FX2", 2022, true);
    Airplane myPlane("Boeing", "747", 2020, 40000);

    std::cout << "\n--- 汽车操作 ---" << std::endl;
    myCar.displayInfo();
    myCar.start();
    myCar.accelerate(60.0);
    std::cout << "Car speed: " << myCar.getSpeed() << " mph" << std::endl;
    myCar.stop();

    std::cout << "\n--- 自行车操作 ---" << std::endl;
    myBike.displayInfo();
    myBike.start();
    myBike.pedal(15.0);
    std::cout << "Bicycle speed: " << myBike.getSpeed() << " mph" << std::endl;
    myBike.stop();

    std::cout << "\n--- 飞机操作 ---" << std::endl;
    myPlane.displayInfo();
    myPlane.start();
    myPlane.accelerate(250.0); // 加速到起飞速度
    myPlane.takeOff();
    myPlane.climb(10000);
    std::cout << "Airplane altitude: " << myPlane.getCurrentAltitude() << " feet" << std::endl;
    std::cout << "Airplane speed: " << myPlane.getSpeed() << " mph" << std::endl;
    myPlane.stop();

    return 0;
}