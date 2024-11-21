import os

ROOT_DIR = os.getcwd()

AUDIO_FOLDER = "audios"
PHRASES_FILE = "_phrases.txt"
NATIVE_PRONOUNCE_FILE = "_native_pronounce.wav"
STUDENT_PRONOUNCE_FILE = "_student_pronounce.wav"

TEXT_DB_FILE = "text.db"
AUDIO_DB_FILE = "audio.db"

COLOR_RESET = "\033[0m"
COLOR_RED = "\033[0;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_YELLOW = "\033[0;33m"
COLOR_BLUE = "\033[0;34m"
COLOR_CYAN = "\033[0;36m"

SAMPLING_RATE = 16000

EXPECTED_SIMILARITY_FACTOR = 60

MAX_FAIL_TIMES = 3
