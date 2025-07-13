import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

<<<<<<< HEAD
# Import common types
from common.types import State, add_messages, FunctionMessage # FunctionMessage also needed here for messages
=======
class State(TypedDict):
    youtube_url: STARTmetadata:dict|None
    transcript:str|None
    summary: str |None 
    error_message: str|None
    messages: Annotated[list[BaseMessage], add_mmessages]
>>>>>>> 35df10456e29709dc29c9f6b2f3fca904328b67c



def extract_text_function(state: State) -> dict:
    """
    Extracts the transcript from the YouTube video using the video_id derived from the URL.
    Updates 'transcript' and 'messages' in the state.
    """
    youtube_url = state.get("youtube_url")
    if not youtube_url:
        return {"error_message": "YouTube URL not found in state.", "messages": state.get("messages", []) + [FunctionMessage(name="extract_text", content="Error: YouTube URL not provided.")]}

    video_id_match = re.search(r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|\?v=)|youtu\.be\/)([^"&?\/\s]{11})', youtube_url)
    if not video_id_match:
        return {"error_message": "Invalid YouTube URL format.", "messages": state.get("messages", []) + [FunctionMessage(name="extract_text", content="Error: Invalid YouTube URL format.")]}
    
    video_id = video_id_match.group(1)

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        transcript = ""
        try:
            # Prioritize English, then any available generated/translatable
            english_transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
            transcript_data = english_transcript.fetch()
        except NoTranscriptFound:
            if transcript_list:
                print(f"No English transcript found for {video_id}, falling back to first available.")
                # Fallback to the first available transcript (either generated or manually uploaded)
                available_transcripts = [t for t in transcript_list._generated_transcripts + transcript_list._manually_created_transcripts if t.is_translatable or t.is_generated]
                if available_transcripts:
                    transcript_data = available_transcripts[0].fetch()
                else:
                    return {"error_message": f"No transcripts found for video ID: {video_id}", "messages": state.get("messages", []) + [FunctionMessage(name="extract_text", content=f"Error: No transcripts found for {video_id}.")]}
            else:
                return {"error_message": f"No transcripts found for video ID: {video_id}", "messages": state.get("messages", []) + [FunctionMessage(name="extract_text", content=f"Error: No transcripts found for {video_id}.")]}

        formatted_transcript_parts = []
        for entry in transcript_data:
            start_time = int(entry['start'])
            formatted_transcript_parts.append(f"[{start_time}]: {entry['text']}")
        
        transcript = "\n".join(formatted_transcript_parts)
        
        new_messages = state.get("messages", []) + [
            FunctionMessage(name="extract_text", content=f"Successfully extracted transcript for video ID: {video_id}")
        ]
        return {"transcript": transcript, "messages": new_messages}
    except Exception as e:
        return {"error_message": f"Error extracting transcript: {e}", "messages": state.get("messages", []) + [FunctionMessage(name="extract_text", content=f"Error extracting transcript: {e}")]}


graph_builder = StateGraph(State)



graph_builder= Stategraph(AgentState)
graph_builder.add_node("retrieve_metadata", retrieve_metadata_function)
graph_builder.add_node("extract_text", extract_text_function)
graph_builder.add_node("summrize_text", summarize_text_function)

graph_builder.add_edge(START, "retrieve_metadata") 
graph_builder.add_edge("retrieve_metadata", "extract_text")
graph_builder.add_edge("extract_text", "summrize_text")
graph_builder.add_edge("summrize_text", END)

