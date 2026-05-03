# 挑战 1：构建一个简单的游戏角色系统

## 目标
使用结构体和枚举创建一个简单的 RPG（角色扮演游戏）角色系统。

## 要求

### 1. 定义角色类别的枚举
创建一个 `CharacterClass` 枚举，包含以下变体：
- `Warrior`（战士）
- `Mage`（法师） 
- `Rogue`（盗贼）
- `Archer`（弓箭手）

### 2. 定义角色状态的枚举
创建一个 `CharacterStatus` 枚举，包含以下变体：
- `Alive { health: u32, max_health: u32 }`
- `Dead`
- `Poisoned { health: u32, max_health: u32, poison_damage: u32 }`

### 3. 定义角色结构体
创建一个 `Character` 结构体，包含以下字段：
- `name: String`
- `class: CharacterClass`
- `level: u32`
- `status: CharacterStatus`
- `experience: u32`

### 4. 实现方法
为 `Character` 结构体实现以下方法：

- `new(name: String, class: CharacterClass) -> Character`：构造函数
- `take_damage(&mut self, damage: u32)`：处理伤害
- `heal(&mut self, amount: u32)`：恢复生命值
- `gain_experience(&mut self, exp: u32)`：获得经验值（每100点经验升一级）
- `get_info(&self) -> String`：返回角色信息字符串

### 5. 额外挑战
- 实现一个 `attack` 方法，根据角色类别造成不同类型的伤害
- 使用 `Option` 来处理角色死亡后的无效操作

## 提示
- 使用 match 表达式来处理不同的枚举变体
- 注意在处理 `Dead` 状态时的安全性
- 考虑生命值不能超过最大生命值的限制