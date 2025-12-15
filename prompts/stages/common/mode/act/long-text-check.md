# Long Text Check

> **文件说明**：本文件包含 long text check 相关规则
> **规则来源**：rules/stages/common/mode/act/long-text-check.md

---

#### 长文本写入强制检查机制

**重要原则**：
- ✅ **必须检查**：写入前必须检查文件大小
- ✅ **必须判断**：根据大小自动选择写入策略
- ✅ **必须执行**：大文件必须采用分步写入
- ❌ **禁止违反**：不能跳过检查直接一次性写入大文件

---

**写入前强制检查流程**

**第一步：计算文件大小**

在执行 `write` 工具前，必须先计算内容大小：

```typescript
// 伪代码示例
const lines = content.split('\n').length;
const sizeKB = Buffer.byteLength(content, 'utf8') / 1024;

console.log(`文件大小：${lines} 行 / ${sizeKB.toFixed(2)} KB`);
```

**计算标准**：
- **行数**：按换行符 `\n` 计数
- **大小**：按 UTF-8 编码字节数计算（KB）

---

**第二步：判断写入策略**

根据计算结果，自动选择写入策略：

| 文件大小 | 策略 | 说明 |
|---------|------|------|
| **< 200 行 且 < 10KB** | ✅ 直接写入 | 可以一次性写入 |
| **200-500 行 或 10-25KB** | ⚠️ 建议分步 | 建议分步写入，但可选 |
| **> 500 行 或 > 25KB** | ❌ 必须分步 | 强制分步写入 |

**判断逻辑**：

```typescript
// 伪代码
function getWriteStrategy(lines: number, sizeKB: number) {
  // 强制分步：大文件（与文件写入规则保持一致：> 500 行或 > 25KB）
  if (lines > 500 || sizeKB > 25) {
    return {
      strategy: 'step-by-step',
      reason: '文件较大，必须分步写入',
      required: true  // 强制要求
    };
  }
  
  // 建议分步：中等文件（与文件写入规则保持一致：200-500 行或 10-25KB）
  if (lines > 200 || sizeKB > 10) {
    return {
      strategy: 'step-by-step',
      reason: '文件较大，建议分步写入',
      required: false  // 建议但不强制
    };
  }
  
  // 直接写入：小文件（< 200 行且 < 10KB）
  return {
    strategy: 'direct',
    reason: '文件较小，可以直接写入',
    required: false
  };
}
```

---

**第三步：执行写入（根据策略）**

**策略A：直接写入（小文件 < 200行）**

```typescript
// 文件 < 200行 且 < 10KB
write({
  file_path: 'path/to/file.md',
  contents: fullContent  // 一次性写入全部内容
});
```

**优点**：
- ✅ 速度快
- ✅ 步骤少

**风险**：
- ⚠️ 小文件风险可控

---

**策略B：分步写入（大文件 > 500行）**

```typescript
// 文件 > 1000行 或 > 50KB

// 第1步：写入框架
write({
  file_path: 'path/to/file.md',
  contents: `# 文档标题

## 第一章
<!-- SECTION_1: 待填充 -->

## 第二章
<!-- SECTION_2: 待填充 -->

## 第三章
<!-- SECTION_3: 待填充 -->
`
});

// 第2步：填充第一章
search_replace({
  file_path: 'path/to/file.md',
  old_string: '<!-- SECTION_1: 待填充 -->',
  new_string: '第一章的实际内容...'
});

// 第3步：填充第二章
search_replace({
  file_path: 'path/to/file.md',
  old_string: '<!-- SECTION_2: 待填充 -->',
  new_string: '第二章的实际内容...'
});

// 第4步：填充第三章
search_replace({
  file_path: 'path/to/file.md',
  old_string: '<!-- SECTION_3: 待填充 -->',
  new_string: '第三章的实际内容...'
});

// 第5步：验证完整性
// 检查是否还有未填充的占位符
grep('<!-- SECTION_.*: 待填充 -->', { path: 'path/to/file.md' });
// 预期结果：无匹配
```

**优点**：
- ✅ 避免一次性写入中断
- ✅ 可以分步验证
- ✅ 出问题容易定位

**注意**：
- ⚠️ 占位符命名要清晰唯一
- ⚠️ 最后必须验证完整性

---

**AI 助手自动提示规则**

当 AI 准备写入文件时，必须先执行检查并提示：

**提示1：小文件（< 200行）**

```
准备写入文件：path/to/file.md
- 行数：150 行
- 大小：8 KB
- 策略：✅ 直接写入

将一次性写入全部内容。
```

**提示2：中等文件（200-500行）**

```
准备写入文件：path/to/file.md
- 行数：350 行
- 大小：18 KB
- 策略：⚠️ 建议分步写入

文件较大，建议采用分步写入策略：
1. 先写入框架（标题 + 占位符）
2. 逐章节填充内容
3. 验证完整性

是否采用分步写入？（建议：是）
```

**提示3：大文件（> 500行）**

```
准备写入文件：path/to/file.md
- 行数：1200 行
- 大小：60 KB
- 策略：❌ 必须分步写入

⚠️ 文件较大，必须采用分步写入策略。

分步写入流程：
1. 第1步：写入文档框架（约 50 行）
2. 第2-N步：逐章节填充内容（约 8-10 步）
3. 最后1步：验证完整性

预计执行步骤：10-12 步
预计耗时：约 2-3 分钟

开始执行分步写入...
```

---

**常见错误和纠正**

**❌ 错误1：跳过检查直接写入**

```typescript
// 错误示例
write({
  file_path: 'large-file.md',
  contents: veryLongContent  // 1200行，直接写入
});
```

**✅ 正确做法**：

```typescript
// 1. 先检查
const lines = veryLongContent.split('\n').length;  // 1200 行
const sizeKB = Buffer.byteLength(veryLongContent, 'utf8') / 1024;  // 60 KB

// 2. 判断策略
if (lines > 1000 || sizeKB > 50) {
  // 3. 采用分步写入
  // 先写入框架，再逐模块填充
}
```

---

**❌ 错误2：占位符不清晰**

```markdown
<!-- TODO -->
<!-- CONTENT -->
<!-- MORE -->
```

**✅ 正确做法**：

```markdown
<!-- SECTION_INTRODUCTION: 待填充 -->
<!-- SECTION_ARCHITECTURE: 待填充 -->
<!-- SECTION_IMPLEMENTATION: 待填充 -->
```

---

**❌ 错误3：没有验证完整性**

```typescript
// 错误：填充后没有验证
search_replace({ /* ... */ });
search_replace({ /* ... */ });
// 结束，没有检查
```

**✅ 正确做法**：

```typescript
// 填充所有模块
search_replace({ /* ... */ });
search_replace({ /* ... */ });

// 验证：检查是否还有占位符
grep('<!-- .*: 待填充 -->', { path: 'file.md' });
// 预期：无匹配结果（说明全部填充完成）
```

---

**检查清单**

在执行文件写入前，必须完成以下检查：

- [ ] **计算文件大小**：行数和 KB 数
- [ ] **判断写入策略**：直接 / 分步
- [ ] **选择正确方法**：
  - 小文件：使用 `write` 一次性写入
  - 大文件：先 `write` 框架，再 `search_replace` 填充
- [ ] **准备占位符**：（如果分步写入）
  - 命名清晰唯一
  - 格式统一规范
- [ ] **验证完整性**：（如果分步写入）
  - 检查占位符是否全部替换
  - 确认内容完整无遗漏

---

**适用场景总结**

| 场景 | 文件大小 | 推荐策略 | 示例 |
|------|---------|---------|------|
| **配置文件** | < 100 行 | 直接写入 | `config.json` |
| **简单文档** | < 500 行 | 直接写入 | `README.md` |
| **中等文档** | 500-1000 行 | 建议分步 | 技术方案（600行） |
| **大型文档** | > 1000 行 | 必须分步 | 实施计划（1200行） |
| **超大文档** | > 5000 行 | 必须分步 + 更多模块 | 完整系统文档 |

---

**重要原则（必须遵守）**

1. ✅ **检查优先**：写入前必须检查文件大小
2. ✅ **策略自动**：根据大小自动选择策略
3. ✅ **分步强制**：大文件（>1000行）必须分步
4. ✅ **验证完整**：分步写入后必须验证
5. ❌ **禁止跳过**：不能跳过检查直接写入大文件
6. ❌ **禁止混用**：不能在分步写入中插入一次性写入

---