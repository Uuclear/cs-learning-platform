#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：Saga模式实现

这个脚本实现了Saga模式，用于处理分布式事务。Saga将一个长事务分解为一系列
本地事务，每个本地事务都有对应的补偿事务用于回滚。

场景：电商订单创建流程
1. 预扣用户余额（本地事务）
2. 创建订单记录（本地事务）
3. 扣减商品库存（本地事务）

如果任何步骤失败，执行相应的补偿操作。
"""

import json
import threading
import time
from enum import Enum
from typing import List, Dict, Any, Optional


class SagaStatus(Enum):
    """Saga状态枚举"""
    PENDING = "pending"      # 待执行
    EXECUTING = "executing"  # 执行中
    COMPLETED = "completed"  # 已完成
    COMPENSATING = "compensating"  # 补偿中
    FAILED = "failed"        # 失败


class SagaStep:
    """Saga步骤定义"""

    def __init__(self, name: str, action, compensation, description: str = ""):
        """
        :param name: 步骤名称
        :param action: 执行函数
        :param compensation: 补偿函数
        :param description: 步骤描述
        """
        self.name = name
        self.action = action
        self.compensation = compensation
        self.description = description
        self.executed = False
        self.compensated = False


class SagaOrchestrator:
    """Saga协调器 - 管理Saga的执行和补偿"""

    def __init__(self, saga_id: str, steps: List[SagaStep]):
        self.saga_id = saga_id
        self.steps = steps
        self.status = SagaStatus.PENDING
        self.current_step = 0
        self.execution_log = []
        self.lock = threading.Lock()

    def execute(self) -> bool:
        """执行Saga"""
        with self.lock:
            if self.status != SagaStatus.PENDING:
                raise ValueError(f"Saga {self.saga_id} 已经在执行或已完成")

            self.status = SagaStatus.EXECUTING
            print(f"🔄 开始执行Saga: {self.saga_id}")

            try:
                # 按顺序执行所有步骤
                for i, step in enumerate(self.steps):
                    self.current_step = i
                    print(f"   📋 执行步骤 {i+1}: {step.description}")

                    success = step.action()
                    step.executed = True
                    self.execution_log.append({
                        'step': step.name,
                        'action': 'execute',
                        'success': success,
                        'timestamp': time.time()
                    })

                    if not success:
                        print(f"   ❌ 步骤 {i+1} 失败: {step.description}")
                        self._compensate()
                        return False

                self.status = SagaStatus.COMPLETED
                print(f"   ✅ Saga {self.saga_id} 执行成功")
                return True

            except Exception as e:
                print(f"   ❌ Saga执行异常: {e}")
                self._compensate()
                return False

    def _compensate(self):
        """执行补偿操作"""
        self.status = SagaStatus.COMPENSATING
        print(f"   🔁 开始补偿Saga: {self.saga_id}")

        # 逆序执行已执行步骤的补偿操作
        for i in range(self.current_step, -1, -1):
            step = self.steps[i]
            if step.executed and not step.compensated:
                print(f"   🔄 补偿步骤 {i+1}: {step.description}")
                try:
                    step.compensation()
                    step.compensated = True
                    self.execution_log.append({
                        'step': step.name,
                        'action': 'compensate',
                        'success': True,
                        'timestamp': time.time()
                    })
                except Exception as e:
                    print(f"   ⚠️  补偿步骤 {i+1} 失败: {e}")
                    # 补偿失败需要人工干预，但继续尝试其他补偿

        self.status = SagaStatus.FAILED
        print(f"   ❌ Saga {self.saga_id} 补偿完成，状态为失败")


# 模拟服务类
class UserService:
    """用户服务 - 管理用户余额"""

    def __init__(self):
        self.balances = {'user123': 1000.0}  # 初始余额
        self.lock = threading.Lock()

    def reserve_balance(self, user_id: str, amount: float) -> bool:
        """预扣余额（Saga步骤1）"""
        with self.lock:
            if user_id not in self.balances:
                print(f"      用户 {user_id} 不存在")
                return False

            if self.balances[user_id] >= amount:
                self.balances[user_id] -= amount
                print(f"      预扣用户 {user_id} 余额 {amount}，剩余 {self.balances[user_id]}")
                return True
            else:
                print(f"      用户 {user_id} 余额不足")
                return False

    def release_balance(self, user_id: str, amount: float) -> bool:
        """释放预扣余额（补偿步骤1）"""
        with self.lock:
            self.balances[user_id] += amount
            print(f"      释放用户 {user_id} 预扣余额 {amount}，当前余额 {self.balances[user_id]}")
            return True


class OrderService:
    """订单服务 - 管理订单"""

    def __init__(self):
        self.orders = {}
        self.lock = threading.Lock()

    def create_order(self, order_data: Dict[str, Any]) -> bool:
        """创建订单（Saga步骤2）"""
        with self.lock:
            order_id = f"ORD-{int(time.time())}"
            self.orders[order_id] = {
                **order_data,
                'status': 'created',
                'created_at': time.time()
            }
            print(f"      创建订单 {order_id}")
            return True

    def cancel_order(self, order_id: str) -> bool:
        """取消订单（补偿步骤2）"""
        with self.lock:
            if order_id in self.orders:
                self.orders[order_id]['status'] = 'cancelled'
                print(f"      取消订单 {order_id}")
                return True
            return False


class InventoryService:
    """库存服务 - 管理商品库存"""

    def __init__(self):
        self.inventory = {'prod456': 10}  # 初始库存
        self.lock = threading.Lock()

    def deduct_inventory(self, product_id: str, quantity: int) -> bool:
        """扣减库存（Saga步骤3）"""
        with self.lock:
            if product_id not in self.inventory:
                print(f"      商品 {product_id} 不存在")
                return False

            if self.inventory[product_id] >= quantity:
                self.inventory[product_id] -= quantity
                print(f"      扣减商品 {product_id} 库存 {quantity}，剩余 {self.inventory[product_id]}")
                return True
            else:
                print(f"      商品 {product_id} 库存不足")
                return False

    def restore_inventory(self, product_id: str, quantity: int) -> bool:
        """恢复库存（补偿步骤3）"""
        with self.lock:
            self.inventory[product_id] += quantity
            print(f"      恢复商品 {product_id} 库存 {quantity}，当前库存 {self.inventory[product_id]}")
            return True


def create_order_saga(user_service: UserService, order_service: OrderService,
                     inventory_service: InventoryService,
                     user_id: str, product_id: str, quantity: int, amount: float) -> SagaOrchestrator:
    """创建订单Saga"""

    # 订单数据
    order_data = {
        'user_id': user_id,
        'product_id': product_id,
        'quantity': quantity,
        'amount': amount
    }

    # 定义Saga步骤
    steps = [
        SagaStep(
            name="reserve_balance",
            action=lambda: user_service.reserve_balance(user_id, amount),
            compensation=lambda: user_service.release_balance(user_id, amount),
            description="预扣用户余额"
        ),
        SagaStep(
            name="create_order",
            action=lambda: order_service.create_order(order_data),
            compensation=lambda: order_service.cancel_order(list(order_service.orders.keys())[-1]) if order_service.orders else False,
            description="创建订单记录"
        ),
        SagaStep(
            name="deduct_inventory",
            action=lambda: inventory_service.deduct_inventory(product_id, quantity),
            compensation=lambda: inventory_service.restore_inventory(product_id, quantity),
            description="扣减商品库存"
        )
    ]

    saga_id = f"saga-{int(time.time())}"
    return SagaOrchestrator(saga_id, steps)


def test_successful_saga():
    """测试成功的Saga执行"""
    print("\n" + "="*50)
    print("✅ 测试成功的Saga执行")
    print("="*50)

    # 初始化服务
    user_svc = UserService()
    order_svc = OrderService()
    inventory_svc = InventoryService()

    # 创建Saga
    saga = create_order_saga(user_svc, order_svc, inventory_svc,
                           "user123", "prod456", 2, 200.0)

    # 执行Saga
    success = saga.execute()
    print(f"\n结果: {'成功' if success else '失败'}")
    print(f"最终状态: {saga.status.value}")


def test_failed_saga():
    """测试失败的Saga执行（库存不足）"""
    print("\n" + "="*50)
    print("❌ 测试失败的Saga执行（库存不足）")
    print("="*50)

    # 初始化服务（库存只有1个）
    user_svc = UserService()
    order_svc = OrderService()
    inventory_svc = InventoryService()
    inventory_svc.inventory['prod456'] = 1  # 设置库存不足

    # 创建Saga（尝试购买2个）
    saga = create_order_saga(user_svc, order_svc, inventory_svc,
                           "user123", "prod456", 2, 200.0)

    # 执行Saga
    success = saga.execute()
    print(f"\n结果: {'成功' if success else '失败'}")
    print(f"最终状态: {saga.status.value}")

    # 验证补偿效果
    print(f"\n验证补偿效果:")
    print(f"用户余额: {user_svc.balances['user123']}")
    print(f"商品库存: {inventory_svc.inventory['prod456']}")


def test_user_not_found_saga():
    """测试用户不存在的Saga执行"""
    print("\n" + "="*50)
    print("❌ 测试用户不存在的Saga执行")
    print("="*50)

    # 初始化服务
    user_svc = UserService()
    order_svc = OrderService()
    inventory_svc = InventoryService()

    # 创建Saga（用户不存在）
    saga = create_order_saga(user_svc, order_svc, inventory_svc,
                           "user999", "prod456", 1, 100.0)

    # 执行Saga
    success = saga.execute()
    print(f"\n结果: {'成功' if success else '失败'}")
    print(f"最终状态: {saga.status.value}")


if __name__ == '__main__':
    print("📚 Saga模式解决方案演示")
    print("本示例展示了如何使用Saga模式处理分布式事务，确保最终一致性")

    # 测试成功的场景
    test_successful_saga()

    # 测试失败的场景
    test_failed_saga()

    # 测试用户不存在的场景
    test_user_not_found_saga()

    print("\n💡 Saga模式关键点:")
    print("   • 将长事务分解为本地事务序列")
    print("   • 每个步骤都有对应的补偿操作")
    print("   • 失败时逆序执行补偿，保证最终一致性")
    print("   • 适用于不能使用两阶段提交的场景")

    print("\n👋 演示结束")