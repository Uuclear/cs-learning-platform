// solution-03.js - 示例3的解答：值类型vs引用类型的区别

// 这个解决方案提供了处理值类型和引用类型的最佳实践

/**
 * 深拷贝函数 - 处理嵌套对象和数组
 * 注意：这个简单版本不处理循环引用、函数、Symbol等复杂情况
 * @param {*} obj - 要深拷贝的对象
 * @returns {*} - 深拷贝后的对象
 */
function deepClone(obj) {
    // 处理基本类型和null
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }

    // 处理日期对象
    if (obj instanceof Date) {
        return new Date(obj.getTime());
    }

    // 处理数组
    if (Array.isArray(obj)) {
        return obj.map(item => deepClone(item));
    }

    // 处理普通对象
    const cloned = {};
    for (let key in obj) {
        if (obj.hasOwnProperty(key)) {
            cloned[key] = deepClone(obj[key]);
        }
    }
    return cloned;
}

/**
 * 安全的对象合并函数
 * 避免直接修改原对象
 */
function safeMerge(base, overrides) {
    return {
        ...base,
        ...overrides
    };
}

console.log("=== 值类型 vs 引用类型最佳实践 ===");

// 1. 不可变数据操作示例
const originalUser = {
    name: "张三",
    profile: {
        email: "zhang@example.com",
        settings: {
            theme: "light",
            notifications: true
        }
    },
    hobbies: ["读书", "游泳"]
};

// 错误做法：直接修改
// originalUser.profile.email = "new@example.com"; // 会修改原对象

// 正确做法：使用展开运算符创建新对象
const updatedUser = {
    ...originalUser,
    profile: {
        ...originalUser.profile,
        email: "new@example.com",
        settings: {
            ...originalUser.profile.settings,
            theme: "dark"
        }
    },
    hobbies: [...originalUser.hobbies, "编程"] // 添加新爱好
};

console.log("原用户邮箱:", originalUser.profile.email);
console.log("更新后邮箱:", updatedUser.profile.email);
console.log("原用户主题:", originalUser.profile.settings.theme);
console.log("更新后主题:", updatedUser.profile.settings.theme);
console.log("原用户爱好:", originalUser.hobbies.join(", "));
console.log("更新后爱好:", updatedUser.hobbies.join(", "));

// 2. 函数参数的不可变处理
function updateUserSettings(user, newSettings) {
    // 返回新对象，不修改原对象
    return {
        ...user,
        profile: {
            ...user.profile,
            settings: {
                ...user.profile.settings,
                ...newSettings
            }
        }
    };
}

const userWithNewSettings = updateUserSettings(originalUser, {
    theme: "blue",
    language: "zh-CN"
});

console.log("添加语言设置后:", userWithNewSettings.profile.settings.language);

// 3. 数组的不可变操作
const originalItems = [1, 2, 3, 4, 5];

// 不可变方式添加元素
const itemsWithNew = [...originalItems, 6];
console.log("原数组:", originalItems.join(", "));
console.log("新数组:", itemsWithNew.join(", "));

// 不可变方式修改元素
const itemsModified = [
    ...originalItems.slice(0, 2),
    99,
    ...originalItems.slice(3)
];
console.log("修改第3个元素:", itemsModified.join(", "));

// 不可变方式删除元素
const itemsWithoutThird = [
    ...originalItems.slice(0, 2),
    ...originalItems.slice(3)
];
console.log("删除第3个元素:", itemsWithoutThird.join(", "));

// 4. 深拷贝的实际应用
const complexObject = {
    id: 1,
    data: {
        users: [
            { name: "用户1", roles: ["admin", "user"] },
            { name: "用户2", roles: ["user"] }
        ],
        config: {
            api: "https://api.example.com",
            timeout: 5000
        }
    }
};

const clonedComplex = deepClone(complexObject);
clonedComplex.data.users[0].roles.push("moderator");
clonedComplex.data.config.timeout = 10000;

console.log("原对象超时:", complexObject.data.config.timeout);
console.log("克隆对象超时:", clonedComplex.data.config.timeout);
console.log("原对象用户1角色:", complexObject.data.users[0].roles.join(", "));
console.log("克隆对象用户1角色:", clonedComplex.data.users[0].roles.join(", "));

// 5. 实际开发中的模式
// 使用const声明所有变量，即使它们包含可变对象
// 这样可以防止意外的重新赋值
const CONFIG = {
    API_BASE: "https://api.example.com",
    DEFAULT_TIMEOUT: 5000
};

// 如果需要修改配置，创建新对象
const PROD_CONFIG = {
    ...CONFIG,
    API_BASE: "https://prod-api.example.com"
};

console.log("开发配置:", CONFIG.API_BASE);
console.log("生产配置:", PROD_CONFIG.API_BASE);

console.log("\n=== 关键原则总结 ===");
console.log("1. 基本类型：按值传递，修改互不影响");
console.log("2. 引用类型：按引用传递，修改会影响所有引用");
console.log("3. 使用展开运算符(...)进行浅拷贝");
console.log("4. 复杂嵌套对象需要深拷贝");
console.log("5. 优先使用不可变操作模式");
console.log("6. 函数应该返回新对象而不是修改参数");

console.log("\n=== 解答结束 ===");