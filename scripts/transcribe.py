from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from langchain_core.tools import tool
@tool
def youtube_get_transcripts(youtube_url: str, filename = "defaulttranscript.txt") -> str:
    """
    Extracts and saves the transcript of a YouTube video to transcript.txt.
    Returns the path to the saved transcript file.
    """
    from pytube import extract
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import NoTranscriptFound

    try:
        video_id = extract.video_id(youtube_url)
        if not video_id:
            raise ValueError("Could not extract a video ID from the URL.")
    except Exception:
        raise ValueError("Invalid YouTube URL format.")

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
                raise ValueError(f"No usable transcripts found for video ID {video_id}.")
            transcript_data = available_transcripts[0].fetch()

        formatted_lines = [f"[{int(entry.start)}]: {entry.text}" for entry in transcript_data]
        transcript_str = "\n".join(formatted_lines)

        output_path = filename
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript_str)

        return f"Transcript saved to {output_path}"

    except Exception as e:
        raise ValueError(f"Error retrieving transcript: {e}")
