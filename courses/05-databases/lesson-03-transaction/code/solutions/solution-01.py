#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1: 票务预订系统

实现一个防止超卖的票务系统，使用数据库事务确保库存一致性。
"""

import sqlite3
import threading
import time
import random
import os


class TicketBookingSystem:
    def __init__(self, db_path='tickets.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化数据库"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建演出表
        cursor.execute('''
            CREATE TABLE events (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                total_tickets INTEGER NOT NULL,
                available_tickets INTEGER NOT NULL
            )
        ''')

        # 创建订单表
        cursor.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                ticket_count INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (event_id) REFERENCES events(id)
            )
        ''')

        # 插入测试数据
        cursor.execute(
            "INSERT INTO events (name, total_tickets, available_tickets) VALUES (?, ?, ?)",
            ("周杰伦演唱会", 100, 100)
        )

        conn.commit()
        conn.close()

    def book_tickets(self, event_id, customer_name, ticket_count):
        """
        预订门票 - 使用事务确保不会超卖

        Args:
            event_id: 演出ID
            customer_name: 顾客姓名
            ticket_count: 预订数量

        Returns:
            bool: 是否预订成功
        """
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("BEGIN")

            # 检查可用票数（在事务中锁定行）
            cursor = conn.execute(
                "SELECT available_tickets FROM events WHERE id = ? FOR UPDATE",
                (event_id,)
            )
            row = cursor.fetchone()

            if not row:
                print(f"❌ 演出 {event_id} 不存在")
                return False

            available = row[0]

            if available < ticket_count:
                print(f"❌ 票数不足！剩余 {available} 张，需要 {ticket_count} 张")
                return False

            # 创建订单
            cursor = conn.execute(
                "INSERT INTO orders (event_id, customer_name, ticket_count, status) VALUES (?, ?, ?, ?)",
                (event_id, customer_name, ticket_count, 'confirmed')
            )
            order_id = cursor.lastrowid

            # 更新可用票数
            conn.execute(
                "UPDATE events SET available_tickets = available_tickets - ? WHERE id = ?",
                (ticket_count, event_id)
            )

            conn.commit()
            print(f"✅ 顾客 {customer_name} 成功预订 {ticket_count} 张票 (订单ID: {order_id})")
            return True

        except Exception as e:
            conn.rollback()
            print(f"❌ 预订失败: {e}")
            return False
        finally:
            conn.close()

    def get_event_info(self, event_id):
        """获取演出信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT name, total_tickets, available_tickets FROM events WHERE id = ?",
            (event_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return row

    def simulate_concurrent_bookings(self):
        """模拟并发预订场景"""
        print("🎭 开始模拟并发票务预订...")
        print("=" * 50)

        # 显示初始状态
        event_info = self.get_event_info(1)
        print(f"演出: {event_info[0]}")
        print(f"总票数: {event_info[1]}, 可用票数: {event_info[2]}")
        print()

        def booking_thread(customer_name, ticket_count):
            """预订线程"""
            # 随机延迟模拟网络延迟
            time.sleep(random.uniform(0.1, 0.5))
            self.book_tickets(1, customer_name, ticket_count)

        # 创建多个预订线程
        customers = [
            ("张三", 20),
            ("李四", 30),
            ("王五", 25),
            ("赵六", 15),
            ("钱七", 10)
        ]

        threads = []
        for customer_name, ticket_count in customers:
            thread = threading.Thread(
                target=booking_thread,
                args=(customer_name, ticket_count)
            )
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        # 显示最终状态
        print("\n📊 最终状态:")
        event_info = self.get_event_info(1)
        print(f"演出: {event_info[0]}")
        print(f"总票数: {event_info[1]}, 可用票数: {event_info[2]}")

        # 查询所有成功订单
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT customer_name, ticket_count FROM orders WHERE status = 'confirmed'"
        )
        orders = cursor.fetchall()
        conn.close()

        print(f"\n📝 成功订单 ({len(orders)} 笔):")
        total_sold = 0
        for customer, count in orders:
            print(f"- {customer}: {count} 张")
            total_sold += count

        print(f"\n总计售出: {total_sold} 张")
        print(f"验证: 总票数({event_info[1]}) - 可用票数({event_info[2]}) = {event_info[1] - event_info[2]} 张")


def main():
    """主函数"""
    system = TicketBookingSystem()
    system.simulate_concurrent_bookings()


if __name__ == "__main__":
    main()