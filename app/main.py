from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import gradio as gr
from .ui import create_ui

# .envファイルを読み込む
load_dotenv()

from .job_controller import router

app = FastAPI(title="SocialEar API")

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルートパスへのアクセスを/uiにリダイレクト
@app.get("/")
async def root():
    return RedirectResponse(url="/ui")

# ルーターの登録
app.include_router(router)

# Gradioインターフェースの登録
interface = create_ui()
app = gr.mount_gradio_app(app, interface, path="/ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 