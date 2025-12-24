# 错误处理策略

> **文件说明**：本文件包含 错误处理策略 相关规则
> **规则来源**：rules/stages/common/code/error-handling/strategy.md

---

## 概述

本文件定义了错误处理策略，包括错误处理策略、异常捕获、错误边界等。适用于所有代码文件，确保错误处理统一、完整、及时，提高代码的健壮性和可维护性。

---

### 错误处理策略

#### 基本原则

- **统一错误处理机制**：在代码中实现统一的错误处理机制，确保所有可能的错误情况都被捕获和处理
- **具体异常类型**：捕获异常时，应指定具体的异常类型，避免使用通用的 `except`
- **及时处理**：所有可能引发异常的代码块应使用 `try-except` 进行处理
- **错误传播**：合理处理错误传播，避免错误被忽略或隐藏
- **设计时考虑**：错误处理应在代码设计时考虑，而非问题修复时盲目添加
  - ✅ **正常开发**：编写新代码时，应根据业务逻辑设计合理的错误处理机制
  - ❌ **问题修复**：修复已存在的问题时，应先遵循 `problem-location.md` 定位问题，再根据定位结果添加必要的错误处理

#### 异常捕获规范

**✅ 好的做法：捕获具体异常类型**

```javascript
// ✅ 好的做法：捕获具体异常类型
try {
    const data = JSON.parse(jsonString);
    return processData(data);
} catch (error) {
    if (error instanceof SyntaxError) {
        // 处理 JSON 解析错误
        logger.error('JSON 解析失败', { error, jsonString });
        throw new ValidationError('无效的 JSON 格式');
    } else if (error instanceof TypeError) {
        // 处理类型错误
        logger.error('类型错误', { error });
        throw new ValidationError('数据类型不正确');
    } else {
        // 处理其他未知错误
        logger.error('未知错误', { error });
        throw error;
    }
}
```

```python
# ✅ 好的做法：捕获具体异常类型
try:
    data = json.loads(json_string)
    return process_data(data)
except json.JSONDecodeError as e:
    # 处理 JSON 解析错误
    logger.error('JSON 解析失败', extra={'error': str(e), 'json_string': json_string})
    raise ValidationError('无效的 JSON 格式') from e
except TypeError as e:
    # 处理类型错误
    logger.error('类型错误', extra={'error': str(e)})
    raise ValidationError('数据类型不正确') from e
except Exception as e:
    # 处理其他未知错误
    logger.error('未知错误', extra={'error': str(e)})
    raise
```

**❌ 不好的做法：使用通用异常捕获**

```javascript
// ❌ 不好的做法：捕获所有异常但不处理
try {
    const data = JSON.parse(jsonString);
    return processData(data);
} catch (error) {
    // 捕获所有错误但不处理，隐藏了真正的问题
    return null;
}
```

```python
# ❌ 不好的做法：使用通用的 except
try:
    data = json.loads(json_string)
    return process_data(data)
except:  # 捕获所有异常，但不指定类型
    # 捕获所有错误但不处理，隐藏了真正的问题
    return None
```

#### 错误处理模式

**模式1：立即处理并返回**

```javascript
// ✅ 好的做法：立即处理错误并返回
function getUserById(userId) {
    try {
        const user = fetchUserFromDatabase(userId);
        return user;
    } catch (error) {
        logger.error('获取用户失败', { userId, error });
        return null;  // 返回默认值
    }
}
```

**模式2：处理并抛出新的错误**

```javascript
// ✅ 好的做法：处理错误并抛出新的错误
function validateUserData(userData) {
    try {
        validateEmail(userData.email);
        validatePhone(userData.phone);
        return true;
    } catch (error) {
        logger.error('用户数据验证失败', { userData, error });
        throw new ValidationError('用户数据无效', { cause: error });
    }
}
```

**模式3：错误恢复**

```javascript
// ✅ 好的做法：实现错误恢复机制
async function fetchUserData(userId) {
    try {
        return await fetchFromPrimaryDatabase(userId);
    } catch (error) {
        logger.warn('主数据库查询失败，尝试备用数据库', { userId, error });
        try {
            return await fetchFromBackupDatabase(userId);
        } catch (backupError) {
            logger.error('备用数据库查询也失败', { userId, error: backupError });
            throw new DatabaseError('无法获取用户数据', { cause: backupError });
        }
    }
}
```

#### 错误边界处理

- **边界检查**：在函数入口处进行参数验证，避免无效输入导致错误
- **资源清理**：使用 `finally` 块确保资源被正确清理
- **错误传播**：合理决定是否向上传播错误，还是就地处理

**示例**：

```javascript
// ✅ 好的做法：边界检查和资源清理
async function processFile(filePath) {
    // 边界检查
    if (!filePath || typeof filePath !== 'string') {
        throw new ValidationError('文件路径无效');
    }

    let fileHandle = null;
    try {
        fileHandle = await openFile(filePath);
        const content = await readFile(fileHandle);
        return processContent(content);
    } catch (error) {
        logger.error('文件处理失败', { filePath, error });
        throw new ProcessingError('无法处理文件', { cause: error });
    } finally {
        // 确保资源被清理
        if (fileHandle) {
            await closeFile(fileHandle);
        }
    }
}
```