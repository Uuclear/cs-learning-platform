# 示例3：系统设计面试模板框架
from typing import Dict, List, Any

class SystemDesignTemplate:
    """
    系统设计面试结构化模板
    帮助面试者系统性地思考和表达设计方案
    """

    def __init__(self, system_name: str):
        self.system_name = system_name
        self.requirements = {}
        self.api_design = {}
        self.data_model = {}
        self.scaling_considerations = {}

    def step1_define_requirements(self, functional_reqs: List[str],
                                 non_functional_reqs: List[str],
                                 scale_estimates: Dict[str, Any]):
        """
        步骤1: 需求分析

        :param functional_reqs: 功能需求列表
        :param non_functional_reqs: 非功能需求列表
        :param scale_estimates: 规模估算（QPS、存储、用户数等）
        """
        self.requirements = {
            'functional': functional_reqs,
            'non_functional': non_functional_reqs,
            'scale': scale_estimates
        }
        print(f"✅ 步骤1完成: {self.system_name} 需求定义")

    def step2_design_apis(self, endpoints: Dict[str, Dict[str, Any]]):
        """
        步骤2: API设计

        :param endpoints: API端点定义
        """
        self.api_design = endpoints
        print(f"✅ 步骤2完成: {self.system_name} API设计")

    def step3_define_data_model(self, entities: Dict[str, Dict[str, Any]]):
        """
        步骤3: 数据模型设计

        :param entities: 实体及其属性
        """
        self.data_model = entities
        print(f"✅ 步骤3完成: {self.system_name} 数据模型")

    def step4_consider_scaling(self, strategies: List[str],
                              bottlenecks: List[str]):
        """
        步骤4: 扩展性考虑

        :param strategies: 扩展策略
        :param bottlenecks: 潜在瓶颈
        """
        self.scaling_considerations = {
            'strategies': strategies,
            'bottlenecks': bottlenecks
        }
        print(f"✅ 步骤4完成: {self.system_name} 扩展性分析")

    def generate_interview_script(self) -> str:
        """
        生成面试脚本模板
        """
        script = f"""
系统设计面试模板: {self.system_name}

1. 需求澄清阶段:
   - 请问这个系统的具体功能是什么？
   - 预期的用户规模和请求量是多少？
   - 对延迟、可用性和一致性有什么要求？

2. API设计阶段:
   - 我建议设计以下核心API端点...
   - 每个端点的请求/响应格式如下...

3. 数据模型阶段:
   - 主要的数据实体包括...
   - 表之间的关系是...
   - 考虑使用SQL还是NoSQL？

4. 扩展性设计阶段:
   - 初始架构可以是单体应用
   - 当遇到性能瓶颈时，可以考虑...
   - 缓存策略: Redis用于热点数据
   - 负载均衡: 使用Nginx或云服务

5. 潜在改进:
   - 监控和告警
   - 自动化部署
   - 容灾备份方案
"""
        return script

# 使用示例：设计一个URL短链系统
def design_url_shortener():
    """URL短链系统设计示例"""
    url_shortener = SystemDesignTemplate("URL Shortener")

    # 步骤1: 需求分析
    url_shortener.step1_define_requirements(
        functional_reqs=[
            "将长URL转换为短URL",
            "通过短URL重定向到原始URL",
            "支持自定义短码",
            "统计点击次数"
        ],
        non_functional_reqs=[
            "高可用性（99.9% uptime）",
            "低延迟（<100ms）",
            "可扩展性（支持10亿URL）"
        ],
        scale_estimates={
            'qps': 10000,
            'storage': '10TB',
            'users': '100M'
        }
    )

    # 步骤2: API设计
    url_shortener.step2_design_apis({
        'create_short_url': {
            'method': 'POST',
            'endpoint': '/api/shorten',
            'request': {'long_url': 'string', 'custom_alias': 'string?'},
            'response': {'short_url': 'string', 'alias': 'string'}
        },
        'redirect': {
            'method': 'GET',
            'endpoint': '/{alias}',
            'response': '302 redirect'
        }
    })

    # 步骤3: 数据模型
    url_shortener.step3_define_data_model({
        'urls': {
            'alias': 'string (primary key)',
            'long_url': 'string',
            'created_at': 'timestamp',
            'click_count': 'integer'
        }
    })

    # 步骤4: 扩展性考虑
    url_shortener.step4_consider_scaling(
        strategies=[
            "分布式ID生成器（如Snowflake）",
            "Redis缓存热门短URL映射",
            "数据库分片存储URL数据",
            "CDN加速全球访问"
        ],
        bottlenecks=[
            "ID生成器成为单点",
            "数据库写入瓶颈",
            "缓存击穿问题"
        ]
    )

    return url_shortener.generate_interview_script()

if __name__ == "__main__":
    script = design_url_shortener()
    print(script)