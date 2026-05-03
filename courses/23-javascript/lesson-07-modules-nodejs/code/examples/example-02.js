// example-02.js - Node.js fs模块和文件操作
// 这个示例展示了Node.js文件系统模块的基本用法

import { readFile, writeFile, mkdir, readdir, stat } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

// 获取当前文件目录（兼容ESM）
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function demonstrateFileOperations() {
  console.log('=== Node.js 文件系统操作示例 ===');

  try {
    // 1. 创建目录
    const dataDir = join(__dirname, 'data');
    await mkdir(dataDir, { recursive: true });
    console.log('✅ 创建目录:', dataDir);

    // 2. 写入文件
    const sampleData = {
      name: '张三',
      age: 25,
      hobbies: ['编程', '阅读', '音乐']
    };

    const filePath = join(dataDir, 'user.json');
    await writeFile(filePath, JSON.stringify(sampleData, null, 2), 'utf8');
    console.log('✅ 写入文件:', filePath);

    // 3. 读取文件
    const fileContent = await readFile(filePath, 'utf8');
    const userData = JSON.parse(fileContent);
    console.log('✅ 读取文件内容:', userData);

    // 4. 列出目录内容
    const files = await readdir(dataDir);
    console.log('📁 目录内容:', files);

    // 5. 获取文件信息
    const fileInfo = await stat(filePath);
    console.log('📊 文件信息:');
    console.log('  大小:', fileInfo.size, '字节');
    console.log('  是否为文件:', fileInfo.isFile());
    console.log('  是否为目录:', fileInfo.isDirectory());
    console.log('  修改时间:', new Date(fileInfo.mtime).toLocaleString('zh-CN'));

  } catch (error) {
    console.error('❌ 文件操作错误:', error.message);
  }
}

demonstrateFileOperations();