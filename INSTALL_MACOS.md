# macOS 安装说明

## Python 和 pip 使用说明

在 macOS 上，系统自带的 Python 3 需要使用 `pip3` 或 `python3 -m pip`，而不是 `pip`。

### 常用命令

```bash
# 安装包
pip3 install 包名
# 或
python3 -m pip install 包名

# 查看已安装的包
pip3 list
# 或
python3 -m pip list

# 升级 pip
python3 -m pip install --upgrade pip
```

## 路径问题

如果安装后提示脚本不在 PATH 中，可以：

### 方法1：添加到 PATH（推荐）

编辑 `~/.zshrc` 文件：

```bash
nano ~/.zshrc
```

添加以下行：

```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```

然后重新加载配置：

```bash
source ~/.zshrc
```

### 方法2：使用 python3 -m 方式

直接使用 `python3 -m` 运行脚本，例如：

```bash
python3 -m pip install buildozer
python3 test_android.py
```

## 测试 Android 版本

```bash
# 确保已安装依赖
python3 -m pip install kivy plyer --user

# 运行测试
python3 test_android.py
```

## 常见问题

### 1. 找不到 pip 命令

**解决方案**：使用 `pip3` 或 `python3 -m pip`

### 2. 权限问题

**解决方案**：使用 `--user` 参数安装到用户目录

```bash
python3 -m pip install --user 包名
```

### 3. 虚拟环境

如果使用虚拟环境（推荐），在虚拟环境中 `pip` 命令可以直接使用：

```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 现在可以直接使用 pip
pip install kivy plyer
```

