import json
import zipfile
from io import BytesIO
import requests
import hashlib

import streamlit as st
from moviepy.editor import AudioFileClip
import tempfile
import io
import os

from audio_summariser import main, get_audio_transcript

ACCESS_KEY = "2d9f7bda8178f04ac5b2b7daa3b59db5"  # Set your simple access password here


def md5_hash(text):
    """Return the MD5 hash of the input text."""
    return hashlib.md5(text.encode()).hexdigest()

def run_script(video_urls, model, prompt, api_key):
    """
    Runs the main script of YouTube Summariser, this returns a dictionary containing the required values
    """
    return main(video_urls, prompt, model, api_key)

# def extract_audio(video_file):
#     """Extract audio from video file and return it as an audio file in memory."""
#     print(video_file.name)
#     temp_audio = AudioFileClip(video_file.name)
#     audio_buffer = io.BytesIO()
#     temp_audio.write_audiofile(audio_buffer, codec='aac')
#     audio_buffer.seek(0)
#     return audio_buffer


def extract_audio(video_file) -> bytes:
    """
    Extract audio from video file and return it as an audio file in memory.
    """
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(video_file.name)[1]) as tmp:
        tmp.write(video_file.getvalue())
        tmp_path = tmp.name

    # Load the video file from the temporary file path
    temp_audio = AudioFileClip(tmp_path)
    
    # Write the audio to a bytes buffer
    audio_buffer = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_audio.write_audiofile(audio_buffer.name, codec='mp3')
    
    # Clean up the temporary video file
    os.unlink(tmp_path)
    
    return audio_buffer.name

def save_audio_file(uploaded_file):
    # Save the uploaded audio to the server's filesystem
    file_path = f"temp_audio_file_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())  # Rewind to the start if read previously
    return file_path

    # Initialize Streamlit layout
st.title("Audio Summariser")

audio_file = st.file_uploader("Upload your audio file:", type=['wav', 'mp3', 'm4a', 'mp4'])
model = st.selectbox("Choose Model:", ["haiku", "sonnet", "opus"])
prompt = st.text_area("Enter Prompt:")
api_key = st.text_input("Enter API Key:", type="password")

output_container = st.empty()

if 'audio_summary' not in st.session_state:
     st.session_state['audio_summary'] = ''

if st.button("Start Processing"):
    if not audio_file:
        st.warning("Please upload an audio file.")
    elif not api_key.strip():
        st.warning("Please enter your API Key.")
    else:
        # Check if the uploaded file is MP4/M4A and needs audio extraction
        if audio_file.type in ["audio/mp4", "video/mp4"]:
            audio_path = extract_audio(audio_file)
        else:
            print(audio_file)
            audio_path = save_audio_file(audio_file)
            
        transcript = get_audio_transcript(audio_path)
        
        st.session_state['audio_summary'] = transcript

        prompted_output = main(transcript=transcript, prompt=prompt, model=model, api_key=api_key)

        output_container.success("Processing complete! See results below:")
        output_container.text(prompted_output)


st.button("Quit", on_click=st.stop)
