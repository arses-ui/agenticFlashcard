import os
import re
import json
from typing import List, Dict, Union
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("Please set your OPENAI_API_KEY environment variable.")

# Configure OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)
MODEL_NAME = "gpt-4o"

# --- Helper: Chunk transcript into overlapping parts with estimated timestamps ---
def chunk_transcript_with_timestamps(
    transcript_text: str,
    words_per_chunk: int = 400,
    overlap_words: int = 50,
    avg_words_per_second: float = 2.5
) -> List[Dict[str, str]]:
    words = transcript_text.split()
    chunks = []
    current_word_index = 0

    while current_word_index < len(words):
        chunk_words = words[current_word_index:current_word_index + words_per_chunk]
        chunk_text = " ".join(chunk_words)

        # Estimate timestamp
        estimated_seconds = int(current_word_index / avg_words_per_second)
        hours = estimated_seconds // 3600
        minutes = (estimated_seconds % 3600) // 60
        seconds = estimated_seconds % 60
        timestamp_str = f"{hours:02}:{minutes:02}:{seconds:02}"

        chunks.append({"text": chunk_text, "timestamp": timestamp_str})
        current_word_index += (words_per_chunk - overlap_words)
        current_word_index = max(current_word_index, 0)

    return chunks

# --- Main Tool: Generate flashcards from a chunk ---
def extract_flashcards_from_chunk_agent_openai(
    chunk_text: str,
    chunk_timestamp: str,
    openai_client: openai.OpenAI = client,
    model_name: str = MODEL_NAME
) -> List[Dict[str, Union[str, List[str]]]]:
    system_message = """
        You are an expert at extracting key information from educational content and converting it into concise flashcards suitable for Anki.
        Your output MUST be a JSON array of objects. Each object in the array MUST strictly follow the provided schema.
        Ensure tags have no spaces (use hyphens for multi-word tags, e.g., 'Cell-Membrane').
        If no relevant flashcards can be generated from a chunk, return an empty JSON array `[]`.
        Do NOT generate cards for greetings, introductions, or irrelevant tangents.
        """

    user_message = f"""
        Analyze the following transcript chunk and identify significant terms, definitions, concepts, or questions and their answers. For each identified concept, create a flashcard.

        **Schema for flashcards:**
        ```json
        [
        {{
            "term": "string (The key term or concept)",
            "definition": "string (Its concise definition or explanation)",
            "context": "string (A very short, direct phrase or sentence from the transcript chunk where the concept appeared, ideally less than 150 characters, use ellipses if truncated)",
            "timestamp": "string (The timestamp of the *start* of the chunk, in HH:MM:SS format)",
            "tags": ["list of strings (Relevant keywords, no spaces allowed in individual tags; use hyphens for multi-word tags, e.g., 'Biology', 'Cell-Membrane')"]
        }},
        {{
            "question": "string (A question related to a concept)",
            "answer": "string (The direct answer to the question)",
            "context": "string (A very short, direct phrase or sentence from the transcript chunk where the concept appeared, ideally less than 150 characters, use ellipses if truncated)",
            "timestamp": "string (The timestamp of the *start* of the chunk, in HH:MM:SS format)",
            "tags": ["list of strings (Relevant keywords, no spaces allowed in individual tags)"]
        }}
        ]
        Transcript Chunk:
        Timestamp: {chunk_timestamp}
        Text: {chunk_text}
        """
    try:
        response = openai_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content

        try:
            flashcards = json.loads(content)
            if isinstance(flashcards, list):
                return flashcards
            else:
                print("Warning: Response was not a list. Returning empty list.")
                return []
        except json.JSONDecodeError:
            print("Warning: Could not parse JSON from model output.")
            return []

    except Exception as e:
        print(f"Error during OpenAI call: {e}")
        return []

   