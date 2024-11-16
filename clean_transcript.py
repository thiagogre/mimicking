import re


def clean_transcript(file_path: str, output_path: str) -> None:
    cleaned_dialogues = []
    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        # Remove non-dialogue lines (e.g., scene descriptions)
        if not re.match(r"\[.*?\]", line) and ":" in line:
            # Split by ':' to separate character name from dialogue
            character, dialogue = line.split(":", 1)
            dialogue = re.sub(r"\.\.\.", "", dialogue).strip()
            dialogue = re.sub(r"[()]", "", dialogue)

            # Check if the dialogue contains more than one word
            if len(dialogue.split()) > 1:
                cleaned_dialogues.append(dialogue)

    with open(output_path, "w") as output_file:
        for dialogue in cleaned_dialogues:
            output_file.write(dialogue + "\n")
