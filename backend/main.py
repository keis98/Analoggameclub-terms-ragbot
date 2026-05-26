from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag_engine import RAGEngine

# アプリケーションの初期化
app = FastAPI(title="Analog Game Club RAG API")

# CORSの設定（フロントエンドとバックエンドで通信できるようにする必須設定）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発用。どこからでもアクセス許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AIエンジンの読み込み
engine = RAGEngine()

# フロントエンドから受け取るデータの形を定義
class ChatRequest(BaseModel):
    question: str

# APIのエンドポイント（URLの窓口）
@app.post("/api/chat")
async def chat(request: ChatRequest):
    # 質問を受け取り、RAGEngineで回答を生成して返す
    answer = engine.get_answer(request.question)
    return {"answer": answer}