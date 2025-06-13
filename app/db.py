import os
import boto3
from typing import Optional, List
from datetime import datetime
from .model import AnalysisResult

# 環境変数の読み込みを確認
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "socialear-results")

# デバッグ情報の出力
print("AWS認証情報の確認:")
print(f"AWS_ACCESS_KEY_ID: {'設定されています' if AWS_ACCESS_KEY_ID else '未設定'}")
print(f"AWS_SECRET_ACCESS_KEY: {'設定されています' if AWS_SECRET_ACCESS_KEY else '未設定'}")
print(f"AWS_REGION: {AWS_REGION}")
print(f"DYNAMODB_TABLE: {DYNAMODB_TABLE}")

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    raise ValueError("AWS認証情報が設定されていません。.envファイルを確認してください。")

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)
table = dynamodb.Table(DYNAMODB_TABLE)

async def save_result(result: AnalysisResult) -> None:
    """
    分析結果をDynamoDBに保存する
    """
    item = {
        'query': result.query,
        'date_from': result.date_from,
        'date_to': result.date_to,
        'sentiment': {
            'positive': result.sentiment.positive,
            'negative': result.sentiment.negative,
            'neutral': result.sentiment.neutral,
            'mixed': result.sentiment.mixed
        },
        'total_articles': result.total_articles,
        'created_at': datetime.now().isoformat()
    }
    
    table.put_item(Item=item)

def get_result(query: str, date_from: Optional[str] = None, date_to: Optional[str] = None) -> Optional[AnalysisResult]:
    """
    DynamoDBから分析結果を取得する
    """
    # 完全一致検索
    if date_from and date_to:
        response = table.get_item(
            Key={
                'query': query,
                'date_from': date_from,
                'date_to': date_to
            }
        )
        item = response.get('Item')
        if item:
            return AnalysisResult.parse_obj(item)
    
    # クエリのみの検索（最新の結果を返す）
    else:
        response = table.query(
            KeyConditionExpression='query = :q',
            ExpressionAttributeValues={':q': query},
            ScanIndexForward=False,  # 降順
            Limit=1
        )
        items = response.get('Items', [])
        if items:
            return AnalysisResult.parse_obj(items[0])
    
    return None 