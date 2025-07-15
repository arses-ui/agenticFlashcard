import os
import re
import json
from typing import List, Dict, Union
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Load API key from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.5
)

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

        estimated_seconds = int(current_word_index / avg_words_per_second)
        hours = estimated_seconds // 3600
        minutes = (estimated_seconds % 3600) // 60
        seconds = estimated_seconds % 60
        timestamp_str = f"{hours:02}:{minutes:02}:{seconds:02}"

        chunks.append({"text": chunk_text, "timestamp": timestamp_str})
        current_word_index += (words_per_chunk - overlap_words)
        current_word_index = max(current_word_index, 0)

    return chunks

# --- Main Tool: Generate flashcards from a chunk using Gemini ---
def extract_flashcards_from_chunk_with_gemini(
    chunk_text: str,
    chunk_timestamp: str,
    model: ChatGoogleGenerativeAI = llm
) -> List[Dict[str, Union[str, List[str]]]]:
    system_message = """
You are an expert at extracting key information from educational content and converting it into concise flashcards suitable for Anki.
Your output MUST be a JSON array of objects. Each object in the array MUST strictly follow the provided schema.
Ensure tags have no spaces (use hyphens for multi-word tags, e.g., 'Cell-Membrane').
If no relevant flashcards can be generated from a chunk, return an empty JSON array `[]`.
"""

    user_message = f"""
Analyze the following transcript chunk and identify significant terms, definitions, concepts, or questions and their answers. For each identified concept, create a flashcard.

Schema:
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

Transcript Chunk:
Timestamp: {chunk_timestamp}
Text: {chunk_text}
"""

    try:
        # Create prompt and invoke Gemini model
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message.strip()),
            ("user", user_message.strip())
        ])
        chain = prompt | model
        response = chain.invoke({})

        content = getattr(response, "content", None)
        if not content:
            print("Warning: Gemini returned no content.")
            return []

        try:
            flashcards = json.loads(content)
            if isinstance(flashcards, list):
                return flashcards
            else:
                print("Warning: Parsed content is not a list.")
                return []
        except json.JSONDecodeError:
            print("Warning: Could not parse JSON from Gemini output.")
            return []

    except Exception as e:
        print(f"Error using Gemini to generate flashcards: {e}")
        return []
