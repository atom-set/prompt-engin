---
name: return-values
description: 返回值规范，包括返回值模式、错误处理等。本规范定义了函数返回值的设计原则和模式，确保返回值格式统一、类型明确，便于调用者处理和错误处理，适用于所有编程语言的函数设计场景。
priority: 3
tags: ['core', 'code', 'error-handling', 'return']
---

# 返回值规范

## 使用场景

当用户需要：
- 设计函数返回值时
- 处理函数返回值时
- 代码审查时

## 触发条件

以下情况自动应用此规范：
- 设计函数返回值时自动应用
- 处理返回值时自动应用

## 与其他规则的配合

- 与核心规则配合使用

---

# 返回值规范

## 概述

本规范定义了函数返回值的设计原则和模式，包括返回值格式、错误处理方式、类型明确性等要求。遵循本规范可以确保函数返回值格式统一、类型明确，便于调用者处理和错误处理，提高代码的可维护性和可读性。

---

### 返回值规范

#### 基本原则

- **明确返回值**：函数应明确返回值，避免返回 `None` 或不确定的值
- **错误处理**：在可能失败的情况下，函数应返回错误码或抛出异常，以便调用者进行处理
- **一致性**：返回值格式应保持一致，便于调用者处理
- **类型明确**：返回值类型应明确，避免返回多种类型的值

#### 返回值模式

**模式1：返回结果对象**

```javascript
// ✅ 好的做法：返回结果对象
function getUserById(userId) {
    try {
        const user = fetchUser(userId);
        if (!user) {
            return {
                success: false,
                error: 'USER_NOT_FOUND',
                message: '用户不存在'
            };
        }
        return {
            success: true,
            data: user
        };
    } catch (error) {
        logger.error('获取用户失败', { userId, error });
        return {
            success: false,
            error: 'DATABASE_ERROR',
            message: '获取用户信息失败'
        };
    }
}
```

**模式2：抛出异常**

```javascript
// ✅ 好的做法：抛出异常
function getUserById(userId) {
    if (!userId) {
        throw new ValidationError('用户ID不能为空');
    }
    
    const user = fetchUser(userId);
    if (!user) {
        throw new UserNotFoundError(`用户不存在: ${userId}`);
    }
    
    return user;
}

// 调用者处理异常
try {
    const user = getUserById(userId);
    // 处理用户数据
} catch (error) {
    if (error instanceof UserNotFoundError) {
        // 处理用户不存在的情况
    } else if (error instanceof ValidationError) {
        // 处理验证错误
    } else {
        // 处理其他错误
    }
}
```

**模式3：使用 Result 类型**

```typescript
// ✅ 好的做法：使用 Result 类型（TypeScript）
type Result<T, E> = 
    | { success: true; data: T }
    | { success: false; error: E };

function getUserById(userId: string): Result<User, string> {
    try {
        const user = fetchUser(userId);
        if (!user) {
            return { success: false, error: 'USER_NOT_FOUND' };
        }
        return { success: true, data: user };
    } catch (error) {
        return { success: false, error: 'DATABASE_ERROR' };
    }
}
```

#### 禁止的返回值模式

**❌ 不好的做法：返回 null 或 undefined 表示错误**

```javascript
// ❌ 不好的做法：返回 null 表示错误
function getUserById(userId) {
    const user = fetchUser(userId);
    return user || null;  // 无法区分"用户不存在"和"查询失败"
}

// 调用者无法区分错误类型
const user = getUserById(userId);
if (user === null) {
    // 不知道是用户不存在还是查询失败
}
```

**❌ 不好的做法：返回多种类型的值**

```javascript
// ❌ 不好的做法：返回多种类型的值
function processData(data) {
    if (!data) {
        return null;  // 返回 null
    }
    if (data.invalid) {
        return false;  // 返回布尔值
    }
    return { result: 'success' };  // 返回对象
}

// 调用者需要检查多种类型
const result = processData(data);
if (result === null) {
    // 处理 null
} else if (result === false) {
    // 处理 false
} else {
    // 处理对象
}
```

#### 返回值文档

函数应明确文档化返回值：

```javascript
/**
 * 根据用户ID获取用户信息
 * @param {string} userId - 用户ID
 * @returns {Promise<{success: boolean, data?: User, error?: string}>}
 *   - success: true 时，返回 data（用户对象）
 *   - success: false 时，返回 error（错误码）
 * @throws {ValidationError} 当用户ID无效时抛出
 */
async function getUserById(userId) {
    // 函数实现
}
```

### 使用场景示例

#### 示例1：API 接口返回值设计

**场景**：设计一个获取用户信息的 API 接口

**返回值设计**：
```javascript
// ✅ 好的做法：返回结果对象，包含成功状态和数据
async function getUserById(userId) {
    try {
        const user = await fetchUser(userId);
        if (!user) {
            return {
                success: false,
                error: 'USER_NOT_FOUND',
                message: '用户不存在'
            };
        }
        return {
            success: true,
            data: user
        };
    } catch (error) {
        logger.error('获取用户失败', { userId, error });
        return {
            success: false,
            error: 'DATABASE_ERROR',
            message: '获取用户信息失败'
        };
    }
}

// 调用者处理
const result = await getUserById('123');
if (result.success) {
    console.log('用户信息:', result.data);
} else {
    console.error('错误:', result.error, result.message);
}
```

#### 示例2：数据验证函数返回值

**场景**：设计一个数据验证函数

**返回值设计**：
```javascript
// ✅ 好的做法：抛出异常表示验证失败
function validateUserData(userData) {
    if (!userData.email) {
        throw new ValidationError('邮箱不能为空');
    }
    if (!userData.phone) {
        throw new ValidationError('手机号不能为空');
    }
    if (!isValidEmail(userData.email)) {
        throw new ValidationError('邮箱格式不正确');
    }
    return true; // 验证通过
}

// 调用者处理
try {
    validateUserData(userData);
    // 验证通过，继续处理
} catch (error) {
    if (error instanceof ValidationError) {
        // 处理验证错误
        showError(error.message);
    } else {
        // 处理其他错误
        handleUnexpectedError(error);
    }
}
```

#### 示例3：数据处理函数返回值

**场景**：设计一个数据处理函数，可能返回多种类型的结果

**返回值设计**：
```typescript
// ✅ 好的做法：使用 Result 类型，类型明确
type Result<T, E> = 
    | { success: true; data: T }
    | { success: false; error: E };

function processData(data: unknown): Result<ProcessedData, string> {
    if (!data) {
        return { success: false, error: '数据不能为空' };
    }
    if (!isValidData(data)) {
        return { success: false, error: '数据格式不正确' };
    }
    const processed = transformData(data);
    return { success: true, data: processed };
}

// 调用者处理
const result = processData(inputData);
if (result.success) {
    // TypeScript 可以正确推断 result.data 的类型
    useProcessedData(result.data);
} else {
    // TypeScript 可以正确推断 result.error 的类型
    handleError(result.error);
}
```