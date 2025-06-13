import os
import asyncio
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv
from .model import Sentiment

# 環境変数の読み込み
load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        # 感情分析モデルの初期化
        model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.pipeline = pipeline(
            "sentiment-analysis",
            model=self.model,
            tokenizer=self.tokenizer
        )

    def analyze_text(self, text: str) -> dict:
        """
        テキストの感情分析を実行
        """
        try:
            # トークン化して長さを確認
            tokens = self.tokenizer.encode(text, truncation=True, max_length=512)
            # トークン化されたテキストをデコード
            truncated_text = self.tokenizer.decode(tokens, skip_special_tokens=True)
            
            # 感情分析の実行
            result = self.pipeline(truncated_text)[0]
            
            # 結果の整形
            label = result['label']
            score = result['score']
            
            # ラベルを感情に変換（1-5のスケールを3段階に変換）
            rating = int(label.split()[0])
            if rating >= 4:
                sentiment = 'positive'
            elif rating <= 2:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            print(f"感情分析結果: {sentiment} (スコア: {score:.2f}, 評価: {rating})")
            
            return {
                'sentiment': sentiment,
                'score': score,
                'text': truncated_text
            }
        except Exception as e:
            print(f"感情分析エラー: {str(e)}")
            return {
                'sentiment': 'ERROR',
                'score': 0.0,
                'text': text
            }

# シングルトンインスタンス
analyzer = SentimentAnalyzer()

async def analyze_text(text: str) -> dict:
    """
    テキストの感情分析を行う
    """
    if not text:
        raise ValueError("分析するテキストが空です")
    
    # テキストを8KB以下に制限
    if len(text.encode('utf-8')) > 8000:
        text = text[:4000]  # テキストを切り詰める
    
    try:
        # 非同期で感情分析を実行
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            analyzer.analyze_text,
            text
        )
        
        return result
        
    except Exception as e:
        print(f"感情分析エラー: {str(e)}")
        print("エラーの詳細:")
        import traceback
        print(traceback.format_exc())
        raise Exception(f"感情分析中にエラーが発生しました: {str(e)}") 