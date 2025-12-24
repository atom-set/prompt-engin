# 返回值规范

> **文件说明**：本文件包含 返回值规范 相关规则
> **规则来源**：rules/stages/common/code/error-handling/return-values.md

---

## 概述

本文件定义了返回值规范，包括返回值模式、禁止的返回值模式、返回值文档等。适用于所有函数定义，确保返回值明确、一致、类型明确，便于调用者处理和错误处理。

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