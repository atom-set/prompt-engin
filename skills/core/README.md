# 核心规则 Skills

> **说明**：本目录包含所有核心规则 skills，这些规则在每次对话中都会自动应用
> **自动生成时间**：2026-01-29 15:31:02

## 📚 Skills 列表

### 模式相关 Skills（必须应用）

1. **工具权限系统** - `tool-permission-system.md`
   - 描述：工具权限系统，定义工具分类体系和统一检查流程
   - 标签：core, mode, permission, security

2. **模式通用规则** - `mode-common.md`
   - 描述：模式通用规则，包括模式切换、响应格式等
   - 标签：core, mode, common

3. **安全规则和权限规则** - `security-permissions.md`
   - 描述：安全规则和权限规则，系统化整理权限矩阵
   - 标签：core, mode, security, permission

4. **Plan 模式行为规范** - `plan-mode.md`
   - 描述：Plan 模式行为规范，定义 Plan 模式下的允许和禁止操作
   - 标签：core, mode, plan

5. **Act 模式行为规范** - `act-mode.md`
   - 描述：Act 模式行为规范，定义 Act 模式下的执行规范
   - 标签：core, mode, act

6. **代码修改前的方案输出机制** - `solution-output.md`
   - 描述：代码修改前的方案输出机制，定义方案输出的内容和格式
   - 标签：core, mode, plan, solution

7. **文件写入规则** - `file-write.md`
   - 描述：文件写入规则，包括文件大小检查和写入策略
   - 标签：core, mode, act, file

### 代码规范 Skills（自动应用）

1. **代码格式规范** - `code-format.md`
   - 描述：代码格式规范，包括缩进、行长度、空行等
   - 标签：core, code, format

2. **命名规范** - `naming.md`
   - 描述：命名规范，包括变量、函数、类、常量等命名规则
   - 标签：core, code, naming

3. **函数设计规范** - `function-design.md`
   - 描述：函数设计规范，包括函数命名、参数处理、代码嵌套等
   - 标签：core, code, function, design

4. **注释规范** - `comments.md`
   - 描述：注释规范，包括单行注释、多行注释、文档注释等
   - 标签：core, code, comments

5. **错误处理策略** - `error-handling-strategy.md`
   - 描述：错误处理策略，包括异常捕获、错误处理模式等
   - 标签：core, code, error-handling, strategy

6. **错误日志记录** - `error-logging.md`
   - 描述：错误日志记录，包括日志级别、日志内容、结构化日志等
   - 标签：core, code, error-handling, logging

7. **错误信息格式** - `error-message-format.md`
   - 描述：错误信息格式，包括用户可见错误、错误码规范等
   - 标签：core, code, error-handling, message

8. **返回值规范** - `return-values.md`
   - 描述：返回值规范，包括返回值模式、错误处理等
   - 标签：core, code, error-handling, return

## 🔄 使用方式

### 方式一：通过 openskills 命令

```bash
# 读取单个 skill
openskills read core/tool-permission-system

# 读取所有核心 skills
openskills read core
```

### 方式二：在 Cursor 配置中引用

在 `.cursorrules` 或项目配置中：

```markdown
# 核心规则（必须应用）

@skills/core/tool-permission-system.md
@skills/core/mode-common.md
@skills/core/security-permissions.md
```

## 📝 维护说明

这些 skills 是核心规则，位于 `skills/core/` 目录。如果需要修改：

1. 直接编辑对应的 skill 文件
2. 确保修改后保持格式一致
3. 更新相关文档（如需要）

## 🔗 相关文档

- [skills/README.md](../README.md) - Skills 主文档
- [README.md](../../README.md) - 项目主文档
