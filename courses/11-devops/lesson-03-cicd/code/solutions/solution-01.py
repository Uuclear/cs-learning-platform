#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 01: CI/CD 流水线阶段

这个解决方案展示了一个更健壮的 CI/CD 流水线实现，
包含错误处理、日志记录和可配置的阶段。
"""

import time
import random
import sys
from typing import Callable, List


class PipelineStage:
    """流水线阶段基类"""
    def __init__(self, name: str, success_rate: float = 0.9):
        self.name = name
        self.success_rate = success_rate
        self.duration = 0

    def execute(self) -> bool:
        """执行阶段逻辑"""
        print(f"🔍 执行阶段: {self.name}")
        start_time = time.time()

        # 模拟工作
        time.sleep(random.uniform(0.5, 2.0))

        # 模拟成功率
        success = random.random() < self.success_rate

        end_time = time.time()
        self.duration = end_time - start_time

        if success:
            print(f"✅ 阶段 {self.name} 成功 (耗时: {self.duration:.2f}s)")
        else:
            print(f"❌ 阶段 {self.name} 失败")

        return success


class CICDPipeline:
    """CI/CD 流水线管理器"""
    def __init__(self, name: str):
        self.name = name
        self.stages: List[PipelineStage] = []
        self.start_time = 0
        self.end_time = 0

    def add_stage(self, stage: PipelineStage):
        """添加阶段到流水线"""
        self.stages.append(stage)

    def run(self) -> bool:
        """运行完整的流水线"""
        print(f"🏗️  开始执行流水线: {self.name}")
        print("=" * 50)

        self.start_time = time.time()

        for stage in self.stages:
            if not stage.execute():
                self.end_time = time.time()
                print(f"\n❌ 流水线在阶段 '{stage.name}' 失败")
                return False
            print()  # 空行分隔

        self.end_time = time.time()
        total_duration = self.end_time - self.start_time
        print(f"🎉 流水线 {self.name} 执行成功！总耗时: {total_duration:.2f}s")
        return True


def main():
    """主函数 - 创建并运行示例流水线"""
    pipeline = CICDPipeline("Python 应用 CI/CD")

    # 添加各个阶段
    pipeline.add_stage(PipelineStage("代码检查", success_rate=0.95))
    pipeline.add_stage(PipelineStage("单元测试", success_rate=0.90))
    pipeline.add_stage(PipelineStage("集成测试", success_rate=0.85))
    pipeline.add_stage(PipelineStage("构建制品", success_rate=0.98))
    pipeline.add_stage(PipelineStage("部署到预发布", success_rate=0.99))

    # 运行流水线
    success = pipeline.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()