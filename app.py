import streamlit as st
import os
from backend.rag_engine import RAGEngine

# ページの設定
st.set_page_config(page_title="サークル規約BOT", page_icon="🎲")
st.title("🎲 アナログゲームサークル 規約AIボット")
st.write("貸出プロトコルや行動規範など、サークルの規約について何でも質問してください！")

# RAGエンジンの読み込み（毎回読み込まないようキャッシュ化して高速化）
@st.cache_resource
def load_engine():
    if not os.path.exists("vector_store"):
        st.error("エラー: 規約データベースが見つかりません。先にバックエンドでデータを取り込んでください。")
        st.stop()
    return RAGEngine()

engine = load_engine()

# チャットの会話履歴を初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去の会話履歴を画面に描画
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの入力欄
if prompt := st.chat_input("質問を入力（例：備品を借りる手順を教えて）"):
    # ユーザーの質問を履歴に追加し、画面に表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIの回答を生成して履歴に追加し、画面に表示
    with st.chat_message("assistant"):
        with st.spinner("規約を確認中..."):
            answer = engine.get_answer(prompt)
            st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})