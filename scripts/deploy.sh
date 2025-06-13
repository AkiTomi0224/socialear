#!/bin/bash

# エラー時に停止
set -e

# 環境変数の読み込み
if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found"
    exit 1
fi

# 必要な環境変数のチェック
if [ -z "$AWS_ACCESS_KEY" ] || [ -z "$AWS_SECRET_KEY" ]; then
    echo "Error: AWS credentials not set in .env"
    exit 1
fi

# EC2インスタンスのIPアドレス（環境変数から取得）
EC2_HOST="${EC2_HOST:-}"
if [ -z "$EC2_HOST" ]; then
    echo "Error: EC2_HOST not set in .env"
    exit 1
fi

# デプロイ用の一時ディレクトリ作成
DEPLOY_DIR="deploy_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$DEPLOY_DIR"

# 必要なファイルをコピー
cp -r app requirements.txt .env "$DEPLOY_DIR/"

# EC2インスタンスにファイルを転送
echo "Copying files to EC2..."
scp -r "$DEPLOY_DIR"/* "ec2-user@${EC2_HOST}:/home/ec2-user/socialear/"

# アプリケーションの再起動
echo "Restarting application..."
ssh "ec2-user@${EC2_HOST}" << 'EOF'
cd ~/socialear
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart socialear
EOF

# 一時ディレクトリの削除
rm -rf "$DEPLOY_DIR"

echo "Deployment completed successfully!" 