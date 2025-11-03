#!/bin/bash
# 使用 GitHub Actions 构建 Android APK 的辅助脚本

echo "=========================================="
echo "使用 GitHub Actions 构建 Android APK"
echo "=========================================="
echo ""

# 检查是否在 git 仓库中
if [ ! -d ".git" ]; then
    echo "初始化 Git 仓库..."
    git init
    git add .
    git commit -m "Initial commit: Fund Industry Qualification Certificate App"
    echo "✓ Git 仓库已初始化"
    echo ""
fi

# 检查是否已设置远程仓库
if ! git remote | grep -q "origin"; then
    echo "请先设置 Git 远程仓库："
    echo "  git remote add origin <your-github-repo-url>"
    echo ""
    echo "或者创建新的 GitHub 仓库后运行："
    echo "  gh repo create --public --source=. --remote=origin"
    echo ""
    read -p "是否现在创建 GitHub 仓库？(需要安装 GitHub CLI: gh) (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v gh &> /dev/null; then
            gh repo create --public --source=. --remote=origin --push
        else
            echo "请先安装 GitHub CLI: brew install gh"
            exit 1
        fi
    else
        echo "请手动设置远程仓库后重试"
        exit 1
    fi
fi

# 检查 GitHub Actions 工作流文件
if [ ! -f ".github/workflows/build-android.yml" ]; then
    echo "创建 GitHub Actions 工作流..."
    mkdir -p .github/workflows
    # 文件已经创建好了，只需要添加
    git add .github/workflows/build-android.yml
    git commit -m "Add GitHub Actions workflow for Android build"
fi

echo ""
echo "推送代码到 GitHub..."
git add .
git commit -m "Update: Prepare for Android build" || echo "没有新更改"
git push origin main || git push origin master

echo ""
echo "=========================================="
echo "✓ 代码已推送到 GitHub"
echo ""
echo "下一步："
echo "1. 访问您的 GitHub 仓库"
echo "2. 点击 'Actions' 标签页"
echo "3. 查看构建进度"
echo "4. 构建完成后，在 'Artifacts' 中下载 APK"
echo ""
echo "或者手动触发构建："
echo "  在 GitHub 仓库的 Actions 页面点击 'Run workflow'"
echo "=========================================="

