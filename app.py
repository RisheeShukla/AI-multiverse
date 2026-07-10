import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import random
import time
from datetime import datetime

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
st.set_page_config(
    page_title="AI Multiverse",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stChatInputContainer { padding-bottom: 20px; }
    .footer { text-align:center; padding-top:20px; color:gray; font-size: 14px; }
</style>
""", unsafe_allow_html=True)


if "history" not in st.session_state:
    st.session_state.history = []


personalities = {
    "🦾 Iron Man": "You are Tony Stark (Iron Man). Speak confidently with humor and intelligence.",
    "🦇 Batman": "You are Batman. Be dark, serious and mysterious.",
    "🕵 Sherlock Holmes": "You are Sherlock Holmes. Answer with logical deductions.",
    "⚽ Ronaldo Fan": "You are Cristiano Ronaldo's biggest fan.",
    "💻 Hacker": "You are an ethical hacker who explains cybersecurity.",
    "🧙 Harry Potter": "You are Harry Potter from Hogwarts.",
    "🤣 Stand-up Comedian": "Always answer with jokes.",
    "🇺🇸 Donald Trump": "Talk like Donald Trump.",
    "🤖 Robot": "You are a futuristic AI robot.",
    "🧠 Albert Einstein": "Explain everything scientifically.",
    "⚡ Thor": "You are Thor, God of Thunder.",
    "😈 Loki": "You are Loki, clever and mischievous.",
    "🏏 Virat Kohli": "Speak like Virat Kohli.",
    "🚀 Elon Musk": "Talk like Elon Musk.",
    "📱 Steve Jobs": "Talk like Steve Jobs.",
    "🎬 Deadpool": "Talk like Deadpool with funny sarcasm."
}


avatars = { key: key.split(" ")[0] for key in personalities.keys() }

styles = {
    "Friendly": "Be friendly.",
    "Funny": "Be humorous.",
    "Professional": "Be professional.",
    "Motivational": "Motivate the user.",
    "Short": "Keep replies concise."
}

lengths = {
    "Short": "Maximum 60 words.",
    "Medium": "Around 120 words.",
    "Long": "Around 250 words."
}

surprise_prompts = [
    "Tell me a joke.", "Motivate me.", "Teach me AI.",
    "Explain quantum physics simply.", "How can I become successful?",
    "What is happiness?", "Give me study tips.", "Write a poem."
]


with st.sidebar:
    st.title("⚙️ Settings")
    
    personality = st.selectbox("🎭 Choose Personality", list(personalities.keys()))
    reply_style = st.selectbox("🎨 Response Style", list(styles.keys()))
    reply_length = st.selectbox("📏 Response Length", list(lengths.keys()))
    
    st.divider()
    
    # Actions
    st.subheader("🛠️ Actions")
    surprise_clicked = st.button("🎲 Surprise Me (Auto-Send)", use_container_width=True)
    
    if st.button("🗑️ Clear Chat", use_container_width=True, type="primary"):
        st.session_state.history = []
        st.rerun()

    # Chat Statistics Expander
    with st.expander("📊 Chat Statistics"):
        total_messages = len(st.session_state.history)
        total_characters = sum(len(chat["user"]) for chat in st.session_state.history)
        total_words = sum(len(chat["user"].split()) for chat in st.session_state.history)
        
        st.metric("Total Messages", total_messages)
        st.metric("Total Characters", total_characters)
        st.metric("Total Words", total_words)

    # Download Chat
    if len(st.session_state.history) > 0:
        full_chat = ""
        for chat in st.session_state.history:
            full_chat += f"You: {chat['user']}\n{chat['personality']}: {chat['ai']}\n{'-'*30}\n\n"
        
        st.download_button(
            "📥 Download Conversation",
            full_chat,
            file_name="multiverse_chat.txt",
            use_container_width=True
        )
st.title("🌌 The Multiverse Chatbot")
st.caption(f"Currently talking to: **{personality}** | Style: **{reply_style}**")

# Display Chat History
for chat in st.session_state.history:
    with st.chat_message("user", avatar="👤"):
        st.markdown(chat["user"])
    with st.chat_message("assistant", avatar=avatars.get(chat["personality"], "🤖")):
        st.caption(f"{chat['personality']} • {chat['time']}")
        st.markdown(chat["ai"])


user_input = st.chat_input("💬 Type your message to the multiverse...")

if surprise_clicked:
    user_input = random.choice(surprise_prompts)

if user_input:
    if len(user_input) > 500:
        st.error("Message should be less than 500 characters.")
        st.stop()

    
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

  
    system_prompt = f"""
    {personalities[personality]}
    {styles[reply_style]}
    {lengths[reply_length]}
    Stay completely in character.
    User: {user_input}
    """

    with st.chat_message("assistant", avatar=avatars.get(personality, "🤖")):
        with st.spinner("Thinking..."):
            try:
                start = time.time()
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=system_prompt
                )
                reply = response.text
                end = time.time()
                current_time = datetime.now().strftime("%I:%M %p")
            
                st.caption(f"{personality} • {current_time} (Took {round(end-start, 2)}s)")
                st.markdown(reply)
                st.session_state.history.append({
                    "user": user_input,
                    "ai": reply,
                    "time": current_time,
                    "personality": personality
                })
                
            except Exception as e:
                st.error(f"Error generating response: {e}")


st.markdown("""
<div class="footer">
    <hr>
    🚀 <b>AI Multiverse Upgraded</b><br>
    
</div>
""", unsafe_allow_html=True)
