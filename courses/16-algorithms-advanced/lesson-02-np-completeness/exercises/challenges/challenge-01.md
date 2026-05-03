# 挑战1：3-SAT求解器实现 ⭐⭐

## 问题描述

实现一个完整的3-SAT求解器，能够处理任意规模的3-SAT实例，并输出可满足性结果和具体的赋值（如果可满足）。

你的求解器应该包含以下功能：
1. **输入解析**：支持DIMACS CNF格式的输入
2. **预处理**：实现简单的预处理优化（如纯文字消除、单元子句传播）
3. **搜索算法**：实现DPLL算法或CDCL算法的核心逻辑
4. **输出格式**：输出SAT/UNSAT，以及满足赋值（如果存在）

## 输入/输出规格

### 输入格式（DIMACS CNF）
```
p cnf <变量数> <子句数>
<子句1>
<子句2>
...
<子句n>
```

每个子句由空格分隔的整数表示，以0结尾。正数表示变量，负数表示否定。

### 输出格式
- 如果可满足：`SAT` 后跟满足赋值（变量编号和值）
- 如果不可满足：`UNSAT`

### 示例
**输入**：
```
p cnf 3 2
1 2 3 0
-1 -2 3 0
```

**输出**：
```
SAT
1 1
2 0  
3 1
```

## 约束条件

- 必须正确处理标准DIMACS CNF格式
- 预处理步骤必须包括单元子句传播
- 搜索算法必须是完备的（能正确判断所有实例）
- 对于小规模实例（≤20变量）应该在合理时间内完成
- 代码必须有详细的中文注释

## 提示

1. **单元子句传播**：如果存在只有一个文字的子句，该文字必须为真
2. **纯文字消除**：如果某个变量只以一种极性出现，可以安全地赋值
3. **DPLL算法**：递归地选择变量赋值，应用预处理，回溯
4. **数据结构**：考虑使用watched literals等高效数据结构

<details>
<summary>参考解决方案</summary>

```python
class SATSolver:
    """
    简化的3-SAT求解器，实现DPLL算法
    """
    
    def __init__(self):
        self.clauses = []
        self.assignment = {}
        self.variables = set()
    
    def parse_dimacs(self, lines):
        """解析DIMACS CNF格式"""
        clauses = []
        num_vars = 0
        num_clauses = 0
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('c'):
                continue
            if line.startswith('p'):
                parts = line.split()
                num_vars = int(parts[2])
                num_clauses = int(parts[3])
                continue
            
            # 解析子句
            literals = list(map(int, line.split()))
            if literals and literals[-1] == 0:
                literals = literals[:-1]
            if literals:
                clauses.append(literals)
                for lit in literals:
                    self.variables.add(abs(lit))
        
        self.clauses = clauses
        return num_vars, num_clauses
    
    def unit_propagation(self, clauses, assignment):
        """单元子句传播"""
        changed = True
        while changed:
            changed = False
            new_clauses = []
            
            for clause in clauses:
                # 检查子句状态
                satisfied = False
                unassigned_lits = []
                
                for lit in clause:
                    var = abs(lit)
                    if var in assignment:
                        val = assignment[var]
                        lit_val = not val if lit < 0 else val
                        if lit_val:
                            satisfied = True
                            break
                    else:
                        unassigned_lits.append(lit)
                
                if satisfied:
                    continue  # 子句已满足，跳过
                
                if not unassigned_lits:
                    return None, False  # 冲突
                
                if len(unassigned_lits) == 1:
                    # 单元子句
                    lit = unassigned_lits[0]
                    var = abs(lit)
                    val = lit > 0
                    assignment[var] = val
                    changed = True
                else:
                    new_clauses.append(clause)
            
            clauses = new_clauses
        
        return clauses, True
    
    def dpll(self, clauses, assignment):
        """DPLL递归算法"""
        # 应用单元传播
        clauses, ok = self.unit_propagation(clauses, assignment.copy())
        if not ok:
            return None  # 冲突
        
        if not clauses:
            return assignment  # 所有子句满足
        
        # 选择未赋值变量
        unassigned_vars = set()
        for clause in clauses:
            for lit in clause:
                var = abs(lit)
                if var not in assignment:
                    unassigned_vars.add(var)
        
        if not unassigned_vars:
            return assignment
        
        var = min(unassigned_vars)  # 简单选择策略
        
        # 尝试赋值为True
        assignment_true = assignment.copy()
        assignment_true[var] = True
        result = self.dpll(clauses, assignment_true)
        if result is not None:
            return result
        
        # 尝试赋值为False
        assignment_false = assignment.copy()
        assignment_false[var] = False
        result = self.dpll(clauses, assignment_false)
        return result
    
    def solve(self):
        """求解SAT问题"""
        result = self.dpll(self.clauses, {})
        return result

# 使用示例
def main():
    # 读取DIMACS输入
    import sys
    lines = sys.stdin.readlines()
    
    solver = SATSolver()
    solver.parse_dimacs(lines)
    
    result = solver.solve()
    if result is None:
        print("UNSAT")
    else:
        print("SAT")
        for var in sorted(result.keys()):
            print(f"{var} {int(result[var])}")

if __name__ == "__main__":
    main()
```

</details>