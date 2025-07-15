from typing import TypedDict, Optional, List
from langchain_core.messages import BaseMessage

class State(TypedDict, total=False):
    transcript: Optional[str]
    summary: Optional[str]
    messages: List[BaseMessage]
    error_message: Optional[str]
