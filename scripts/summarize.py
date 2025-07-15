import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import FunctionMessage # Needed for messages list

from common.types import State
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.5
)

def summarize_text_function(state: State) -> dict:
    """
    Summarizes the extracted transcript using the LLM.
    Updates 'summary' and 'messages' in the state.
    """
    transcript = state.get("transcript")
    if not transcript:
        return {"error_message": "Transcript not found in state for summarization.", "messages": state.get("messages", []) + [FunctionMessage(name="summarize_text", content="Error: Transcript not available for summarization.")]}

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant that is supposed to take the transcript and generate a clear concise summary of the most important parts of the transcript. While summarizing, make sure to retain the time stamps and provide the time stamp along with the summarized sentence."),
        ("user", "Summarize the following transcript:\n\n{transcript}")
    ])

    try:
        summarize_chain = prompt_template | llm
        response = summarize_chain.invoke({"transcript": transcript})
        summary = response.content
        
        new_messages = state.get("messages", []) + [
            FunctionMessage(name="summarize_text", content="Successfully generated summary.")
        ]
        return {"summary": summary, "messages": new_messages}
    except Exception as e:
        return {"error_message": f"Error summarizing transcript: {e}", "messages": state.get("messages", []) + [FunctionMessage(name="summarize_text", content=f"Error summarizing transcript: {e}")]}