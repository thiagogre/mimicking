import argparse
from typing import *
import os
import re

from application.services import *
from adapters import *
from application.models import *
from settings import *


def natural_key(filename):
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r"(\d+)", filename)
    ]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process mode for main application.")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["text", "audio"],
        required=True,
        help="Select mode: 'text' for text files or 'audio' for audio processing",
    )
    return parser.parse_args()


def process_audio_filenames(
    audio_filenames: List[str],
    phrase_service: PhraseService,
    audio_service: AudioService,
    transcription_service: TranscriptionService,
) -> None:
    global_index, file_index = phrase_service.get_indexes()
    last_index = global_index + len(audio_filenames)

    for _ in range(global_index, last_index):
        _, file_index = phrase_service.get_indexes()
        audio_filename = audio_filenames[file_index]
        print(
            f"\n{COLOR_YELLOW}{file_index}: Processing {audio_filename}{COLOR_RESET}\n"
        )

        native_audio_filename = os.path.join(AUDIO_FOLDER, audio_filename)

        native_text = transcription_service.transcribe(native_audio_filename)

        process_student_audio(
            native_text,
            native_audio_filename,
            phrase_service,
            transcription_service,
            audio_service,
            global_index,
        )

        phrase_service.increment_indexes()


def process_phrases_from_file(
    phrases: List[str],
    phrase_service: PhraseService,
    audio_service: AudioService,
    transcription_service: TranscriptionService,
    speech_synthesis_service: SpeechSynthesisService,
):
    global_index, phrase_index = phrase_service.get_indexes()
    last_index = global_index + len(phrases)

    for _ in range(global_index, last_index):
        _, phrase_index = phrase_service.get_indexes()
        phrase = phrases[phrase_index]
        print(f"\n{COLOR_YELLOW}{phrase_index + 1}: {phrase}{COLOR_RESET}\n")

        speech_synthesis_service.execute(phrase, output_filename=NATIVE_PRONOUNCE_FILE)
        native_text = transcription_service.transcribe(NATIVE_PRONOUNCE_FILE)

        process_student_audio(
            native_text,
            NATIVE_PRONOUNCE_FILE,
            phrase_service,
            transcription_service,
            audio_service,
            global_index,
            phrase=phrase,
        )

        phrase_service.increment_indexes()


def process_student_audio(
    native_text: str,
    native_audio_filename: str,
    phrase_service: PhraseService,
    transcription_service: TranscriptionService,
    audio_service: AudioService,
    global_index: int,
    phrase: str = "",
):
    fail = False
    fail_times = 0
    while True:
        if fail:
            print(
                f"{COLOR_BLUE}[native]{COLOR_RESET} {COLOR_GREEN}{native_text}{COLOR_RESET}"
            )

        audio_service.load_and_play(native_audio_filename)
        audio_service.record_student_pronunciation(
            native_audio_filename, STUDENT_PRONOUNCE_FILE
        )
        student_text = transcription_service.transcribe(STUDENT_PRONOUNCE_FILE)
        if student_text.lower() == "next":
            break

        phoneme_similarity = transcription_service.calculate_phoneme_similarity(
            native_text, student_text
        )
        print(f"{COLOR_BLUE}[similarity]{COLOR_RESET} {phoneme_similarity:.2f}%")

        phrase
        new_audio_entry = PhraseModel(
            phoneme_similarity,
            native_text,
            student_text,
            phrase,
            global_index,
        )
        phrase_service.save(new_audio_entry)

        if phoneme_similarity <= EXPECTED_SIMILARITY_FACTOR:
            fail = False
            fail_times = 0
            break
        else:
            fail_times = fail_times + 1
            if fail_times == MAX_FAIL_TIMES:
                break
            fail = True


def main(mode: Literal["text", "audio"]):
    db_file = TEXT_DB_FILE if mode == "text" else AUDIO_DB_FILE
    database_adapter = DatabaseAdapter(db_file)
    database_service = DatabaseService(database_port=database_adapter)
    database_service.init_db()

    phrase_service = PhraseService(database_service=database_service)
    audio_adapter = AudioAdapter(sampling_rate=SAMPLING_RATE)
    transcription_adapter = TranscriptionAdapter()
    phoneme_adapter = PhonemeAdapter()
    wer_adapter = WerAdapter()

    transcription_service = TranscriptionService(
        audio_port=audio_adapter,
        transcription_port=transcription_adapter,
        phoneme_port=phoneme_adapter,
        wer_port=wer_adapter,
    )

    audio_service = AudioService(audio_port=audio_adapter)
    speech_synthesis_adapter = SpeechSynthesisAdapter()
    speech_synthesis_service = SpeechSynthesisService(
        audio_port=audio_adapter, speech_synthesis_port=speech_synthesis_adapter
    )

    try:
        if mode == "audio":
            audio_filenames = sorted(
                [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".wav")],
                key=natural_key,
            )
            process_audio_filenames(
                audio_filenames, phrase_service, audio_service, transcription_service
            )
        else:
            phrases = phrase_service.load_phrases_from_file(PHRASES_FILE)
            process_phrases_from_file(
                phrases,
                phrase_service,
                audio_service,
                transcription_service,
                speech_synthesis_service,
            )
    finally:
        database_service.close()


if __name__ == "__main__":
    args = parse_arguments()
    main(args.mode)
