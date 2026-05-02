# 挑战2: 实现一个简易任务调度器

## 难度
⭐⭐⭐⭐

## 描述
实现一个简易的任务调度器，模拟操作系统中的时间片轮转调度（Round Robin）。

多个任务在队列中等待执行，每个任务分配一个时间片（如3秒）。如果任务在时间片内没完成，就回到队列尾部等待下一次调度。如果完成了，就记录完成时间。

## 输入
- `tasks`: 任务列表，每个任务包含 `{"name": 任务名, "duration": 需要的时间}`
- `time_slice`: 每个任务的时间片大小

## 输出
- 打印每个时间片的调度情况
- 返回所有任务的完成顺序

## 示例

**示例 1:**
```
输入: tasks=[
    {"name": "A", "duration": 6},
    {"name": "B", "duration": 3},
    {"name": "C", "duration": 8}
], time_slice=3

输出:
时间片 1: 执行 A (剩余 3) → A回到队尾
时间片 2: 执行 B (完成!) → B完成
时间片 3: 执行 C (剩余 5) → C回到队尾
时间片 4: 执行 A (剩余 0) → A完成
时间片 5: 执行 C (剩余 2) → C回到队尾
时间片 6: 执行 C (完成!) → C完成
完成顺序: [B, A, C]
```

## 约束条件
- 1 <= 任务数 <= 20
- 1 <= 每个任务duration <= 20
- 1 <= time_slice <= 10

## 提示
- 用队列存储等待执行的任务
- 每次从队首取出一个任务执行
- 如果剩余时间 > time_slice，减去time_slice后放回队尾
- 如果剩余时间 <= time_slice，任务完成，不再放回

## 进阶思考
- 如果任务的优先级不同，应该如何修改调度策略？
- 这个调度器和优先队列调度有什么区别和优劣？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
用队列模拟时间片轮转：任务入队等待，队首任务获得时间片执行。如果没完成就回到队尾，完成了就记录。

### 代码
```python
from collections import deque


class TaskScheduler:
    """
    简易任务调度器 - 时间片轮转调度（Round Robin）
    """
    def __init__(self, time_slice=3):
        self.time_slice = time_slice
        self.queue = deque()       # 等待执行的任务队列
        self.completed = []        # 已完成的任务列表
        self.time_slot = 0         # 当前时间片计数

    def add_task(self, name, duration):
        """添加任务到队列"""
        task = {"name": name, "remaining": duration}
        self.queue.append(task)
        print(f"  添加任务: {name} (需要 {duration} 个时间单位)")

    def run(self):
        """执行调度"""
        print(f"\n=== 开始调度 (时间片={self.time_slice}) ===\n")

        while self.queue:
            self.time_slot += 1
            task = self.queue.popleft()

            name = task["name"]
            remaining = task["remaining"]

            if remaining <= self.time_slice:
                # 任务在时间片内可以完成
                self.completed.append(name)
                print(f"时间片 {self.time_slot}: 执行 {name} (剩余{remaining} ≤ 时间片{self.time_slice}) → {name}完成! ✓")
            else:
                # 任务未完成，回到队尾
                new_remaining = remaining - self.time_slice
                task["remaining"] = new_remaining
                self.queue.append(task)
                print(f"时间片 {self.time_slot}: 执行 {name} (剩余{new_remaining}) → {name}回到队尾")

        print(f"\n=== 调度完成 ===")
        print(f"完成顺序: {self.completed}")
        return self.completed


# 测试
if __name__ == "__main__":
    scheduler = TaskScheduler(time_slice=3)

    scheduler.add_task("A", 6)
    scheduler.add_task("B", 3)
    scheduler.add_task("C", 8)

    order = scheduler.run()

    print(f"\n总时间片数: {scheduler.time_slot}")
    print(f"完成任务数: {len(order)}")
```

### 复杂度分析
- 时间复杂度: O(总时间 / 时间片)，每个时间片处理一个任务
- 空间复杂度: O(n)，队列最多存储n个任务

</details>
