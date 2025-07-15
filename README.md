# Agentic AI Flashcard

In this project, we develop an agentic workflow that takes source material (Youtube links, pdfs, websites), summarizes it, highlights the key takeaways, then creates flashcards based on the highlights that can be integrated to Anki. 

## Table of Contents 
[Installation](#installation) <br>
[Output](#output)<br>
[Dependencies](#dependencies)<br> 

## Installation
1. Clone the repository:
```bash
git clone https://github.com/psakshyam/agenticFlashcard.git
cd your-repository-name
```

2. Create and activate a virtual environment:
```bash
python -m venv venv 
a. source venv/Scripts/activate # For Windows + Git Bash or WSL
b. venv\Scripts\activate #For Windows Command Prompt 
c. venv/bin/activate #For Mac/Linux
```

3. Install requried packages:
```bash
pip install -r requirements.txt 
 ```
5. Run the Project:
```bash
python run_app.py
```
In `run_app.py`, you can modify the `test_youtube_url` and `user_choice` variables to control the application's input.

```bash

# In your_project/run_app.py

# Replace with the YouTube URL you want to process
test_youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Example: Rick Astley
# Choose the desired output type:
# "summary"    : Generate only a concise summary with timestamps.
# "flashcards" : Generate Anki-style flashcards with terms/definitions/questions.
# "both"       : Generate both a summary and flashcards (summary first, then flashcards).
user_choice = "both" # Change this to "summary", "flashcards", or "both"
```

## Output 
The script will then print the processing steps (if `app.stream` is used) and the final output (summary and/or flashcards) to your console.

## Dependencies
- Python 3.x 
- Packages listed in requirements.txt 

## Authors
Arses Prasai -[Github](https://github.com/arses-ui)  
Sakshyam Pokharel -[Github](https://github.com/psakshyam)

