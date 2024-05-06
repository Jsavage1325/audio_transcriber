import json
import zipfile
from io import BytesIO
import requests
import hashlib

import streamlit as st

from audio_summariser import main

ACCESS_KEY = "2d9f7bda8178f04ac5b2b7daa3b59db5"  # Set your simple access password here


def md5_hash(text):
    """Return the MD5 hash of the input text."""
    return hashlib.md5(text.encode()).hexdigest()

def run_script(video_urls, model, prompt, api_key):
    """
    Runs the main script of YouTube Summariser, this returns a dictionary containing the required values
    """
    return main(video_urls, prompt, model, api_key)

def start_processing(video_urls, model, prompt, api_key):
    results = run_script(video_urls, model, prompt, api_key)
    # Create ZIP file in memory for all the output files
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, filedata in results.items():
            zip_file.writestr(filename, filedata)
    return zip_buffer

    # Initialize Streamlit layout
st.title("Audio Summariser")

audio_file = st.file_uploader("Upload your audio file:", type=['mp3', 'm4a', 'mp4'])
model = st.selectbox("Choose Model:", ["haiku", "sonnet", "opus"])
prompt = st.text_area("Enter Prompt:")
api_key = st.text_input("Enter API Key:", type="password")

output_container = st.empty()

if not st.session_state['audio_summary']:
     st.session_state['audio_summary'] = ''

if st.button("Start Processing"):
    if not audio_file or st.session_state['audio_summary']:
        st.warning("Please enter at least one video URL.")
    elif not api_key.strip():
        st.warning("Please enter your API Key.")
    else:
        st.session_state['audio_summary'] = start_processing(audio_file, model, prompt, api_key)
        # output_container.success("Processing complete! See results below:")
        output_container.text(st.session_state['audio_summary'])

st.button("Quit", on_click=st.stop)
