from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
import re
from langchain_core.tools import tool


@tool
def youtube_get_transcripts(youtube_url: str) -> str:
    """
    Extracts the transcript from a YouTube video URL and returns it as a formatted string.
    Raises ValueError on failure.
    """
    match = re.search(
        r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|\?v=)|youtu\.be\/)([^"&?\/\s]{11})',
        youtube_url
    )
    if not match:
        raise ValueError("Invalid YouTube URL format.")

    video_id = match.group(1)

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            english_transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
            transcript_data = english_transcript.fetch()
        except NoTranscriptFound:
            available_transcripts = [
                t for t in transcript_list._generated_transcripts + transcript_list._manually_created_transcripts
                if t.is_translatable or t.is_generated
            ]
            if not available_transcripts:
                raise ValueError(f"No transcripts available for video ID {video_id}.")
            transcript_data = available_transcripts[0].fetch()

        formatted_lines = [
            f"[{int(entry['start'])}]: {entry['text']}" for entry in transcript_data
        ]
        return "\n".join(formatted_lines)

    except Exception as e:
        raise ValueError(f"Error retrieving transcript: {e}")
