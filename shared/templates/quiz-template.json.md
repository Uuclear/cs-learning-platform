# 选择题模板

```json
{
  "questions": [
    {
      "id": 1,
      "type": "single_choice",
      "question": "问题内容",
      "options": [
        "选项A",
        "选项B",
        "选项C",
        "选项D"
      ],
      "correct": 0,
      "explanation": "答案解析，解释为什么选这个",
      "difficulty": 1
    },
    {
      "id": 2,
      "type": "single_choice",
      "question": "问题内容",
      "options": [
        "选项A",
        "选项B",
        "选项C",
        "选项D"
      ],
      "correct": 2,
      "explanation": "答案解析",
      "difficulty": 2
    },
    {
      "id": 3,
      "type": "true_false",
      "question": "判断题内容",
      "correct": true,
      "explanation": "答案解析",
      "difficulty": 1
    }
  ],
  "metadata": {
    "total_questions": 3,
    "difficulty_distribution": {
      "easy": 1,
      "medium": 1,
      "hard": 1
    }
  }
}
```

## 题型说明

| 类型 | type值 | 说明 |
|------|--------|------|
| 单选题 | single_choice | 四个选项，选唯一正确答案 |
| 判断题 | true_false | 正确/错误 |
| 多选题 | multiple_choice | 多个正确答案 |

## 难度等级

| 等级 | 说明 |
|------|------|
| 1 | 基础概念，直接记忆 |
| 2 | 简单应用，需要理解 |
| 3 | 综合应用，需要分析 |
| 4 | 复杂问题，需要推理 |
| 5 | 开放性问题，需要深度思考 |
