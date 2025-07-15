import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool

from scripts import transcribe
from scripts import summarize as summarizes
from scripts import flashcards
from scripts import export_to_anki

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("Please set your GOOGLE_API_KEY in a .env file")

# Wrap your tools with descriptions
tools = [
    Tool(
        name="TranscribeVideo",
        func=transcribe.youtube_get_transcripts,
        description="Use this to transcribe a YouTube video. Input should be a YouTube URL.",
    ),
    Tool(
        name="Summarize",
        func=summarizes.summarize_text_function,
        description="Use this to summarize a transcript. Can be focused for different flashcard types like 'concepts', 'formulas', or 'definitions'.",
    ),
    Tool(
        name="GenerateFlashcards",
        func=flashcards.extract_flashcards_from_chunk_with_gemini,
        description="Use this to generate flashcards from a summary. Flashcard styles include: 'question-answer', 'fill-in-the-blank', or 'conceptual overview'.",
    ),
    Tool(
        name="ExportToAnki",
        func=export_to_anki.generate_anki_apkg_with_custom_note_name,
        description="Use this to export flashcards into a .apkg file for Anki. Input should be a list of flashcards.",
    ),
]
from langchain.llms.base import LLM
from typing import Optional

class DummyLLM(LLM):
    def _call(self, prompt: str, stop: Optional[list] = None) -> str:
        raise NotImplementedError("This LLM is a placeholder and should not be called.")
    
    @property
    def _llm_type(self) -> str:
        return "dummy"

agent = initialize_agent(
    tools=tools,
    llm=DummyLLM(),
    agent="zero-shot-react-description",
    verbose=True
)

if __name__ == "__main__":
    print("YouTube to Flashcards Agent")
    print("Type your request below (e.g., 'Make fill-in-the-blank flashcards from this video: https://...')")

    while True:
        user_input = input("\nYour prompt (or type 'exit'): ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting agent.")
            break
        try:
            result = agent.run(user_input)
            print("\nDone!\n")
        except Exception as e:
            print(f"Error: {e}")
