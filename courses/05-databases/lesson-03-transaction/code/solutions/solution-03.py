#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3: 库存管理系统

创建一个库存管理系统，包含死锁检测和重试逻辑。
"""

import sqlite3
import threading
import time
import random
import os
from typing import Optional


class InventorySystem:
    def __init__(self, db_path='inventory.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化数据库"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建产品表
        cursor.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                stock INTEGER NOT NULL CHECK (stock >= 0),
                price REAL NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 创建订单表
        cursor.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')

        # 插入初始产品数据
        products = [
            ("iPhone 15", 50, 5999.0),
            ("MacBook Pro", 30, 12999.0),
            ("AirPods Pro", 100, 1899.0),
            ("iPad Air", 40, 4599.0)
        ]

        for name, stock, price in products:
            cursor.execute(
                "INSERT INTO products (name, stock, price) VALUES (?, ?, ?)",
                (name, stock, price)
            )

        conn.commit()
        conn.close()

    def get_product_info(self, product_name: str) -> Optional[tuple]:
        """获取产品信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT id, stock, price FROM products WHERE name = ?",
            (product_name,)
        )
        row = cursor.fetchone()
        conn.close()
        return row

    def update_stock_with_deadlock_retry(
        self,
        product_id: int,
        quantity_change: int,
        max_retries: int = 5
    ) -> bool:
        """
        更新库存，包含死锁重试逻辑

        Args:
            product_id: 产品ID
            quantity_change: 库存变化量（负数表示减少）
            max_retries: 最大重试次数

        Returns:
            bool: 是否成功更新
        """
        for attempt in range(max_retries):
            try:
                # 设置较短的超时时间以快速检测死锁
                conn = sqlite3.connect(self.db_path, timeout=1.0)
                conn.execute("BEGIN")

                # 锁定产品行
                cursor = conn.execute(
                    "SELECT stock FROM products WHERE id = ? FOR UPDATE",
                    (product_id,)
                )
                current_stock = cursor.fetchone()[0]

                # 检查库存是否足够（如果是减少操作）
                if quantity_change < 0 and current_stock + quantity_change < 0:
                    conn.rollback()
                    conn.close()
                    print(f"❌ 库存不足！当前库存: {current_stock}, 需要减少: {abs(quantity_change)}")
                    return False

                # 更新库存
                new_stock = current_stock + quantity_change
                conn.execute(
                    "UPDATE products SET stock = ?, last_updated = CURRENT_TIMESTAMP WHERE id = ?",
                    (new_stock, product_id)
                )

                conn.commit()
                conn.close()
                return True

            except sqlite3.OperationalError as e:
                if "database is locked" in str(e).lower():
                    conn.rollback()
                    conn.close()

                    if attempt < max_retries - 1:
                        # 使用指数退避算法增加等待时间
                        backoff_time = min(0.1 * (2 ** attempt), 2.0)
                        jitter = random.uniform(0, 0.1)
                        wait_time = backoff_time + jitter

                        print(f"⚠️  检测到数据库锁定，{wait_time:.2f}秒后重试... (尝试 {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"❌ 达到最大重试次数 ({max_retries})，操作失败")
                        return False
                else:
                    conn.rollback()
                    conn.close()
                    raise e
            except Exception as e:
                conn.rollback()
                conn.close()
                raise e

        return False

    def process_order(self, product_name: str, quantity: int) -> bool:
        """
        处理订单

        Args:
            product_name: 产品名称
            quantity: 订购数量

        Returns:
            bool: 订单是否成功处理
        """
        product_info = self.get_product_info(product_name)
        if not product_info:
            print(f"❌ 产品 '{product_name}' 不存在")
            return False

        product_id, current_stock, price = product_info

        if current_stock < quantity:
            print(f"❌ 库存不足！产品 '{product_name}' 当前库存: {current_stock}, 需要: {quantity}")
            return False

        # 尝试更新库存（减少）
        if self.update_stock_with_deadlock_retry(product_id, -quantity):
            # 创建订单记录
            conn = sqlite3.connect(self.db_path)
            conn.execute(
                "INSERT INTO orders (product_id, quantity, status) VALUES (?, ?, ?)",
                (product_id, quantity, 'completed')
            )
            conn.commit()
            conn.close()

            total_price = quantity * price
            print(f"✅ 成功订购 {quantity} 个 '{product_name}' (¥{total_price:.2f})")
            return True
        else:
            return False

    def restock_product(self, product_name: str, quantity: int) -> bool:
        """
        补充库存

        Args:
            product_name: 产品名称
            quantity: 补充数量

        Returns:
            bool: 是否成功补充
        """
        product_info = self.get_product_info(product_name)
        if not product_info:
            print(f"❌ 产品 '{product_name}' 不存在")
            return False

        product_id = product_info[0]

        if self.update_stock_with_deadlock_retry(product_id, quantity):
            print(f"✅ 成功补充 {quantity} 个 '{product_name}' 库存")
            return True
        else:
            return False

    def simulate_concurrent_operations(self):
        """模拟并发库存操作"""
        print("📦 开始模拟并发库存操作...")
        print("=" * 50)

        # 显示初始库存
        products = ["iPhone 15", "MacBook Pro", "AirPods Pro", "iPad Air"]
        print("初始库存:")
        for product in products:
            info = self.get_product_info(product)
            if info:
                print(f"- {product}: {info[1]} 件 (¥{info[2]:.2f})")
        print()

        def order_task(product_name: str, quantity: int):
            """下单任务"""
            time.sleep(random.uniform(0.1, 0.5))
            self.process_order(product_name, quantity)

        def restock_task(product_name: str, quantity: int):
            """补货任务"""
            time.sleep(random.uniform(0.2, 0.6))
            self.restock_product(product_name, quantity)

        # 定义并发任务
        tasks = [
            # 下单任务
            ("order", "iPhone 15", 10),
            ("order", "MacBook Pro", 5),
            ("order", "AirPods Pro", 20),
            ("order", "iPad Air", 8),
            # 补货任务
            ("restock", "iPhone 15", 15),
            ("restock", "AirPods Pro", 30),
            # 更多下单任务（可能触发死锁）
            ("order", "iPhone 15", 8),
            ("order", "MacBook Pro", 3),
        ]

        # 创建并启动线程
        threads = []
        for task_type, product_name, quantity in tasks:
            if task_type == "order":
                thread = threading.Thread(target=order_task, args=(product_name, quantity))
            else:
                thread = threading.Thread(target=restock_task, args=(product_name, quantity))
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        # 显示最终库存
        print("\n📊 最终库存:")
        total_value = 0
        for product in products:
            info = self.get_product_info(product)
            if info:
                stock, price = info[1], info[2]
                value = stock * price
                total_value += value
                print(f"- {product}: {stock} 件 (¥{price:.2f}) = ¥{value:.2f}")

        print(f"\n💰 库存总价值: ¥{total_value:.2f}")

        # 统计订单数量
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'completed'")
        completed_orders = cursor.fetchone()[0]
        conn.close()

        print(f"📋 完成订单数量: {completed_orders} 笔")


def main():
    """主函数"""
    inventory = InventorySystem()
    inventory.simulate_concurrent_operations()


if __name__ == "__main__":
    main()