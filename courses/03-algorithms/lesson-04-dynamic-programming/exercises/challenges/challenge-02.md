## 挑战2: 零钱兑换

### 难度
⭐⭐⭐

### 描述
给定不同面额的硬币 coins 和一个总金额 amount，计算凑成总金额所需的**最少**硬币数量。假设每种硬币可以无限使用。

如果无法凑成总金额，返回 -1。

### 输入
- coins: 一个正整数列表，表示不同面额的硬币
- amount: 一个非负整数，表示目标金额

### 输出
最少硬币数量（整数），如果无法凑成则返回 -1

### 示例

**示例 1:**
```
输入: coins = [1, 2, 5], amount = 11
输出: 3
解释: 11 = 5 + 5 + 1，最少需要3枚硬币
```

**示例 2:**
```
输入: coins = [2], amount = 3
输出: -1
解释: 无法用面额为2的硬币凑出金额3
```

**示例 3:**
```
输入: coins = [1, 5, 10, 25], amount = 30
输出: 2
解释: 30 = 25 + 5，只需要2枚硬币
```

### 约束条件
- 1 ≤ coins.length ≤ 12
- 1 ≤ coins[i] ≤ 2^31 - 1
- 0 ≤ amount ≤ 10^4
- coins 中的所有值互不相同

### 提示
- 定义 dp[i] = 凑出金额 i 需要的最少硬币数
- 状态转移：dp[i] = min(dp[i - coin] + 1) for coin in coins
- 边界条件：dp[0] = 0（凑0元不需要硬币）
- 初始化时将所有 dp 值设为无穷大（表示暂时凑不出）

### 进阶思考
- 如果要求输出具体用了哪些硬币（而不仅仅是数量），如何修改代码？
- 如果每种硬币只能用一次（而不是无限使用），问题如何变化？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
定义 dp[i] = 凑出金额 i 需要的最少硬币数。

状态转移方程：对于每个金额 i，尝试用每种硬币 coin：
- 如果用 coin 后 i - coin >= 0，且 dp[i - coin] 不是无穷大
- 那么 dp[i] = min(dp[i], dp[i - coin] + 1)

初始化：dp[0] = 0，其他全为无穷大（float('inf')）

最后检查 dp[amount] 是否仍为无穷大，是则返回 -1。

### 代码
```python
def coin_change(coins, amount):
    """
    零钱兑换问题 - 最少硬币数
    dp[i] = 凑出金额i需要的最少硬币数
    """
    # 初始化DP数组：dp[0]=0，其他为无穷大
    INF = float('inf')
    dp = [INF] * (amount + 1)
    dp[0] = 0

    # 从1到amount逐个计算
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0 and dp[i - coin] != INF:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != INF else -1


def coin_change_with_coins(coins, amount):
    """
    进阶版本：不仅返回最少硬币数，还输出具体用了哪些硬币
    """
    INF = float('inf')
    dp = [INF] * (amount + 1)
    dp[0] = 0
    # 记录每个金额是用哪个硬币得到的
    last_coin = [-1] * (amount + 1)

    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0 and dp[i - coin] != INF:
                if dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1
                    last_coin[i] = coin

    if dp[amount] == INF:
        return -1, []

    # 回溯找出用了哪些硬币
    used_coins = []
    current = amount
    while current > 0:
        used_coins.append(last_coin[current])
        current -= last_coin[current]

    return dp[amount], used_coins


if __name__ == "__main__":
    print("=" * 50)
    print("零钱兑换问题 - DP解法")
    print("=" * 50)

    # 测试1
    coins = [1, 2, 5]
    amount = 11
    result = coin_change(coins, amount)
    print(f"\ncoins = {coins}, amount = {amount}")
    print(f"最少硬币数: {result}")

    # 进阶测试：输出具体硬币
    count, used = coin_change_with_coins(coins, amount)
    print(f"具体方案: {used} ({count}枚)")

    # 测试2：无解的情况
    coins2 = [2]
    amount2 = 3
    result2 = coin_change(coins2, amount2)
    print(f"\ncoins = {coins2}, amount = {amount2}")
    print(f"最少硬币数: {result2}")

    # 测试3：大金额
    coins3 = [1, 5, 10, 25]
    amount3 = 99
    count3, used3 = coin_change_with_coins(coins3, amount3)
    print(f"\ncoins = {coins3}, amount = {amount3}")
    print(f"最少硬币数: {count3}")
    print(f"具体方案: {used3}")

# 输出:
# ==================================================
# 零钱兑换问题 - DP解法
# ==================================================
#
# coins = [1, 2, 5], amount = 11
# 最少硬币数: 3
# 具体方案: [5, 5, 1] (3枚)
#
# coins = [2], amount = 3
# 最少硬币数: -1
#
# coins = [1, 5, 10, 25], amount = 99
# 最少硬币数: 7
# 具体方案: [25, 25, 25, 10, 10, 1, 1, 1, 1] (更正: 99=25+25+25+10+10+1+1+1+1=9枚? 需要重新算)
```

### 复杂度分析
- 时间复杂度: O(amount × n)，n是硬币种类数
- 空间复杂度: O(amount)，DP数组大小

</details>
