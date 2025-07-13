# your_project/run_app.py

import os
# Import the build_app function from your main.py
from main import build_app
# Also import State, if you need to construct initial_state using its type hint
from scripts.commontypes import State

# Ensure OPENAI_API_KEY is set in your environment
if os.environ.get("OPENAI_API_KEY") is None:
    print(" **CRITICAL ERROR:** OPENAI_API_KEY environment variable not set.")
    print("Please set it before running the script:")
    print("  On Linux/macOS: `export OPENAI_API_KEY='your_api_key_here'`")
    print("  On Windows (CMD): `set OPENAI_API_KEY='your_api_key_here'`")
    print("  On Windows (PowerShell): `$env:OPENAI_API_KEY='your_api_key_here'`")
    exit(1)

# Build the application
app = build_app()

# Define a test YouTube URL
test_youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Rick Astley - Never Gonna Give You Up

print("--- Simulating a User Request: Get Summary ---")

# A user would provide these inputs, e.g., via a web form, CLI, etc.
user_input_state: State = {
    "youtube_url": test_youtube_url,
    "user_choice": "summary", # User wants only a summary
    "messages": [] # Initialize messages
}

# Invoke the application with the user's input
final_output_state = app.invoke(user_input_state)

print("\nUser Request Processed. Final Output:")
print(f"Summary: {final_output_state.get('summary', 'No summary available')[:500]}...") # Print summary
print(f"Flashcards generated: {len(final_output_state.get('flashcards', []))} cards")
if final_output_state.get('error_message'):
    print(f"Error: {final_output_state.get('error_message')}")

print("\n--- Simulating another User Request: Get Flashcards ---")
user_input_state_flashcards: State = {
    "youtube_url": test_youtube_url,
    "user_choice": "flashcards", # User wants only flashcards
    "messages": []
}

final_output_state_flashcards = app.invoke(user_input_state_flashcards)

print("\nUser Request Processed. Final Output:")
print(f"Summary: {final_output_state_flashcards.get('summary', 'No summary available')}") # Should be None
print(f"Flashcards generated: {len(final_output_state_flashcards.get('flashcards', []))} cards")
if len(final_output_state_flashcards.get('flashcards', [])) > 0:
    print("Sample Flashcard:", final_output_state_flashcards['flashcards'][0]) # Print a sample
if final_output_state_flashcards.get('error_message'):
    print(f"Error: {final_output_state_flashcards.get('error_message')}")