import streamlit as st
import requests
import urllib.parse
import random
import time
import json

# ============================================================
# PAGE CONFIG — Dark Theme, Mobile Friendly
# ============================================================
st.set_page_config(
    page_title="Devi Onfire AI",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;900&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .main, .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: white !important;
    }
    
    .stTextArea textarea, .stTextInput input {
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 15px !important;
        padding: 12px !important;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #ff416c, #ff4b2b) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 14px 32px !important;
        font-weight: 700 !important;
        font-size: 1.1em !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 30px rgba(255, 75, 43, 0.4) !important;
    }
    
    .success-box {
        background: linear-gradient(90deg, rgba(46, 213, 115, 0.2), rgba(46, 213, 115, 0.05));
        border-left: 5px solid #2ed573;
        padding: 18px;
        border-radius: 15px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
    }
    
    .warning-box {
        background: linear-gradient(90deg, rgba(255, 193, 7, 0.2), rgba(255, 193, 7, 0.05));
        border-left: 5px solid #ffc107;
        padding: 18px;
        border-radius: 15px;
        margin: 15px 0;
        color: #ffc107 !important;
        backdrop-filter: blur(10px);
    }
    
    .info-box {
        background: linear-gradient(90deg, rgba(0, 168, 255, 0.2), rgba(0, 168, 255, 0.05));
        border-left: 5px solid #00a8ff;
        padding: 18px;
        border-radius: 15px;
        margin: 15px 0;
        color: #00a8ff !important;
        backdrop-filter: blur(10px);
    }
    
    .chat-container {
        background: rgba(255,255,255,0.03);
        border-radius: 25px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(255,255,255,0.08);
        max-height: 450px;
        overflow-y: auto;
    }
    
    .user-msg {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 14px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 8px 0 8px auto;
        max-width: 75%;
        word-wrap: break-word;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .ai-msg {
        background: rgba(255,255,255,0.08);
        color: white;
        padding: 14px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 8px auto 8px 0;
        max-width: 75%;
        word-wrap: break-word;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .poster-container {
        border-radius: 25px;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(0,0,0,0.6);
        margin: 25px 0;
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .audio-container {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 15px !important;
        color: rgba(255,255,255,0.7) !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #ff416c, #ff4b2b) !important;
        color: white !important;
        box-shadow: 0 5px 20px rgba(255, 75, 43, 0.3) !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .stSpinner > div { border-top-color: #ff416c !important; }
    
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# API KEYS FROM SECRETS
# ============================================================
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
AI_MUSIC_API_KEY = st.secrets.get("AI_MUSIC_API_KEY", "")  # aimusicapi.ai
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# ============================================================
# SYSTEM PROMPTS
# ============================================================
LYRICS_SYSTEM_PROMPT = """
You are an elite Punjabi Music Lyricist in Sidhu Moose Wala's signature style.

RULES:
- Roman Punjabi mein likh (English letters mein Punjabi words)
- Aggressive, deep, meaningful lyrics
- Street life, pride, friendship, struggle, success
- Heavy Punjabi cultural references
- Sidhu's unique flow and attitude

OUTPUT FORMAT:
🎵 [BEAT SPECIFICATION]
Genre: Punjabi Drill / Hip Hop
BPM: 140-160
Beat: Heavy 808, dark synth, trap drums

📝 [SONG LYRICS]
[INTRO]
...

[VERSE 1]
...

[CHORUS] (Hook - catchy, repeat)
...

[VERSE 2]
...

[OUTRO]
...

🔥 [VIBE]
Overall feel describe karo.
"""

CHAT_SYSTEM_PROMPT = """
You are "Sidhu Moose Wala AI" — baat karne ka style bilkul Sidhu jaisa.

RULES:
- Roman Punjabi mein jawab de
- Aggressive but respectful
- "Bai", "Putt", "Jatt", "Scene" use kar
- Confident, attitude wale replies
- User ko "Bai" ya "Veere" bula
- Short, punchy replies
- Emojis use kar 🔥💯🎤
"""

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div style="text-align: center; padding: 30px 0 20px 0;">
    <h1 style="font-size: 3em; background: linear-gradient(90deg, #ff416c, #ff4b2b, #f9ca24, #ff416c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; letter-spacing: -1px;">
        🔥 Devi Onfire AI
    </h1>
    <p style="color: rgba(255,255,255,0.6); font-size: 1.2em; margin-top: -5px;">
        Sidhu Moose Wala AI Studio — Lyrics • Beats • Posters • Full Songs
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["💬 AI Chat", "🎵 Song Generator", "ℹ️ Setup Guide"])

# ============================================================
# TAB 1: CHAT
# ============================================================
with tab1:
    st.markdown("### 💬 Sidhu AI se Baat Karein")
    st.markdown("<p style='color: rgba(255,255,255,0.5);'>Apne veere se kuch bhi poochho!</p>", unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_html += f'<div style="display: flex; justify-content: flex-end;"><div class="user-msg">{msg["content"]}</div></div>'
        else:
            chat_html += f'<div style="display: flex; justify-content: flex-start;"><div class="ai-msg">{msg["content"]}</div></div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    
    user_chat = st.text_input("Message...", placeholder="Veere life mein struggle chal rahi hai...", key="chat_input", label_visibility="collapsed")
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("🚀 Send", key="send_chat", use_container_width=True):
            if not user_chat:
                st.warning("Pehle kuch likh toh sahi!")
            elif not GROQ_API_KEY:
                st.error("GROQ_API_KEY missing!")
            else:
                st.session_state.chat_history.append({"role": "user", "content": user_chat})
                with st.spinner("Veere soch raha hai..."):
                    try:
                        import groq
                        client = groq.Groq(api_key=GROQ_API_KEY)
                        messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
                        for h in st.session_state.chat_history[-6:]:
                            messages.append({"role": h["role"], "content": h["content"]})
                        
                        response = client.chat.completions.create(
                            messages=messages,
                            model="llama-3.3-70b-versatile",
                            temperature=0.9,
                            max_tokens=500
                        )
                        ai_reply = response.choices[0].message.content
                        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

# ============================================================
# TAB 2: SONG GENERATOR (SUNO-STYLE)
# ============================================================
with tab2:
    st.markdown("### 🎤 AI Song Generator — Suno Style")
    st.markdown("<p style='color: rgba(255,255,255,0.5);'>Sirf prompt likho, AI pura gaana banayega: Lyrics + Beat + Vocals + Poster!</p>", unsafe_allow_html=True)
    
    # Input Section
    col1, col2 = st.columns([3, 1])
    with col1:
        user_prompt = st.text_area(
            "✍️ Song Topic / Idea:",
            placeholder="e.g. Doston ki yaari, mehnat, gaddari, aggressive drill vibe...",
            height=120
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        song_style = st.selectbox("Style:", ["Punjabi Drill", "Hip Hop", "Sad/Melodic", "Gangster Vibe"])
        make_vocals = st.toggle("🎙️ Vocals ke saath gaana", value=True)
    
    # Advanced options
    with st.expander("⚙️ Advanced Settings"):
        duration = st.slider("⏱️ Song Duration (seconds):", 30, 240, 120, 30)
        poster_style = st.selectbox("🎨 Poster Style:", ["Cinematic Dark", "Neon Cyberpunk", "Vintage Desi", "Studio Portrait"])
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    if st.button("🔥 FULL SONG GENERATE KAREIN", type="primary"):
        if not user_prompt:
            st.warning("Pehle koi topic likh bhai!")
        elif not GROQ_API_KEY:
            st.error("❌ GROQ_API_KEY missing! Streamlit Secrets mein add karein.")
        else:
            try:
                # ==========================================================
                # STEP 1: LYRICS
                # ==========================================================
                with st.spinner("⚡ Step 1/4: AI Lyrics generate ho rahe hain..."):
                    import groq
                    client = groq.Groq(api_key=GROQ_API_KEY)
                    
                    style_addition = f"\nStyle: {song_style}. Duration: {duration} seconds ke hisaab se lyrics adjust karo."
                    
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": LYRICS_SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt + style_addition}
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.85,
                        max_tokens=2500
                    )
                    generated_lyrics = chat_completion.choices[0].message.content

                st.markdown("""
                <div class="success-box">
                    <h4>✅ Lyrics Tayar Hain!</h4>
                </div>
                """, unsafe_allow_html=True)
                
                st.text_area("📜 Generated Lyrics:", value=generated_lyrics, height=300)

                # ==========================================================
                # STEP 2: POSTER IMAGE
                # ==========================================================
                with st.spinner("🖼️ Step 2/4: HD Poster generate ho raha hai..."):
                    random_seed = random.randint(1, 999999)
                    
                    style_modifiers = {
                        "Cinematic Dark": "cinematic dark lighting, dramatic shadows, film grain, moody atmosphere",
                        "Neon Cyberpunk": "neon lights, cyberpunk city, futuristic, glowing effects",
                        "Vintage Desi": "vintage Punjabi aesthetic, warm golden colors, desi background, old school",
                        "Studio Portrait": "professional studio lighting, clean dark background, portrait photography"
                    }
                    
                    image_prompt = (
                        f"Professional album cover, Punjabi male singer with orange turban pagri, "
                        f"black sunglasses, thick beard, wearing designer black outfit, "
                        f"standing near black luxury SUV, {user_prompt}, "
                        f"{style_modifiers[poster_style]}, "
                        f"8k ultra detailed, photorealistic, movie poster style, aggressive confident pose"
                    )
                    
                    encoded_prompt = urllib.parse.quote(image_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={random_seed}&enhance=true"

                st.markdown("### 🖼️ Song Poster")
                
                # Try to load image
                try:
                    img_response = requests.get(image_url, timeout=30)
                    if img_response.status_code == 200:
                        st.markdown(f"""
                        <div class="poster-container">
                            <img src="{image_url}" style="width: 100%; border-radius: 25px;">
                        </div>
                        """, unsafe_allow_html=True)
                        st.caption(f"🎨 AI Poster | Seed: {random_seed} | Style: {poster_style}")
                    else:
                        st.image(image_url, use_container_width=True)
                except:
                    st.image(image_url, use_container_width=True)

                # ==========================================================
                # STEP 3: FULL SONG WITH VOCALS (AI Music API)
                # ==========================================================
                st.markdown("### 🎵 AI Generated Song")
                
                if make_vocals and AI_MUSIC_API_KEY:
                    with st.spinner("🎙️ Step 3/4: Full song with vocals generate ho raha hai... (30-60 sec)"):
                        
                        # Extract clean lyrics for API (remove headers/formatting)
                        clean_lyrics = generated_lyrics.replace("🎵", "").replace("📝", "").replace("🔥", "")
                        clean_lyrics = clean_lyrics.replace("[BEAT SPECIFICATION]", "").replace("[SONG LYRICS]", "")
                        clean_lyrics = clean_lyrics.replace("[INTRO]", "").replace("[VERSE 1]", "")
                        clean_lyrics = clean_lyrics.replace("[CHORUS]", "").replace("[VERSE 2]", "")
                        clean_lyrics = clean_lyrics.replace("[OUTRO]", "").replace("[VIBE]", "")
                        clean_lyrics = " ".join(clean_lyrics.split())[:800]  # Limit for API
                        
                        # AI Music API call
                        api_url = "https://api.aimusicapi.ai/v1/songs"
                        headers = {
                            "Authorization": f"Bearer {AI_MUSIC_API_KEY}",
                            "Content-Type": "application/json"
                        }
                        
                        payload = {
                            "prompt": f"Punjabi {song_style.lower()} song, aggressive, energetic, Sidhu Moose Wala style, {user_prompt}",
                            "lyrics": clean_lyrics if clean_lyrics else "auto",
                            "duration": duration,
                            "studio_quality": True
                        }
                        
                        # Make API request
                        response = requests.post(api_url, headers=headers, json=payload, timeout=120)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            if result.get("status") == "completed" and result.get("audio_url"):
                                audio_url = result["audio_url"]
                                
                                st.markdown("""
                                <div class="audio-container">
                                    <h4>🔊 Your AI Song is Ready!</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Stream audio from URL
                                st.audio(audio_url, format="audio/mp3")
                                
                                st.markdown(f"""
                                <div class="success-box">
                                    ✅ <b>Gaana tayar hai bhai!</b><br>
                                    🎵 Style: {song_style}<br>
                                    ⏱️ Duration: {duration}s<br>
                                    💾 <a href="{audio_url}" target="_blank" style="color: #2ed573;">Download Song</a>
                                </div>
                                """, unsafe_allow_html=True)
                                
                            elif result.get("status") == "pending" and result.get("id"):
                                job_id = result["id"]
                                st.info(f"⏳ Song queue mein hai (Job ID: {job_id}). Thodi der mein refresh karein.")
                                
                                # Poll for result
                                progress_bar = st.progress(0)
                                for i in range(20):
                                    time.sleep(3)
                                    poll_resp = requests.get(f"{api_url}/{job_id}", headers=headers, timeout=30)
                                    if poll_resp.status_code == 200:
                                        poll_result = poll_resp.json()
                                        if poll_result.get("status") == "completed":
                                            audio_url = poll_result["audio_url"]
                                            st.audio(audio_url, format="audio/mp3")
                                            st.success("✅ Gaana tayar hai!")
                                            break
                                    progress_bar.progress((i + 1) * 5)
                                else:
                                    st.warning("⏳ Abhi tak ready nahi hua. Baad mein check karein.")
                            else:
                                st.warning(f"⚠️ API Response: {result}")
                        else:
                            st.error(f"❌ API Error: {response.status_code} - {response.text[:200]}")
                            
                elif make_vocals and not AI_MUSIC_API_KEY:
                    st.markdown("""
                    <div class="warning-box">
                        ⚠️ <b>AI Music API Key missing!</b><br>
                        Vocals ke saath gaana chahiye toh <b>AI_MUSIC_API_KEY</b> add karo Streamlit Secrets mein.<br>
                        👉 <b>aimusicapi.ai</b> pe jake free account banao — 30 free credits milenge!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Fallback: MusicGen Beat only
                    st.markdown("### 🥁 Fallback: Instrumental Beat Only")
                    
                    if HF_TOKEN:
                        with st.spinner("MusicGen se beat generate ho raha hai..."):
                            from huggingface_hub import InferenceClient
                            hf_client = InferenceClient(token=HF_TOKEN)
                            
                            beat_prompt = f"Punjabi {song_style.lower()} beat, heavy 808 bass, dark synth, trap drums, energetic, {user_prompt}"
                            
                            for attempt in range(3):
                                try:
                                    audio_bytes = hf_client.text_to_audio(beat_prompt, model="facebook/musicgen-small")
                                    st.audio(audio_bytes, format="audio/wav")
                                    st.success("✅ Beat tayar hai! (Vocals ke liye AI Music API lagao)")
                                    break
                                except:
                                    time.sleep(5)
                            else:
                                st.error("❌ Beat bhi fail ho gaya. HF server busy hai.")
                    else:
                        st.info("💡 HF_TOKEN bhi missing hai. Beat generate nahi ho sakta.")
                        
                else:
                    # Vocals toggle off — only beat
                    st.markdown("### 🥁 Instrumental Beat Only")
                    
                    if HF_TOKEN:
                        with st.spinner("Beat generate ho raha hai..."):
                            from huggingface_hub import InferenceClient
                            hf_client = InferenceClient(token=HF_TOKEN)
                            beat_prompt = f"Punjabi {song_style.lower()} instrumental, 808 bass, dark atmosphere, {user_prompt}"
                            
                            try:
                                audio_bytes = hf_client.text_to_audio(beat_prompt, model="facebook/musicgen-small")
                                st.audio(audio_bytes, format="audio/wav")
                                st.success("✅ Beat tayar hai!")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                    else:
                        st.info("💡 HF_TOKEN add karein beat ke liye.")

                # ==========================================================
                # STEP 4: SUMMARY
                # ==========================================================
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                st.markdown("""
                <div class="info-box">
                    <h4>📋 Song Summary</h4>
                    <p>🎤 <b>Topic:</b> {topic}</p>
                    <p>🎵 <b>Style:</b> {style}</p>
                    <p>⏱️ <b>Duration:</b> {dur}s</p>
                    <p>🎨 <b>Poster Seed:</b> {seed}</p>
                </div>
                """.format(topic=user_prompt, style=song_style, dur=duration, seed=random_seed), unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error aaya: {str(e)}")

# ============================================================
# TAB 3: SETUP GUIDE
# ============================================================
with tab3:
    st.markdown("### 📖 Setup Guide — API Keys Kaise Lein")
    
    st.markdown("""
    <div class="info-box">
        <h4>🔑 1. GROQ API KEY (Free)</h4>
        <p>👉 <a href="https://console.groq.com" target="_blank" style="color: #00a8ff;">console.groq.com</a> pe jao</p>
        <p>→ Sign up karo (FREE — $500 credit monthly!)</p>
        <p>→ API Keys section se key copy karo</p>
        <p>→ Streamlit Secrets mein <code>GROQ_API_KEY</code> ke naam se paste karo</p>
    </div>
    
    <div class="info-box">
        <h4>🎵 2. AI Music API KEY (30 Free Credits)</h4>
        <p>👉 <a href="https://aimusicapi.ai" target="_blank" style="color: #00a8ff;">aimusicapi.ai</a> pe jao</p>
        <p>→ Free account banao (NO credit card!)</p>
        <p>→ 30 free credits milenge (~3-4 gaane)</p>
        <p>→ API key copy karke Streamlit Secrets mein <code>AI_MUSIC_API_KEY</code> ke naam se paste karo</p>
        <p>→ Credits khatam hone pe sirf <b>$0.08 per song</b> — sabse sasta!</p>
    </div>
    
    <div class="info-box">
        <h4>🥁 3. HuggingFace Token (Optional — Beat ke liye)</h4>
        <p>👉 <a href="https://huggingface.co" target="_blank" style="color: #00a8ff;">huggingface.co</a> pe jao</p>
        <p>→ Account banao → Settings → Access Tokens</p>
        <p>→ New token generate karo</p>
        <p>→ Streamlit Secrets mein <code>HF_TOKEN</code> ke naam se paste karo</p>
    </div>
    
    <div class="warning-box">
        <h4>⚠️ Streamlit Secrets Kaise Set Karein</h4>
        <p>1. Streamlit Cloud pe app open karo</p>
        <p>2. App settings → Secrets</p>
        <p>3. Yeh format mein add karo:</p>
        <pre style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px; color: #ffc107;">
GROQ_API_KEY = "gsk_xxxxxxxx"
AI_MUSIC_API_KEY = "aim_xxxxxxxx"
HF_TOKEN = "hf_xxxxxxxx"
        </pre>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div style="text-align: center; padding: 40px 0 20px 0; color: rgba(255,255,255,0.3);">
    <p style="font-size: 1.1em;">🔥 <b>Devi Onfire AI</b> | Built for Sidhu Moose Wala Fans</p>
    <p style="font-size: 0.9em;">Lyrics: Groq | Images: Pollinations | Songs: AI Music API</p>
    <p style="font-size: 0.8em; margin-top: 10px;">Note: AI-generated content. Respect artists and their legacy.</p>
</div>
""", unsafe_allow_html=True)
