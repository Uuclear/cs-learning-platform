#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1：Kubernetes Manifests 生成器

这个脚本演示如何使用 Python 动态生成 Kubernetes YAML manifests，
包括 Deployment、Service 和 Ingress 配置。
"""

import yaml
from typing import Dict, Any


def generate_deployment_manifest(
    app_name: str,
    image: str,
    replicas: int = 2,
    cpu_request: str = "100m",
    memory_request: str = "128Mi",
    cpu_limit: str = "200m",
    memory_limit: str = "256Mi"
) -> Dict[str, Any]:
    """生成 Deployment manifest"""
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": f"{app_name}-deployment",
            "labels": {
                "app": app_name
            }
        },
        "spec": {
            "replicas": replicas,
            "selector": {
                "matchLabels": {
                    "app": app_name
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": app_name
                    }
                },
                "spec": {
                    "containers": [{
                        "name": app_name,
                        "image": image,
                        "ports": [{"containerPort": 80}],
                        "resources": {
                            "requests": {
                                "cpu": cpu_request,
                                "memory": memory_request
                            },
                            "limits": {
                                "cpu": cpu_limit,
                                "memory": memory_limit
                            }
                        },
                        "livenessProbe": {
                            "httpGet": {
                                "path": "/health",
                                "port": 80
                            },
                            "initialDelaySeconds": 30,
                            "periodSeconds": 10
                        },
                        "readinessProbe": {
                            "httpGet": {
                                "path": "/ready",
                                "port": 80
                            },
                            "initialDelaySeconds": 5,
                            "periodSeconds": 5
                        }
                    }]
                }
            }
        }
    }


def generate_service_manifest(app_name: str) -> Dict[str, Any]:
    """生成 Service manifest"""
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": f"{app_name}-service",
            "labels": {
                "app": app_name
            }
        },
        "spec": {
            "selector": {
                "app": app_name
            },
            "ports": [{
                "protocol": "TCP",
                "port": 80,
                "targetPort": 80
            }],
            "type": "ClusterIP"
        }
    }


def generate_ingress_manifest(app_name: str, host: str) -> Dict[str, Any]:
    """生成 Ingress manifest"""
    return {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": f"{app_name}-ingress",
            "labels": {
                "app": app_name
            }
        },
        "spec": {
            "rules": [{
                "host": host,
                "http": {
                    "paths": [{
                        "path": "/",
                        "pathType": "Prefix",
                        "backend": {
                            "service": {
                                "name": f"{app_name}-service",
                                "port": {
                                    "number": 80
                                }
                            }
                        }
                    }]
                }
            }]
        }
    }


def main():
    """主函数：生成完整的 Web 应用 manifests"""
    app_name = "web-app"
    image = "nginx:1.21"
    host = "web-app.example.com"

    print("=== 生成 Kubernetes Manifests ===\n")

    # 生成 Deployment
    deployment = generate_deployment_manifest(app_name, image, replicas=3)
    print("Deployment Manifest:")
    print(yaml.dump(deployment, default_flow_style=False, allow_unicode=True))
    print("-" * 50)

    # 生成 Service
    service = generate_service_manifest(app_name)
    print("Service Manifest:")
    print(yaml.dump(service, default_flow_style=False, allow_unicode=True))
    print("-" * 50)

    # 生成 Ingress
    ingress = generate_ingress_manifest(app_name, host)
    print("Ingress Manifest:")
    print(yaml.dump(ingress, default_flow_style=False, allow_unicode=True))

    print("✅ 所有 manifests 已成功生成！")


if __name__ == "__main__":
    main()