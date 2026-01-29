---
name: function-design
description: 函数设计规范，包括函数命名、参数处理、代码嵌套等
priority: 3
tags: ['core', 'code', 'function', 'design']
---

# 函数设计规范

## 使用场景

当用户需要：
- 设计函数时
- 重构函数时
- 代码审查时

## 触发条件

以下情况自动应用此规范：
- 设计函数时自动应用
- 重构函数时自动应用

## 与其他规则的配合

- 与核心规则配合使用

---

# 函数设计规范

---

### 函数设计规范

#### 基本原则

- **简短且单一用途**：函数应简短且具有单一用途，指令数量少于 20 条
- **函数命名**：函数名称应包含动词和其他含义，清晰表达函数功能
- **避免嵌套**：避免代码块嵌套，提高代码可读性
- **函数类型选择**：根据函数复杂度选择合适的函数类型（箭头函数或命名函数）

#### 函数命名规范

- **布尔值函数**：如果返回布尔值，使用 `isX`、`hasX`、`canX` 等命名方式
- **无返回值函数**：如果不返回任何值，使用 `executeX`、`saveX`、`processX` 等命名方式
- **返回值函数**：如果返回数据，使用 `getX`、`fetchX`、`loadX` 等命名方式

**命名示例**：

```javascript
// ✅ 好的命名
function isUserActive(user) { /* ... */ }
function hasPermission(user, permission) { /* ... */ }
function canAccessResource(user, resource) { /* ... */ }

function saveUserData(user) { /* ... */ }
function executeTask(task) { /* ... */ }
function processData(data) { /* ... */ }

function getUserById(id) { /* ... */ }
function fetchUserData(userId) { /* ... */ }
function loadConfig() { /* ... */ }

// ❌ 不好的命名
function check(user) { /* ... */ }  // 不明确返回类型
function do(user) { /* ... */ }  // 动词不具体
function data() { /* ... */ }  // 缺少动词
```

#### 避免代码嵌套

**方法1：尽早检查并返回结果**

```javascript
// ❌ 不好的做法：深层嵌套
function processUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        // 处理逻辑
        return result;
      }
    }
  }
  return null;
}

// ✅ 好的做法：尽早返回
function processUser(user) {
  if (!user) return null;
  if (!user.isActive) return null;
  if (!user.hasPermission) return null;
  
  // 处理逻辑
  return result;
}
```

**方法2：提取到实用函数**

```javascript
// ❌ 不好的做法：嵌套逻辑
function processUsers(users) {
  return users.map(user => {
    if (user.isActive) {
      return user.data.map(item => {
        if (item.valid) {
          return processItem(item);
        }
      });
    }
  });
}

// ✅ 好的做法：提取函数
function processUsers(users) {
  return users
    .filter(isActiveUser)
    .flatMap(getUserData)
    .filter(isValidItem)
    .map(processItem);
}

function isActiveUser(user) {
  return user.isActive;
}

function getUserData(user) {
  return user.data;
}

function isValidItem(item) {
  return item.valid;
}
```

**方法3：使用高阶函数**

```javascript
// ❌ 不好的做法：手动循环和嵌套
function getActiveUserNames(users) {
  const result = [];
  for (let i = 0; i < users.length; i++) {
    if (users[i].isActive) {
      result.push(users[i].name);
    }
  }
  return result;
}

// ✅ 好的做法：使用高阶函数
function getActiveUserNames(users) {
  return users
    .filter(user => user.isActive)
    .map(user => user.name);
}
```

#### 函数类型选择

- **简单函数**（少于 3 条指令）：使用箭头函数
- **非简单函数**：使用命名函数

**示例**：

```javascript
// ✅ 简单函数：使用箭头函数
const double = (x) => x * 2;
const isEven = (n) => n % 2 === 0;
const getFullName = (user) => `${user.firstName} ${user.lastName}`;

// ✅ 非简单函数：使用命名函数
function processUserData(user) {
  const validated = validateUser(user);
  const processed = transformUser(validated);
  const saved = saveUser(processed);
  return saved;
}

function calculateTotal(items) {
  let total = 0;
  for (const item of items) {
    total += item.price * item.quantity;
  }
  return total;
}
```

#### 参数处理

- **使用默认参数**：使用默认参数值，而不是检查是否为 `null` 或 `undefined`
- **RO-RO 模式**：使用 RO-RO（Read-Only, Read-Only）模式减少函数参数

**示例**：

```javascript
// ❌ 不好的做法：检查 null/undefined
function greet(name) {
  if (name === null || name === undefined) {
    name = 'Guest';
  }
  return `Hello, ${name}!`;
}

// ✅ 好的做法：使用默认参数
function greet(name = 'Guest') {
  return `Hello, ${name}!`;
}

// ❌ 不好的做法：多个参数
function createUser(firstName, lastName, email, phone, address) {
  // ...
}

// ✅ 好的做法：使用对象参数（RO-RO 模式）
function createUser({ firstName, lastName, email, phone, address }) {
  // ...
}

// 调用时更清晰
createUser({
  firstName: 'John',
  lastName: 'Doe',
  email: 'user@example.com',
  phone: '1234567890',
  address: '123 Main St'
});
```