# 贡献指南

感谢您对 Prompt Engine 项目的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议，请：

1. 检查 [Issues](https://github.com/your-username/prompt-engin/issues) 中是否已有相关问题
2. 如果没有，请创建新的 Issue，详细描述问题或建议

### 提交代码

1. **Fork 项目**
   ```bash
   git clone https://github.com/your-username/prompt-engin.git
   cd prompt-engin
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **进行修改**
   - 遵循项目的代码风格
   - 添加必要的测试
   - 更新相关文档

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

5. **推送并创建 Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 代码规范

### Python 代码风格

- 使用 `black` 格式化代码
- 遵循 PEP 8 代码风格
- 使用类型注解（Type Hints）

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

### 测试要求

- 新功能必须包含测试用例
- 确保所有测试通过
- 保持测试覆盖率

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/your-username/prompt-engin.git
cd prompt-engin

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 运行测试
pytest
```

## 提示词贡献

### 添加新的提示词模板

1. 确定提示词所属的阶段或类型
2. 在对应目录下创建 Markdown 文件
3. 遵循提示词模板格式
4. 添加使用说明和示例

### 提示词格式要求

- 使用 Markdown 格式
- 包含清晰的标题和说明
- 提供使用示例
- 标注适用场景

## 问题反馈

如有任何问题，请通过以下方式联系：

- 创建 Issue
- 发送邮件至 [your-email@example.com]

再次感谢您的贡献！

