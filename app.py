import streamlit as st
from openai import OpenAI

# --- App Configuration ---
st.set_page_config(
    page_title="🤖 Chatbot Assistant",
    page_icon="🐑",
    layout="centered",
)

# --- Secrets Management ---
# For local development, you can set the API key directly.
# For deployment, use Streamlit Secrets: https://docs.streamlit.io/deploy/concepts/secrets-management
api_key = st.secrets["OPENROUTER_API_KEY"]

# --- OpenAI Client Initialization ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# --- UI Elements ---
st.title("🤖 Chatbot Assistant")
st.caption("Masukkan Pesan yang Anda Inginkan untuk Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hai! Aku adalah Chatbot yang siap membantu kamu!"}
    ]

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input and Logic ---
user_prompt = st.chat_input("Ketik pesanmu untuk chatbot di sini...")

if user_prompt:
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            completion = client.chat.completions.create(
                extra_headers={
                    # Optional: Add these if you want them for OpenRouter rankings
                    # "HTTP-Referer": "<YOUR_SITE_URL>",
                    # "X-Title": "<YOUR_SITE_NAME>",
                },
                model="deepseek/deepseek-r1-0528:free", # Or any other model you prefer on OpenRouter
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True, # Optional: for a streaming effect
            )
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Oops! Terjadi kesalahan: {e}")
            full_response = "Maaf, aku sedang tidak bisa membantumu saat ini. 🥺"
            message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Optional: Add a sidebar with more info or controls ---
with st.sidebar:
    st.header("Tentang Bot Ini")
    st.markdown("""
    Bot ini menggunakan model AI dari OpenRouter untuk membantu kebutuhan Anda.
    Cukup ketik permintaanmu dan lihat hasilnya! 🐐🎉
    """)
    st.subheader("Model Digunakan:")
    st.markdown("Deepseek R1 (via OpenRouter)")

    st.markdown("---")
    if st.button("Mulai Percakapan Baru"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hai! Silahkan ketik pesanmu di sini!"}
        ]
        st.rerun()

    st.markdown("---")
    st.markdown("Dibuat oleh Mohammad Aris Darmawan")
