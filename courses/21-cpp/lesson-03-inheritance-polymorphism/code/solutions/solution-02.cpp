#include <iostream>
#include <vector>
#include <memory>
#include <cstdlib>
#include <ctime>

// 角色基类
class Character {
protected:
    std::string name;
    int health;
    int maxHealth;
    int attackPower;

public:
    Character(const std::string& n, int hp, int ap)
        : name(n), health(hp), maxHealth(hp), attackPower(ap) {}

    virtual ~Character() = default;

    // 纯虚函数
    virtual void attack(Character& target) = 0;
    virtual void defend() = 0;
    virtual std::string getRole() const = 0;

    // 普通函数
    bool isAlive() const { return health > 0; }
    int getHealth() const { return health; }
    int getMaxHealth() const { return maxHealth; }
    std::string getName() const { return name; }

    void takeDamage(int damage) {
        health -= damage;
        if (health < 0) health = 0;
        std::cout << name << " takes " << damage << " damage! Health: " << health << "/" << maxHealth << std::endl;
    }

    void heal(int amount) {
        health += amount;
        if (health > maxHealth) health = maxHealth;
        std::cout << name << " heals for " << amount << " HP! Health: " << health << "/" << maxHealth << std::endl;
    }
};

// 战士类
class Warrior : public Character {
private:
    int defense;

public:
    Warrior(const std::string& n)
        : Character(n, 120, 25), defense(10) {}

    void attack(Character& target) override {
        int damage = attackPower + (rand() % 10); // 随机伤害
        std::cout << name << " swings mighty sword at " << target.getName() << " for " << damage << " damage!" << std::endl;
        target.takeDamage(damage);
    }

    void defend() override {
        std::cout << name << " raises shield and gains extra defense!" << std::endl;
        // 在实际游戏中，这里可能会增加防御力或减少受到的伤害
    }

    std::string getRole() const override {
        return "Warrior";
    }

    int getDefense() const { return defense; }
};

// 法师类
class Mage : public Character {
private:
    int mana;
    int maxMana;

public:
    Mage(const std::string& n)
        : Character(n, 80, 35), mana(100), maxMana(100) {}

    void attack(Character& target) override {
        if (mana >= 20) {
            int damage = attackPower + (rand() % 15); // 法术伤害更高
            mana -= 20;
            std::cout << name << " casts fireball at " << target.getName() << " for " << damage << " magical damage!" << std::endl;
            target.takeDamage(damage);
        } else {
            std::cout << name << " is out of mana! Cannot cast spell." << std::endl;
        }
    }

    void defend() override {
        std::cout << name << " creates a magical shield!" << std::endl;
        // 回复一些法力值
        mana += 10;
        if (mana > maxMana) mana = maxMana;
        std::cout << name << " mana restored to " << mana << "/" << maxMana << std::endl;
    }

    std::string getRole() const override {
        return "Mage";
    }

    int getMana() const { return mana; }
    int getMaxMana() const { return maxMana; }
};

// 弓箭手类
class Archer : public Character {
private:
    int accuracy;

public:
    Archer(const std::string& n)
        : Character(n, 90, 30), accuracy(85) {} // 85% 命中率

    void attack(Character& target) override {
        int roll = rand() % 100;
        if (roll < accuracy) {
            int damage = attackPower + (rand() % 12);
            std::cout << name << " shoots arrow at " << target.getName() << " for " << damage << " damage!" << std::endl;
            target.takeDamage(damage);
        } else {
            std::cout << name << "'s arrow misses " << target.getName() << "!" << std::endl;
        }
    }

    void defend() override {
        std::cout << name << " takes cover behind nearby obstacle!" << std::endl;
        // 弓箭手的防御可能包括增加闪避率
        accuracy += 5; // 临时提高命中率作为补偿
        if (accuracy > 95) accuracy = 95; // 最大命中率限制
        std::cout << name << " accuracy increased to " << accuracy << "%" << std::endl;
    }

    std::string getRole() const override {
        return "Archer";
    }

    int getAccuracy() const { return accuracy; }
};

// 战斗函数
void battle(Character& attacker, Character& defender) {
    if (attacker.isAlive() && defender.isAlive()) {
        std::cout << "\n--- Battle Round ---" << std::endl;
        attacker.attack(defender);
    }
}

// 显示角色状态
void displayStatus(const Character& character) {
    std::cout << character.getName() << " (" << character.getRole() << ") - "
              << "HP: " << character.getHealth() << "/" << character.getMaxHealth();

    // 如果是法师，显示法力值
    const Mage* mage = dynamic_cast<const Mage*>(&character);
    if (mage) {
        std::cout << ", Mana: " << mage->getMana() << "/" << mage->getMaxMana();
    }
    std::cout << std::endl;
}

int main() {
    srand(static_cast<unsigned int>(time(nullptr)));

    std::cout << "=== 游戏角色系统解决方案 ===" << std::endl;

    // 创建不同角色
    Warrior warrior("Conan");
    Mage mage("Gandalf");
    Archer archer("Legolas");

    std::cout << "\n--- 角色初始状态 ---" << std::endl;
    displayStatus(warrior);
    displayStatus(mage);
    displayStatus(archer);

    // 创建敌人
    Warrior enemy("Orc Warrior", 100, 20);

    std::cout << "\n--- 战斗演示 ---" << std::endl;
    displayStatus(enemy);

    // 战士攻击敌人
    battle(warrior, enemy);
    if (enemy.isAlive()) {
        // 敌人反击
        enemy.attack(warrior);
    }

    std::cout << "\n--- 法师战斗演示 ---" << std::endl;
    Mage enemyMage("Dark Sorcerer", 70, 30);
    displayStatus(enemyMage);

    // 法师对战
    battle(mage, enemyMage);
    if (enemyMage.isAlive()) {
        enemyMage.attack(mage);
    }

    std::cout << "\n--- 弓箭手战斗演示 ---" << std::endl;
    Archer enemyArcher("Enemy Archer", 85, 28);
    displayStatus(enemyArcher);

    // 弓箭手对战（多轮）
    for (int round = 1; round <= 3 && archer.isAlive() && enemyArcher.isAlive(); ++round) {
        std::cout << "\nRound " << round << ":" << std::endl;
        battle(archer, enemyArcher);
        if (enemyArcher.isAlive()) {
            battle(enemyArcher, archer);
        }
    }

    std::cout << "\n--- 最终状态 ---" << std::endl;
    displayStatus(warrior);
    displayStatus(mage);
    displayStatus(archer);

    return 0;
}