# your_project/common/types.py

from typing import TypedDict, Annotated, List, Dict, Union
from langchain_core.messages import BaseMessage, FunctionMessage

# Helper function for adding messages to the state list
def add_messages(left: list[BaseMessage], right: list[BaseMessage]) -> list[BaseMessage]:
    """Appends new messages to the existing list."""
    if not isinstance(left, list):
        left = []
    if not isinstance(right, list):
        right = []
    return left + right

# Define the State TypedDict
class State(TypedDict):
    youtube_url: str | None
    transcript: str | None
    summary: str | None
    flashcards: List[Dict[str, Union[str, List[str]]]] | None
    user_choice: str | None # "summary", "flashcards", or "both"
    error_message: str | None
    messages: Annotated[list[BaseMessage], add_messages] # Annotated for LangGraph's merge behavior