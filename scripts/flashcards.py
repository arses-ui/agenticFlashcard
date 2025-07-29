import os
import json
from typing import List, Dict, Union
from langchain_ollama import OllamaLLM
from langchain_core.tools import tool

# Initialize LLaMA via Ollama
llm = OllamaLLM(model="llama3", temperature=0.5)

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

    return chunks

def extract_flashcards_from_chunk_with_llama(
    chunk_text: str,
    chunk_timestamp: str,
    max_flashcards: int = 10
) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Dynamically extracts flashcards using LLaMA based on chunk density.
    Returns a list of flashcard dictionaries.
    """

    # Estimate ideal number of flashcards based on word count
    word_count = len(chunk_text.split())
    min_cards = 2
    max_cards = max_flashcards
    ideal_card_count = min(max_cards, max(min_cards, word_count // 100))

    prompt = f"""
You are an assistant that creates high-quality Anki flashcards from educational lecture text.

Instructions:
- Generate up to {ideal_card_count} flashcards for this chunk.
- Do NOT force the number. Return fewer if content is shallow.
- Use either 'term-definition' or 'question-answer' format.
- Include context, timestamp, and tags for each card.

JSON Format Example:
[
  {{
    "term": "Photosynthesis",
    "definition": "The process by which green plants convert sunlight into energy.",
    "context": "Used while discussing plant biology.",
    "timestamp": "{chunk_timestamp}",
    "tags": ["biology", "plants"]
  }},
  {{
    "question": "What is the powerhouse of the cell?",
    "answer": "The mitochondrion.",
    "context": "Explained during cell structure section.",
    "timestamp": "{chunk_timestamp}",
    "tags": ["biology", "cells"]
  }}
]

Chunk Timestamp: {chunk_timestamp}
Chunk Text:
\"\"\"{chunk_text}\"\"\"

Respond ONLY with a JSON array of flashcards.
    """

    try:
        response = llm.invoke(prompt).strip()
        json_start = response.find("[")
        json_end = response.rfind("]") + 1

        if json_start == -1 or json_end == -1:
            raise ValueError("No JSON structure found in output.")

        json_str = response[json_start:json_end]
        flashcards = json.loads(json_str)

        if isinstance(flashcards, list):
            return flashcards
        else:
            print("Warning: Output was not a list.")
            return []

    except json.JSONDecodeError:
        print("Warning: LLaMA output was not valid JSON.")
        return []
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return []

@tool
def generate_flashcard_dict() -> str:
    """
    Generates flashcards from transcript.txt using LLaMA and saves them to flashcards.json.
    Returns the path to the JSON file.
    """
    transcript_path = "defaulttranscript.txt"
    output_path = "defaultflashcards.json"
    if not os.path.exists(transcript_path):
        raise FileNotFoundError(f"{transcript_path} not found.")

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    if not transcript.strip():
        raise ValueError("Transcript file is empty.")

    chunks = chunk_transcript_with_timestamps(transcript)
    all_flashcards = []

    for i, chunk in enumerate(chunks):
        print(f"Generating flashcards for chunk {i+1}/{len(chunks)} — Timestamp: {chunk['timestamp']}")
        cards = extract_flashcards_from_chunk_with_llama(chunk["text"], chunk["timestamp"], max_flashcards=10)
        print(f"Chunk {i+1} returned {len(cards)} cards")
        all_flashcards.extend(cards)


    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_flashcards, f, indent=2)
        
    return "Flashcards generated and saved to flashcards.json"

