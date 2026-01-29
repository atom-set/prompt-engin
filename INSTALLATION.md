# 安装和使用说明

## 问题：`skill-engine` 命令找不到

如果遇到 `zsh: command not found: skill-engine` 错误，有以下几种解决方案：

## 解决方案

### 方案 1: 使用项目根目录的包装脚本（推荐）

在项目根目录下，直接使用 `./skill-engine`：

```bash
# 在项目根目录下
./skill-engine analyze
./skill-engine apply-optimize
```

### 方案 2: 使用 `python3 -m` 方式

```bash
# 分析 skills
python3 -m skill_engine.cli analyze

# 应用优化
python3 -m skill_engine.cli apply-optimize

# 查看帮助
python3 -m skill_engine.cli --help
```

### 方案 3: 将命令添加到 PATH（永久解决）

#### 对于 zsh（macOS 默认）

1. 编辑 `~/.zshrc` 文件：
```bash
nano ~/.zshrc
```

2. 添加以下行：
```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```

3. 重新加载配置：
```bash
source ~/.zshrc
```

4. 验证：
```bash
which skill-engine
skill-engine --help
```

#### 对于 bash

1. 编辑 `~/.bashrc` 或 `~/.bash_profile`：
```bash
nano ~/.bashrc
```

2. 添加相同的 PATH 配置：
```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```

3. 重新加载配置：
```bash
source ~/.bashrc
```

### 方案 4: 创建别名（临时解决）

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
alias skill-engine='python3 -m skill_engine.cli'
```

然后重新加载配置：
```bash
source ~/.zshrc  # 或 source ~/.bashrc
```

## 验证安装

运行以下命令验证安装是否成功：

```bash
# 使用 python -m 方式
python3 -m skill_engine.cli --help

# 或使用项目根目录的脚本
./skill-engine --help
```

## 常用命令

### 分析 Skills

```bash
# 使用 python -m 方式
python3 -m skill_engine.cli analyze

# 或使用项目根目录的脚本
./skill-engine analyze
```

### 应用优化

```bash
# 使用 python -m 方式
python3 -m skill_engine.cli apply-optimize

# 或使用项目根目录的脚本
./skill-engine apply-optimize
```

## 注意事项

1. **Python 版本**：确保使用 Python 3.8 或更高版本
2. **虚拟环境**：如果在虚拟环境中，确保已激活虚拟环境
3. **安装位置**：脚本安装在 `~/Library/Python/3.9/bin`（macOS）或 `~/.local/bin`（Linux）

## 故障排除

### 问题：仍然找不到命令

1. 检查 Python 版本：
```bash
python3 --version
```

2. 检查包是否安装：
```bash
pip3 list | grep skill-engine
```

3. 重新安装包：
```bash
pip3 install -e .
```

### 问题：权限错误

如果遇到权限错误，尝试：
```bash
chmod +x skill-engine
```

### 问题：模块找不到

确保在项目根目录下运行，或使用绝对路径：
```bash
cd /path/to/prompt-engin
python3 -m skill_engine.cli analyze
```
