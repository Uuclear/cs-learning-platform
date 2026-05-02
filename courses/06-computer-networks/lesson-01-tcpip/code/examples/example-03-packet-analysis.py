#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 数据包头部分析

演示如何解析网络数据包的IP头部信息。
虽然实际应用中很少需要手动解析，但了解这些底层结构有助于理解网络协议。
"""

import socket
import struct

def analyze_ip_packet(packet_data):
    """
    分析IP数据包头部

    IP头部结构（20字节最小）：
    - 版本(4位) + 头部长度(4位)
    - 服务类型(8位)
    - 总长度(16位)
    - 标识(16位)
    - 标志(3位) + 片偏移(13位)
    - 生存时间TTL(8位)
    - 协议(8位)
    - 头部校验和(16位)
    - 源IP地址(32位)
    - 目标IP地址(32位)
    """
    # 确保有足够的数据进行分析
    if len(packet_data) < 20:
        print("错误：数据包太短，无法分析IP头部")
        return

    # 提取IP头部（前20字节）
    ip_header = packet_data[:20]

    # 使用struct.unpack解析二进制数据
    # '!BBHHHBBH4s4s' 表示：
    # ! = 网络字节序（大端）
    # B = unsigned char (1字节)
    # H = unsigned short (2字节)
    # 4s = 4字节字符串
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

    # 解析各个字段
    version_ihl = iph[0]  # 版本 + 头部长度
    version = version_ihl >> 4  # 高4位是版本号
    ihl = version_ihl & 0xF     # 低4位是头部长度（以32位字为单位）

    tos = iph[1]           # 服务类型
    total_length = iph[2]  # 总长度
    identification = iph[3]  # 标识
    flags_frag = iph[4]    # 标志 + 片偏移
    ttl = iph[5]           # 生存时间
    protocol = iph[6]      # 协议类型
    checksum = iph[7]      # 头部校验和
    src_addr = socket.inet_ntoa(iph[8])  # 源IP地址
    dst_addr = socket.inet_ntoa(iph[9])  # 目标IP地址

    # 打印分析结果
    print("=" * 50)
    print("IP数据包头部分析结果")
    print("=" * 50)
    print(f"IP版本: IPv{version}")
    print(f"头部长度: {ihl * 4} 字节 ({ihl}个32位字)")
    print(f"服务类型(TOS): {tos}")
    print(f"总长度: {total_length} 字节")
    print(f"标识: {identification}")
    print(f"标志+片偏移: {flags_frag}")
    print(f"生存时间(TTL): {ttl}")
    print(f"协议类型: {protocol} ({get_protocol_name(protocol)})")
    print(f"头部校验和: 0x{checksum:04X}")
    print(f"源IP地址: {src_addr}")
    print(f"目标IP地址: {dst_addr}")
    print("=" * 50)

def get_protocol_name(protocol_num):
    """根据协议号返回协议名称"""
    protocol_names = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        2: "IGMP",
        89: "OSPF"
    }
    return protocol_names.get(protocol_num, f"未知({protocol_num})")

def create_mock_ip_packet():
    """
    创建模拟的IP数据包用于演示
    实际的数据包捕获需要特殊权限（如root）和专门的库（如scapy）
    """
    print("创建模拟IP数据包用于演示...")

    # 构造IP头部字段
    version = 4          # IPv4
    ihl = 5              # 标准IP头部长度（5个32位字 = 20字节）
    version_ihl = (version << 4) | ihl

    tos = 0              # 服务类型
    total_length = 40    # 总长度（头部20字节 + 数据20字节）
    identification = 54321  # 随机标识
    flags_frag = 0       # 不分片
    ttl = 64             # 生存时间
    protocol = 6         # TCP协议
    checksum = 0x1234    # 模拟校验和（实际计算很复杂）

    # IP地址（转换为二进制格式）
    src_ip = socket.inet_aton('192.168.1.100')  # 源IP
    dst_ip = socket.inet_aton('8.8.8.8')        # 目标IP（Google DNS）

    # 打包成二进制数据
    ip_header = struct.pack('!BBHHHBBH4s4s',
                           version_ihl, tos, total_length,
                           identification, flags_frag, ttl,
                           protocol, checksum, src_ip, dst_ip)

    # 添加一些模拟的数据
    data = b"Hello, IP Packet!" + b"\x00" * 3  # 填充到20字节

    return ip_header + data

def main():
    """主函数：创建模拟数据包并分析"""
    # 创建模拟IP数据包
    mock_packet = create_mock_ip_packet()

    # 分析数据包
    analyze_ip_packet(mock_packet)

    print("\n注意：实际的网络数据包分析通常使用Wireshark等专业工具，")
    print("或使用scapy等Python库进行实时抓包分析。")

if __name__ == "__main__":
    main()