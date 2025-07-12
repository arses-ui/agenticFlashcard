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

ytt_api = YoutubetTranscriptApi()
checkpointer = InMemorySaver() 

class State(TypedDict):
    youtube_url: STARTmetadata:dict|None
    transcript:str|None
    summary: str |None 
    error_message: str|N one
    messages: Annotated[list, add_mmessages]

def youtube_get_transcripts(url, state:)
    match = re.search(r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|\?v=)|youtu\.be\/)([^"&?\/\s]{11})', url)
    snippets = ytt_api.fetch(video_id)[0]
    return snippet if match else None

llm = ChaptOpenAI(
    model ="gpt-4o", temperature=0, 
    max_tokens = None, 
    timeout=None, 
    api_key = "OPENAI_API_KEY"
)

def get_youtube_metadata(video_id, api_key): 
    try: 
        youtube= build('youtube', 'v3', developerKey= api_key)
        request= youtube.videos().lsit(
            prt =""
        )




def get_transcript(state: State): 

agent = create_react_agent(
    model = ".."
    tools= [get_trasncript]
    prompt = "You are an assistant that is supposed to take the transcript and generate a clear concise summary of the most important parts of the transcript. While summarizing, make sure to retain the time stamps and provide the time stamp along with the summarized sentence"
    checkpointer=checkpointer 
)

#Each node can revieve the current State as input and output an update
# to the state 

#Updated messages will be appended to the existing list rather than overwriting it, due to the prebuild add_messages 
class State(TypedDict):
    youtube_url: STARTmetadata:dict|None
    transcript:str|None
    summary: str |None 
    error_message: str|N one
    messages: Annotated[list, add_mmessages]

graph_builder = StateGraph(State)



graph_builder= Stategraph(AgentState)
graph_builder.add_node("retrieve_metadata", retrieve_metadata_function)
graph_builder.add_node("extract_text", extract_text_function)
graph_builder.add_node("summrize_text", summarize_text_function)

graph_builder.add_edge(START, "retrieve_metadata") 
graph_builder.add_edge("retrieve_metadata", "extract_text")
graph_builder.add_edge("extract_text", "summrize_text")
graph_builder.add_edge("summrize_text", END)

