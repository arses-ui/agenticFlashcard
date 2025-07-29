from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

from scripts.transcribe import youtube_get_transcripts
from scripts.summarize import summarize_transcript
from scripts.flashcards import generate_flashcard_dict
from scripts.export_to_anki import export_to_anki

load_dotenv()

llm = OllamaLLM(model="llama3", temperature=0.5)

tools = [
    Tool(
        name="TranscribeVideo",
        func=youtube_get_transcripts,
        description="Transcribes a YouTube video and saves it to transcript.txt. Input: YouTube URL."
    ),
    Tool(
        name="SummarizeTranscript",
        func=summarize_transcript,
        description="Summarizes transcript.txt and saves it to summary.txt. Input: anything to trigger."
    ),
    Tool(
        name="GenerateFlashcards",
        func=generate_flashcard_dict,
        description="Generates flashcards from transcript.txt and saves to flashcards.json. Input: anything to trigger."
    ),
    Tool(
        name="ExportToAnki",
        func=lambda _: export_to_anki("flashcards.json"),
        description="Exports flashcards.json to anki_flashcards.apkg. Input: anything to trigger."
    )
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


agent = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={
        "system_message": """
You are a perfect, smart, rigid assistant that follows a strict four-step workflow to generate flashcards, then export it to .apkg to be used in Anki from a YouTube video:
Never repeat steps or skip steps. Check each step's output before proceeding to the next. There will be an output confirming the successful completion of each step.
1. Transcribe the YouTube video using TranscribeVideo tool.
2. Summarize the transcript using SummarizeTranscript tool.
3. Generate flashcards from transcript.txt using GenerateFlashcards tool.
4. Export the flashcards into anki_flashcards.apkg using ExportToAnki tool.
Only run one step at a time. After step 4 is complete, check the output message. If the output says "Anki package exported to anki_flashcards.apkg", then STOP. Never run tools again after that.
"""
    }
)

if __name__ == "__main__":
    youtube_url = input("Enter YouTube URL: ").strip()
    output = agent.run(youtube_url)
    if "Anki package exported to anki_flashcards.apkg" in output:
        print("It's over")
        exit()

