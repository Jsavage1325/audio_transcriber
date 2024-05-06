import json
import os
from time import sleep

import whisper

from claude_llm import Claude


def get_audio_transcript(audio_file: bytes) -> str:
    """
    Transcribes audio using OpenAI's Whisper model.

    Args:
        audio_file (bytes): The audio file loaded into memory.

    Returns:
        str: The transcribed text from the audio file.
    """

    # Load the model, using the "base" model for a balance between speed and accuracy
    model = whisper.load_model("base")

    # Decode the audio file
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)

    # Run the model
    result = model.transcribe(audio)

    # Extract the transcription text
    return result["text"]


def summarise_audio_transcript(transcript: str, title: str, model: str, prompt: str, api_key: str):
    """Summarize the video transcript."""
    if api_key:
        cl = Claude(api_key=api_key)
    else:
        cl = Claude()

    summary = cl.summarise_transcript(transcript, title, model, prompt)

    return summary

def main(audio_file, prompt, model: str, api_key: str=None):
    """Process each video URL provided and return results as a dictionary."""
    results = {}
    try:
        transcript = get_audio_transcript(audio_file)
        # Generate summary
        summary_text = summarise_audio_transcript(transcript, title, model, prompt, api_key)
        # summary_text, summary_filename = f"{title.replace(' ', '-')}-output.txt"
        # results[summary_filename] = summary.encode('utf-8')  # Encode summary as bytes
        sleep(15)  # Throttle requests to avoid overloading servers or hitting API limits
        return summary_text
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e)
        print(f'Error processing transcript.')
    return results

