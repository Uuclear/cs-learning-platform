// solution-02.js - 文件操作解决方案
// 这是练习2的完整解决方案

import { readFile, writeFile, mkdir, access } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

class FileManager {
  constructor(baseDir = 'data') {
    this.baseDir = join(__dirname, baseDir);
  }

  async init() {
    try {
      await mkdir(this.baseDir, { recursive: true });
      console.log('✅ 文件管理器初始化成功');
    } catch (error) {
      console.error('❌ 初始化失败:', error.message);
      throw error;
    }
  }

  async saveUser(user) {
    const filePath = join(this.baseDir, `user-${user.id}.json`);
    await writeFile(filePath, JSON.stringify(user, null, 2), 'utf8');
    console.log(`✅ 用户 ${user.name} 保存成功`);
    return filePath;
  }

  async loadUser(userId) {
    const filePath = join(this.baseDir, `user-${userId}.json`);
    try {
      await access(filePath); // 检查文件是否存在
      const content = await readFile(filePath, 'utf8');
      return JSON.parse(content);
    } catch (error) {
      if (error.code === 'ENOENT') {
        console.log(`⚠️  用户 ${userId} 不存在`);
        return null;
      }
      throw error;
    }
  }

  async backupData() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupDir = join(this.baseDir, `backup-${timestamp}`);

    await mkdir(backupDir, { recursive: true });

    // 这里简化处理，实际应用中可能需要复制所有文件
    const sampleUser = { id: 'backup-test', name: '备份测试', timestamp };
    await writeFile(join(backupDir, 'backup-info.json'), JSON.stringify(sampleUser, null, 2), 'utf8');

    console.log(`✅ 备份创建成功: ${backupDir}`);
    return backupDir;
  }
}

async function demonstrateSolution() {
  console.log('=== 文件操作练习解决方案 ===');

  const fileManager = new FileManager();

  try {
    // 初始化
    await fileManager.init();

    // 创建用户数据
    const user1 = { id: 1, name: '李明', email: 'liming@example.com', age: 28 };
    const user2 = { id: 2, name: '王芳', email: 'wangfang@example.com', age: 32 };

    // 保存用户
    await fileManager.saveUser(user1);
    await fileManager.saveUser(user2);

    // 加载用户
    const loadedUser1 = await fileManager.loadUser(1);
    const loadedUser2 = await fileManager.loadUser(2);
    const nonExistentUser = await fileManager.loadUser(999);

    console.log('\n加载的用户数据:');
    console.log('用户1:', loadedUser1);
    console.log('用户2:', loadedUser2);
    console.log('不存在的用户:', nonExistentUser);

    // 创建备份
    await fileManager.backupData();

  } catch (error) {
    console.error('❌ 操作失败:', error.message);
  }
}

demonstrateSolution();