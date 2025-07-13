from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated 
import os
import getpass
import os
from langchain_openai import ChatOpenAI
from youtube_transcript_api import YoutubeTranscriptApi
checkpointer = InMemorySaver() 

llm = ChatOpenAI(
    model = "gpt-4o", temperature =0, 
    max_tokens = None, 
    timeout = None, 
    api_key = "OPENAI_API_KEY"
)

def summarize_text_function(state: State) -> dict: 

    transcript = state.get("transcript")
    if not transcript:
        return{"error_message": "Transcript not found in state for summariztion,","messages": state.get("messages", [])+ [FunctionMessage(name = "summarize_text", content= "Error:Transcript not available for summarization.")]}

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant that is supposed to take the transcript and generate a clear concise summary of the most improtant parts of the transcript. While summarizing, make sure to retain the time stamps and provide the time stamp alonf with the sumamrized sentence"), 
        ("user", "Summarize the following transcript:\n\n{transcript}")
    ])
    try: 
        summarize_chin = prompt_template | llm 
        response = summarize_chain.invoke({"transcript" : transcript})
        summary = response.content
        new_messges = state.get("messages", []) + [
            FunctionMessage(name= "summarize_text", content = "Successfully generte summary.")
        ]
        return {"summary": summary, "messages": new_messages }
    execept Exception as e:
        return {"error_message": f"Error summarizing transcript {e}", "messages":state.get("messages", [])+ [FunctionMesssage(name = "summarize_text", content= f"Error summarizing transcript : {e}")]}
