# 安装依赖 - 手动方案

由于网络连接问题，请按照以下步骤手动安装：

## 方案1：使用国内镜像源（推荐）

在终端中执行以下命令：

```bash
cd /Users/sec-test2/Desktop/my-code/FundIndustryQualificationCertificate
source .venv/bin/activate

# 使用清华镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PyQt6

# 或者使用阿里云镜像源
pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt6

# 或者使用豆瓣镜像源
pip install -i https://pypi.douban.com/simple/ PyQt6
```

## 方案2：检查网络连接后重试

1. 检查您的网络连接
2. 如果使用 VPN，确保 VPN 正常工作
3. 重试安装命令：

```bash
source .venv/bin/activate
pip install PyQt6
```

## 方案3：使用 pip 的下载重试功能

```bash
source .venv/bin/activate
pip install --upgrade pip --retries 10
pip install PyQt6 --retries 10
```

## 安装完成后运行程序

```bash
source .venv/bin/activate
python main.py
```

