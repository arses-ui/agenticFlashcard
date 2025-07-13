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

class State(TypedDict):
    youtube_url: STARTmetadata:dict|None
    transcript:str|None
    summary: str |None 
    error_message: str|None
    messages: Annotated[list[BaseMessage], add_mmessages]




def youtube_get_transcripts(state:State) ->: 

    youtube_url = state.get("youtube_url")
    if not youtube_url: 
        reutrn {"error_message": "YouTube URL not found for transcript extraction."}
    
    video_id_match = re.search(r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|\?v=)|youtu\.be\/)([^"&?\/\s]{11})', youtube_url)
    if not video_id_match: 
        return {"error": "Invalid YouTube URL format for transcript extraction."}
    video_id= video_id_match.group(1)
    snippets = ytt_api.fetch(video_id)[0]

    try: 
        transcript_list= YoutubetTranscriptApi.list_transcriptions(video_id)

        transcript = ""
        try: 
            english_transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
            transcript_data = english_transcript.fetch()
        except NoTranscriptFound: 
            if transcript_list: 
                print(f"No English transcript found for {video_id}, falling back to first available")

                availabe_transcripts = [to for t in transcript_list.generate_transcripts if t.is_translatable or t.is_generated]
                if available_transcripts: 
                    transcript_data= available_transcripts[0].fetch()
                else: 
                    return {"error_message:" f"Jo transcripts found forvideo ID:{video_id}", "messages": state.get("messages", []) + [FunctionMessage(name= "extract_text", content= f"Error:  No transcripts found for {video_id}.")]}

            else:  
                return{"error_message": f"No transcript found for video ID : {video_id}", "messages":state.get("messages", [])+ [FunctionMessage(name="extract_text", content= f"Error: No transcripts found for {video_id}.")]}

        #Format transcript with timestamps

        formatted_transcript_parts = []
        for entry in transcipt_data: 
            start_time= int(entry['start'])
            formatted_transcript_parts.append(f"[{start_time}]: {entry['text']}")

        transcript = "\n".join(formatted_transcript_parts)

        new_messages = stte.get("messages", [])+ [
            FunctionMessage(name= "extract_text", content = f"Successfully extracted transcript for video ID: {video_id}")
        ]
        return {"transcript": transcript, "messages": new_messages}
    except Exception as e: 
        return{"error_message:" f"Error extracting transcript:{e}", "messages":state.get("message", []) + [FunctionMessage(name= "extract_text", content= f"Error extracting transcript: {e}")]}


graph_builder = StateGraph(State)



graph_builder= Stategraph(AgentState)
graph_builder.add_node("retrieve_metadata", retrieve_metadata_function)
graph_builder.add_node("extract_text", extract_text_function)
graph_builder.add_node("summrize_text", summarize_text_function)

graph_builder.add_edge(START, "retrieve_metadata") 
graph_builder.add_edge("retrieve_metadata", "extract_text")
graph_builder.add_edge("extract_text", "summrize_text")
graph_builder.add_edge("summrize_text", END)

