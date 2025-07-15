from typing import TypedDict, List, Optional, Union
from langchain_core.messages import BaseMessage

class State(TypedDict, total=False):
    youtube_url: Optional[str]
    metadata: Optional[dict]
    transcript: Optional[str]
    summary: Optional[str]
    error_message: Optional[str]
    messages: List[BaseMessage]

# Optional wrapper that simulates adding messages
def add_messages(messages: List[BaseMessage]) -> List[BaseMessage]:
    return messages

# Add this line if you're using FunctionMessage in your state
from langchain_core.messages import FunctionMessage
