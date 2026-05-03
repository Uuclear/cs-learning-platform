# 挑战2：实现分布式追踪采样策略

## 背景
在高流量的生产环境中，记录每个请求的完整追踪数据会产生巨大的存储和性能开销。因此，需要实现智能的采样策略来平衡可观测性和资源消耗。

## 任务
扩展现有的`Tracer`类，实现多种采样策略：

1. **固定比率采样**：以固定的概率（如10%）采样请求
2. **基于错误的采样**：始终采样包含错误的请求，正常请求按低比率采样
3. **自适应采样**：根据系统负载动态调整采样率

## 要求
- 添加`Sampler`接口和具体的采样器实现
- 修改`Tracer`类以支持可配置的采样策略
- 实现上下文传播时正确传递采样决策
- 所有代码必须包含中文注释

## 具体实现
### 固定比率采样器
```python
class RateSampler:
    def __init__(self, rate: float):  # rate: 0.0-1.0之间的采样率
        self.rate = rate
    
    def should_sample(self, trace_id: str, tags: Dict[str, Any]) -> bool:
        # 基于trace_id的哈希值决定是否采样，确保同一trace的一致性
        pass
```

### 错误优先采样器
```python
class ErrorPrioritySampler:
    def __init__(self, error_rate: float = 1.0, normal_rate: float = 0.1):
        self.error_rate = error_rate
        self.normal_rate = normal_rate
    
    def should_sample(self, trace_id: str, tags: Dict[str, Any]) -> bool:
        # 如果span包含错误标签，则使用error_rate，否则使用normal_rate
        pass
```

## 验证
创建测试用例，验证不同采样策略在各种场景下的行为是否符合预期，特别是确保同一Trace的所有Span保持一致的采样决策。