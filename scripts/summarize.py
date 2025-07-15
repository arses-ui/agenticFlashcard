import os
import google.generativeai as genai
from dotenv import load_dotenv
from common.types import State, FunctionMessage

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def summarize_text_function(state: State) -> dict:
    transcript = state.get("transcript")
    if not transcript:
        return {
            "error_message": "Transcript not found in state for summarization.",
            "messages": state.get("messages", []) + [
                FunctionMessage(name="summarize_text", content="Transcript missing.")
            ]
        }

    prompt = (
        "You are an assistant that summarizes transcripts for educational purposes. "
        "Keep the most important points and include timestamps (if provided). "
        "Here's the transcript:\n\n" + transcript
    )

    try:
        response = model.generate_content(prompt)
        summary = response.text

        new_messages = state.get("messages", []) + [
            FunctionMessage(name="summarize_text", content="Summary generated successfully.")
        ]
        return {"summary": summary, "messages": new_messages}

    except Exception as e:
        return {
            "error_message": f"Error: {e}",
            "messages": state.get("messages", []) + [
                FunctionMessage(name="summarize_text", content=f"Error during summarization: {e}")
            ]
        }
