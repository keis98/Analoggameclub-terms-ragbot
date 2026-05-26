import asyncio
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag_engine import RAGEngine
from fastapi.concurrency import run_in_threadpool

# アプリケーションの初期化
app = FastAPI(title="Analog Game Club RAG API")

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AIエンジンの読み込み
engine = RAGEngine()

# サーバーを眠らせないためのPing処理（10分おきに自分にアクセス）
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(keep_alive())

async def keep_alive():
    url = "https://analoggameclub-terms-ragbot.onrender.com"
    async with httpx.AsyncClient() as client:
        while True:
            try:
                await client.get(url)
            except:
                pass
            await asyncio.sleep(600)

# フロントエンドから受け取るデータの形を定義
class ChatRequest(BaseModel):
    question: str

# APIのエンドポイント
# @app.post("/api/chat")
# async def chat(request: ChatRequest):
#     # 質問を受け取り、RAGEngineで回答を生成して返す
#     answer = engine.get_answer(request.question)
#     return {"answer": answer}
@app.post("/api/chat")
async def chat(request: ChatRequest):
    # 重い処理を別スレッドで実行してタイムアウトを防ぐ
    answer = await run_in_threadpool(engine.get_answer, request.question)
    return {"answer": answer}