# 修复 GitHub Token 权限问题

## 问题

错误信息显示您的 GitHub Personal Access Token 缺少 `workflow` 权限，无法创建或更新 GitHub Actions 工作流文件。

## 解决方案

### 方案一：更新 Token 权限（推荐）

1. **访问 GitHub Token 设置**
   - 访问：https://github.com/settings/tokens
   - 找到您正在使用的 Token，或创建新 Token

2. **创建新 Token（带 workflow 权限）**
   - 点击 "Generate new token" → "Generate new token (classic)"
   - 勾选以下权限：
     - ✅ `repo`（完整仓库访问）
     - ✅ `workflow`（工作流访问）
   - 点击 "Generate token"
   - **重要**：复制 Token（只显示一次）

3. **更新本地 Git 凭据**

   **如果使用 HTTPS：**
   ```bash
   # 删除旧的凭据
   git config --global --unset credential.helper
   
   # 下次推送时会提示输入用户名和新的 Token
   ```

   **或直接更新远程 URL：**
   ```bash
   # 格式：https://<token>@github.com/<username>/<repo>.git
   git remote set-url origin https://<YOUR_TOKEN>@github.com/<username>/<repo>.git
   ```

### 方案二：手动上传 Workflow 文件（简单）

如果不想更新 Token，可以手动在 GitHub 网站上创建：

1. **在 GitHub 网站上创建文件**
   - 访问您的仓库：`https://github.com/<username>/<repo>`
   - 点击 "Add file" → "Create new file"
   - 路径输入：`.github/workflows/build-android.yml`
   - 复制 `build-android.yml` 的内容粘贴进去
   - 点击 "Commit new file"

2. **或者先推送其他文件，再手动添加 workflow**
   ```bash
   # 临时移除 workflow 文件
   git rm --cached .github/workflows/build-android.yml
   git commit -m "Remove workflow for manual setup"
   git push
   
   # 然后在 GitHub 网站上手动创建 workflow 文件
   ```

### 方案三：使用 GitHub CLI（如果已安装）

```bash
# 重新认证 GitHub CLI（会更新权限）
gh auth login

# 然后推送
git push
```

## 快速修复步骤

1. **创建新 Token**
   - https://github.com/settings/tokens/new
   - 勾选 `repo` 和 `workflow`
   - 生成并复制 Token

2. **更新远程 URL**
   ```bash
   # 查看当前远程 URL
   git remote -v
   
   # 更新为包含 Token 的 URL（替换 YOUR_TOKEN 和用户名、仓库名）
   git remote set-url origin https://YOUR_TOKEN@github.com/USERNAME/REPO.git
   ```

3. **重新推送**
   ```bash
   git push origin main
   ```

## 验证

推送成功后：
- 访问仓库的 Actions 页面
- 应该能看到构建工作流
- 点击 "Run workflow" 可以手动触发构建

