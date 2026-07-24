import streamlit as st
from groq import Groq
import replicate

# Page Config
st.set_page_config(page_title="Sidhu Moose Wala AI Song Generator", page_icon="🎵", layout="centered")

# Title & Description
st.title("🎤 Sidhu Moose Wala AI Song Generator")
st.markdown("Apna topic likhein aur Sidhu Moose Wala ke signature style mein AI song generate karein!")

# API Keys from Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
REPLICATE_API_TOKEN = st.secrets.get("REPLICATE_API_TOKEN", "")

# System Prompt
SYSTEM_PROMPT = """
You are an elite Punjabi Music Generator specialized in creating songs in the signature style, flow, lyrics, and vocal delivery of Sidhu Moose Wala.

When the user inputs ANY prompt or topic, generate a complete song blueprint.

OUTPUT FORMAT REQUIREMENTS:
1. [MUSIC & BEAT SPECIFICATION]: Genre, BPM, Beat Elements.
2. [VOCAL & PITCH SETTINGS]: Pitch shift, ad-libs, tone.
3. [SONG LYRICS]: Written in Roman Punjabi with strong rhyming and rhythmic cadence (Intro, Verse 1, Chorus, Verse 2, Outro).
"""

# User Input
user_prompt = st.text_area("✍️ Song ka Topic ya Idea likhein:", placeholder="e.g. Mere doston ki yaari aur dushmano ke liye fast drill beat song...", height=100)

if st.button("🚀 Song Generate Karein", type="primary"):
    if not user_prompt:
        st.warning("Meharbani karke pehle koi prompt likhein!")
    elif not GROQ_API_KEY:
        st.error("GROQ API Key missing hai! Streamlit Secrets mein add karein.")
    else:
        try:
            # 1. Generate Lyrics & Beats via Groq API
            with st.spinner("⚡ AI Lyrics aur Beat Parameters generate ho rahe hain..."):
                client = Groq(api_key=GROQ_API_KEY)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                generated_script = chat_completion.choices[0].message.content

            st.success("✅ Lyrics aur Beat Specification Tayar Hai!")
            st.text_area("📜 Generated Song Script:", value=generated_script, height=300)

            # 2. Voice Conversion via Replicate (If API key provided)
            if REPLICATE_API_TOKEN:
                with st.spinner("🎙️ Voice Convert ho rahi hai Sidhu Moose Wala ki aawaz mein..."):
                    # Demo call to Replicate RVC Model API
                    output_audio_url = replicate.run(
                        "aiprompt/rvc-sidhu-moosewala:latest_model_id",
                        input={
                            "text_script": generated_script,
                            "pitch": -1
                        }
                    )
                    st.subheader("🔊 Final AI Song Audio:")
                    st.audio(output_audio_url)
            else:
                st.info("💡 Tip: Replicate API Key add karke aap direct audio bhi stream kar sakte hain.")

        except Exception as e:
            st.error(f"Error aaya hai: {str(e)}")

