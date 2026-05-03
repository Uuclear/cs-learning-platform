// example-01.js - ES Modules import/export示例
// 这个示例展示了ES Modules的基本用法

// utils.js - 工具函数模块
export function formatDate(date) {
  return date.toLocaleDateString('zh-CN');
}

export function formatTime(date) {
  return date.toLocaleTimeString('zh-CN');
}

// 默认导出一个配置对象
export default {
  appName: '我的应用',
  version: '1.0.0',
  debug: true
};

// main.js - 主程序文件
import config, { formatDate, formatTime } from './utils.js';

console.log('=== ES Modules 示例 ===');
console.log('应用名称:', config.appName);
console.log('当前日期:', formatDate(new Date()));
console.log('当前时间:', formatTime(new Date()));

// 命名空间导入示例
import * as utils from './utils.js';
console.log('通过命名空间访问:', utils.formatDate(new Date()));

// 动态导入示例
async function loadModuleDynamically() {
  const { formatDate } = await import('./utils.js');
  console.log('动态导入结果:', formatDate(new Date()));
}

loadModuleDynamically();