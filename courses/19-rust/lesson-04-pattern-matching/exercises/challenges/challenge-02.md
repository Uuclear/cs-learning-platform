# 挑战2：实现一个状态机驱动的游戏角色控制器

## 目标
使用模式匹配和状态机实现一个简单的游戏角色控制器。

## 要求
1. 定义游戏角色的状态枚举，至少包含以下状态：
   - Idle（空闲）
   - Walking { direction: Direction, speed: f32 }
   - Running { direction: Direction, stamina: f32 }
   - Jumping { height: f32, airborne_time: f32 }
   - Attacking { weapon: WeaponType, damage: i32 }
   - TakingDamage { health: i32, invulnerable: bool }
   - Dead

2. 定义相关的辅助枚举：
   ```rust
   enum Direction { North, South, East, West }
   enum WeaponType { Sword, Bow, Magic }
   ```

3. 实现状态转换函数：
   ```rust
   fn handle_input(current_state: PlayerState, input: PlayerInput) -> PlayerState;
   fn update_state(current_state: PlayerState, delta_time: f32) -> PlayerState;
   ```

4. 使用模式匹配处理所有状态转换逻辑，确保：
   - 在空中时不能开始行走或奔跑
   - 生命值为0时进入死亡状态
   - 攻击时有冷却时间
   - 体力耗尽时从奔跑切换到行走

## 输入类型定义
```rust
enum PlayerInput {
    Move(Direction),
    Run,
    Jump,
    Attack,
    TakeDamage(i32),
    None,
}
```

## 扩展挑战
- 添加动画状态字段到每个状态变体
- 实现状态进入和退出的回调函数
- 添加状态历史记录功能，支持撤销操作