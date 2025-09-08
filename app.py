import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# Dify APIキーとベースURL
API_KEY = os.getenv("DIFY_API_KEY")
API_URL = "https://api.dify.ai/v1/chat-messages"

st.set_page_config(
    page_title="舞妓さんとのお話", 
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# カスタムCSSで和風デザインを適用
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #f5f1e8 0%, #e8dcc0 50%, #d4c4a8 100%);
        font-family: 'Noto Sans JP', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f1e8 0%, #e8dcc0 50%, #d4c4a8 100%);
    }
    
    .stApp > div {
        background: transparent;
    }
    
    /* タイトルスタイル */
    .main-title {
        text-align: center;
        color: #8B4513;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(45deg, #8B4513, #D2691E, #CD853F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* 舞妓さんアイコン */
    .maiko-icon {
        font-size: 3rem;
        text-align: center;
        margin: 1rem 0;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* チャットコンテナ */
    .chat-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 2px solid #D2691E;
    }
    
    /* ユーザーメッセージ（右寄り） */
    .user-message {
        background: linear-gradient(135deg, #FFE4B5, #F5DEB3);
        border: 2px solid #D2691E;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0 0.5rem auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        max-width: 70%;
        margin-left: auto;
        margin-right: 0;
    }
    
    .user-icon {
        font-size: 2rem;
        flex-shrink: 0;
        margin-top: 0.25rem;
        order: 2;
    }
    
    .user-content {
        flex: 1;
        order: 1;
        text-align: right;
    }
    
    /* アシスタントメッセージ（左寄り） */
    .assistant-message {
        background: linear-gradient(135deg, #F0F8FF, #E6F3FF);
        border: 2px solid #4682B4;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem auto 0.5rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        max-width: 70%;
        margin-left: 0;
        margin-right: auto;
    }
    
    .assistant-icon {
        font-size: 2rem;
        flex-shrink: 0;
        margin-top: 0.25rem;
        order: 1;
    }
    
    .assistant-content {
        flex: 1;
        order: 2;
        text-align: left;
    }
    
    /* 入力フィールド */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #D2691E;
        border-radius: 25px;
        padding: 0.75rem 1rem;
        font-family: 'Noto Sans JP', sans-serif;
    }
    
    /* ボタンスタイル */
    .stButton > button {
        background: linear-gradient(135deg, #D2691E, #CD853F);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-family: 'Noto Sans JP', sans-serif;
        font-weight: 500;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    /* 桜の装飾 */
    .sakura-decoration {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .sakura-petal {
        position: absolute;
        width: 10px;
        height: 10px;
        background: #FFB6C1;
        border-radius: 50% 0;
        animation: fall 10s linear infinite;
    }
    
    @keyframes fall {
        0% {
            transform: translateY(-100vh) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    /* サイドバー */
    .css-1d391kg {
        background: linear-gradient(180deg, #f5f1e8 0%, #e8dcc0 100%);
    }
</style>
""", unsafe_allow_html=True)

# 桜の装飾を追加
st.markdown("""
<div class="sakura-decoration" id="sakura-container"></div>
<script>
    function createSakuraPetal() {
        const container = document.getElementById('sakura-container');
        const petal = document.createElement('div');
        petal.className = 'sakura-petal';
        petal.style.left = Math.random() * 100 + '%';
        petal.style.animationDelay = Math.random() * 10 + 's';
        petal.style.animationDuration = (Math.random() * 5 + 5) + 's';
        container.appendChild(petal);
        
        setTimeout(() => {
            petal.remove();
        }, 10000);
    }
    
    setInterval(createSakuraPetal, 500);
</script>
""", unsafe_allow_html=True)

# メインタイトル
st.markdown('<div class="main-title">🌸 舞妓さんとのお話 🌸</div>', unsafe_allow_html=True)

# 舞妓さんアイコン
st.markdown('<div class="maiko-icon">👘</div>', unsafe_allow_html=True)

# 舞妓さんからの会話のヒント
st.markdown("""
<div style="background: rgba(255, 255, 255, 0.8); border-radius: 15px; padding: 1rem; margin: 1rem 0; border: 2px solid #D2691E;">
    <p style="margin: 0; text-align: center; font-size: 0.9rem; color: #8B4513;">
        💡 <strong>舞妓桜との会話のヒント</strong><br>
        「京都の名所について教えて」「和菓子について聞きたい」「舞妓の文化について知りたい」<br>
        「季節の行事について」「着物について」「お茶について」など、お気軽にお話しくださいませ
    </p>
</div>
""", unsafe_allow_html=True)

# セッションステートの初期化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

# 舞妓さんからの挨拶メッセージ（初回のみ表示）
if not st.session_state.messages:
    # 季節に応じた挨拶を生成
    import datetime
    now = datetime.datetime.now()
    month = now.month
    
    if month in [3, 4, 5]:
        season_greeting = "桜の季節が過ぎ、新緑が美しい頃となりました"
    elif month in [6, 7, 8]:
        season_greeting = "暑い夏の日が続いておりますが、京都の夏は風情があります"
    elif month in [9, 10, 11]:
        season_greeting = "秋の深まりとともに、紅葉の美しい季節となりました"
    else:
        season_greeting = "寒い冬の日が続いておりますが、京都の冬も風情があります"
    
    st.markdown(f"""
    <div class="chat-container">
        <div class="assistant-message">
            <p style="font-size: 1.1rem; margin: 0; text-align: center;">
                🌸 こんにちは、お客様 🌸<br>
                舞妓の桜と申します。<br>
                {season_greeting}どす。<br>
                京都の美しい文化や伝統について、<br>
                お話しさせていただければと思います。<br>
                何でもお気軽にお聞かせくださいませ。
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# チャット履歴の表示
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <div class="user-icon">👨‍💼</div>
            <div class="user-content">
                <p style="margin: 0; font-weight: 500;">{message["content"]}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <div class="assistant-icon">🌸</div>
            <div class="assistant-content">
                <p style="margin: 0; font-weight: 400;">{message["content"]}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ユーザーからの入力
if prompt := st.chat_input("舞妓さんに何かお話しください..."):
    # ユーザーメッセージをチャット履歴に追加して表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"""
    <div class="user-message">
        <div class="user-icon">👨‍💼</div>
        <div class="user-content">
            <p style="margin: 0; font-weight: 500;">{prompt}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Dify APIへのリクエスト準備
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    # 舞妓さん風のプロンプトを追加
    maiko_prompt = f"""
あなたは京都の舞妓「桜」です。以下の性格と話し方で応答してください：

【性格・話し方】
- 丁寧で上品な敬語を常に使用
- 京都弁の要素を少し取り入れる（「〜どす」「〜はんなり」「〜やす」など）
- 優雅で控えめ、上品な話し方
- 京都の文化や伝統について詳しく説明できる
- 季節感を大切にし、季節に応じた話題を提供
- 舞妓としての誇りと京都への愛着を持っている

【京都の知識】
- 京都の名所、寺院、神社について詳しい
- 和菓子、お茶、着物、舞妓の文化について説明できる
- 京都の四季の美しさや行事について語れる
- 伝統工芸や文化について深い理解がある

【会話スタイル】
- 相手を「お客様」と呼ぶ
- 京都の美しさや伝統を自然に会話に織り込む
- 季節の話題を積極的に取り入れる
- 控えめで上品、でも親しみやすい

ユーザーの質問: {prompt}

舞妓桜として、上記の性格と話し方で応答してください。
"""
    
    data = {
        "inputs": {},
        "query": maiko_prompt,
        "response_mode": "streaming",
        "user": "maiko-sakura-user", # ユーザーを識別するための一意のID
    }
    if st.session_state.conversation_id:
        data["conversation_id"] = st.session_state.conversation_id

    # アシスタントの応答を待つ間にプレースホルダーを表示
    message_placeholder = st.empty()
    full_response = ""
    
    try:
        with requests.post(API_URL, headers=headers, json=data, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_lines():
                if chunk:
                    decoded_chunk = chunk.decode('utf-8')
                    if decoded_chunk.startswith('data:'):
                        try:
                            json_data = json.loads(decoded_chunk[5:])
                            event = json_data.get("event")
                            if event == "message":
                                answer_chunk = json_data.get("answer", "")
                                full_response += answer_chunk
                                message_placeholder.markdown(f"""
                                <div class="assistant-message">
                                    <div class="assistant-icon">🌸</div>
                                    <div class="assistant-content">
                                        <p style="margin: 0; font-weight: 400;">{full_response}▌</p>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            elif event == "message_end":
                                st.session_state.conversation_id = json_data.get("conversation_id")
                        except json.JSONDecodeError:
                            # JSONデコードエラーは無視して次の行へ
                            continue
        message_placeholder.markdown(f"""
        <div class="assistant-message">
            <div class="assistant-icon">🌸</div>
            <div class="assistant-content">
                <p style="margin: 0; font-weight: 400;">{full_response}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # アシスタントの応答をチャット履歴に追加
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except requests.exceptions.RequestException as e:
        st.error(f"APIリクエスト中にエラーが発生しました: {e}")
    except Exception as e:
        st.error(f"予期せぬエラーが発生しました: {e}")

