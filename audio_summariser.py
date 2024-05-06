import json
import os
from time import sleep

from claude_llm import Claude

def get_audio_transcript(audio_file) -> str:
    """
    summarises audio using openais whisper
    """


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

