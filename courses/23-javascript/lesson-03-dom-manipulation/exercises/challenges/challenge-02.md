# 编程挑战 2：实时表单验证器

## 任务描述
创建一个实时表单验证器，能够在用户输入时提供即时反馈，并在提交时进行最终验证。

## 具体要求

### 表单字段
创建包含以下字段的表单：
1. **用户名**：3-20个字符，只能包含字母、数字和下划线
2. **邮箱**：有效的邮箱格式
3. **密码**：至少8个字符，包含大小写字母和数字
4. **确认密码**：必须与密码字段完全一致
5. **年龄**：18-100之间的整数

### 实时验证功能
1. **输入时验证**：当用户离开每个字段时（blur事件），立即验证并显示反馈
2. **视觉反馈**：
   - 有效：绿色边框 + ✓ 图标
   - 无效：红色边框 + ✗ 图标 + 错误消息
3. **提交验证**：点击提交按钮时，验证所有字段，只有全部有效才能提交

### HTML结构要求
- 表单容器：`<form id="registration-form">`
- 每个字段包装：`<div class="form-group">`
- 输入字段：`<input type="text" id="username" name="username">`
- 反馈元素：`<span class="feedback"></span>`
- 提交按钮：`<button type="submit" id="submit-btn">注册</button>`

### 验证规则实现
使用正则表达式实现验证逻辑：

```javascript
// 用户名验证：3-20字符，字母数字下划线
const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;

// 邮箱验证
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// 密码验证：至少8位，包含大小写字母和数字
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
```

## 完整解决方案

```javascript
// 实时表单验证器完整实现
class FormValidator {
  constructor(formId) {
    this.form = document.getElementById(formId);
    this.fields = {
      username: { 
        element: null, 
        valid: false,
        regex: /^[a-zA-Z0-9_]{3,20}$/,
        message: '用户名必须是3-20个字符，只能包含字母、数字和下划线'
      },
      email: { 
        element: null, 
        valid: false,
        regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        message: '请输入有效的邮箱地址'
      },
      password: { 
        element: null, 
        valid: false,
        regex: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/,
        message: '密码至少8位，必须包含大小写字母和数字'
      },
      confirmPassword: { 
        element: null, 
        valid: false,
        message: '两次输入的密码必须一致'
      },
      age: { 
        element: null, 
        valid: false,
        message: '年龄必须是18-100之间的整数'
      }
    };

    if (this.form) {
      this.init();
    }
  }

  // 初始化表单
  init() {
    // 创建表单HTML结构
    this.createFormStructure();
    
    // 获取所有字段元素
    Object.keys(this.fields).forEach(fieldName => {
      this.fields[fieldName].element = document.getElementById(fieldName);
    });

    // 绑定事件
    this.bindEvents();

    // 应用样式
    this.applyStyles();
  }

  // 创建表单HTML结构
  createFormStructure() {
    const formGroups = [
      { id: 'username', label: '用户名', type: 'text', placeholder: '3-20个字符' },
      { id: 'email', label: '邮箱', type: 'email', placeholder: 'example@email.com' },
      { id: 'password', label: '密码', type: 'password', placeholder: '至少8位' },
      { id: 'confirmPassword', label: '确认密码', type: 'password', placeholder: '再次输入密码' },
      { id: 'age', label: '年龄', type: 'number', placeholder: '18-100' }
    ];

    formGroups.forEach(group => {
      const formGroup = document.createElement('div');
      formGroup.className = 'form-group';
      
      const label = document.createElement('label');
      label.htmlFor = group.id;
      label.textContent = group.label;
      
      const input = document.createElement('input');
      input.type = group.type;
      input.id = group.id;
      input.name = group.id;
      input.placeholder = group.placeholder;
      
      const feedback = document.createElement('span');
      feedback.className = 'feedback';
      
      formGroup.appendChild(label);
      formGroup.appendChild(input);
      formGroup.appendChild(feedback);
      this.form.appendChild(formGroup);
    });

    const submitBtn = document.createElement('button');
    submitBtn.type = 'submit';
    submitBtn.id = 'submit-btn';
    submitBtn.textContent = '注册';
    this.form.appendChild(submitBtn);
  }

  // 应用CSS样式
  applyStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .form-group {
        margin-bottom: 15px;
      }
      .form-group label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
      }
      .form-group input {
        width: 100%;
        padding: 8px;
        border: 2px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
        box-sizing: border-box;
      }
      .form-group input.valid {
        border-color: #28a745;
      }
      .form-group input.invalid {
        border-color: #dc3545;
      }
      .feedback {
        display: block;
        margin-top: 5px;
        font-size: 12px;
        min-height: 16px;
      }
      .feedback.valid::before {
        content: "✓ ";
        color: #28a745;
        font-weight: bold;
      }
      .feedback.invalid::before {
        content: "✗ ";
        color: #dc3545;
        font-weight: bold;
      }
      #submit-btn {
        padding: 10px 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
      }
      #submit-btn:disabled {
        background-color: #6c757d;
        cursor: not-allowed;
      }
    `;
    document.head.appendChild(style);
  }

  // 验证单个字段
  validateField(fieldName) {
    const field = this.fields[fieldName];
    const value = field.element.value.trim();
    let isValid = false;
    let message = '';

    switch(fieldName) {
      case 'username':
        isValid = field.regex.test(value);
        message = field.message;
        break;
        
      case 'email':
        isValid = field.regex.test(value);
        message = field.message;
        break;
        
      case 'password':
        isValid = field.regex.test(value);
        message = field.message;
        break;
        
      case 'confirmPassword':
        const passwordValue = this.fields.password.element.value;
        isValid = value === passwordValue && value.length > 0;
        message = field.message;
        break;
        
      case 'age':
        const age = parseInt(value);
        isValid = !isNaN(age) && age >= 18 && age <= 100;
        message = field.message;
        break;
        
      default:
        isValid = value.length > 0;
        message = '此字段为必填项';
    }

    field.valid = isValid;
    this.updateFieldUI(fieldName, isValid, message);
    this.updateSubmitButton();
    return isValid;
  }

  // 更新字段UI状态
  updateFieldUI(fieldName, isValid, message) {
    const field = this.fields[fieldName];
    const input = field.element;
    const feedback = input.nextElementSibling;

    // 清除之前的类
    input.classList.remove('valid', 'invalid');
    feedback.classList.remove('valid', 'invalid');

    if (input.value.trim().length > 0) {
      if (isValid) {
        input.classList.add('valid');
        feedback.classList.add('valid');
        feedback.textContent = '有效';
      } else {
        input.classList.add('invalid');
        feedback.classList.add('invalid');
        feedback.textContent = message;
      }
    } else {
      feedback.textContent = '';
    }
  }

  // 验证整个表单
  validateForm() {
    let isFormValid = true;
    
    Object.keys(this.fields).forEach(fieldName => {
      const isValid = this.validateField(fieldName);
      if (!isValid) isFormValid = false;
    });
    
    return isFormValid;
  }

  // 更新提交按钮状态
  updateSubmitButton() {
    const submitBtn = document.getElementById('submit-btn');
    const allValid = Object.values(this.fields).every(field => field.valid);
    submitBtn.disabled = !allValid;
  }

  // 绑定事件
  bindEvents() {
    // 单个字段验证（blur事件）
    Object.keys(this.fields).forEach(fieldName => {
      const element = this.fields[fieldName].element;
      element.addEventListener('blur', () => this.validateField(fieldName));
      
      // 密码确认字段需要监听密码字段的变化
      if (fieldName === 'confirmPassword') {
        this.fields.password.element.addEventListener('input', () => {
          if (element.value.trim().length > 0) {
            this.validateField('confirmPassword');
          }
        });
      }
    });

    // 表单提交事件
    this.form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (this.validateForm()) {
        alert('表单验证通过！可以提交数据。');
        // 这里可以添加实际的表单提交逻辑
        console.log('表单数据:', this.getFormData());
      }
    });
  }

  // 获取表单数据
  getFormData() {
    const data = {};
    Object.keys(this.fields).forEach(fieldName => {
      data[fieldName] = this.fields[fieldName].element.value;
    });
    return data;
  }
}

// 使用示例
// const validator = new FormValidator('registration-form');
```

## 测试说明
1. 在HTML文件中创建一个 `<form id="registration-form"></form>`
2. 引入上述JavaScript代码
3. 调用 `new FormValidator('registration-form')`
4. 测试各种输入场景，验证实时反馈是否正确

## 扩展思考
- 如何添加自定义验证规则？
- 如何支持异步验证（如检查用户名是否已存在）？
- 如何本地化错误消息以支持多语言？
- 如何将验证规则配置化，便于维护？