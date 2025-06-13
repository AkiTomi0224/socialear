# SocialEar

SocialEarは、ニュース記事の感情分析を行うWebアプリケーションです。News APIを使用して記事を取得し、Hugging Faceの感情分析モデルを使用して記事の感情を分析します。

## 機能

- キーワード検索によるニュース記事の取得
- 日付範囲指定による記事の絞り込み
- 記事の感情分析（ポジティブ/ネガティブ/ニュートラル）
- 分析結果の可視化
- 非同期処理による高速な分析
- 多言語対応（英語ニュースの感情分析）

## 技術スタック

- FastAPI: バックエンドフレームワーク
- Gradio: Webインターフェース
- News API: ニュース記事の取得
- Hugging Face Transformers: 感情分析モデル
- Python 3.9+

## セットアップ

1. リポジトリをクローン:
```bash
git clone https://github.com/yourusername/socialear.git
cd socialear
```

2. 仮想環境を作成して有効化:
```bash
python -m venv venv
source venv/bin/activate  # Linuxの場合
# または
.\venv\Scripts\activate  # Windowsの場合
```

3. 依存関係をインストール:
```bash
pip install -r requirements.txt
```

4. 環境変数の設定:
`.env`ファイルを作成し、以下の内容を設定:
```
NEWS_API_KEY=your_api_key_here
```

## 使用方法

1. アプリケーションを起動:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

2. ブラウザでアクセス:
```
http://127.0.0.1:8080/ui
```

3. 検索条件を入力:
   - キーワード: 検索したい単語やフレーズ
   - 開始日: 検索開始日（YYYY-MM-DD形式）
   - 終了日: 検索終了日（YYYY-MM-DD形式）

4. 「分析開始」ボタンをクリックして分析を実行

## 感情分析について

- 使用モデル: `nlptown/bert-base-multilingual-uncased-sentiment`
- 評価スケール: 1-5の5段階評価
  - 4-5: ポジティブ
  - 3: ニュートラル
  - 1-2: ネガティブ
- テキスト制限: 最大8KB（約4000文字）

## 注意事項

- News APIの無料プランでは、過去1ヶ月分の記事のみ取得可能です
- 感情分析は英語のテキストに対して最適化されています
- 大量の記事を一度に分析する場合は、処理に時間がかかる場合があります

## ライセンス

MIT License

## 作者

Akihiro Tomita

# News API設定
NEWS_API_KEY=取得したNews API Key

# AWS認証情報
AWS_ACCESS_KEY_ID=取得したAWSアクセスキー
AWS_SECRET_ACCESS_KEY=取得したAWSシークレットキー
AWS_REGION=ap-northeast-1

# アプリケーション設定
DEBUG=True
HOST=0.0.0.0
PORT=8080