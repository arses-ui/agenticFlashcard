import genanki
import random # For generating unique IDs

def generate_anki_apkg_with_custom_note_name(
    flashcard_data,
    deck_name="YouTube Learning Flashcards",
    note_type_name="YouTube Lecture Notes", # New parameter for note type name
    output_filepath="anki_flashcards.apkg"
):
    """
        flashcard_data (list): A list of dictionaries, where each dictionary represents a flashcard with potential keys: "term"/"question", "definition"/"answer", "context", "timestamp", "tags".
        deck_name (str): The name of the Anki deck to be created.
        note_type_name (str): The name of the custom note type to be created in Anki.
        output_filepath (str): The path to save the generated .apkg file.
    """

    # --- 1. Define your Note Type (Model) ---
    # Model ID: A unique ID for your note type. IMPORTANT: Use the same ID
    #           if you ever want to update existing notes of this type or share the model.
    #           Changing this ID will create a *new* note type in Anki.
    # We'll use a fixed ID for consistency in this example, but in a real app
    # you might want to generate stable IDs (e.g., using a hash of the name)
    # or allow the user to specify them for advanced control.
    my_model_id = 1607077777 # An arbitrary fixed integer for the model ID
    my_deck_id = 1607077778  # An arbitrary fixed integer for the deck ID

    my_model = genanki.Model(
        my_model_id,
        note_type_name,
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
            {'name': 'Context'},
            {'name': 'Timestamp'}
        ],
        templates=[
            {
                'name': 'Card 1 (Front to Back)',
                'qfmt': '{{Front}}',  # Question format
                'afmt': '''
                    {{FrontSide}}
                    <hr id="answer">
                    {{Back}}
                    {{#Context}}<div class="field-label">Context:</div><div class="field-content">{{Context}}</div>{{/Context}}
                    {{#Timestamp}}<div class="field-label">Timestamp:</div><div class="field-content">{{Timestamp}}</div>{{/Timestamp}}
                ''', # Answer format - using #Field syntax for optional fields
            },
        ],
        css='''
            .card {
                font-family: Arial;
                font-size: 22px;
                text-align: center;
                color: black;
                background-color: white;
            }
            .card.nightMode {
                color: white;
                background-color: #333;
            }
            .field-label {
                font-size: 16px;
                color: #888; /* Lighter grey for labels */
                margin-top: 10px;
                text-align: left;
                padding-left: 10px;
            }
            .field-content {
                font-size: 18px;
                text-align: left;
                padding-left: 10px;
            }
            hr {
                border: 0;
                height: 1px;
                background: #ccc;
                margin: 20px 0;
            }
        '''
    )

    # ---  generating the deck ---
    my_deck = genanki.Deck(
        my_deck_id,
        deck_name
    )

    # --- iterate through the flash card data and create notes ---
    for card_data in flashcard_data:
        front_content = card_data.get("question") or card_data.get("term", "")
        back_content = card_data.get("answer") or card_data.get("definition", "")
        context_content = card_data.get("context", "")
        timestamp_content = card_data.get("timestamp", "")
        tags = card_data.get("tags", [])

        my_note = genanki.Note(
            model=my_model,
            fields=[
                front_content,
                back_content,
                context_content,
                timestamp_content
            ],
            tags=tags 
        )
        my_deck.add_note(my_note)

    # --- Generate the .apkg file ---
    genanki.Package(my_deck).write_to_file(output_filepath)
    print(f"Anki package generated to '{output_filepath}'")

# --- Test Data ---
sample_flashcard_data = [
    {
        "term": "Quantum Entanglement",
        "definition": "A phenomenon where two or more particles become linked in such a way that they share the same fate, no matter how far apart they are.",
        "context": "The lecture introduced the concept of quantum entanglement as a peculiar aspect of quantum mechanics.",
        "timestamp": "00:15:20",
        "tags": ["Physics", "Quantum Mechanics"]
    },
    {
        "question": "What is the primary function of ribosomes?",
        "answer": "To synthesize proteins.",
        "context": "Ribosomes, often described as protein factories, play a vital role in cell biology.",
        "timestamp": "00:08:45",
        "tags": ["Biology", "Cell Biology"]
    },
    {
        "term": "Big O Notation",
        "definition": "A mathematical notation that describes the limiting behavior of a function when the argument tends towards a particular value or infinity. Used to classify algorithms by how they respond to changes in input size.",
        "context": "When analyzing algorithm efficiency, we often use Big O notation.",
        "timestamp": "00:22:10",
        "tags": ["Computer Science", "Algorithms"]
    },
    { # Example of a card with only term/definition, no context/timestamp/tags
        "term": "Algorithm",
        "definition": "A set of rules or instructions to be followed in calculations or other problem-solving operations.",
        "tags": ["General"]
    }
]

# --- Call the function ---
if __name__ == "__main__":
    # --- Using the default note type name ---
    print("Generating with default note type name...")
    generate_anki_apkg_with_custom_note_name(
        sample_flashcard_data,
        output_filepath="my_default_note_type_cards.apkg"
    )

    # --- Specifying a custom note type name ---
    print("\nGenerating with a custom note type name: 'My Science Concepts'")
    generate_anki_apkg_with_custom_note_name(
        sample_flashcard_data,
        note_type_name="My Science Concepts", # User-defined name
        output_filepath="my_science_concepts_cards.apkg"
    )

    # --- Another custom name for a different set of cards ---
    print("\nGenerating with another custom note type name: 'CS Algo Study'")
    generate_anki_apkg_with_custom_note_name(
        [
            {
                "term": "Binary Search",
                "definition": "An efficient algorithm for finding an item from a sorted list of items. It works by repeatedly dividing in half the portion of the list that could contain the item.",
                "context": "We applied binary search in the lecture to find elements quickly.",
                "timestamp": "00:30:00",
                "tags": ["Computer Science", "Algorithms", "Search"]
            }
        ],
        deck_name="CS Algorithms",
        note_type_name="CS Algo Study", # Another user-defined name
        output_filepath="cs_algo_study_cards.apkg"
    )