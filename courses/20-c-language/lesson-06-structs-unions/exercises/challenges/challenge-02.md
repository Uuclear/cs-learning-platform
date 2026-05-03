# 挑战 2：网络协议头解析器

## 目标
使用联合体和位域实现一个简单的网络协议头解析器，能够解析和显示不同格式的数据包头部信息。

## 要求

### 1. 协议头结构定义
定义以下结构体和联合体：

#### IPv4 头部结构（使用位域）
```c
struct IPv4Header {
    unsigned int version : 4;        // 版本号 (4位)
    unsigned int ihl : 4;            // 头部长度 (4位)
    unsigned int tos : 8;            // 服务类型 (8位)
    unsigned int total_length : 16;  // 总长度 (16位)
    unsigned int identification : 16;// 标识 (16位)
    unsigned int flags : 3;          // 标志 (3位)
    unsigned int fragment_offset : 13;// 分片偏移 (13位)
    unsigned int ttl : 8;            // 生存时间 (8位)
    unsigned int protocol : 8;       // 协议 (8位)
    unsigned int header_checksum : 16;// 头部校验和 (16位)
    uint32_t source_address;         // 源地址 (32位)
    uint32_t destination_address;    // 目标地址 (32位)
};
```

#### 数据包联合体
```c
union PacketData {
    struct IPv4Header ipv4;
    uint8_t raw_bytes[sizeof(struct IPv4Header)];
    uint32_t words[sizeof(struct IPv4Header) / sizeof(uint32_t)];
};
```

### 2. 功能实现
实现以下函数：
- `void parseIPv4Header(const uint8_t *raw_data)` - 解析原始字节数据并显示IPv4头部信息
- `void createTestPacket(union PacketData *packet)` - 创建一个测试数据包
- `void displayPacketInfo(union PacketData *packet)` - 显示数据包的详细信息
- `void convertEndian(union PacketData *packet)` - 处理字节序转换（网络字节序到主机字节序）

### 3. 主程序
- 创建一个测试的IPv4数据包
- 使用联合体以不同方式访问同一块数据（作为结构体、字节数组、32位整数数组）
- 显示每种访问方式的结果
- 验证位域是否正确存储了各个字段

## 提示
- 注意字节序问题（大端 vs 小端）
- 使用 `htons()`, `htonl()`, `ntohs()`, `ntohl()` 函数进行字节序转换
- 网络协议通常使用大端字节序（网络字节序）
- 联合体允许你用多种方式解释同一块内存

## 扩展挑战（可选）
- 添加TCP头部解析功能
- 实现简单的校验和计算
- 从实际网络数据包文件中读取数据进行解析

## 评估标准
- 位域定义的正确性（30%）
- 联合体使用的合理性（25%）
- 字节序处理的正确性（25%）
- 代码的健壮性和错误处理（20%）