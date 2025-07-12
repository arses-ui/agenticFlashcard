import openai # Import the OpenAI library
import json
import re
from typing import List, Dict, Union
import os

# Configure your OpenAI API key
# Make sure to set this securely, e.g., from an environment variable.
# export OPENAI_API_KEY="YOUR_ACTUAL_API_KEY"
try:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except openai.APIAccessorError:
    print("Error: OPENAI_API_KEY environment variable not set or invalid.")
    print("Please set it before running the script (e.g., export OPENAI_API_KEY='YOUR_KEY')")
    exit()


MODEL_NAME = "gpt-4o" 

# --- Helper Function to Chunk Transcript ---
def chunk_transcript_with_timestamps(transcript_text: str, words_per_chunk: int = 400, overlap_words: int = 50, avg_words_per_second: float = 2.5) -> List[Dict[str, str]]:
    """
    Chunks a long transcript text into smaller segments and assigns an estimated timestamp.
    
    Args:
        transcript_text (str): The full text of the transcript.
        words_per_chunk (int): Desired number of words in each chunk.
        overlap_words (int): Number of words to overlap between consecutive chunks.
        avg_words_per_second (float): Average words spoken per second, for timestamp estimation.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each with 'text' and 'timestamp'.
    """
    words = transcript_text.split()
    chunks = []
    current_word_index = 0

    while current_word_index < len(words):
        chunk_words = words[current_word_index:current_word_index + words_per_chunk]
        chunk_text = " ".join(chunk_words)

        # Estimate timestamp for the start of this chunk
        estimated_seconds = int(current_word_index / avg_words_per_second)
        hours = estimated_seconds // 3600
        minutes = (estimated_seconds % 3600) // 60
        seconds = estimated_seconds % 60
        timestamp_str = f"{hours:02}:{minutes:02}:{seconds:02}"

        chunks.append({"text": chunk_text, "timestamp": timestamp_str})

        current_word_index += (words_per_chunk - overlap_words)
        if current_word_index < 0:
            current_word_index = 0

    return chunks

# --- Agent Function to Extract Flashcards from a Single Chunk using OpenAI ---
def extract_flashcards_from_chunk_agent_openai(
    chunk_text: str,
    chunk_timestamp: str,
    openai_client: openai.OpenAI = client, # Use the configured OpenAI client
    model_name: str = MODEL_NAME
) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Feeds a transcript chunk to an OpenAI LLM to generate flashcards
    in the specified dictionary format.

    Args:
        chunk_text (str): The text content of the transcript chunk.
        chunk_timestamp (str): The starting timestamp of this chunk (HH:MM:SS).
        openai_client (openai.OpenAI): The configured OpenAI client instance.
        model_name (str): The name of the OpenAI model to use (e.g., 'gpt-4o').

    Returns:
        List[Dict]: A list of flashcard dictionaries, or an empty list if none generated.
    """

    # Define the system message to set the LLM's persona and primary instructions
    system_message = """
You are an expert at extracting key information from educational content and converting it into concise flashcards suitable for Anki.
Your output MUST be a JSON array of objects. Each object in the array MUST strictly follow the provided schema.
Ensure tags have no spaces (use hyphens for multi-word tags, e.g., 'Cell-Membrane').
If no relevant flashcards can be generated from a chunk, return an empty JSON array `[]`.
Do NOT generate cards for greetings, introductions, or irrelevant tangents.
"""

    # Define the user message, including the transcript chunk, timestamp, and schema
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
    "tags": ["list of strings (Relevant keywords, no spaces allowed in individual tags; use hyphens for multi-word tags)"]
  }}
]
```
"""