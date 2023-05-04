import itertools
import math
import os
import re
import subprocess
import time

from concurrent.futures import ThreadPoolExecutor
from fuzzywuzzy import fuzz
import openai
import psutil
import pyaudio
import pytesseract
import pyttsx3
import speech_recognition as sr
import textdistance
import wave
import winsound
import win32api
import win32con
import win32gui
import win32process

from PIL import Image
from pytesseract import Output
import pyautogui

# pip install speechrecognition pyautogui pytesseract pillow screeninfo textdistance pyttsx3 fuzzywuzzy python-Levenshtein pywin32
# conda install pywin32

# Set the Tesseract OCR executable path (optional if already in PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Start the speech recognition engine
r = sr.Recognizer()

# Set the Levenshtein distance threshold
levenshtein_threshold = 2

developer_mode = False
api_key = "API_KEY_HERE"
os.system('title Voice Recognition Computer')
lang = 'en'
said = ""
guy = ""
openai.api_key = api_key
stop_flag = False

def get_audio(said):
    try:
        winsound.PlaySound("fetching.wav", winsound.SND_ASYNC)
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": said}])
    except openai.OpenAIError as e:
        print("OpenAI error: {0}".format(e))
        return

    # Remove any non-alphanumeric characters from the text
    text = re.sub(r'[^\w\s]', '', completion.choices[0].message.content)
    
    # Use os.system to generate TTS audio and save it as an MP3 file
    os.system(f'tts --text "{text}" --model_name tts_models/en/ljspeech/vits--neon > {"nul" if os.name == "nt" else "/dev/null"} 2>&1')
    
    # Play the saved MP3 file using winsound
    winsound.PlaySound("tts_output.wav", winsound.SND_ASYNC)
    
    # Get the duration of the audio file
    with wave.open("tts_output.wav", "rb") as wave_file:
        audio_duration = wave_file.getnframes() / wave_file.getframerate()
    
    # Wait for the audio to finish playing
    time.sleep(audio_duration)

def find_text_on_screen(text, screenshot):
    ocr_data = pytesseract.image_to_data(screenshot, output_type=Output.DICT)
    locations = []

    for i, word in enumerate(ocr_data['text']):
        if textdistance.levenshtein.distance(text.lower(), word.lower()) <= levenshtein_threshold:
            x = ocr_data['left'][i] + ocr_data['width'][i] // 2
            y = ocr_data['top'][i] + ocr_data['height'][i] // 2
            locations.append((x, y))
    
    return locations

def capture_screenshot(monitor):
    return pyautogui.screenshot(region=(monitor.x, monitor.y, monitor.width, monitor.height))

def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def find_min_distance_combination(locations_list):
    min_distance = float('inf')
    min_combination = None

    for combination in itertools.product(*locations_list):
        distance_sum = sum(distance(combination[i], combination[i + 1]) for i in range(len(combination) - 1))

        if distance_sum < min_distance:
            min_distance = distance_sum
            min_combination = combination

    return min_combination

def process_monitor(monitor, keywords):
    screenshot = capture_screenshot(monitor)
    locations_list = []
    for keyword in keywords:
        variations = keyword_variations.get(keyword.lower(), [keyword])
        locations = []
        for variation in variations:
            locations.extend(find_text_on_screen(variation, screenshot))
        locations_list.append(locations)
    if any(not locations for locations in locations_list):
        return None
    min_combination = find_min_distance_combination(locations_list)
    if min_combination:
        x, y = min_combination[0]
        pyautogui.moveTo(x + monitor.x, y + monitor.y)
        return True
    return None

def switch_to_window(window_name):
    windows = []
    win32gui.EnumWindows(lambda hwnd, windows: windows.append(hwnd), windows)
    matching_window = None
    closest_match = float('inf')
    for window in windows:
        if win32gui.IsWindowVisible(window):
            process_name = get_process_name_by_window(window)
            window_title = win32gui.GetWindowText(window)
            for name in (process_name, window_title):
                if name is not None:
                    match = re.search(window_name, name, re.IGNORECASE)
                    if match is not None and match.start() < closest_match:
                        matching_window = window
                        closest_match = match.start()

    if matching_window is not None:
        win32gui.ShowWindow(matching_window, win32con.SW_RESTORE)
        win32gui.SetWindowPos(matching_window, win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetForegroundWindow(matching_window)
        print(f"Switched to window '{window_name}'")
    else:
        print(f"No window found with name '{window_name}'")

def get_process_name_by_window(hwnd):
    process_id = win32process.GetWindowThreadProcessId(hwnd)[0]
    try:
        process = psutil.Process(process_id)
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None

def maximize_current_window():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    win32api.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)

def minimize_current_window():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    win32api.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MINIMIZE, 0)

def process_command(command):
    for pattern, action in COMMANDS.items():
        if re.search(pattern, command, re.IGNORECASE):
            action["action"]()
            if "message" in action:
                print(action["message"])
            break
    else:
        print("Sorry, I didn't understand that command.")

def listen_for_command():
    with sr.Microphone() as source:
        print("Speak a command:")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
    except sr.UnknownValueError:
        print("Sorry, I could not understand your command.")
        return None
    return command

def open_domain(domain):
    pyautogui.keyDown('ctrl')
    pyautogui.press('t')
    pyautogui.keyUp('ctrl')
    pyautogui.typewrite(domain)
    pyautogui.press('enter')
    print(f"Opened {domain} in a new tab.")
    
def ping_domain(domain):
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    pyautogui.typewrite("cmd")
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.typewrite(f"ping {domain}")
    pyautogui.press("enter")
    print(f"Pinged {domain} in a new terminal.")

def open_command_prompt(commandprompt='cmd.exe'):
    pyautogui.keyDown('win')
    pyautogui.press('r')
    pyautogui.keyUp('win')
    pyautogui.typewrite(commandprompt)
    pyautogui.press('enter')
    print(f"Opened Command Prompt")


def locate_words(words):
    keywords = words.split()
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda monitor: process_monitor(monitor, keywords), get_monitors()))
    if any(results):
        print(f"Located the words: {keywords}")
    else:
        print(f"Could not locate the words: {keywords}")

keyword_variations = {
}

def switch_tab_number(tab_number):
    pyautogui.keyDown('ctrl')
    pyautogui.press(str(tab_number))
    pyautogui.keyUp('ctrl')


def extract_arguments(text, keyword):
    pattern = command_patterns.get(keyword)
    if not pattern:
        return None
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return ()
    arguments = match.groups()
    return arguments

command_actions = {
    "locate": locate_words,
    "click there": lambda *args: pyautogui.click() if not args else None,
    "full screen": lambda *args: pyautogui.press('f'),
    "exit fullscreen": lambda: pyautogui.press('esc'),
    "next video": lambda: pyautogui.hotkey('shift', 'n'),
    "previous video": lambda: pyautogui.press('j'),
    "pause": lambda: pyautogui.press('k'),
    "play": lambda: pyautogui.press('k'),
    "mute": lambda: pyautogui.press('m'),
    "unmute": lambda: pyautogui.press('m'),
    "new tab": lambda: pyautogui.hotkey('ctrl', 't'),
    "close tab": lambda: pyautogui.hotkey('ctrl', 'w'),
    "scroll down": lambda n=1: pyautogui.scroll(-int(n)),
    "scroll up": lambda n=1: pyautogui.scroll(int(n)),
    "zoom in": lambda: pyautogui.hotkey('ctrl', '+'),
    "zoom out": lambda: pyautogui.hotkey('ctrl', '-'),
    "open run": lambda: pyautogui.hotkey('win', 'r'),
    "copy": lambda: pyautogui.hotkey('ctrl', 'c'),
    "paste": lambda: pyautogui.hotkey('ctrl', 'v'),
    "select all": lambda: pyautogui.hotkey('ctrl', 'a'),
    "type string": lambda *args: pyautogui.typewrite(*args),
    "search": lambda: pyautogui.press('enter'),
    "tab": lambda: pyautogui.press('tab'),
    "backspace": lambda: pyautogui.press('backspace'),
    "space": lambda: pyautogui.press('space'),
    "alt tab": lambda: pyautogui.hotkey('alt', 'tab'),
    "maximise": lambda: maximize_current_window(),
    "minimise": lambda: minimize_current_window(),
    "switch tab next": lambda: pyautogui.hotkey('ctrl', 'tab'),
    "switch tab previous": lambda: pyautogui.hotkey('ctrl', 'shift', 'tab'),
    "switch to": lambda window_name: switch_to_window(window_name),
    "open": open_domain,
    "switch tab": switch_tab_number,
    "refresh page": lambda: pyautogui.hotkey('ctrl', 'r'),
    "cut": lambda: pyautogui.hotkey('ctrl', 'x'),
    "open file explorer": lambda: pyautogui.hotkey('win', 'e'),
    "create new folder": lambda: pyautogui.hotkey('ctrl', 'shift', 'n'),
    "undo": lambda: pyautogui.hotkey('ctrl', 'z'),
    "redo": lambda: pyautogui.hotkey('ctrl', 'y'),
    "save": lambda: pyautogui.hotkey('ctrl', 's'),
    "save as": lambda: pyautogui.hotkey('ctrl', 'shift', 's'),
    "double click": lambda: pyautogui.doubleClick(),
    "open command prompt": open_command_prompt,
    "send text": lambda: pyautogui.press('enter'),
    "stop command": lambda: pyautogui.hotkey('ctrl', 'c'),
    "developer mode on": lambda: set_developer_mode(True),
    "developer mode off": lambda: set_developer_mode(False),
    "ping": ping_domain,
    "ask ai": get_audio,
}

def set_developer_mode(mode):
    global developer_mode
    developer_mode = mode
    print(f"Developer mode {'on' if mode else 'off'}")

command_patterns = {
    "locate": r"locate (.*)",
    "switch to": r"switch to (.*)",
    "click there": r"(?:click|pick|select)(?: (?:there|that|it))?",
    "full screen": r"full(-|\s)?screen",
    "exit fullscreen": r"exit full(?:-|\s)screen",
    "next video": r"next video",
    "previous video": r"previous video",
    "pause": r"(?:pause|paws)",
    "play": r"play",
    "mute": r"mute",
    "unmute": r"unmute",
    "new tab": r"new tab",
    "close tab": r"close tab",
    "scroll down": r"scroll down(?: by)? (\d+)?",
    "scroll up": r"scroll up(?: by)? (\d+)?",
    "zoom in": r"zoom in",
    "zoom out": r"zoom out",
    "open run": r"open run",
    "copy": r"copy",
    "paste": r"paste",
    "select all": r"select all",
    "type string": r"type string (.*)",
    "search": r"search",
    "tab": r"^tab$",
    "backspace": r"backspace",
    "space": r"space",
    "alt tab": r"alt tab",
    "maximise": r"maxim(?:i|ou?)se",
    "minimise": r"minim(?:i|ou?)se",
    "switch tab next": r"switch tab next",
    "switch tab previous": r"switch tab previous",
    "open": r"open\s+([a-z0-9]+(?:-[a-z0-9]+)*\.)+[a-z]{2,}",
    "switch tab": r"(?i)switch tab (\d)",
    "refresh page": r"refresh page|reload page|reload",
    "cut": r"cut|cut selected|cut that|delete that|delete selected",
    "open file explorer": r"open file explorer|open explorer|file explorer|explore files",
    "create new folder": r"create new folder|make a new folder|new folder",
    "undo": r"undo|undo that|undo last",
    "redo": r"redo|redo that|redo last",
    "save": r"save|save file|save changes",
    "save as": r"save as|save this file as|save file as",
    "double click": r"double click|double-click|doubleclick|2 clicks|two clicks",
    "open command prompt": r"open command prompt",
    "send text": r"send text",
    "stop command": r"stop command",
    "developer mode on": r"developer mode on",
    "developer mode off": r"developer mode off",
    "ping": r"ping\s+([a-zA-Z0-9]+\.[a-zA-Z]{2,})",
    "ask ai": r"ask ai (.*)"
}

# Loop until the program is stopped
while True:
    command = listen_for_command()
    if command is None:
        continue
    if developer_mode:
        for cmd, action in command_actions.items():
            if re.search(command_patterns[cmd], command, re.IGNORECASE):
                arguments = extract_arguments(command, cmd)
                print(f"cmd: {cmd}, command: {command}, arguments: {arguments}")
                action(*arguments) if arguments else action()
                break
        else:
            print(f"Sorry, I could not understand your command: {command}")
    else:
        # Developer mode is off
        if command.lower() == "developer mode on":
            set_developer_mode(True)
        else:
            print("Sorry, developer mode is currently off. Say 'Developer mode on' to enable it.") 
