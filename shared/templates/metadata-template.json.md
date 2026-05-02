# 课程元数据模板

```json
{
  "id": "XX-YY",
  "title": "课程标题",
  "slug": "lesson-xx-course-name",
  "module": "XX-module-name",
  "module_name": "模块中文名",
  "module_order": 1,
  "lesson_order": 1,
  "difficulty": 2,
  "difficulty_label": "简单",
  "duration_minutes": 20,
  "prerequisites": ["XX-YY"],
  "tags": ["tag1", "tag2", "tag3"],
  "author": "sub-agent",
  "created_at": "2026-05-03",
  "updated_at": "2026-05-03",
  "status": "completed",
  "description": "课程简短描述",
  "learning_objectives": [
    "学习目标1",
    "学习目标2",
    "学习目标3"
  ],
  "files": {
    "main_content": "index.mdx",
    "code_examples": 3,
    "exercises": {
      "quiz_questions": 5,
      "programming_challenges": 3
    }
  }
}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 课程唯一标识，格式"模块号-课号" |
| title | string | 课程标题 |
| slug | string | URL友好的标识 |
| module | string | 模块标识 |
| module_name | string | 模块中文名 |
| module_order | number | 模块排序 |
| lesson_order | number | 课程在模块内的排序 |
| difficulty | number | 难度等级1-5 |
| difficulty_label | string | 难度标签 |
| duration_minutes | number | 预计学习时长 |
| prerequisites | array | 前置课程ID列表 |
| tags | array | 标签列表 |
| author | string | 作者 |
| created_at | string | 创建日期 |
| updated_at | string | 更新日期 |
| status | string | 状态：draft/completed/review |
| description | string | 课程描述 |
| learning_objectives | array | 学习目标列表 |
| files | object | 文件统计信息 |
