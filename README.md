# Agentic AI Flashcard

In this project, my friend Sakshyam and I developed an agentic workflow that takes in source material—such as YouTube links highlights the key takeaways, and generates and summary as well as flashcards that is integrated into Anki.

The workflow consists of four main modules:

`transcribe.py`
This module uses the YouTube API to fetch transcripts from YouTube videos and saves them in a transcribe.txt file.

`summarize.py`
This module uses Ollama to summarize the transcript. It breaks the transcript into smaller chunks, summarizes each chunk, and compiles the results into a summary.txt file.

`flashcards.py`
This module reads from summary.txt and generates between 2 to 10 flashcards based on the key information. The output is stored in a flashcards.json file.

`export_to_anki.py`
This module takes the flashcards from flashcards.json and exports them into an .apkg file that can be directly imported into Anki.

## Table of Contents 
[Installation](#installation) <br>
[Output](#output)<br>
[Dependencies](#dependencies)<br> 
[Contribution](#my_contribution)<br>

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
4. Set up model 
```bash
ollama serve
```
This lets you run AI/LLM models locally.

5. Fetch a model 
```bash
ollama pull ollama3 
```
This downloads the ollama model3 and lets you run them locally. You can try using other models. Write `ollama list` in the terminal and choose among the models shown. 

6. Run the model 
```bash 
python main.py 
```


```bash
# In your_project/main.py

Enter Deck : (your prompt to system)
# Based on this deck, the model has an internal dialogue with itself
Note type:  "both"
# "summary"    : Generate only a concise summary with timestamps.
# "flashcards" : Generate Anki-style flashcards with terms/definitions/questions.
# "both"       : Generate both a summary and flashcards (summary first, then flashcards).
# Replace with the YouTube URL you want to process
Enter Youtube URl = "your youtube url" # Example: Rick Astley
# Choose the desired output type:

```

## Output 
The script creates either a txt file for summary, anki flashcars or both depending on your prompt. 

## Dependencies
- Python 3.x 
- Packages listed in requirements.txt 


## My Cintribution 

In this collaborative project, I focused on developing the transcribe.py and summarize.py modules. I was mostly responsible for building them and ensuring their  integration with the rest of the workflow, including the flashcard generation and Anki export modules. I also worked jointly on the main.py script, which connects all the modules into a cohesive pipeline and handles the overall execution of the workflow.

Once the individual modules were complete, we worked together on integrating them into a functional end-to-end system. Currently, I am working on building a local front-end interface to host the workflow on a webpage, with plans to deploy it soon.

## Future work

While the workflow is functional, there are several areas for improvement, and the project is still ongoing. One major issue is the slow generation speed, which we aim to optimize. Additionally, the current use of .txt files for intermediate steps, though simple, is somewhat outdated and limits flexibility. We are exploring a shift back to LangGraph to better utilize its capabilities for modularity and asynchronous processing.

## Authors
Arses Prasai -[Github](https://github.com/arses-ui)  
Sakshyam Pokharel -[Github](https://github.com/psakshyam)

