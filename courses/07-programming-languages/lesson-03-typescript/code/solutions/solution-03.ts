// 编程挑战3解答：实现类型安全的事件发射器

// 事件监听器类型
type EventListener<T> = (data: T) => void;

// 事件映射接口，用于定义事件名称和对应的数据类型
interface EventMap {
  [eventName: string]: any;
}

// 泛型事件发射器类
class EventEmitter<Events extends EventMap> {
  private listeners: Map<keyof Events, Set<EventListener<any>>> = new Map();

  // 订阅事件
  on<EventName extends keyof Events>(
    eventName: EventName,
    listener: EventListener<Events[EventName]>
  ): void {
    if (!this.listeners.has(eventName)) {
      this.listeners.set(eventName, new Set());
    }
    this.listeners.get(eventName)!.add(listener);
  }

  // 取消订阅事件
  off<EventName extends keyof Events>(
    eventName: EventName,
    listener: EventListener<Events[EventName]>
  ): void {
    const listeners = this.listeners.get(eventName);
    if (listeners) {
      listeners.delete(listener);
      if (listeners.size === 0) {
        this.listeners.delete(eventName);
      }
    }
  }

  // 发射事件
  emit<EventName extends keyof Events>(
    eventName: EventName,
    data: Events[EventName]
  ): void {
    const listeners = this.listeners.get(eventName);
    if (listeners) {
      listeners.forEach(listener => listener(data));
    }
  }

  // 获取事件监听器数量
  listenerCount<EventName extends keyof Events>(eventName: EventName): number {
    return this.listeners.get(eventName)?.size || 0;
  }

  // 清空所有监听器
  removeAllListeners(): void {
    this.listeners.clear();
  }
}

// 定义具体的应用事件类型
interface AppEvents {
  'user-login': { userId: number; username: string; timestamp: Date };
  'user-logout': { userId: number; timestamp: Date };
  'error': { code: string; message: string; context?: any };
  'notification': { title: string; body: string; priority: 'low' | 'medium' | 'high' };
}

// 创建类型安全的事件发射器实例
const appEmitter = new EventEmitter<AppEvents>();

// 订阅事件（类型安全）
appEmitter.on('user-login', (data) => {
  console.log(`用户登录: ${data.username} (ID: ${data.userId}) at ${data.timestamp}`);
});

appEmitter.on('user-logout', (data) => {
  console.log(`用户登出: ID ${data.userId} at ${data.timestamp}`);
});

appEmitter.on('error', (data) => {
  console.log(`错误发生: [${data.code}] ${data.message}`);
  if (data.context) {
    console.log(`上下文:`, data.context);
  }
});

appEmitter.on('notification', (data) => {
  console.log(`通知: [${data.priority.toUpperCase()}] ${data.title} - ${data.body}`);
});

// 发射事件（类型安全）
appEmitter.emit('user-login', {
  userId: 123,
  username: '张三',
  timestamp: new Date()
});

appEmitter.emit('notification', {
  title: '欢迎使用TypeScript',
  body: '类型安全让编程更可靠！',
  priority: 'high'
});

appEmitter.emit('error', {
  code: 'TS001',
  message: '类型检查错误',
  context: { file: 'example.ts', line: 42 }
});

console.log(`用户登录事件监听器数量: ${appEmitter.listenerCount('user-login')}`);
console.log(`错误事件监听器数量: ${appEmitter.listenerCount('error')}`);