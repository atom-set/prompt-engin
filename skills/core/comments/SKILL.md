---
name: comments
description: 注释规范，包括单行注释、多行注释、文档注释等
priority: 3
tags: ['core', 'code', 'comments']
---

# 注释规范

## 使用场景

当用户需要：
- 编写注释时
- 文档化代码时
- 代码审查时

## 触发条件

以下情况自动应用此规范：
- 编写注释时自动应用
- 文档化代码时自动应用

## 与其他规则的配合

- 与核心规则配合使用

---

# 注释规范

---

### 注释规范

#### 基本原则

- **完整句子**：使用完整的句子进行注释，首字母大写，句末加句号
- **清晰表达**：注释应清晰表达代码的意图和逻辑
- **及时更新**：代码修改时，应同步更新相关注释
- **避免冗余**：避免注释与代码重复，注释应解释"为什么"而不是"是什么"

#### 单行注释

- **格式**：使用 `//` 进行单行注释
- **位置**：注释应放在代码行的上方或右侧
- **内容**：解释代码的意图或重要逻辑

**示例**：

```javascript
// ✅ 好的做法：清晰的单行注释
// 计算用户的总订单金额
const totalAmount = orders.reduce((sum, order) => sum + order.amount, 0);

// 验证用户是否有权限访问资源
if (!user.hasPermission(resource)) {
    return null;
}

const maxRetries = 3; // 最大重试次数
```

#### 多行注释

- **格式**：使用 `/* */` 进行多行注释
- **使用场景**：用于解释复杂的逻辑或算法
- **格式要求**：每行注释前加 `*`，保持格式统一

**示例**：

```javascript
// ✅ 好的做法：格式统一的多行注释
/*
 * 计算用户的总订单金额
 * 包括已支付和待支付的订单
 * 排除已取消的订单
 */
const totalAmount = orders
    .filter(order => order.status !== 'cancelled')
    .reduce((sum, order) => sum + order.amount, 0);
```

#### 文档注释

- **函数注释**：函数和类的定义应包含文档字符串，描述其功能和参数
- **参数说明**：说明每个参数的类型和用途
- **返回值说明**：说明返回值的类型和含义
- **格式要求**：使用 JSDoc 或其他文档注释格式

**示例**：

```javascript
// ✅ 好的做法：完整的文档注释
/**
 * 根据用户ID获取用户信息
 * @param {string} userId - 用户ID
 * @param {boolean} includeProfile - 是否包含用户详细信息
 * @returns {Promise<User>} 用户对象
 * @throws {Error} 当用户不存在时抛出错误
 */
async function getUserById(userId, includeProfile = false) {
    // 函数实现
}

/**
 * 用户服务类
 * 提供用户相关的业务逻辑处理
 */
class UserService {
    /**
     * 创建新用户
     * @param {Object} userData - 用户数据
     * @param {string} userData.name - 用户名称
     * @param {string} userData.email - 用户邮箱
     * @returns {Promise<User>} 创建的用户对象
     */
    async createUser(userData) {
        // 方法实现
    }
}
```

#### TODO 注释

- **格式**：使用 `// TODO:` 标记待完成的任务
- **内容要求**：说明需要完成的任务和原因
- **责任人**：可以添加责任人信息（可选）

**示例**：

```javascript
// ✅ 好的做法：清晰的 TODO 注释
// TODO: 优化数据库查询性能，当前查询较慢
function getUserOrders(userId) {
    // 当前实现
}

// TODO(张三): 添加缓存机制，减少数据库查询
function getProductList() {
    // 当前实现
}
```

#### 禁止的注释

- ❌ **注释与代码重复**：注释只是重复代码内容，没有提供额外信息
- ❌ **过时的注释**：代码已修改但注释未更新
- ❌ **无意义的注释**：注释没有提供有用信息

**示例**：

```javascript
// ❌ 不好的做法：注释与代码重复
// 设置用户名为 'John'
const userName = 'John';

// ❌ 不好的做法：过时的注释
// 获取用户ID（已废弃，应使用 getUserById）
function getUserId() {
    // 新实现
}

// ❌ 不好的做法：无意义的注释
// 这是一个函数
function processData(data) {
    // 处理数据
    return data;
}
```