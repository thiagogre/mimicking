import re
import string


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

            # Remove punctuation
            dialogue = dialogue.translate(str.maketrans("", "", string.punctuation))

            # Remove special characters (e.g., emoticons and other symbols)
            dialogue = re.sub(r"[^\w\s]", "", dialogue)

            # Check if the dialogue contains more than one word
            if len(dialogue.split()) > 1:
                words = dialogue.split()
                # Break dialogue into lines of up to 10 words
                for i in range(0, len(words), 10):
                    cleaned_dialogues.append(" ".join(words[i : i + 10]))

    with open(output_path, "w") as output_file:
        for dialogue in cleaned_dialogues:
            output_file.write(dialogue + "\n")


def remove_empty_lines(file_path: str, output_path: str) -> None:
    cleaned_lines = []
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Filter out empty lines
    for line in lines:
        if line.strip():  # Only keep non-empty lines
            cleaned_lines.append(line)

    with open(output_path, "w") as output_file:
        output_file.writelines(cleaned_lines)


# clean_transcript("texts/TwitterConvCorpus.txt", "_phrases.txt")
remove_empty_lines("texts/reddit_phrases.txt", "_phrases.txt")
