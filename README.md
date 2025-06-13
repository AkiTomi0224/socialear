# 🎧 SocialEar

ニュース記事を収集し、AWS Comprehendを使用して感情分析を行うWebアプリケーション

## 機能

- News APIを使用したニュース記事の収集
- AWS Comprehendによる感情分析
- DynamoDBを使用した分析結果の保存
- FastAPI + Gradioによる直感的なUI

## 必要条件

- Python 3.8以上
- News API Key
- AWS認証情報（IAMユーザー）
  - AWS Comprehendへのアクセス権限
  - DynamoDBへのアクセス権限

## セットアップ

1. リポジトリのクローン
```bash
git clone https://github.com/yourusername/socialear.git
cd socialear
```

2. 仮想環境の作成と有効化
```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

3. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

4. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集し、必要な認証情報を設定
```

5. アプリケーションの起動
```bash
uvicorn app.main:app --reload
```

## 使用方法

1. ブラウザで http://localhost:8000/ui にアクセス
2. 検索キーワードと期間を入力
3. 「分析開始」ボタンをクリック
4. 分析結果が表示されます

## API エンドポイント

- `POST /api/v1/analyze`: 新規分析の実行
- `GET /api/v1/results/{query}`: 過去の分析結果の取得

## 開発者向け情報

### テストの実行
```bash
pytest
```

### デプロイ
```bash
./scripts/deploy.sh
```

## ライセンス

MIT

## 作者

Your Name 

# News API設定
NEWS_API_KEY=取得したNews API Key

# AWS認証情報
AWS_ACCESS_KEY_ID=取得したAWSアクセスキー
AWS_SECRET_ACCESS_KEY=取得したAWSシークレットキー
AWS_REGION=ap-northeast-1

# アプリケーション設定
DEBUG=True
HOST=0.0.0.0
PORT=8000 