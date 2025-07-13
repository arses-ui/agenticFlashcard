import os
from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver
from typing import Literal

# Import shared types and utility functions
from common.types import State, add_messages

# Import node functions from refactored files
from transcribe import extract_text_function
from summarize import summarize_text_function
from flashcards import generate_flashcards


def route_after_extraction(state: State) -> Literal["summarize_text", "generate_flashcards", END]:
    """
    Determines the next step after transcript extraction based on user_choice.
    """
    choice = state.get("user_choice")
    if choice == "summary" or choice == "both":
        return "summarize_text"
    elif choice == "flashcards":
        return "generate_flashcards"
    else:
        # Fallback for invalid choice
        state["error_message"] = "Invalid output choice specified after transcript extraction."
        return END

def route_after_summarization(state: State) -> Literal["generate_flashcards", END]:
    """
    Determines the next step after summarization. If user chose 'both', proceeds to flashcards.
    """
    choice = state.get("user_choice")
    if choice == "both":
        return "generate_flashcards"
    else:
        return END

def main():
    # Initialize checkpointer for graph state persistence
    checkpointer = MemorySaver()

    # Create the StateGraph with the shared State definition
    graph_builder = StateGraph(State)

    # Add the individual functions as nodes in the graph
    graph_builder.add_node("extract_text", extract_text_function)
    graph_builder.add_node("summarize_text", summarize_text_function)
    graph_builder.add_node("generate_flashcards", generate_flashcards)

    # Define the graph's entry point
    graph_builder.set_entry_point("extract_text")

    # Define conditional edges from "extract_text"
    graph_builder.add_conditional_edges(
        "extract_text",
        route_after_extraction, # The routing function determines the next node
        {
            "summarize_text": "summarize_text",
            "generate_flashcards": "generate_flashcards",
            END: END # If the routing function returns END, the graph terminates
        }
    )

    # Define conditional edges from "summarize_text"
    graph_builder.add_conditional_edges(
        "summarize_text",
        route_after_summarization, # Determines if it proceeds to flashcards or ends
        {
            "generate_flashcards": "generate_flashcards",
            END: END
        }
    )

    # Define a direct edge from "generate_flashcards" to END, as it's the final step
    graph_builder.add_edge("generate_flashcards", END)

    # Compile the graph
    app = graph_builder.compile(checkpointer=checkpointer)

    # --- Example Usage: Test with different user choices ---

    # Make sure to set your OPENAI_API_KEY environment variable before running!
    # e.g., in your terminal: export OPENAI_API_KEY="sk-YOUR_KEY_HERE"

    # Example YouTube URL (replace with a real one for testing)
    # This example is for testing, please use a real YouTube URL that has transcripts.
    test_youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Rick Astley - Never Gonna Give You Up

    print("--- Running for Summary Only ---")
    initial_state_summary = {
        "youtube_url": test_youtube_url,
        "user_choice": "summary",
        "messages": []
    }
    for s in app.stream(initial_state_summary):
        print(s)
        print("---")
    final_state_summary = app.invoke(initial_state_summary)
    print("\nFinal State (Summary):")
    print(f"Summary (first 200 chars): {final_state_summary.get('summary', 'No summary generated')[:200]}...")
    print(f"Flashcards generated: {len(final_state_summary.get('flashcards', []))} cards")
    print(f"Error Message: {final_state_summary.get('error_message')}")

    print("\n\n--- Running for Flashcards Only ---")
    initial_state_flashcards = {
        "youtube_url": test_youtube_url,
        "user_choice": "flashcards",
        "messages": []
    }
    for s in app.stream(initial_state_flashcards):
        print(s)
        print("---")
    final_state_flashcards = app.invoke(initial_state_flashcards)
    print("\nFinal State (Flashcards):")
    print(f"Summary: {final_state_flashcards.get('summary')}") # Should be None
    print(f"Flashcards generated: {len(final_state_flashcards.get('flashcards', []))} cards")
    print(f"Error Message: {final_state_flashcards.get('error_message')}")

    print("\n\n--- Running for Both Summary and Flashcards ---")
    initial_state_both = {
        "youtube_url": test_youtube_url,
        "user_choice": "both",
        "messages": []
    }
    for s in app.stream(initial_state_both):
        print(s)
        print("---")
    final_state_both = app.invoke(initial_state_both)
    print("\nFinal State (Both):")
    print(f"Summary (first 200 chars): {final_state_both.get('summary', 'No summary generated')[:200]}...")
    print(f"Flashcards generated: {len(final_state_both.get('flashcards', []))} cards")
    print(f"Error Message: {final_state_both.get('error_message')}")

if __name__ == "__main__":
    if os.environ.get("OPENAI_API_KEY") is None:
        print("🔥 **CRITICAL ERROR:** OPENAI_API_KEY environment variable not set.")
        print("Please set it before running the script:")
        print("  On Linux/macOS: `export OPENAI_API_KEY='your_api_key_here'`")
        print("  On Windows (CMD): `set OPENAI_API_KEY='your_api_key_here'`")
        print("  On Windows (PowerShell): `$env:OPENAI_API_KEY='your_api_key_here'`")
        exit(1) # Exit with an error code
    main()
