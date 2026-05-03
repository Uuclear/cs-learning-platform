# 解决方案2：社交媒体Feed系统设计
from typing import Dict, List, Any

class SocialFeedSystemDesign:
    """
    社交媒体Feed系统设计方案
    """

    def __init__(self):
        self.system_name = "Social Media Feed System"

    def define_requirements(self):
        """定义系统需求"""
        functional_reqs = [
            "用户可以发布文本、图片内容",
            "用户可以关注/取消关注其他用户",
            "用户可以查看关注用户的最新动态（Feed）",
            "支持点赞、评论、分享功能",
            "支持@提及和话题标签"
        ]

        non_functional_reqs = [
            "高可用性（99.95% uptime）",
            "低延迟（Feed加载 < 500ms）",
            "可扩展性（支持1亿用户，10万QPS）",
            "数据一致性（最终一致性可接受）"
        ]

        scale_estimates = {
            'daily_active_users': 50_000_000,
            'posts_per_day': 10_000_000,
            'feed_requests_per_second': 100_000,
            'storage_growth_per_day': '1TB'
        }

        return {
            'functional': functional_reqs,
            'non_functional': non_functional_reqs,
            'scale': scale_estimates
        }

    def design_apis(self):
        """API设计"""
        return {
            'create_post': {
                'method': 'POST',
                'endpoint': '/api/posts',
                'request': {
                    'user_id': 'string',
                    'content': 'string',
                    'media_urls': 'string[]?',
                    'visibility': 'public|followers'
                },
                'response': {
                    'post_id': 'string',
                    'created_at': 'timestamp'
                }
            },
            'follow_user': {
                'method': 'POST',
                'endpoint': '/api/follows',
                'request': {
                    'follower_id': 'string',
                    'following_id': 'string'
                },
                'response': {'status': 'success'}
            },
            'get_feed': {
                'method': 'GET',
                'endpoint': '/api/feed',
                'query_params': {
                    'user_id': 'string',
                    'limit': 'integer (default: 20)',
                    'offset': 'integer (default: 0)'
                },
                'response': {
                    'posts': 'Post[]',
                    'has_more': 'boolean'
                }
            },
            'like_post': {
                'method': 'POST',
                'endpoint': '/api/likes',
                'request': {
                    'user_id': 'string',
                    'post_id': 'string'
                },
                'response': {'like_count': 'integer'}
            }
        }

    def define_data_model(self):
        """数据模型设计"""
        return {
            'users': {
                'user_id': 'string (primary key)',
                'username': 'string (unique)',
                'email': 'string',
                'profile_info': 'json',
                'created_at': 'timestamp'
            },
            'posts': {
                'post_id': 'string (primary key)',
                'user_id': 'string (foreign key)',
                'content': 'text',
                'media_urls': 'json array',
                'visibility': 'enum',
                'created_at': 'timestamp',
                'like_count': 'integer (default: 0)',
                'comment_count': 'integer (default: 0)'
            },
            'follows': {
                'follower_id': 'string',
                'following_id': 'string',
                'created_at': 'timestamp',
                'primary_key': '(follower_id, following_id)'
            },
            'likes': {
                'user_id': 'string',
                'post_id': 'string',
                'created_at': 'timestamp',
                'primary_key': '(user_id, post_id)'
            },
            'comments': {
                'comment_id': 'string (primary key)',
                'post_id': 'string (foreign key)',
                'user_id': 'string (foreign key)',
                'content': 'text',
                'created_at': 'timestamp'
            }
        }

    def consider_scaling_strategies(self):
        """扩展性策略"""
        strategies = [
            "推拉混合模式（Hybrid Push-Pull）: 热门用户用拉模式，普通用户用推模式",
            "Redis缓存用户关注列表和热门Feed",
            "数据库读写分离：主库写入，从库读取",
            "分库分表：按用户ID哈希分片",
            "CDN加速静态资源（图片、视频）",
            "消息队列处理异步任务（通知、统计）",
            "Elasticsearch用于全文搜索和话题标签"
        ]

        bottlenecks = [
            "Feed生成的计算复杂度",
            "热门用户的关注者更新延迟",
            "数据库写入瓶颈（高并发发帖）",
            "缓存一致性维护",
            "存储成本快速增长"
        ]

        return {
            'strategies': strategies,
            'bottlenecks': bottlenecks,
            'architecture_diagram': """
            用户客户端 → API网关 →
                ├── 写服务（发帖、关注、点赞）
                │   ├── 消息队列（Kafka/RabbitMQ）
                │   └── 数据库集群（MySQL分片）
                └── 读服务（获取Feed）
                    ├── Redis缓存层
                    └── 数据库从库集群

            异步服务 ← 消息队列
                ├── Feed生成服务
                ├── 通知服务
                └── 统计服务
            """
        }

    def generate_complete_design(self) -> Dict[str, Any]:
        """生成完整设计方案"""
        return {
            'system_name': self.system_name,
            'requirements': self.define_requirements(),
            'apis': self.design_apis(),
            'data_model': self.define_data_model(),
            'scaling': self.consider_scaling_strategies()
        }

if __name__ == "__main__":
    feed_system = SocialFeedSystemDesign()
    design = feed_system.generate_complete_design()

    print(f"社交媒体Feed系统设计方案")
    print("=" * 50)
    print(f"系统名称: {design['system_name']}")
    print(f"\n功能需求 ({len(design['requirements']['functional'])}项):")
    for req in design['requirements']['functional']:
        print(f"  • {req}")

    print(f"\n核心API端点 ({len(design['apis'])}个):")
    for api_name, api_spec in design['apis'].items():
        print(f"  • {api_name}: {api_spec['method']} {api_spec['endpoint']}")

    print(f"\n主要数据表 ({len(design['data_model'])}张):")
    for table_name, schema in design['data_model'].items():
        print(f"  • {table_name}: {list(schema.keys())[:3]}...")

    print(f"\n扩展策略 ({len(design['scaling']['strategies'])}项):")
    for strategy in design['scaling']['strategies'][:3]:
        print(f"  • {strategy}")
    print("  ...（更多策略在完整设计中）")