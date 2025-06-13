import pytest
from datetime import datetime
from app.model import Article, Sentiment, AnalysisResult

def test_sentiment_model():
    """感情分析モデルのテスト"""
    sentiment = Sentiment(
        positive=75.5,
        negative=10.2,
        neutral=12.3,
        mixed=2.0
    )
    assert sentiment.positive == 75.5
    assert sentiment.negative == 10.2
    assert sentiment.neutral == 12.3
    assert sentiment.mixed == 2.0

def test_article_model():
    """記事モデルのテスト"""
    article = Article(
        title="テスト記事",
        description="これはテスト記事です",
        url="https://example.com",
        published_at=datetime.now(),
        source="テストソース"
    )
    assert article.title == "テスト記事"
    assert article.description == "これはテスト記事です"
    assert article.url == "https://example.com"
    assert article.source == "テストソース"

def test_analysis_result_model():
    """分析結果モデルのテスト"""
    sentiment = Sentiment(
        positive=75.5,
        negative=10.2,
        neutral=12.3,
        mixed=2.0
    )
    result = AnalysisResult(
        query="テスト",
        date_from="2023-01-01",
        date_to="2023-12-31",
        sentiment=sentiment,
        total_articles=10
    )
    assert result.query == "テスト"
    assert result.date_from == "2023-01-01"
    assert result.date_to == "2023-12-31"
    assert result.sentiment == sentiment
    assert result.total_articles == 10 