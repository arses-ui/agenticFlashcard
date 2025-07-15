import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict, Union

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

def chunk_transcript_with_timestamps(
    transcript_text: str,
    words_per_chunk: int = 400,
    overlap_words: int = 50,
    avg_words_per_second: float = 2.5
) -> List[Dict[str, str]]:
    """Breaks transcript into overlapping chunks with estimated timestamps."""
    words = transcript_text.split()
    chunks = []
    current_word_index = 0

    while current_word_index < len(words):
        chunk_words = words[current_word_index:current_word_index + words_per_chunk]
        chunk_text = " ".join(chunk_words)

        estimated_seconds = int(current_word_index / avg_words_per_second)
        hours = estimated_seconds // 3600
        minutes = (estimated_seconds % 3600) // 60
        seconds = estimated_seconds % 60
        timestamp_str = f"{hours:02}:{minutes:02}:{seconds:02}"

        chunks.append({"text": chunk_text, "timestamp": timestamp_str})
        current_word_index += (words_per_chunk - overlap_words)

    return chunks

def extract_flashcards_from_chunk_with_gemini(
    chunk_text: str,
    chunk_timestamp: str
) -> List[Dict[str, Union[str, List[str]]]]:
    """Generates flashcards from a transcript chunk using Gemini."""
    prompt = f"""
You are an expert at creating Anki flashcards from educational content.
Generate a JSON array of flashcards from the chunk below. Use the schema strictly.

[
  {{
    "term": "string",
    "definition": "string",
    "context": "string",
    "timestamp": "string",
    "tags": ["string"]
  }},
  {{
    "question": "string",
    "answer": "string",
    "context": "string",
    "timestamp": "string",
    "tags": ["string"]
  }}
]

Chunk:
Timestamp: {chunk_timestamp}
Text: {chunk_text}
    """

    try:
        response = model.generate_content(prompt)
        content = response.text

        flashcards = json.loads(content)
        if isinstance(flashcards, list):
            return flashcards
        else:
            print("Warning: Output was not a list.")
            return []

    except json.JSONDecodeError:
        print("Warning: Gemini output was not valid JSON.")
        return []
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return []
