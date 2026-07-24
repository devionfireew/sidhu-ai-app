import streamlit as st
from groq import Groq
import replicate

# Page Config
st.set_page_config(page_title="Sidhu Moose Wala AI Studio", page_icon="🎤", layout="centered")

# Title & Description
st.title("🎤 Sidhu Moose Wala AI Song & Poster Generator")
st.markdown("Apna topic likhein — AI Lyrics, Punjabi Beat Audio, aur Custom Song Poster ek saath generate karein!")

# API Keys from Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
REPLICATE_API_TOKEN = st.secrets.get("REPLICATE_API_TOKEN", "")

# System Prompt for Lyrics
SYSTEM_PROMPT = """
You are an elite Punjabi Music Lyricist specialized in creating songs in the signature style, flow, lyrics, and vocal delivery of Sidhu Moose Wala.

When the user inputs ANY prompt or topic, generate a complete song blueprint in Roman Punjabi.

OUTPUT FORMAT REQUIREMENTS:
1. [MUSIC & BEAT SPECIFICATION]: Genre, BPM, Beat Elements.
2. [SONG LYRICS]: Written in Roman Punjabi with strong rhyming (Intro, Verse 1, Chorus, Verse 2, Outro).
"""

# User Input
user_prompt = st.text_area("✍️ Song ka Topic ya Idea likhein:", placeholder="e.g. Mere doston ki yaari, mehnat, aur dushmano ke liye aggressive drill song...", height=100)

if st.button("🚀 Complete Song & Picture Generate Karein", type="primary"):
    if not user_prompt:
        st.warning("Meharbani karke pehle koi prompt likhein!")
    elif not GROQ_API_KEY:
        st.error("GROQ_API_KEY missing hai! Streamlit Secrets mein add karein.")
    elif not REPLICATE_API_TOKEN:
        st.error("REPLICATE_API_TOKEN missing hai! Streamlit Secrets mein add karein.")
    else:
        try:
            # -------------------------------------------------------------
            # STEP 1: Lyrics & Script Generation (Groq API)
            # -------------------------------------------------------------
            with st.spinner("⚡ 1/3: AI Lyrics aur Beat Script generate ho rahe hain..."):
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
            st.text_area("📜 Generated Song Script:", value=generated_script, height=250)

            # -------------------------------------------------------------
            # STEP 2: Song Cover Picture Generation (Replicate Flux Model)
            # -------------------------------------------------------------
            with st.spinner("🖼️ 2/3: Sidhu Moose Wala Style AI Poster Image generate ho rahi hai..."):
                image_prompt = (
                    f"Album cover poster of a confident Punjabi hip hop singer inspired by Sidhu Moose Wala style, "
                    f"standing near luxury dark SUV car, aggressive street style, dark cinematic lighting, 8k resolution, "
                    f"theme: {user_prompt}"
                )
                image_output = replicate.run(
                    "black-forest-labs/flux-schnell",
                    input={"prompt": image_prompt}
                )
                
                st.subheader("🖼️ Generated Song Cover Poster:")
                # Handle list or single string response from Replicate
                if isinstance(image_output, list) and len(image_output) > 0:
                    st.image(image_output[0], caption="AI Song Poster", use_container_width=True)
                else:
                    st.image(image_output, caption="AI Song Poster", use_container_width=True)

            # -------------------------------------------------------------
            # STEP 3: Audio & Beat Track Generation (Replicate MusicGen)
            # -------------------------------------------------------------
            with st.spinner("🎙️ 3/3: AI Music & Voice Audio Track generate ho raha hai..."):
                audio_prompt = f"Aggressive Punjabi drill hiphop beat, 808 bass, dark synth, fast Punjabi vocal flow, topic: {user_prompt}"
                audio_output = replicate.run(
                    "meta/musicgen:67198c23f0481d2a132420a72c3d5e2193b22ed7c813be6a77d853e8dd2c505d",
                    input={
                        "prompt": audio_prompt,
                        "model_version": "encodec_32khz",
                        "output_format": "mp3",
                        "duration": 12
                    }
                )
                st.subheader("🔊 Final AI Audio Track:")
                st.audio(audio_output)

        except Exception as e:
            st.error(f"Error aaya hai: {str(e)}")
