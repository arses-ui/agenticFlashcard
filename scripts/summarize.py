import os
from dotenv import load_dotenv
import google.generativeai as genai
from common.types import State, FunctionMessage

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro")

def summarize_text_function(state: State) -> dict:
    """
    Summarizes the extracted transcript using Gemini (gemini-pro).
    Updates 'summary' and 'messages' in the state.
    """
    transcript = state.get("transcript")
    if not transcript:
        return {
            "error_message": "Transcript not found in state for summarization.",
            "messages": state.get("messages", []) + [
                FunctionMessage(name="summarize_text", content="Error: Transcript not available for summarization.")
            ]
        }

    try:
        prompt = (
            "You are an assistant that generates clear, timestamped summaries from transcripts. "
            "For each important point, include the corresponding timestamp and make the summary concise.\n\n"
            f"Transcript:\n{transcript}"
        )

        response = model.generate_content(prompt)

        # .text sometimes doesn't exist if Gemini failed — be cautious
        summary = getattr(response, "text", None)
        if not summary:
            raise ValueError("No summary returned from Gemini model.")

        new_messages = state.get("messages", []) + [
            FunctionMessage(name="summarize_text", content="Successfully generated summary.")
        ]
        return {"summary": summary, "messages": new_messages}

    except Exception as e:
        return {
            "error_message": f"Error summarizing transcript: {e}",
            "messages": state.get("messages", []) + [
                FunctionMessage(name="summarize_text", content=f"Error summarizing transcript: {e}")
            ]
        }
