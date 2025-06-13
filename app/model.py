from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class Sentiment(BaseModel):
    """感情分析のスコア"""
    sentiment: str
    score: float
    text: str

class Article(BaseModel):
    """ニュース記事"""
    title: str
    description: str
    url: str
    published_at: datetime
    source: str

class AnalysisRequest(BaseModel):
    """分析リクエスト"""
    query: str
    date_from: str
    date_to: str

class AnalysisResult(BaseModel):
    """分析結果"""
    query: str
    date_from: str
    date_to: str
    article_count: int
    sentiment: Dict[str, Any]
    created_at: Optional[str] = None 