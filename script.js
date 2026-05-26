marked.setOptions({ breaks: true });
const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// アイコン付きのメッセージ生成（新構造）
function appendMessage(role, text) {
    const row = document.createElement('div');
    row.className = `chat-row ${role}-row`;
    
    const avatar = document.createElement('div');
    avatar.className = `avatar ${role}-avatar`;
    avatar.textContent = role === 'user' ? '👤' : '🤖';
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    messageDiv.innerHTML = role === 'assistant' ? marked.parse(text) : text;
    
    if (role === 'assistant') { row.appendChild(avatar); row.appendChild(messageDiv); }
    else { row.appendChild(messageDiv); row.appendChild(avatar); }
    
    chatHistory.appendChild(row);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return row; // 生成したDOM要素を返す（削除用）
}

async function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return;

    appendMessage('user', question);
    userInput.value = '';

    // 「回答を生成中」メッセージを表示し、その要素を保持
    const loadingRow = document.createElement('div');
    loadingRow.className = 'chat-row assistant-row';
    loadingRow.innerHTML = `<div class="avatar assistant-avatar">🤖</div><div class="message assistant-message loading">回答を生成中...</div>`;
    chatHistory.appendChild(loadingRow);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
        // const response = await fetch('http://localhost:8000/api/chat', {
        const response = await fetch('https://analoggameclub-terms-ragbot.onrender.com/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });
        const data = await response.json();
        
        // 成功したら「回答を生成中」を削除
        loadingRow.remove();
        appendMessage('assistant', data.answer);
    } catch (e) {
        loadingRow.remove();
        appendMessage('assistant', 'サーバーとの通信に失敗しました。');
    }
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });