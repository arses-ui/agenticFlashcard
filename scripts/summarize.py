import os
from langchain_ollama import OllamaLLM
from langchain_core.tools import tool

# Initialize LLaMA via Ollama
llm = OllamaLLM(model="llama3", temperature=0.5)

@tool
def summarize_transcript() -> str:
    """
    Summarizes transcript.txt using a local LLaMA model and saves it to summary.txt.
    Returns the summary string.
    """
    transcript_path = "defaulttranscript.txt"
    output_path ="defaultsummary.txt" 
    # Read transcript from file
    if not os.path.exists(transcript_path):
        raise FileNotFoundError(f"Transcript file not found: {transcript_path}")

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    if not transcript.strip():
        raise ValueError("Transcript file is empty.")

    # Prompt for summarization
    prompt = (
        "You are an assistant that summarizes transcripts for studying. Focus on the key ideas, "
        "preserve any timestamps if present, and write in a concise, structured way.\n\n"
        f"Transcript:\n{transcript}"
    )

    try:
        summary = llm.invoke(prompt).strip()

        # Save summary to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)

        return "Transcript summarized and saved to summary.txt"

    except Exception as e:
        raise RuntimeError(f"Error during summarization: {e}")
