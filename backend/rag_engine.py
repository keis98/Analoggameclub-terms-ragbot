import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
# ↓ 【修正箇所】「langchain.chains」から「langchain_classic.chains」に変更！
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# 環境変数の読み込み(.envファイルからAPIキーを取得)
load_dotenv()

class RAGEngine:
    def __init__(self, persist_directory="vector_store"):
        # 【重要】データベース作成時と同じ最新のモデルを指定
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        
        self.vectorstore = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
        
        # 質問に関連する部分を上位3件取得する設定
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        
        # 回答を生成するAI（無料で高速なGemini 1.5 Flashを使用）
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        
        # AIに対するプロンプト（指示）
        system_prompt = (
            "あなたはアナログゲームサークルの規約案内アシスタントです。\n"
            "以下の提供されたコンテキスト（サークル規約）のみを使用して、質問に答えてください。\n"
            "コンテキストに答えがない場合は、勝手な推測はせず「規約には明確に記載されていません」と答えてください。\n"
            "丁寧で分かりやすい日本語で回答してください。\n\n"
            "コンテキスト:\n"
            "{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        # 検索結果とAIの思考を繋ぐチェーンの作成
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, question_answer_chain)

    def get_answer(self, question):
        # 検索と回答生成を実行
        response = self.rag_chain.invoke({"input": question})
        return response["answer"]