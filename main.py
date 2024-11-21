import dearpygui.dearpygui as dpg
import os
import re
from typing import *
from threading import Thread
import json

from application.services import *
from adapters import *
from application.models import *
from settings import *

WIDTH = 1280
HEIGHT = 800

SETTINGS_FILE = "settings.json"

is_processing = False


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {
        "phrases_file": "",
        "audio_folder": "",
        "similarity_factor": EXPECTED_SIMILARITY_FACTOR,
        "max_fail_times": MAX_FAIL_TIMES,
        "mode_selector": "text",
    }


def save_settings(settings):
    with open(SETTINGS_FILE, "w+") as file:
        json.dump(settings, file, indent=4)


def apply_settings(settings):
    dpg.set_value("phrases_file", settings["phrases_file"])
    dpg.set_value("audio_folder", settings["audio_folder"])
    dpg.set_value("similarity_factor", settings["similarity_factor"])
    dpg.set_value("max_fail_times", settings["max_fail_times"])
    dpg.set_value("mode_selector", settings["mode_selector"])


def on_input_change(sender, app_data):
    current_settings = {
        "phrases_file": dpg.get_value("phrases_file"),
        "audio_folder": dpg.get_value("audio_folder"),
        "similarity_factor": dpg.get_value("similarity_factor"),
        "max_fail_times": dpg.get_value("max_fail_times"),
        "mode_selector": dpg.get_value("mode_selector"),
    }
    save_settings(current_settings)


# Function to stop the process
def stop_process_callback():
    global is_processing
    is_processing = False
    update_logs("Process stopped.")


def natural_key(filename):
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r"(\d+)", filename)
    ]


def process_audio_filenames(
    audio_filenames: List[str],
    phrase_service: PhraseService,
    audio_service: AudioService,
    transcription_service: TranscriptionService,
    similarity_factor: float,
    max_fail_times: int,
) -> None:
    global is_processing
    global_index, file_index = phrase_service.get_indexes()
    last_index = global_index + len(audio_filenames)

    for _ in range(global_index, last_index):
        if not is_processing:
            break

        _, file_index = phrase_service.get_indexes()
        audio_filename = audio_filenames[file_index]

        print(
            f"\n{COLOR_YELLOW}{file_index}: Processing {audio_filename}{COLOR_RESET}\n"
        )
        update_phrase(f"{file_index}: Processing {audio_filename}")
        update_logs(f"{file_index}: Processing {audio_filename}")
        native_audio_filename = os.path.join(AUDIO_FOLDER, audio_filename)

        native_text = transcription_service.transcribe(native_audio_filename)

        process_student_audio(
            native_text,
            native_audio_filename,
            phrase_service,
            transcription_service,
            audio_service,
            global_index,
            similarity_factor,
            max_fail_times,
        )

        phrase_service.increment_indexes()


def process_phrases_from_file(
    phrases: List[str],
    phrase_service: PhraseService,
    audio_service: AudioService,
    transcription_service: TranscriptionService,
    speech_synthesis_service: SpeechSynthesisService,
    similarity_factor: float,
    max_fail_times: int,
):
    global is_processing
    global_index, phrase_index = phrase_service.get_indexes()
    last_index = global_index + len(phrases)

    for _ in range(global_index, last_index):
        if not is_processing:
            break

        _, phrase_index = phrase_service.get_indexes()
        phrase = phrases[phrase_index]
        print(f"\n{COLOR_YELLOW}{phrase_index + 1}: {phrase}{COLOR_RESET}\n")
        update_phrase(f"{phrase_index + 1}: {phrase}")
        update_logs(f"{phrase_index + 1}: {phrase}")
        speech_synthesis_service.execute(phrase, output_filename=NATIVE_PRONOUNCE_FILE)
        native_text = transcription_service.transcribe(NATIVE_PRONOUNCE_FILE)

        process_student_audio(
            native_text,
            NATIVE_PRONOUNCE_FILE,
            phrase_service,
            transcription_service,
            audio_service,
            global_index,
            similarity_factor,
            max_fail_times,
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
    similarity_factor: float,
    max_fail_times: int,
    phrase: str = "",
):
    global is_processing
    fail_times = 0

    while is_processing:
        audio_service.load_and_play(native_audio_filename)
        print(
            f"{COLOR_BLUE}[native]{COLOR_RESET} {COLOR_GREEN}{native_text}{COLOR_RESET}"
        )
        # update_phrase(native_text)
        update_logs(f"[native] {native_text}")
        dpg.set_item_label("similarity", "")
        audio_service.record_student_pronunciation(
            native_audio_filename, STUDENT_PRONOUNCE_FILE
        )
        student_text = transcription_service.transcribe(STUDENT_PRONOUNCE_FILE)

        phoneme_similarity = transcription_service.calculate_phoneme_similarity(
            native_text, student_text
        )
        print(f"{COLOR_BLUE}[similarity]{COLOR_RESET} {phoneme_similarity:.2f}%")
        dpg.set_item_label("similarity", f"Similarity: {phoneme_similarity:.2f}%")
        update_logs(f"[similarity] {phoneme_similarity:.2f}%")

        new_audio_entry = PhraseModel(
            phoneme_similarity,
            native_text,
            student_text,
            phrase,
            global_index,
        )
        phrase_service.save(new_audio_entry)

        if phoneme_similarity <= similarity_factor:
            fail_times = 0
            break
        else:
            fail_times = fail_times + 1
            if fail_times == max_fail_times:
                break


# Globals for services
services = {}


def initialize_services(db_file):
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

    return {
        "database_service": database_service,
        "phrase_service": phrase_service,
        "audio_service": audio_service,
        "transcription_service": transcription_service,
        "speech_synthesis_service": speech_synthesis_service,
    }


def start_process_callback():
    global is_processing
    mode = dpg.get_value("mode_selector")
    similarity_factor = float(dpg.get_value("similarity_factor"))
    max_fail_times = int(dpg.get_value("max_fail_times"))
    db_file = TEXT_DB_FILE if mode == "text" else AUDIO_DB_FILE

    global services
    services = initialize_services(db_file)

    phrase_service = services["phrase_service"]
    audio_service = services["audio_service"]
    transcription_service = services["transcription_service"]
    speech_synthesis_service = services["speech_synthesis_service"]

    try:
        if mode == "audio":
            audio_folder = dpg.get_value("audio_folder")
            if not audio_folder or not os.path.isdir(audio_folder):
                dpg.set_value("phrase", "Error: Please select a valid audio folder.")
                is_processing = False
                return

            audio_filenames = sorted(
                [f for f in os.listdir(audio_folder) if f.endswith(".wav")],
                key=natural_key,
            )

            process_audio_filenames(
                audio_filenames,
                phrase_service,
                audio_service,
                transcription_service,
                similarity_factor,
                max_fail_times,
            )
            update_logs("Audio processing completed successfully.")
        else:
            phrases_file = dpg.get_value("phrases_file")
            if not phrases_file or not os.path.exists(phrases_file):
                dpg.set_value("phrase", "Error: Please select a valid phrases file.")
                is_processing = False
                return

            phrases = phrase_service.load_phrases_from_file(phrases_file)
            process_phrases_from_file(
                phrases,
                phrase_service,
                audio_service,
                transcription_service,
                speech_synthesis_service,
                similarity_factor,
                max_fail_times,
            )
            update_logs("Text processing completed successfully.")

    finally:
        services["database_service"].close()
        is_processing = False


def start_process_callback_in_thread():
    global is_processing
    is_processing = True

    processing_thread = Thread(target=start_process_callback)
    processing_thread.start()


def file_picker_callback(sender, app_data, user_data):
    dpg.set_value(user_data, app_data["file_path_name"])


def folder_picker_callback(sender, app_data, user_data):
    dpg.set_value(user_data, app_data["file_path_name"])


# def update_phrase(message: str, log_type: str = "default"):
#     # Set the text color based on log type
#     if log_type == "error":
#         color = (255, 0, 0)  # Red
#     elif log_type == "success":
#         color = (0, 255, 0)  # Green
#     elif log_type == "info":
#         color = (255, 255, 0)  # Yellow
#     else:
#         color = (255, 255, 255)  # Default (White)

#     dpg.set_item_label("phrase", message)
#     dpg.set_item_user_data("phrase", color)


def update_phrase(message: str, log_type: str = "default"):
    # Set the text color based on log type
    if log_type == "error":
        color = (255, 0, 0)  # Red
    elif log_type == "success":
        color = (0, 255, 0)  # Green
    elif log_type == "info":
        color = (255, 255, 0)  # Yellow
    else:
        color = (255, 255, 255)  # Default (White)

    dpg.set_value("phrase", message)


def update_logs(message: str):
    existing_logs = dpg.get_value("logs")  # Get current logs
    updated_logs = f"{existing_logs}\n{message}" if existing_logs else message
    dpg.set_value("logs", updated_logs)


def setup_gui():
    with dpg.handler_registry():
        # Use the key code for Escape (27)
        dpg.add_key_press_handler(key=27, callback=lambda: dpg.stop_dearpygui())

    with dpg.font_registry():
        small_font = dpg.add_font(
            "gui/fonts/Fira_Code_v6.2/ttf/FiraCode-Regular.ttf", 14
        )
        normal_font = dpg.add_font(
            "gui/fonts/Fira_Code_v6.2/ttf/FiraCode-Regular.ttf", 18
        )
        big_font = dpg.add_font("gui/fonts/Fira_Code_v6.2/ttf/FiraCode-Bold.ttf", 20)
        larger_font = dpg.add_font("gui/fonts/Fira_Code_v6.2/ttf/FiraCode-Bold.ttf", 28)

    with dpg.window(tag="Primary Window"):
        dpg.bind_font(normal_font)

        # Create a horizontal group to hold both widgets side by side
        main_group = dpg.group(horizontal=True, tag="main_group")
        with main_group:

            # Setup Widget (on the left)
            with dpg.child_window(
                width=WIDTH // 3 - 20, height=-1, border=True, tag="setup_widget"
            ):
                mode_selection_text = dpg.add_text("Mode Selection")
                dpg.bind_item_font(mode_selection_text, big_font)
                dpg.add_radio_button(
                    items=["text", "audio"],
                    default_value="text",
                    tag="mode_selector",
                    callback=lambda sender, app_data, user_data: (
                        on_input_change(sender, app_data),
                        update_visibility(sender, app_data, user_data),
                    ),
                )
                dpg.add_separator()

                # File Browsing
                file_browsing_text = dpg.add_text("File Browsing")
                dpg.bind_item_font(file_browsing_text, big_font)

                with dpg.group(tag="text_mode_group"):
                    dpg.add_text("Phrases File (Text Mode):")
                    dpg.add_input_text(
                        tag="phrases_file",
                        callback=on_input_change,
                        hint="Enter file path or use Select button",
                    )
                    dpg.add_button(
                        label="Select File",
                        callback=lambda: dpg.show_item("file_dialog"),
                    )

                with dpg.group(tag="audio_mode_group", show=False):
                    dpg.add_text("Audio Folder (Audio Mode):")
                    dpg.add_input_text(
                        tag="audio_folder",
                        callback=on_input_change,
                        hint="Enter folder path or use Select button",
                    )
                    dpg.add_button(
                        label="Select Folder",
                        callback=lambda: dpg.show_item("folder_dialog"),
                    )

                dpg.add_separator()

                # Settings Management
                settings_text = dpg.add_text("Settings")
                dpg.bind_item_font(settings_text, big_font)
                similarity_factor_text = dpg.add_input_float(
                    label="Similarity Factor",
                    default_value=EXPECTED_SIMILARITY_FACTOR,
                    callback=on_input_change,
                    tag="similarity_factor",
                )
                dpg.bind_item_font(similarity_factor_text, small_font)
                max_fail_times = dpg.add_input_int(
                    label="Max Fail Times",
                    default_value=MAX_FAIL_TIMES,
                    callback=on_input_change,
                    tag="max_fail_times",
                )
                dpg.bind_item_font(max_fail_times, small_font)
                dpg.add_separator()

                # Start Process Button
                dpg.add_button(
                    label="Start Process",
                    callback=start_process_callback_in_thread,
                )

                # Stop Process Button
                dpg.add_button(
                    label="Stop Process",
                    callback=stop_process_callback,
                )

            # Processing Widget (on the right)
            with dpg.child_window(
                width=WIDTH // 3 * 2 - 10,
                height=-1,
                border=True,
                tag="processing_widget",
            ):
                phrase_title_text = dpg.add_text("Phrase")
                dpg.bind_item_font(phrase_title_text, big_font)
                with dpg.group(tag="phrase_group", horizontal=False):
                    phrase_text = dpg.add_text(
                        "",
                        tag="phrase",
                        color=(255, 255, 255),
                        show=True,
                        wrap=WIDTH // 3 * 2 - 20,
                    )
                    dpg.bind_item_font(phrase_text, larger_font)

                    similarity_text = dpg.add_button(
                        label="",
                        tag="similarity",
                        show=True,
                        enabled=False,
                        width=-1,
                    )
                    dpg.bind_item_font(similarity_text, big_font)

                logs_text = dpg.add_text("Logs")
                dpg.bind_item_font(logs_text, big_font)
                with dpg.group(
                    tag="log_output_group", horizontal=True, width=-1, height=-1
                ):
                    logs_text = dpg.add_text(
                        "",
                        tag="logs",
                        color=(255, 255, 255),
                        show=True,
                        wrap=WIDTH // 3 * 2 - 20,
                    )
                    dpg.bind_item_font(logs_text, small_font)

        # File Dialogs
        with dpg.file_dialog(
            directory_selector=False,
            show=False,
            callback=file_picker_callback,
            user_data="phrases_file",
            tag="file_dialog",
        ):
            dpg.add_file_extension(".txt")

        with dpg.file_dialog(
            directory_selector=True,
            show=False,
            callback=folder_picker_callback,
            user_data="audio_folder",
            tag="folder_dialog",
        ):
            dpg.add_file_extension(".*")


def update_visibility(sender, app_data, user_data):
    selected_mode = dpg.get_value("mode_selector")
    if selected_mode == "text":
        dpg.show_item("text_mode_group")
        dpg.hide_item("audio_mode_group")
    else:
        dpg.show_item("audio_mode_group")
        dpg.hide_item("text_mode_group")


def main():
    dpg.create_context()
    dpg.create_viewport(title="mimicking", width=WIDTH, height=HEIGHT)
    dpg.setup_dearpygui()
    # dpg.maximize_viewport()
    dpg.show_viewport()
    setup_gui()
    settings = load_settings()
    apply_settings(settings)
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
