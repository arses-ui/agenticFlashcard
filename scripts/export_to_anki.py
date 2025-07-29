import os
import json
import genanki
import hashlib
from langchain_core.tools import tool
from typing import List, Dict

def generate_id_from_string(text_string):
    hash_object = hashlib.sha256(text_string.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    large_int = int(hex_dig[:16], 16)
    model_id = (large_int & ((1 << 30) - 1)) | (1 << 30)
    return model_id

def generate_anki_apkg_with_custom_note_name(
    flashcard_data: List[Dict],
    deck_name = input("Enter deck name: ").strip(),
    note_type_name: str = input("Note type: ").strip(), 
    output_filepath: str = "anki_flashcards.apkg"
):
    model_id = generate_id_from_string(note_type_name)
    deck_id = generate_id_from_string(deck_name)

    my_model = genanki.Model(
        model_id,
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
                'qfmt': '{{Front}}',
                'afmt': '''
                    {{FrontSide}}
                    <hr id="answer">
                    {{Back}}
                    {{#Context}}<div class="field-label">Context:</div><div class="field-content">{{Context}}</div>{{/Context}}
                    {{#Timestamp}}<div class="field-label">Timestamp:</div><div class="field-content">{{Timestamp}}</div>{{/Timestamp}}
                '''
            },
        ],
        css='''
            .card { font-family: Arial; font-size: 22px; text-align: center; color: black; background-color: white; }
            .card.nightMode { color: white; background-color: #333; }
            .field-label { font-size: 16px; color: #888; margin-top: 10px; text-align: left; padding-left: 10px; }
            .field-content { font-size: 18px; text-align: left; padding-left: 10px; }
            hr { border: 0; height: 1px; background: #ccc; margin: 20px 0; }
        '''
    )

    my_deck = genanki.Deck(deck_id, deck_name)

    for card_data in flashcard_data:
        front = card_data.get("question") or card_data.get("term", "")
        back = card_data.get("answer") or card_data.get("definition", "")
        context = card_data.get("context", "")
        timestamp = card_data.get("timestamp", "")
        tags = [tag.replace(" ", "-") for tag in card_data.get("tags", [])]

        note = genanki.Note(
            model=my_model,
            fields=[front, back, context, timestamp],
            tags=tags
        )
        my_deck.add_note(note)

    genanki.Package(my_deck).write_to_file(output_filepath)
    print(f"Anki package generated at: {output_filepath}")

@tool
def export_to_anki() -> str:
    """
    Loads flashcard data from a JSON file and exports it to a .apkg file using genanki.
    Input: Path to a JSON file containing flashcard dictionaries
    Output: Path to the generated Anki file
    """
    flashcard_json_path = "defaultflashcards.json"
    output_file = "default_anki_flashcards.apkg"
    if not os.path.exists(flashcard_json_path):
        raise FileNotFoundError(f"{flashcard_json_path} not found.")

    with open(flashcard_json_path, "r", encoding="utf-8") as f:
        try:
            flashcard_data = json.load(f)
            if not isinstance(flashcard_data, list):
                raise ValueError("Flashcard JSON must contain a list of dictionaries.")
        except json.JSONDecodeError:
            raise ValueError("Failed to parse flashcard JSON file.")
    generate_anki_apkg_with_custom_note_name(flashcard_data, output_filepath=output_file)

    return "Anki package exported to anki_flashcards.apkg"

