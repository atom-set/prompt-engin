# 错误信息格式

> **文件说明**：本文件包含 错误信息格式 相关规则
> **规则来源**：rules/stages/common/code/error-handling/message-format.md

---

## 概述

本文件定义了错误信息格式规范，包括用户可见错误、错误码规范、错误信息国际化等。适用于所有需要向用户展示错误的场景，确保错误信息清晰、友好、可操作，提高用户体验。

---

### 错误信息格式

#### 基本原则

- **用户友好**：对于用户可见的错误，提供清晰、简洁的错误提示，避免技术术语
- **技术细节分离**：技术细节应记录在日志中，与用户提示分离
- **可操作性**：错误提示应提供可操作的建议，帮助用户解决问题
- **一致性**：错误信息格式应保持一致，便于用户理解

#### 用户可见错误

用户可见的错误信息应遵循以下原则：

- **清晰简洁**：使用简单明了的语言，避免技术术语
- **具体明确**：明确指出问题所在，而不是泛泛而谈
- **可操作**：提供解决建议或下一步操作指引
- **友好语气**：使用友好的语气，避免指责用户

**示例**：

```javascript
// ✅ 好的做法：用户友好的错误提示
try {
    const user = await getUserById(userId);
    if (!user) {
        throw new UserNotFoundError('抱歉，未找到该用户信息。请检查用户ID是否正确。');
    }
    return user;
} catch (error) {
    if (error instanceof UserNotFoundError) {
        // 用户可见的错误提示
        return {
            success: false,
            message: '未找到用户信息',
            suggestion: '请检查用户ID是否正确，或联系管理员'
        };
    }
    // 其他错误记录到日志，返回通用错误提示
    logger.error('获取用户失败', { userId, error });
    return {
        success: false,
        message: '获取用户信息失败',
        suggestion: '请稍后重试，如问题持续存在，请联系技术支持'
    };
}
```

**❌ 不好的做法：技术术语和模糊提示**

```javascript
// ❌ 不好的做法：使用技术术语
return {
    success: false,
    message: 'SQLException: No rows found in users table for userId=123'
};

// ❌ 不好的做法：模糊的提示
return {
    success: false,
    message: '出错了'
};
```

#### 错误码规范

对于需要程序化处理的错误，应使用错误码：

- **错误码格式**：使用统一的错误码格式（如 `ERR_USER_NOT_FOUND`、`ERR_INVALID_INPUT`）
- **错误码分类**：按模块或功能分类错误码
- **错误码文档**：维护错误码文档，说明每个错误码的含义和处理方式

**示例**：

```javascript
// ✅ 好的做法：使用错误码
const ErrorCodes = {
    USER_NOT_FOUND: 'ERR_USER_NOT_FOUND',
    INVALID_INPUT: 'ERR_INVALID_INPUT',
    DATABASE_ERROR: 'ERR_DATABASE_ERROR',
    NETWORK_ERROR: 'ERR_NETWORK_ERROR'
};

function getUserById(userId) {
    try {
        const user = fetchUser(userId);
        if (!user) {
            throw new AppError(ErrorCodes.USER_NOT_FOUND, '用户不存在');
        }
        return user;
    } catch (error) {
        if (error.code === ErrorCodes.USER_NOT_FOUND) {
            return {
                success: false,
                code: ErrorCodes.USER_NOT_FOUND,
                message: '未找到用户信息'
            };
        }
        throw error;
    }
}
```

#### 错误信息国际化

如果应用支持多语言，错误信息应支持国际化：

- **使用资源文件**：将错误信息存储在资源文件中，而非硬编码
- **语言切换**：根据用户语言偏好显示对应语言的错误信息
- **占位符支持**：支持在错误信息中使用占位符，动态填充变量

**示例**：

```javascript
// ✅ 好的做法：支持国际化
const errorMessages = {
    'zh-CN': {
        USER_NOT_FOUND: '未找到用户信息',
        INVALID_INPUT: '输入数据无效'
    },
    'en-US': {
        USER_NOT_FOUND: 'User not found',
        INVALID_INPUT: 'Invalid input data'
    }
};

function getErrorMessage(code, locale = 'zh-CN') {
    return errorMessages[locale]?.[code] || errorMessages['zh-CN'][code];
}
```