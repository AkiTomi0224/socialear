from pydantic import BaseModel
from typing import Optional

class Sentiment(BaseModel):
    """感情分析の結果を表すモデル"""
    positive: float
    negative: float
    neutral: float
    mixed: float

class AnalysisResult(BaseModel):
    """分析結果を表すモデル"""
    query: str
    date_from: str
    date_to: str
    article_count: int
    sentiment: Sentiment 