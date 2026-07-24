import streamlit as st
from groq import Groq
import urllib.parse
import random
import time
from huggingface_hub import InferenceClient

# Page Config
st.set_page_config(page_title="Sidhu Moose Wala AI Studio", page_icon="🎤", layout="centered")

st.title("🎤 Sidhu Moose Wala AI Song Generator (FREE)")
st.markdown("Apna topic likhein — AI Lyrics, Music Beat Audio, aur Custom HD Poster Image generate karein!")

# API Keys from Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

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

if st.button("🚀 Song & Picture Generate Karein", type="primary"):
    if not user_prompt:
        st.warning("Meharbani karke pehle koi prompt likhein!")
    elif not GROQ_API_KEY:
        st.error("GROQ_API_KEY missing hai! Streamlit Secrets mein add karein.")
    else:
        try:
            # -------------------------------------------------------------
            # STEP 1: Lyrics Generation (Groq API)
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
            # STEP 2: Unique Sidhu Moose Wala Poster (Random Seed)
            # -------------------------------------------------------------
            with st.spinner("🖼️ 2/3: Nayi Sidhu Moose Wala HD Picture generate ho rahi hai..."):
                # Har baar random seed se NAYI picture banegi
                random_seed = random.randint(1, 999999)
                
                image_prompt = (
                    f"Album cover poster of Punjabi singer Sidhu Moose Wala, {user_prompt}, "
                    f"wearing stylish turban and dark sunglasses, standing near black SUV 4x4 car, "
                    f"aggressive look, cinematic lighting, ultra detailed 8k portrait"
                )
                encoded_prompt = urllib.parse.quote(image_prompt)
                
                # Dynamic URL with random seed
                free_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={random_seed}"
                
                st.subheader("🖼️ Generated Song Poster:")
                st.image(free_image_url, caption="AI Song Poster (New)", use_container_width=True)

            # -------------------------------------------------------------
            # STEP 3: Audio Generation with Retry Logic
            # -------------------------------------------------------------
            with st.spinner("🎙️ 3/3: Music Track generate ho raha hai (Wait 10-15 secs)..."):
                if HF_TOKEN:
                    hf_client = InferenceClient(token=HF_TOKEN)
                    audio_prompt = f"Punjabi drill hiphop beat, 808 bass, dark synth, energetic, {user_prompt}"
                    
                    audio_success = False
                    # Retrying up to 3 times in case HF server is warming up
                    for attempt in range(3):
                        try:
                            audio_bytes = hf_client.text_to_audio(
                                audio_prompt,
                                model="facebook/musicgen-small"
                            )
                            st.subheader("🔊 Final AI Audio Track:")
                            st.audio(audio_bytes, format="audio/wav")
                            audio_success = True
                            break
                        except Exception:
                            time.sleep(5) # Wait 5 seconds before retrying
                    
                    if not audio_success:
                        st.warning("⚠️ Audio server filhal busy hai. Kucch der baad dobara 'Generate' button dabayein.")
                else:
                    st.info("💡 Tip: Streamlit Secrets mein HF_TOKEN add karein taaki Audio Player active ho jaye.")

        except Exception as e:
            st.error(f"Error aaya hai: {str(e)}")
