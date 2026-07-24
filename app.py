import streamlit as st
from groq import Groq
import requests
import urllib.parse
import time

# Page Config
st.set_page_config(page_title="Sidhu Moose Wala AI Studio", page_icon="🎤", layout="centered")

st.title("🎤 Sidhu Moose Wala AI Song Generator (FREE)")
st.markdown("Apna topic likhein — Free AI Lyrics, Music Beat, aur Custom Poster Image generate karein!")

# API Keys from Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "") # Hugging Face Free Token

# System Prompt
SYSTEM_PROMPT = """
You are an elite Punjabi Music Lyricist specialized in creating songs in the signature style, flow, lyrics, and vocal delivery of Sidhu Moose Wala.

When the user inputs ANY prompt or topic, generate a complete song blueprint in Roman Punjabi.

OUTPUT FORMAT REQUIREMENTS:
1. [MUSIC & BEAT SPECIFICATION]: Genre, BPM, Beat Elements.
2. [SONG LYRICS]: Written in Roman Punjabi with strong rhyming (Intro, Verse 1, Chorus, Verse 2, Outro).
"""

# User Input
user_prompt = st.text_area("✍️ Song ka Topic ya Idea likhein:", placeholder="e.g. Doston ki yaari, mehnat aur aggressive drill beat song...", height=100)

if st.button("🚀 Free Song & Poster Generate Karein", type="primary"):
    if not user_prompt:
        st.warning("Meharbani karke pehle koi prompt likhein!")
    elif not GROQ_API_KEY:
        st.error("GROQ_API_KEY missing hai! Streamlit Secrets mein add karein.")
    else:
        try:
            # -------------------------------------------------------------
            # STEP 1: Lyrics Generation (Groq API - Free)
            # -------------------------------------------------------------
            with st.spinner("⚡ 1/3: AI Lyrics generate ho rahe hain..."):
                client = Groq(api_key=GROQ_API_KEY)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                generated_script = chat_completion.choices[0].message.content

            st.success("✅ Lyrics Script Tayar Hai!")
            st.text_area("📜 Generated Song Script:", value=generated_script, height=220)

            # -------------------------------------------------------------
            # STEP 2: Song Poster Image Generation (Pollinations - 100% Free)
            # -------------------------------------------------------------
            with st.spinner("🖼️ 2/3: Sidhu Style AI Poster generate ho raha hai..."):
                image_prompt = f"Album cover poster of Punjabi singer in Sidhu Moose Wala style, luxury dark car, aggressive street style, dark cinematic, {user_prompt}"
                encoded_prompt = urllib.parse.quote(image_prompt)
                
                # Free Image URL (No API key required)
                free_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed=42"
                
                st.subheader("🖼️ Generated Song Poster (Free):")
                st.image(free_image_url, caption="AI Song Poster", use_container_width=True)

            # -------------------------------------------------------------
            # STEP 3: Audio/Music Generation (Hugging Face MusicGen - Free)
            # -------------------------------------------------------------
            with st.spinner("🎙️ 3/3: Music Track generate ho raha hai..."):
                if HF_TOKEN:
                    API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
                    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                    audio_payload = {
                        "inputs": f"Punjabi drill hiphop beat, 808 bass, dark synth, aggressive style, {user_prompt}"
                    }
                    
                    response = requests.post(API_URL, headers=headers, json=audio_payload)
                    
                    if response.status_code == 200:
                        st.subheader("🔊 Final AI Audio Track:")
                        st.audio(response.content, format="audio/wav")
                    else:
                        st.info("💡 Hugging Face Model load ho raha hai, script aur image ready hain!")
                else:
                    st.info("💡 Tip: Free Hugging Face Token add karne par direct Music audio track bhi play hoga.")

        except Exception as e:
            st.error(f"Error aaya hai: {str(e)}")
