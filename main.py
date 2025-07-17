from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
import os
from dotenv import load_dotenv
from scripts import transcribe
from scripts import summarize as summarizes
from scripts import flashcards
from scripts import export_to_anki

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("Please set your OPENAI_API_KEY environment variable.")

# Initialize LLM
llm = ChatOpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY)

# Wrap tools with descriptions
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

# initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
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
