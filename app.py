import streamlit as st
import urllib.parse
import random
import time
import requests
import io

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="Devi Onfire AI", page_icon="🔥", layout="centered")

st.markdown("""
<style>
    .main, .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    h1, h2, h3, p, label { color: white !important; }
    .stButton>button { background: linear-gradient(90deg, #ff416c, #ff4b2b) !important; color: white !important; 
        border-radius: 30px !important; padding: 14px !important; font-weight: 700 !important; width: 100% !important; }
    .success-box { background: rgba(46, 213, 115, 0.2); border-left: 4px solid #2ed573; padding: 15px; border-radius: 10px; margin: 10px 0; }
    .warning-box { background: rgba(255, 193, 7, 0.2); border-left: 4px solid #ffc107; padding: 15px; border-radius: 10px; margin: 10px 0; color: #ffc107 !important; }
    .info-box { background: rgba(0, 168, 255, 0.2); border-left: 4px solid #00a8ff; padding: 15px; border-radius: 10px; margin: 10px 0; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# API KEYS (ONLY FREE ONES NEEDED)
# ============================================================
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 2.5em; background: linear-gradient(90deg, #ff416c, #f9ca24); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🔥 Devi Onfire AI
    </h1>
    <p style="color: rgba(255,255,255,0.6);">100% FREE — No Paid APIs Needed!</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["💬 Chat", "🎵 Song Generator", "ℹ️ Free Tools"])

# ============================================================
# TAB 1: CHAT
# ============================================================
with tab1:
    st.markdown("### 💬 Sidhu AI Chat")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div style="text-align: right;"><span style="background: linear-gradient(90deg, #667eea, #764ba2); color: white; padding: 10px 15px; border-radius: 15px 15px 3px 15px; display: inline-block; margin: 5px;">{msg["content"]}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align: left;"><span style="background: rgba(255,255,255,0.1); color: white; padding: 10px 15px; border-radius: 15px 15px 15px 3px; display: inline-block; margin: 5px; border: 1px solid rgba(255,255,255,0.1);">{msg["content"]}</span></div>', unsafe_allow_html=True)
    
    user_chat = st.text_input("Message...", placeholder="Veere kya haal hai...", key="chat_input")
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("🚀 Send", key="send_chat"):
            if not user_chat:
                st.warning("Kuch likh toh sahi!")
            elif not GROQ_API_KEY:
                st.error("GROQ_API_KEY add karo!")
            else:
                st.session_state.chat_history.append({"role": "user", "content": user_chat})
                with st.spinner("Soch raha hai..."):
                    try:
                        from groq import Groq
                        client = Groq(api_key=GROQ_API_KEY)
                        system = "You are Sidhu Moose Wala AI. Reply in Roman Punjabi with attitude. Use 'Bai', 'Veere', 'Jatt'. Short punchy replies. Emojis use kar."
                        messages = [{"role": "system", "content": system}] + st.session_state.chat_history[-6:]
                        r = client.chat.completions.create(messages=messages, model="llama-3.3-70b-versatile", temperature=0.9, max_tokens=400)
                        reply = r.choices[0].message.content
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ============================================================
# TAB 2: SONG GENERATOR (100% FREE)
# ============================================================
with tab2:
    st.markdown("### 🎵 FREE AI Song Generator")
    st.markdown("<p style='color: rgba(255,255,255,0.5);'>Groq (Lyrics) + HuggingFace (Beat + Voice) — Sab FREE!</p>", unsafe_allow_html=True)
    
    user_prompt = st.text_area("✍️ Song Topic:", placeholder="e.g. Doston ki yaari, gaddari, struggle...", height=100)
    song_style = st.selectbox("Style:", ["Punjabi Drill", "Hip Hop", "Sad/Melodic", "Gangster"])
    
    st.markdown("""
    <div class="warning-box">
        ⚠️ <b>Important:</b> Free HuggingFace inference SLOW hota hai (queue system).<br>
        🎤 Vocals = <b>Rap/Spoken style</b> (Bark TTS model). Perfect singing nahi aayegi free mein.<br>
        🥁 Beat = MusicGen se instrumental beat aayega.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔥 GENERATE FREE SONG", type="primary"):
        if not user_prompt:
            st.warning("Topic likh bhai!")
        elif not GROQ_API_KEY:
            st.error("GROQ_API_KEY missing!")
        else:
            try:
                # STEP 1: LYRICS
                with st.spinner("⚡ Lyrics generate ho rahe hain..."):
                    from groq import Groq
                    client = Groq(api_key=GROQ_API_KEY)
                    system = """You are Sidhu Moose Wala style lyricist. Roman Punjabi mein likh.
Format:
[INTRO]
[VERSE 1]
[CHORUS]
[VERSE 2]
[OUTRO]
Aggressive, deep, street life themes. Rhyming honi chahiye."""
                    r = client.chat.completions.create(
                        messages=[{"role": "system", "content": system}, {"role": "user", "content": user_prompt}],
                        model="llama-3.3-70b-versatile", temperature=0.85, max_tokens=2000
                    )
                    lyrics = r.choices[0].message.content
                
                st.markdown('<div class="success-box">✅ Lyrics Tayar!</div>', unsafe_allow_html=True)
                st.text_area("📜 Lyrics:", value=lyrics, height=250)
                
                # STEP 2: POSTER
                with st.spinner("🖼️ Poster ban raha hai..."):
                    seed = random.randint(1, 999999)
                    img_prompt = f"Album cover Punjabi singer orange turban black sunglasses beard, {user_prompt}, cinematic dark lighting, 8k portrait"
                    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(img_prompt)}?width=1024&height=1024&nologo=true&seed={seed}&enhance=true"
                
                st.markdown("### 🖼️ Poster")
                st.image(img_url, use_container_width=True)
                
                # STEP 3: BEAT (MusicGen - HF Free)
                st.markdown("### 🥁 Step 1: Beat (MusicGen)")
                with st.spinner("⏳ Beat generate ho raha hai... (Free HF queue, 1-2 min lag sakte hain)"):
                    try:
                        from huggingface_hub import InferenceClient
                        hf = InferenceClient()
                        
                        beat_prompt = f"Punjabi {song_style.lower()} beat, heavy 808 bass, dark synth, trap drums, energetic, {user_prompt}"
                        audio_bytes = hf.text_to_audio(beat_prompt, model="facebook/musicgen-small")
                        
                        st.audio(audio_bytes, format="audio/wav")
                        st.markdown('<div class="success-box">✅ Beat Tayar!</div>', unsafe_allow_html=True)
                        
                        # Store for download
                        st.session_state["beat_audio"] = audio_bytes
                        
                    except Exception as e:
                        st.error(f"Beat Error: {str(e)[:200]}")
                        st.info("💡 HuggingFace free tier busy hai. Thodi der baad try karein.")
                
                # STEP 4: VOCALS (Bark - HF Free)
                st.markdown("### 🎤 Step 2: Vocals (Bark AI)")
                with st.spinner("⏳ Vocals generate ho rahe hain... (Free HF queue, 1-2 min)"):
                    try:
                        from huggingface_hub import InferenceClient
                        hf = InferenceClient()
                        
                        # Clean lyrics for Bark (remove headers, limit length)
                        clean = lyrics.replace("[INTRO]", "").replace("[VERSE 1]", "").replace("[CHORUS]", "")
                        clean = clean.replace("[VERSE 2]", "").replace("[OUTRO]", "").replace("🎵", "").replace("📝", "")
                        clean = " ".join(clean.split())[:400]  # Bark limit
                        
                        # Bark prompt with music hint
                        bark_prompt = f"♪ {clean} ♪"
                        
                        # Bark via HF Inference API
                        audio_bytes = hf.text_to_audio(bark_prompt, model="suno/bark-small")
                        
                        st.audio(audio_bytes, format="audio/wav")
                        st.markdown('<div class="success-box">✅ Vocals Tayar!</div>', unsafe_allow_html=True)
                        st.session_state["vocal_audio"] = audio_bytes
                        
                    except Exception as e:
                        st.error(f"Vocals Error: {str(e)[:200]}")
                        st.info("💡 Bark model busy hai. Thodi der baad try karein.")
                
                # STEP 5: SUMMARY
                st.markdown("""
                <div class="info-box">
                    <h4>🎧 Song Components Ready!</h4>
                    <p>1️⃣ <b>Beat</b> — MusicGen (Instrumental)</p>
                    <p>2️⃣ <b>Vocals</b> — Bark AI (Rap/Spoken)</p>
                    <p>💡 <b>Tip:</b> Dono ko ek saath sunne ke liye 
                    <a href="https://www.bandlab.com" target="_blank" style="color: #00a8ff;">BandLab</a> 
                    (FREE DAW) mein import karo!</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ============================================================
# TAB 3: FREE EXTERNAL TOOLS
# ============================================================
with tab3:
    st.markdown("### 🆓 100% Free External Tools (No API Needed)")
    
    st.markdown("""
    <div class="info-box">
        <h4>🎵 Brev.ai — FREE Singing AI (No Signup!)</h4>
        <p>👉 <a href="https://brev.ai/features/ai-singing-generator" target="_blank" style="color: #00a8ff;">brev.ai</a></p>
        <p>✅ Text se full song with vocals</p>
        <p>✅ No login required</p>
        <p>✅ 2 songs ek saath generate</p>
        <p>✅ Custom lyrics upload</p>
    </div>
    
    <div class="info-box">
        <h4>🎵 MusicGenAI.net — FREE (No Login!)</h4>
        <p>👉 <a href="https://www.musicgenai.net/" target="_blank" style="color: #00a8ff;">musicgenai.net</a></p>
        <p>✅ Male/Female/Duet vocals</p>
        <p>✅ Custom lyrics</p>
        <p>✅ No signup</p>
    </div>
    
    <div class="info-box">
        <h4>🎵 BandLab — FREE DAW (Mixing)</h4>
        <p>👉 <a href="https://www.bandlab.com" target="_blank" style="color: #00a8ff;">bandlab.com</a></p>
        <p>✅ Beat + Vocals mix karo free mein</p>
        <p>✅ Auto-tune, effects free</p>
    </div>
    
    <div class="warning-box">
        <h4>⚠️ Sachai (Reality Check)</h4>
        <p><b>Free mein "Suno jaisa" perfect gaana nahi banta.</b></p>
        <p>Reason: GPU compute mehnga hai. Companies paise maangti hain.</p>
        <p><b>Best Free Workflow:</b></p>
        <p>1. Lyrics — Groq (Free)</p>
        <p>2. Beat — MusicGen HF (Free)</p>
        <p>3. Vocals — Brev.ai/MusicGenAI.net (Free web tool)</p>
        <p>4. Mix — BandLab (Free)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 30px 0; color: rgba(255,255,255,0.3);">
    <p>🔥 Devi Onfire AI | 100% Free Tools Only</p>
</div>
""", unsafe_allow_html=True)
