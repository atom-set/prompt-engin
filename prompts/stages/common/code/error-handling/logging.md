# 错误日志记录

> **文件说明**：本文件包含 错误日志记录 相关规则
> **规则来源**：rules/stages/common/code/error-handling/logging.md

---

## 概述

本文件定义了错误日志记录规范，包括日志级别、日志内容要求、结构化日志、敏感信息处理等。适用于所有需要记录日志的代码，确保日志记录统一、详细、安全，便于问题定位和系统监控。

---

### 错误日志记录

#### 基本原则

- **统一日志库**：使用统一的日志记录库（如 `logging`、`winston`、`pino` 等）
- **日志级别**：根据事件的重要性设置日志级别
- **详细信息**：记录详细的错误信息，包括时间戳、模块名称、错误类型、堆栈信息等
- **结构化日志**：使用结构化日志格式，便于日志分析和查询

#### 日志级别

根据事件的重要性，使用以下日志级别：

- **DEBUG**：详细的调试信息，通常只在开发环境使用
- **INFO**：一般信息，记录程序正常运行的关键步骤
- **WARNING**：警告信息，表示可能的问题，但不影响程序运行
- **ERROR**：错误信息，表示发生了错误，但程序可以继续运行
- **CRITICAL**：严重错误，表示发生了严重问题，可能导致程序无法继续运行

**使用示例**：

```javascript
// ✅ 好的做法：根据重要性选择合适的日志级别
logger.debug('开始处理用户请求', { userId, requestId });
logger.info('用户登录成功', { userId, loginTime });
logger.warn('API 响应时间较长', { endpoint, duration: 2000 });
logger.error('数据库查询失败', { query, error });
logger.critical('数据库连接丢失', { error });
```

#### 日志内容要求

错误日志应包含以下信息：

1. **时间戳**：错误发生的时间
2. **模块名称**：发生错误的模块或文件
3. **错误类型**：错误的类型（如 `SyntaxError`、`TypeError` 等）
4. **错误消息**：错误的详细消息
5. **堆栈信息**：错误的堆栈跟踪信息
6. **上下文信息**：相关的上下文信息（如用户ID、请求ID、参数值等）

**示例**：

```javascript
// ✅ 好的做法：记录详细的错误信息
try {
    const user = await getUserById(userId);
    return user;
} catch (error) {
    logger.error('获取用户失败', {
        timestamp: new Date().toISOString(),
        module: 'UserService',
        errorType: error.constructor.name,
        errorMessage: error.message,
        stack: error.stack,
        context: {
            userId,
            requestId,
            userAgent
        }
    });
    throw error;
}
```

```python
# ✅ 好的做法：记录详细的错误信息
try:
    user = await get_user_by_id(user_id)
    return user
except Exception as e:
    logger.error('获取用户失败', extra={
        'timestamp': datetime.now().isoformat(),
        'module': 'UserService',
        'error_type': type(e).__name__,
        'error_message': str(e),
        'stack': traceback.format_exc(),
        'context': {
            'user_id': user_id,
            'request_id': request_id,
            'user_agent': user_agent
        }
    })
    raise
```

#### 结构化日志

使用结构化日志格式，便于日志分析和查询：

```javascript
// ✅ 好的做法：使用结构化日志
logger.error({
    level: 'error',
    timestamp: new Date().toISOString(),
    message: '数据库查询失败',
    error: {
        type: error.constructor.name,
        message: error.message,
        stack: error.stack
    },
    context: {
        userId,
        query,
        requestId
    }
});
```

#### 敏感信息处理

- **禁止记录**：不要在日志中记录敏感信息（如密码、Token、密钥等）
- **脱敏处理**：如果必须记录敏感信息，应进行脱敏处理

**示例**：

```javascript
// ❌ 不好的做法：记录敏感信息
logger.info('用户登录', { username, password });  // 密码不应记录

// ✅ 好的做法：脱敏处理
logger.info('用户登录', { 
    username, 
    passwordHash: hashPassword(password)  // 记录哈希值而非明文
});
```