from fastapi import APIRouter, HTTPException
from .model import AnalysisRequest, AnalysisResult
from .fetcher import NewsFetcher
from .analyzer import analyze_text
import traceback
import sys
from datetime import datetime, timedelta

router = APIRouter()

# NewsFetcherのインスタンスを作成
news_fetcher = NewsFetcher()

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_sentiment(query: str, date_from: str, date_to: str):
    """
    ニュース記事を取得し、感情分析を実行する
    """
    try:
        print(f"\n=== 分析開始 ===")
        print(f"クエリ: {query}")
        print(f"期間: {date_from} 〜 {date_to}")
        
        # 日付のバリデーション
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d")
            to_date = datetime.strptime(date_to, "%Y-%m-%d")
            today = datetime.now()
            
            # 日付の範囲チェック
            if from_date > to_date:
                print("警告: 開始日が終了日より後になっています。日付を入れ替えます。")
                from_date, to_date = to_date, from_date
                date_from = from_date.strftime("%Y-%m-%d")
                date_to = to_date.strftime("%Y-%m-%d")
            
            # 未来の日付を現在の日付に調整
            if from_date > today:
                print("警告: 開始日が未来の日付のため、現在の日付に調整します。")
                from_date = today
                date_from = from_date.strftime("%Y-%m-%d")
            
            if to_date > today:
                print("警告: 終了日が未来の日付のため、現在の日付に調整します。")
                to_date = today
                date_to = to_date.strftime("%Y-%m-%d")
            
            # 日付の範囲が広すぎる場合は調整
            max_days = 30
            if (to_date - from_date).days > max_days:
                print(f"警告: 検索期間が{max_days}日を超えています。期間を調整します。")
                from_date = to_date - timedelta(days=max_days)
                date_from = from_date.strftime("%Y-%m-%d")
            
            print(f"調整後の期間: {date_from} 〜 {date_to}")
            
        except ValueError as e:
            print(f"日付のバリデーションエラー: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"日付の形式が正しくありません。YYYY-MM-DD形式で指定してください。"
            )
        
        # ニュース記事を取得
        try:
            articles = news_fetcher.fetch_news(query, date_from, date_to)
        except Exception as e:
            print(f"記事取得エラー: {str(e)}")
            print("エラーの詳細:")
            print(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"記事の取得中にエラーが発生しました: {str(e)}"
            )
        
        if not articles:
            print("警告: 記事が見つかりませんでした")
            raise HTTPException(
                status_code=404,
                detail=f"指定された条件（クエリ: {query}, 期間: {date_from} 〜 {date_to}）で記事が見つかりませんでした。\n別のキーワードや期間を試してみてください。"
            )
        
        print(f"取得した記事数: {len(articles)}")
        
        # 各記事を個別に分析
        try:
            sentiment_results = []
            for article in articles:
                text = f"{article.get('title', '')} {article.get('description', '')}"
                print(f"分析対象テキストの長さ: {len(text)}文字")
                
                sentiment = await analyze_text(text)
                sentiment_results.append(sentiment)
                print(f"感情分析結果: {sentiment}")
            
            # 結果を集計
            sentiment_data = {
                "positive": sum(1 for s in sentiment_results if s.get("sentiment") == "positive"),
                "negative": sum(1 for s in sentiment_results if s.get("sentiment") == "negative"),
                "neutral": sum(1 for s in sentiment_results if s.get("sentiment") == "neutral"),
                "total": len(sentiment_results)
            }
            
        except Exception as e:
            print(f"感情分析エラー: {str(e)}")
            print("エラーの詳細:")
            print(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"記事の処理中にエラーが発生しました: {str(e)}"
            )
        
        # 結果を作成
        result = AnalysisResult(
            query=query,
            date_from=date_from,
            date_to=date_to,
            article_count=len(articles),
            sentiment=sentiment_data
        )
        
        print("=== 分析完了 ===")
        return result
        
    except HTTPException as he:
        print(f"HTTPエラー: {he.detail}")
        raise he
    except Exception as e:
        print(f"予期せぬエラー: {str(e)}")
        print("エラーの詳細:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"予期せぬエラーが発生しました: {str(e)}"
        )

@router.get("/results/{query}")
async def get_analysis_results(query: str):
    """
    過去の分析結果を取得する
    """
    try:
        results = get_result(query)
        if not results:
            raise HTTPException(status_code=404, detail="No results found")
        return results
    except Exception as e:
        error_detail = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving results: {str(e)}\n\nDetails:\n{error_detail}"
        ) 