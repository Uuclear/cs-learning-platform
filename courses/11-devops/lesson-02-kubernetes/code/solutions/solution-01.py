#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1：Kubernetes Manifest 生成器

构建一个简单的 Kubernetes manifest 生成器，接收应用配置并生成优化的 YAML。
支持 Deployment、Service、ConfigMap 和 Secret。
"""

import yaml
from typing import Dict, Any, Optional, List


class KubernetesManifestGenerator:
    """Kubernetes Manifest 生成器"""

    def __init__(self):
        self.manifests = []

    def add_deployment(
        self,
        app_name: str,
        image: str,
        replicas: int = 1,
        ports: Optional[List[Dict[str, Any]]] = None,
        env_vars: Optional[Dict[str, str]] = None,
        config_map_refs: Optional[List[str]] = None,
        secret_refs: Optional[List[str]] = None,
        resources: Optional[Dict[str, Any]] = None,
        health_checks: Optional[Dict[str, Any]] = None
    ) -> 'KubernetesManifestGenerator':
        """添加 Deployment 配置"""
        if ports is None:
            ports = [{"containerPort": 80}]

        if resources is None:
            resources = {
                "requests": {"cpu": "100m", "memory": "128Mi"},
                "limits": {"cpu": "200m", "memory": "256Mi"}
            }

        if health_checks is None:
            health_checks = {
                "liveness": {"httpGet": {"path": "/health", "port": 80}, "initialDelaySeconds": 30},
                "readiness": {"httpGet": {"path": "/ready", "port": 80}, "initialDelaySeconds": 5}
            }

        container_spec = {
            "name": app_name,
            "image": image,
            "ports": ports,
            "resources": resources
        }

        # 添加环境变量
        if env_vars or config_map_refs or secret_refs:
            container_spec["env"] = []

            # 直接环境变量
            if env_vars:
                for key, value in env_vars.items():
                    container_spec["env"].append({"name": key, "value": value})

            # ConfigMap 引用
            if config_map_refs:
                for cm_name in config_map_refs:
                    container_spec["env"].append({
                        "name": cm_name.upper().replace("-", "_"),
                        "valueFrom": {"configMapKeyRef": {"name": cm_name, "key": "value"}}
                    })

            # Secret 引用
            if secret_refs:
                for secret_name in secret_refs:
                    container_spec["env"].append({
                        "name": secret_name.upper().replace("-", "_"),
                        "valueFrom": {"secretKeyRef": {"name": secret_name, "key": "value"}}
                    })

        # 添加健康检查
        if health_checks.get("liveness"):
            container_spec["livenessProbe"] = health_checks["liveness"]
        if health_checks.get("readiness"):
            container_spec["readinessProbe"] = health_checks["readiness"]

        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": f"{app_name}-deployment",
                "labels": {"app": app_name}
            },
            "spec": {
                "replicas": replicas,
                "selector": {"matchLabels": {"app": app_name}},
                "template": {
                    "metadata": {"labels": {"app": app_name}},
                    "spec": {"containers": [container_spec]}
                }
            }
        }

        self.manifests.append(deployment)
        return self

    def add_service(
        self,
        app_name: str,
        service_type: str = "ClusterIP",
        ports: Optional[List[Dict[str, Any]]] = None
    ) -> 'KubernetesManifestGenerator':
        """添加 Service 配置"""
        if ports is None:
            ports = [{"port": 80, "targetPort": 80}]

        service = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": f"{app_name}-service",
                "labels": {"app": app_name}
            },
            "spec": {
                "selector": {"app": app_name},
                "ports": ports,
                "type": service_type
            }
        }

        self.manifests.append(service)
        return self

    def add_configmap(
        self,
        name: str,
        data: Dict[str, str]
    ) -> 'KubernetesManifestGenerator':
        """添加 ConfigMap 配置"""
        configmap = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": name},
            "data": data
        }

        self.manifests.append(configmap)
        return self

    def add_secret(
        self,
        name: str,
        data: Dict[str, str]
    ) -> 'KubernetesManifestGenerator':
        """添加 Secret 配置（注意：实际中应该使用 base64 编码）"""
        # 在实际应用中，Secret 数据应该是 base64 编码的
        encoded_data = {k: v for k, v in data.items()}  # 这里简化处理

        secret = {
            "apiVersion": "v1",
            "kind": "Secret",
            "metadata": {"name": name},
            "type": "Opaque",
            "stringData": data  # 使用 stringData 自动编码
        }

        self.manifests.append(secret)
        return self

    def generate_yaml(self) -> str:
        """生成完整的 YAML 字符串"""
        yaml_output = ""
        for manifest in self.manifests:
            yaml_output += yaml.dump(manifest, default_flow_style=False, allow_unicode=True)
            yaml_output += "---\n"
        return yaml_output.rstrip("---\n")

    def save_to_file(self, filename: str):
        """保存到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_yaml())


def main():
    """主函数：演示 manifest 生成器的使用"""
    print("=== Kubernetes Manifest 生成器 ===\n")

    # 创建一个 Web 应用的完整配置
    generator = KubernetesManifestGenerator()

    # 添加 ConfigMap
    generator.add_configmap(
        "web-app-config",
        {
            "database_url": "postgresql://db:5432/myapp",
            "log_level": "info",
            "feature_flags": "true"
        }
    )

    # 添加 Secret
    generator.add_secret(
        "web-app-secret",
        {
            "database_password": "super-secret-password",
            "api_key": "your-api-key-here"
        }
    )

    # 添加 Deployment
    generator.add_deployment(
        app_name="web-app",
        image="my-registry/web-app:v1.2.3",
        replicas=3,
        ports=[{"containerPort": 8080}],
        env_vars={"NODE_ENV": "production"},
        config_map_refs=["web-app-config"],
        secret_refs=["web-app-secret"],
        resources={
            "requests": {"cpu": "200m", "memory": "256Mi"},
            "limits": {"cpu": "500m", "memory": "512Mi"}
        },
        health_checks={
            "liveness": {
                "httpGet": {"path": "/health", "port": 8080},
                "initialDelaySeconds": 30,
                "periodSeconds": 10
            },
            "readiness": {
                "httpGet": {"path": "/ready", "port": 8080},
                "initialDelaySeconds": 10,
                "periodSeconds": 5
            }
        }
    )

    # 添加 Service
    generator.add_service(
        app_name="web-app",
        service_type="LoadBalancer",
        ports=[{"port": 80, "targetPort": 8080}]
    )

    # 输出结果
    yaml_output = generator.generate_yaml()
    print("生成的 Kubernetes Manifests:")
    print("=" * 60)
    print(yaml_output)
    print("=" * 60)

    # 保存到文件
    generator.save_to_file("web-app-manifests.yaml")
    print("\n✅ Manifests 已保存到 'web-app-manifests.yaml'")


if __name__ == "__main__":
    main()