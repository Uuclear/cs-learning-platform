# 挑战 2：递归与作用域综合应用

## 目标
实现一个文件系统模拟器，使用递归函数处理目录结构，并正确管理变量作用域。

## 要求
1. 创建一个表示文件系统节点的结构体：
   ```c
   typedef struct Node {
       char name[100];
       int is_directory;
       struct Node* children[10];  // 最多10个子节点
       int child_count;
   } Node;
   ```

2. 实现以下函数：
   - `Node* create_node(const char* name, int is_dir)` - 创建新节点
   - `void add_child(Node* parent, Node* child)` - 添加子节点
   - `void print_tree_recursive(Node* root, int depth)` - 递归打印目录树（带缩进）
   - `int count_files_recursive(Node* root)` - 递归计算文件总数
   - `int find_node_depth(Node* root, const char* target_name, int current_depth)` - 查找指定名称节点的深度

3. 在main函数中构建一个示例文件系统结构：
   ```
   root/
   ├── documents/
   │   ├── resume.txt
   │   └── notes.txt
   ├── pictures/
   │   ├── vacation/
   │   │   ├── beach.jpg
   │   │   └── mountain.jpg
   │   └── profile.png
   └── program.c
   ```

4. 使用static变量在`print_tree_recursive`函数中记录总的调用次数

5. 确保正确处理内存分配和释放（可选，但推荐）

## 提示
- 使用递归处理树形结构非常自然
- 在`print_tree_recursive`中，depth参数用于控制缩进级别
- 注意边界情况：空树、不存在的节点等
- static变量可以用来跟踪函数被调用的总次数，展示其持久性

## 扩展挑战（可选）
- 实现路径查找功能：给定路径字符串"/documents/resume.txt"，找到对应的节点
- 添加删除功能，能够安全地删除节点及其所有子节点
- 实现一个函数统计每个目录中的文件数量

## 评估标准
- ✅ 正确使用递归处理树形结构
- ✅ 合理运用作用域概念（局部变量、static变量）
- ✅ 代码结构清晰，函数职责单一
- ✅ 正确处理各种边界情况
- ✅ 输出格式美观，易于理解
