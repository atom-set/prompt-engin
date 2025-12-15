# 代码格式规范

> **文件说明**：本文件包含 代码格式规范 相关规则
> **规则来源**：rules/stages/common/code/code-format/code-format.md

---

### 代码格式规范

#### 缩进规范

- **缩进方式**：使用 4 个空格进行缩进，不使用制表符（Tab）
- **一致性要求**：整个项目应使用统一的缩进方式
- **编辑器配置**：建议在编辑器中配置自动将 Tab 转换为空格

**示例**：

```javascript
// ✅ 好的做法：使用 4 个空格
function processData(data) {
    if (data) {
        return data.map(item => {
            return processItem(item);
        });
    }
    return null;
}

// ❌ 不好的做法：使用 Tab 或混合使用
function processData(data) {
	if (data) {  // Tab 缩进
        return data.map(item => {  // 空格缩进（不一致）
			return processItem(item);  // Tab 缩进
		});
	}
	return null;
}
```

#### 行长度规范

- **最大行长度**：每行代码不超过 80 个字符
- **超长处理**：如果代码行超过 80 个字符，应进行换行处理
- **换行原则**：在逻辑断点处换行，保持代码可读性

**示例**：

```javascript
// ✅ 好的做法：合理换行
const result = users
    .filter(user => user.isActive)
    .map(user => ({
        id: user.id,
        name: user.name,
        email: user.email
    }))
    .sort((a, b) => a.name.localeCompare(b.name));

// ❌ 不好的做法：行过长
const result = users.filter(user => user.isActive).map(user => ({ id: user.id, name: user.name, email: user.email })).sort((a, b) => a.name.localeCompare(b.name));
```

#### 空行规范

- **函数之间**：函数之间使用一个空行分隔
- **类之间**：类之间使用两个空行分隔
- **逻辑块之间**：相关逻辑块之间使用空行分隔，提高可读性

**示例**：

```javascript
// ✅ 好的做法：合理的空行
function getUserById(id) {
    // 函数实现
}

function saveUser(user) {
    // 函数实现
}

class UserService {
    // 类实现
}


class DataProcessor {
    // 类实现
}
```

#### 导入规范

- **导入顺序**：按照标准库、第三方库、本地模块的顺序进行导入
- **空行分隔**：每个部分之间使用一个空行分隔
- **导入格式**：使用统一的导入格式（如 ES6 import 或 CommonJS require）

**示例**：

```javascript
// ✅ 好的做法：按顺序导入，空行分隔
// 标准库
import fs from 'fs';
import path from 'path';

// 第三方库
import express from 'express';
import axios from 'axios';

// 本地模块
import { UserService } from './services/user-service';
import { DataProcessor } from './utils/data-processor';
```

#### 括号和空格规范

- **函数括号**：函数名和括号之间不加空格
- **参数括号**：参数列表的括号内，参数之间使用逗号和空格分隔
- **操作符空格**：操作符前后使用空格（如 `=`、`+`、`-`、`*`、`/`）

**示例**：

```javascript
// ✅ 好的做法：正确的括号和空格
function processData(data) {
    const result = data.map(item => item.value * 2);
    return result.filter(value => value > 10);
}

// ❌ 不好的做法：括号和空格不规范
function processData( data ) {  // 括号内不应有空格
    const result=data.map(item=>item.value*2);  // 操作符缺少空格
    return result.filter(value=>value>10);  // 操作符缺少空格
}
```