#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3: Docker 镜像大小优化器
分析 Dockerfile 层并提供优化建议
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class LayerInfo:
    """Docker 镜像层信息"""
    instruction: str
    content: str
    estimated_size_mb: int
    optimization_tips: List[str]

class DockerImageOptimizer:
    """Docker 镜像优化器"""

    def __init__(self):
        self.base_image_sizes = {
            "alpine": 5,
            "slim": 120,
            "debian": 120,
            "ubuntu": 70,
            "node": {"alpine": 117, "slim": 900},
            "python": {"alpine": 45, "slim": 120},
            "golang": {"alpine": 300, "slim": 800}
        }

    def parse_dockerfile(self, dockerfile_content: str) -> List[str]:
        """解析 Dockerfile 内容为指令列表"""
        lines = dockerfile_content.strip().split('\n')
        instructions = []
        current_instruction = ""

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # 处理多行指令（以反斜杠结尾）
            if line.endswith('\\'):
                current_instruction += line[:-1] + ' '
            else:
                current_instruction += line
                instructions.append(current_instruction.strip())
                current_instruction = ""

        return instructions

    def analyze_layer(self, instruction: str) -> LayerInfo:
        """分析单个 Dockerfile 指令并估算大小"""
        instruction_upper = instruction.upper()
        estimated_size = 0
        optimization_tips = []

        if instruction_upper.startswith('FROM '):
            # 分析基础镜像
            base_image = instruction.split()[1]
            estimated_size = self._estimate_base_image_size(base_image)
            optimization_tips = self._get_base_image_tips(base_image)

        elif instruction_upper.startswith('RUN '):
            # 分析 RUN 指令
            estimated_size = self._estimate_run_size(instruction)
            optimization_tips = self._get_run_optimization_tips(instruction)

        elif instruction_upper.startswith('COPY ') or instruction_upper.startswith('ADD '):
            # 分析 COPY/ADD 指令
            estimated_size = self._estimate_copy_size(instruction)
            optimization_tips = self._get_copy_optimization_tips(instruction)

        elif instruction_upper.startswith('ENV ') or instruction_upper.startswith('WORKDIR '):
            # 这些指令通常不增加显著大小
            estimated_size = 0

        return LayerInfo(
            instruction=instruction.split()[0].upper(),
            content=instruction,
            estimated_size_mb=estimated_size,
            optimization_tips=optimization_tips
        )

    def _estimate_base_image_size(self, base_image: str) -> int:
        """估算基础镜像大小"""
        base_image = base_image.lower()

        # 检查特定的基础镜像
        for lang, sizes in self.base_image_sizes.items():
            if lang in base_image:
                if isinstance(sizes, dict):
                    if 'alpine' in base_image:
                        return sizes['alpine']
                    elif 'slim' in base_image:
                        return sizes['slim']
                    else:
                        return max(sizes.values()) if sizes else 100
                else:
                    return sizes

        # 默认估算
        if 'alpine' in base_image:
            return 5
        elif 'slim' in base_image:
            return 120
        else:
            return 200

    def _get_base_image_tips(self, base_image: str) -> List[str]:
        """获取基础镜像优化建议"""
        tips = []
        base_image_lower = base_image.lower()

        if 'latest' in base_image_lower:
            tips.append("避免使用 'latest' 标签，使用具体版本以确保可重现性")

        if 'alpine' not in base_image_lower and 'slim' not in base_image_lower:
            tips.append("考虑使用 Alpine 或 slim 版本的基础镜像来减小大小")

        return tips

    def _estimate_run_size(self, instruction: str) -> int:
        """估算 RUN 指令增加的大小"""
        run_content = instruction[4:].lower()  # 去掉 "RUN "
        size = 0

        # 根据常见的包管理器估算
        if 'apt-get install' in run_content or 'apt install' in run_content:
            # 估算安装的包数量
            packages = re.findall(r'apt-get install -y ([^&|]+)', run_content)
            if packages:
                size += len(packages[0].split()) * 20  # 每个包约20MB
            else:
                size += 100  # 默认估算

        elif 'yum install' in run_content:
            size += 150

        elif 'pip install' in run_content:
            if '--no-cache-dir' not in run_content:
                size += 50  # 缓存会增加大小
            size += 100  # 依赖包大小

        elif 'npm install' in run_content:
            if 'npm ci' in run_content:
                size += 80
            else:
                size += 150

        return size

    def _get_run_optimization_tips(self, instruction: str) -> List[str]:
        """获取 RUN 指令优化建议"""
        tips = []
        run_content = instruction[4:]

        # 检查是否清理了包管理器缓存
        if ('apt-get' in run_content or 'apt' in run_content) and 'rm -rf /var/lib/apt/lists/*' not in run_content:
            tips.append("在 apt-get install 后添加 '&& rm -rf /var/lib/apt/lists/*' 清理缓存")

        if 'pip install' in run_content and '--no-cache-dir' not in run_content:
            tips.append("使用 '--no-cache-dir' 参数避免 pip 缓存")

        # 检查是否合并了多个 RUN 指令
        if '&&' not in run_content and len(re.findall(r'RUN ', instruction)) == 1:
            # 这里简化处理，实际应该检查相邻的 RUN 指令
            pass

        return tips

    def _estimate_copy_size(self, instruction: str) -> int:
        """估算 COPY/ADD 指令增加的大小"""
        # 简化估算：假设复制源代码约 10-50MB
        return 30

    def _get_copy_optimization_tips(self, instruction: str) -> List[str]:
        """获取 COPY/ADD 指令优化建议"""
        tips = []

        if instruction.upper().startswith('ADD '):
            tips.append("优先使用 COPY 而不是 ADD，COPY 语义更清晰")

        # 检查是否使用了 .dockerignore
        # （这里无法检测，但可以建议）
        tips.append("确保使用 .dockerignore 文件排除不必要的文件")

        return tips

    def analyze_dockerfile(self, dockerfile_content: str) -> Dict:
        """完整分析 Dockerfile 并提供优化建议"""
        instructions = self.parse_dockerfile(dockerfile_content)
        layers = []
        total_size = 0

        for instruction in instructions:
            layer_info = self.analyze_layer(instruction)
            layers.append(layer_info)
            total_size += layer_info.estimated_size_mb

        # 生成总体建议
        overall_tips = self._generate_overall_tips(layers)

        return {
            'layers': layers,
            'total_estimated_size_mb': total_size,
            'overall_optimization_tips': overall_tips
        }

    def _generate_overall_tips(self, layers: List[LayerInfo]) -> List[str]:
        """生成总体优化建议"""
        tips = []

        # 检查是否有多个 RUN 指令可以合并
        run_layers = [layer for layer in layers if layer.instruction == 'RUN']
        if len(run_layers) > 1:
            tips.append("考虑合并多个 RUN 指令以减少镜像层数")

        # 检查是否使用了多阶段构建
        from_layers = [layer for layer in layers if layer.instruction == 'FROM']
        if len(from_layers) == 1:
            tips.append("考虑使用多阶段构建来进一步减小最终镜像大小")

        # 检查是否设置了非 root 用户
        has_user_instruction = any(layer.instruction == 'USER' for layer in layers)
        if not has_user_instruction:
            tips.append("添加 USER 指令使用非 root 用户运行应用，提高安全性")

        return tips

def demonstrate_optimizer():
    """演示镜像优化器"""
    optimizer = DockerImageOptimizer()

    print("=== 解决方案 3: Docker 镜像大小优化器 ===\n")

    # 测试 Dockerfile 示例
    test_dockerfile = """FROM node:16

RUN apt-get update && apt-get install -y curl git

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
"""

    print("分析以下 Dockerfile：")
    print("-" * 50)
    print(test_dockerfile)
    print("-" * 50)

    # 分析 Dockerfile
    analysis = optimizer.analyze_dockerfile(test_dockerfile)

    print(f"\n分析结果：")
    print(f"估算总大小: {analysis['total_estimated_size_mb']} MB")
    print(f"\n各层详细信息：")

    for i, layer in enumerate(analysis['layers'], 1):
        print(f"\n层 {i}: {layer.instruction}")
        print(f"  内容: {layer.content}")
        print(f"  估算大小: {layer.estimated_size_mb} MB")
        if layer.optimization_tips:
            print(f"  优化建议:")
            for tip in layer.optimization_tips:
                print(f"    • {tip}")

    print(f"\n总体优化建议：")
    for i, tip in enumerate(analysis['overall_optimization_tips'], 1):
        print(f"  {i}. {tip}")

    # 显示优化后的 Dockerfile
    optimized_dockerfile = """FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

USER node

EXPOSE 3000

CMD ["node", "server.js"]
"""

    print(f"\n优化后的 Dockerfile 示例：")
    print("-" * 50)
    print(optimized_dockerfile)
    print("-" * 50)

    # 分析优化后的版本
    optimized_analysis = optimizer.analyze_dockerfile(optimized_dockerfile)
    original_size = analysis['total_estimated_size_mb']
    optimized_size = optimized_analysis['total_estimated_size_mb']
    savings = original_size - optimized_size
    savings_percent = (savings / original_size) * 100 if original_size > 0 else 0

    print(f"\n优化效果：")
    print(f"原始大小: {original_size} MB")
    print(f"优化后大小: {optimized_size} MB")
    print(f"节省空间: {savings} MB ({savings_percent:.1f}%)")

def main():
    demonstrate_optimizer()

if __name__ == "__main__":
    main()