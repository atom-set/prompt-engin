# 命名规范

> **文件说明**：本文件包含 命名规范 相关规则
> **规则来源**：rules/stages/common/code/naming/naming.md

---

### 命名规范

#### 基本原则

- **使用完整单词**：使用完整的单词，避免缩写（标准缩写如 API、URL 除外）
- **拼写正确**：确保所有命名拼写正确
- **语义清晰**：命名应清晰表达其含义和用途
- **遵循项目规范**：遵循项目已有的命名规范（如：kebab-case、camelCase、PascalCase）

#### 常用缩写（允许使用）

以下常用缩写可以在代码中使用：

- **循环变量**：`i`、`j`、`k`（用于循环计数器）
- **错误处理**：`err`、`error`（用于错误对象）
- **上下文**：`ctx`、`context`（用于上下文对象）
- **中间件参数**：`req`、`res`、`next`（用于中间件函数参数）

#### 变量和函数命名

- **命名格式**：使用 `lowerCamelCase`（小驼峰命名）
- **函数命名**：应包含动词，表达函数的功能
- **布尔值函数**：使用 `isX`、`hasX`、`canX` 等前缀
- **无返回值函数**：使用 `executeX`、`saveX`、`processX` 等动词开头

**命名示例**：

```javascript
// ✅ 好的命名
const userName = 'John';
const maxRetries = 3;
const isActive = true;
const hasPermission = false;

function getUserById(id) { /* ... */ }
function saveUserData(user) { /* ... */ }
function isUserActive(user) { /* ... */ }
function hasUserPermission(user, permission) { /* ... */ }

// ❌ 不好的命名
const usrNm = 'John';  // 缩写不清晰
const maxR = 3;  // 缩写不清晰
const flag = true;  // 语义不清晰
function get() { /* ... */ }  // 缺少具体含义
```

#### 类名命名

- **命名格式**：使用 `UpperCamelCase`（大驼峰命名，PascalCase）
- **命名原则**：类名应为名词，表达类的用途

**命名示例**：

```javascript
// ✅ 好的命名
class UserService { /* ... */ }
class DataProcessor { /* ... */ }
class ConfigManager { /* ... */ }

// ❌ 不好的命名
class userService { /* ... */ }  // 应使用大驼峰
class data_processor { /* ... */ }  // 应使用大驼峰
class Config { /* ... */ }  // 过于宽泛
```

#### 常量命名

- **命名格式**：使用全大写字母，单词之间以下划线分隔
- **命名原则**：常量名应清晰表达其含义

**命名示例**：

```javascript
// ✅ 好的命名
const MAX_RETRIES = 3;
const DEFAULT_TIMEOUT = 5000;
const API_BASE_URL = 'https://api.example.com';

// ❌ 不好的命名
const maxRetries = 3;  // 应使用全大写
const defaultTimeout = 5000;  // 应使用全大写
const apiBaseUrl = 'https://api.example.com';  // 应使用全大写
```

#### 文件命名

- **命名格式**：遵循项目已有的命名规范
- **命名原则**：文件名应清晰表达文件的主要功能
- **常见格式**：
  - `kebab-case`：`user-service.js`、`data-processor.ts`
  - `camelCase`：`userService.js`、`dataProcessor.ts`
  - `PascalCase`：`UserService.js`、`DataProcessor.ts`（通常用于类文件）

**命名示例**：

- ✅ **好的命名**：
  - `user-service.js`：用户服务
  - `data-processor.ts`：数据处理器
  - `config-manager.js`：配置管理器
- ❌ **不好的命名**：
  - `utils.js`：过于宽泛
  - `helper.js`：不明确
  - `misc.js`：杂项，职责不清