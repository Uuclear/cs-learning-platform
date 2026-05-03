// solution-03.js - 闭包在实际场景中的应用解决方案

console.log("=== 闭包实际应用场景解决方案 ===\n");

// 1. 计数器工厂
console.log("1. 计数器工厂:");

function createCounterFactory() {
  let globalCount = 0; // 全局计数器

  return function(initialValue = 0) {
    let localCount = initialValue; // 每个计数器的本地计数

    return {
      increment: () => {
        globalCount++;
        localCount++;
        return localCount;
      },
      getLocalCount: () => localCount,
      getGlobalCount: () => globalCount
    };
  };
}

const counterFactory = createCounterFactory();
const counter1 = counterFactory(10);
const counter2 = counterFactory(20);

console.log("计数器1递增:", counter1.increment()); // 11
console.log("计数器2递增:", counter2.increment()); // 21
console.log("全局计数:", counter1.getGlobalCount()); // 2 (两个increment调用)

// 2. 配置化工厂函数
console.log("\n2. 配置化工厂函数:");

function createApiRequester(baseUrl, defaultHeaders = {}) {
  return function(endpoint, options = {}) {
    const url = `${baseUrl}${endpoint}`;
    const headers = { ...defaultHeaders, ...options.headers };

    console.log("请求URL:", url);
    console.log("请求头:", headers);

    // 实际应用中这里会返回fetch调用
    return {
      url,
      headers,
      method: options.method || 'GET'
    };
  };
}

const githubApi = createApiRequester('https://api.github.com', {
  'User-Agent': 'MyApp/1.0',
  'Accept': 'application/vnd.github.v3+json'
});

const userRequest = githubApi('/users/octocat', { method: 'GET' });
const repoRequest = githubApi('/repos/octocat/Hello-World', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
});

// 3. 缓存函数（记忆化）
console.log("\n3. 缓存函数（记忆化）:");

function memoize(fn) {
  const cache = new Map();

  return function(...args) {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      console.log(`缓存命中: ${key}`);
      return cache.get(key);
    }

    console.log(`计算: ${key}`);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// 费时的计算函数
const fibonacci = memoize(function(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});

console.log("斐波那契(10):", fibonacci(10));
console.log("斐波那契(10)再次:", fibonacci(10)); // 从缓存获取

// 4. 事件处理器工厂
console.log("\n4. 事件处理器工厂:");

function createEventHandler(context, handlerName) {
  return function(event) {
    console.log(`处理事件: ${handlerName}`);
    console.log(`上下文:`, context);
    console.log(`事件类型: ${event.type}`);

    // 实际应用中会调用具体的处理逻辑
    return { handled: true, context, event };
  };
}

// 模拟事件对象
const clickEvent = { type: 'click', target: 'button' };
const submitEvent = { type: 'submit', target: 'form' };

const buttonHandler = createEventHandler({ page: 'home', user: 'guest' }, '按钮点击');
const formHandler = createEventHandler({ page: 'contact', user: 'guest' }, '表单提交');

buttonHandler(clickEvent);
formHandler(submitEvent);

// 5. 私有模块模式
console.log("\n5. 私有模块模式:");

const MathUtils = (function() {
  // 私有变量和函数
  const PI = Math.PI;
  const precision = 2;

  function round(value) {
    return Math.round(value * Math.pow(10, precision)) / Math.pow(10, precision);
  }

  // 公共API
  return {
    circleArea: function(radius) {
      return round(PI * radius * radius);
    },

    circleCircumference: function(radius) {
      return round(2 * PI * radius);
    },

    getPrecision: function() {
      return precision;
    }
  };
})();

console.log("圆面积(5):", MathUtils.circleArea(5));
console.log("圆周长(5):", MathUtils.circleCircumference(5));
console.log("精度:", MathUtils.getPrecision());
// console.log(MathUtils.PI); // undefined (私有)