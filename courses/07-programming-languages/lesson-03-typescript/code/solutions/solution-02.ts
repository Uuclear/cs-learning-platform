// 编程挑战2解答：实现泛型缓存类

// 泛型缓存接口
interface CacheItem<T> {
  value: T;
  expiry: number; // 过期时间戳（毫秒）
}

// 泛型缓存类
class Cache<T> {
  private storage: Map<string, CacheItem<T>> = new Map();

  // 设置缓存项，可选过期时间（秒）
  set(key: string, value: T, ttlSeconds?: number): void {
    const expiry = ttlSeconds
      ? Date.now() + (ttlSeconds * 1000)
      : Infinity; // 如果没有设置过期时间，则永不过期

    this.storage.set(key, { value, expiry });
  }

  // 获取缓存项
  get(key: string): T | undefined {
    const item = this.storage.get(key);

    if (!item) {
      return undefined;
    }

    // 检查是否过期
    if (item.expiry < Date.now()) {
      this.storage.delete(key); // 清除过期项
      return undefined;
    }

    return item.value;
  }

  // 删除缓存项
  delete(key: string): boolean {
    return this.storage.delete(key);
  }

  // 检查缓存项是否存在且未过期
  has(key: string): boolean {
    const item = this.storage.get(key);
    if (!item) {
      return false;
    }

    if (item.expiry < Date.now()) {
      this.storage.delete(key);
      return false;
    }

    return true;
  }

  // 清空所有缓存
  clear(): void {
    this.storage.clear();
  }

  // 获取缓存大小
  size(): number {
    // 清理过期项并返回有效项数量
    let count = 0;
    for (const [key, item] of this.storage.entries()) {
      if (item.expiry >= Date.now()) {
        count++;
      } else {
        this.storage.delete(key);
      }
    }
    return count;
  }
}

// 使用示例
const stringCache = new Cache<string>();
stringCache.set("greeting", "Hello TypeScript!", 5); // 5秒后过期
stringCache.set("permanent", "This never expires");

const numberCache = new Cache<number>();
numberCache.set("count", 42);
numberCache.set("timeoutValue", 100, 3); // 3秒后过期

console.log("字符串缓存:");
console.log(`问候语: ${stringCache.get("greeting")}`);
console.log(`永久值: ${stringCache.get("permanent")}`);
console.log(`缓存大小: ${stringCache.size()}`);

console.log("\n数字缓存:");
console.log(`计数: ${numberCache.get("count")}`);
console.log(`超时值: ${numberCache.get("timeoutValue")}`);

// 等待3秒后再次检查
setTimeout(() => {
  console.log("\n3秒后检查缓存:");
  console.log(`超时值（应为undefined）: ${numberCache.get("timeoutValue")}`);
  console.log(`缓存大小: ${numberCache.size()}`);
}, 3000);