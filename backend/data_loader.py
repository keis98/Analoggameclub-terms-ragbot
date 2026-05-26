import os
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# 環境変数の読み込み(.envファイルからAPIキーを取得)
load_dotenv()

def create_vector_store(docx_path="data/rules.docx", persist_directory="vector_store"):
    print(f"{docx_path} から規約を読み込んでいます...")
    
    # Wordファイルの読み込み
    loader = Docx2txtLoader(docx_path)
    documents = loader.load()

    # AIが処理しやすいように文章を適切なサイズに分割
    print("文章を分割しています...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,     # 500文字ずつに分割
        chunk_overlap=50    # 文脈が途切れないように50文字重複させる
    )
    docs = text_splitter.split_documents(documents)

    # Geminiのモデルを使ってベクトル化し、ChromaDBに保存
    print("データベースを構築しています...")
    # ↓【修正箇所】現在稼働している最新のモデル「gemini-embedding-001」に変更しました
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectorstore.persist()
    print("✨ ベクトルデータベースの作成が完了しました！")

if __name__ == "__main__":
    # このファイルが直接実行された時にデータベースを作成
    create_vector_store()