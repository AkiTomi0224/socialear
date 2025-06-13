import gradio as gr
from datetime import datetime, timedelta
from .job_controller import analyze_sentiment

def create_ui():
    """Gradioインターフェースを作成"""
    
    async def process_input(query: str, days_ago: int):
        """ユーザー入力を処理"""
        try:
            # 現在の日付を取得
            today = datetime.now()
            # 指定された日数前の日付を計算
            date_from = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            date_to = today.strftime("%Y-%m-%d")
            
            print(f"=== 日付計算 ===")
            print(f"現在の日付: {today.strftime('%Y-%m-%d')}")
            print(f"取得期間: {date_from} 〜 {date_to}")
            
            # 感情分析を実行
            result = await analyze_sentiment(query, date_from, date_to)
            return str(result)
        except Exception as e:
            error_msg = f"エラーが発生しました: {str(e)}"
            print(f"UIエラー: {error_msg}")
            print("エラーの詳細:")
            import traceback
            print(traceback.format_exc())
            return error_msg

    # UIの作成
    with gr.Blocks(
        title="Social Media Sentiment Analysis",
        theme=gr.themes.Soft()
    ) as interface:
        gr.Markdown("""
        # Social Media Sentiment Analysis
        
        Enter keywords to analyze sentiment in news articles.
        
        ## How to Use
        1. Enter search keywords in English (e.g., artificial intelligence, OpenAI, ChatGPT)
        2. Select how many days back to search (1-7 days)
        3. Click "Analyze" button
        
        ## Notes
        - Please use English keywords
        - If no articles are found, try different keywords or time period
        - Analysis may take a few seconds
        """)
        
        with gr.Row():
            query = gr.Textbox(
                label="Search Keywords (English)",
                placeholder="e.g., artificial intelligence, OpenAI, ChatGPT",
                info="Enter keywords in English"
            )
        
        with gr.Row():
            days_ago = gr.Slider(
                minimum=1,
                maximum=7,
                value=1,
                step=1,
                label="Days to Search Back",
                info="Select 1-7 days"
            )
        
        with gr.Row():
            analyze_btn = gr.Button("Analyze", variant="primary")
        
        with gr.Row():
            output = gr.Textbox(
                label="Analysis Results",
                lines=10,
                info="Analysis results will be displayed here"
            )
        
        analyze_btn.click(
            fn=process_input,
            inputs=[query, days_ago],
            outputs=output
        )
    
    return interface 