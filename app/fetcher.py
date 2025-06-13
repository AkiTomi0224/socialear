import os
import requests
from typing import List, Dict, Any
from fastapi import HTTPException
from datetime import datetime, timedelta
from .model import Article

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"

# デバッグ情報の出力
print("\n=== News API設定の確認 ===")
print(f"NEWS_API_KEY: {'設定されています' if NEWS_API_KEY else '未設定'}")
if NEWS_API_KEY:
    print(f"NEWS_API_KEYの長さ: {len(NEWS_API_KEY)}")
    print(f"NEWS_API_KEYの先頭4文字: {NEWS_API_KEY[:4]}...")

def validate_dates(date_from: str, date_to: str) -> tuple[str, str]:
    """
    日付をバリデーションし、必要に応じて調整する
    """
    # 現在の日付を取得
    today = datetime.now()
    
    # 入力された日付をパース
    try:
        from_date = datetime.strptime(date_from, "%Y-%m-%d")
        to_date = datetime.strptime(date_to, "%Y-%m-%d")
    except ValueError:
        raise ValueError("日付の形式が正しくありません。YYYY-MM-DD形式で指定してください。")
    
    # 日付の範囲をチェック
    if from_date > to_date:
        from_date, to_date = to_date, from_date
        print(f"警告: 開始日が終了日より後になっています。日付を入れ替えます。")
    
    # 未来の日付を現在の日付に調整
    if from_date > today:
        from_date = today
        print(f"警告: 開始日が未来の日付のため、現在の日付に調整します。")
    
    if to_date > today:
        to_date = today
        print(f"警告: 終了日が未来の日付のため、現在の日付に調整します。")
    
    return from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")

class NewsFetcher:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"
        
        # APIキーの検証
        if not self.api_key:
            raise ValueError("NEWS_API_KEYが設定されていません")
        
        print("=== News API設定 ===")
        print(f"NEWS_API_KEY: {'設定されています' if self.api_key else '未設定'}")
        print(f"NEWS_API_KEYの長さ: {len(self.api_key)}")
        print(f"NEWS_API_KEYの先頭4文字: {self.api_key[:4]}...")

    def fetch_news(self, query: str, date_from: str, date_to: str) -> List[Dict[str, Any]]:
        """ニュース記事を取得する"""
        try:
            # 日付の検証
            from_date = datetime.strptime(date_from, "%Y-%m-%d")
            to_date = datetime.strptime(date_to, "%Y-%m-%d")
            
            # 日付範囲が広すぎる場合は調整（最大30日）
            if (to_date - from_date).days > 30:
                from_date = to_date - timedelta(days=30)
                date_from = from_date.strftime("%Y-%m-%d")
                print(f"警告: 検索期間が30日を超えています。期間を調整します。")
            
            # クエリの最適化
            if len(query) < 2:
                raise ValueError("検索キーワードは2文字以上必要です")
            
            # リクエストパラメータの設定
            params = {
                'q': query,
                'from': date_from,
                'to': date_to,
                'language': 'en',  # 英語の記事を取得
                'sortBy': 'publishedAt',
                'pageSize': 100,  # 最大記事数を取得
                'apiKey': self.api_key
            }
            
            print(f"\n=== News APIリクエスト ===")
            print(f"クエリ: {query}")
            print(f"期間: {date_from} 〜 {date_to}")
            print(f"リクエストURL: {self.base_url}")
            print(f"パラメータ: {params}")
            
            # APIリクエスト
            response = requests.get(self.base_url, params=params)
            
            print(f"\n=== News APIレスポンス ===")
            print(f"ステータスコード: {response.status_code}")
            print(f"レスポンスデータ: {response.json()}")
            
            if response.status_code != 200:
                error_msg = f"News APIエラー: {response.json().get('message', '不明なエラー')}"
                print(f"エラー: {error_msg}")
                raise HTTPException(status_code=500, detail=error_msg)
            
            data = response.json()
            articles = data.get('articles', [])
            
            print(f"取得した記事数: {len(articles)}")
            
            if not articles:
                error_msg = f"指定された条件（クエリ: {query}, 期間: {date_from} 〜 {date_to}）で記事が見つかりませんでした。\n以下の点を試してみてください：\n1. より具体的なキーワードを使用する\n2. 検索期間を広げる\n3. 検索語を確認する"
                print(f"警告: 記事が見つかりませんでした")
                raise HTTPException(status_code=404, detail=error_msg)
            
            return articles
            
        except ValueError as ve:
            error_msg = str(ve)
            print(f"エラー: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        except Exception as e:
            error_msg = f"記事の取得中にエラーが発生しました: {str(e)}"
            print(f"エラー: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg) 