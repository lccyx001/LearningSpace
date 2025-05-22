#!/bin/bash

# === Step 0: 自定义 key 名称 ===
read -p "请输入 SSH key 文件名称（默认：id_ed25519）: " KEY_NAME
KEY_NAME=${KEY_NAME:-id_ed25519}
KEY_PATH=~/.ssh/$KEY_NAME

EMAIL=$(git config user.email)
if [ -z "$EMAIL" ]; then
  read -p "请输入用于注释的邮箱（GitHub 账号邮箱）: " EMAIL
fi

# === Step 1: 检查是否已有 key ===
if [ -f "$KEY_PATH" ]; then
  echo "✅ 已检测到 SSH 私钥：$KEY_PATH"
else
  echo "🔧 未找到 SSH key，正在生成..."
  ssh-keygen -t ed25519 -C "$EMAIL" -f "$KEY_PATH" -N ""
fi

# === Step 2: 启动 SSH agent ===
echo "🚀 启动 ssh-agent..."
eval "$(ssh-agent -s)"

# === Step 3: 添加私钥 ===
ssh-add "$KEY_PATH"

# === Step 4: 输出公钥 ===
echo ""
echo "📋 请将以下 SSH 公钥复制并添加到 GitHub："
echo "👉 https://github.com/settings/ssh/new"
echo ""
cat "${KEY_PATH}.pub"

