import itertools
import math
import os
import re
import subprocess
import time
from screeninfo import get_monitors

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

from pytesseract import Output
import pyautogui
import keyboard
import PySimpleGUI as sg
from PIL import ImageFont, ImageDraw, Image

code_words = {
    'a1': 'apple', 'b1': 'banana', 'c1': 'carrot', 'd1': 'donut', 'e1': 'elephant', 'f1': 'frog', 'g1': 'curtain', 'h1': 'hamburger', 'i1': 'igloo', 'j1': 'jacket', 'k1': 'kangaroo', 'l1': 'lamp', 'm1': 'mango', 'n1': 'nachos', 'o1': 'octopus', 'p1': 'piano',
    'a2': 'ice cream', 'b2': 'jelly', 'c2': 'car', 'd2': 'carpet', 'e2': 'eggplant', 'f2': 'shark', 'g2': 'pretzel', 'h2': 'hot dog', 'i2': 'iris', 'j2': 'jaguar', 'k2': 'kettle', 'l2': 'llama', 'm2': 'muffin', 'n2': 'notebook', 'o2': 'ostrich', 'p2': 'pumpkin',
    'a3': 'pear', 'b3': 'raspberry', 'c3': 'cat', 'd3': 'train', 'e3': 'emu', 'f3': 'fox', 'g3': 'grape', 'h3': 'red bull', 'i3': 'iceberg', 'j3': 'jeep', 'k3': 'koala', 'l3': 'lemon', 'm3': 'marshmallow', 'n3': 'newt', 'o3': 'owl', 'p3': 'popcorn',
    'a4': 'yellow', 'b4': 'zebra', 'c4': 'chicken', 'd4': 'duck', 'e4': 'eagle', 'f4': 'flower', 'g4': 'noodles', 'h4': 'honey', 'i4': 'island', 'j4': 'jam', 'k4': 'kite', 'l4': 'lobster', 'm4': 'mushroom', 'n4': 'nut', 'o4': 'ocean', 'p4': 'pineapple',
    'a5': 'grapefruit', 'b5': 'horse', 'c5': 'cactus', 'd5': 'dog', 'e5': 'kiwi', 'f5': 'fries', 'g5': 'wallet', 'h5': 'honeydew', 'i5': 'iguana', 'j5': 'jellyfish', 'k5': 'ketchup', 'l5': 'lighthouse', 'm5': 'moon', 'n5': 'nugget', 'o5': 'otter', 'p5': 'penguin',
    'a6': 'orange', 'b6': 'pineapple', 'c6': 'china', 'd6': 'donkey', 'e6': 'strawberry', 'f6': 'water', 'g6': 'tomato', 'h6': 'hazelnut', 'i6': 'inchworm', 'j6': 'jigsaw', 'k6': 'kiwi bird', 'l6': 'lizard', 'm6': 'mountain', 'n6': 'nest', 'o6': 'oyster', 'p6': 'plum',
    'a7': 'watermelon', 'b7': 'bird', 'c7': 'cake', 'd7': 'dolphin', 'e7': 'eggplant', 'f7': 'fish', 'g7': 'grilled cheese', 'h7': 'hot dog', 'i7': 'ice skate', 'j7': 'judo', 'k7': 'keyboard', 'l7': 'lily', 'm7': 'meteor', 'n7': 'nose', 'o7': 'opera', 'p7': 'polar bear',
    'a8': 'butter', 'b8': 'pancake', 'c8': 'cherry', 'd8': 'whale', 'e8': 'eclair', 'f8': 'rose', 'g8': 'juice', 'h8': 'hamburger', 'i8': 'iron', 'j8': 'jump rope', 'k8': 'kumquat', 'l8': 'lock', 'm8': 'mirror', 'n8': 'narwhal', 'o8': 'orchid', 'p8': 'parrot',
    'a9': 'quail', 'b9': 'queen', 'c9': 'quiche', 'd9': 'quinoa', 'e9': 'quokka', 'f9': 'quartz', 'g9': 'quesadilla', 'h9': 'quill', 'i9': 'quiver', 'j9': 'quicksand', 'k9': 'quadrant', 'l9': 'quail egg', 'm9': 'quince', 'n9': 'quinoa salad', 'o9': 'quadrilateral', 'p9': 'quadruplets',
    'a10': 'rabbit', 'b10': 'raccoon', 'c10': 'radio', 'd10': 'radish', 'e10': 'rainbow', 'f10': 'raisin', 'g10': 'rattle', 'h10': 'reindeer', 'i10': 'rhino', 'j10': 'ribbon', 'k10': 'rice', 'l10': 'rooster', 'm10': 'robot', 'n10': 'rocket', 'o10': 'ruler', 'p10': 'rattlesnake',
    'a11': 'squirrel', 'b11': 'starfish', 'c11': 'scarf', 'd11': 'scissors', 'e11': 'seagull', 'f11': 'seashell', 'g11': 'skyscraper', 'h11': 'sloth', 'i11': 'snail', 'j11': 'snake', 'k11': 'snowflake', 'l11': 'spider', 'm11': 'sunflower', 'n11': 'note', 'o11': 'octagon', 'p11': 'popsicle',
    'a12': 'tortoise', 'b12': 'tiger', 'c12': 'telescope', 'd12': 'teddy bear', 'e12': 'television', 'f12': 'taco', 'g12': 'tractor', 'h12': 'tulip', 'i12': 'turtle', 'j12': 'tornado', 'k12': 'tambourine', 'l12': 'toad', 'm12': 'mistletoe', 'n12': 'nest', 'o12': 'oatmeal', 'p12': 'pencil',
    'a13': 'umbrella', 'b13': 'unicorn', 'c13': 'unicycle', 'd13': 'ukulele', 'e13': 'uranium', 'f13': 'utensils', 'g13': 'uniform', 'h13': 'urchin', 'i13': 'upstairs', 'j13': 'underwear', 'k13': 'umpire', 'l13': 'ultrasound', 'm13': 'umbilical', 'n13': 'underpass', 'o13': 'uptown', 'p13': 'uplift',
    'a14': 'violin', 'b14': 'vampire', 'c14': 'vanilla', 'd14': 'vest', 'e14': 'vase', 'f14': 'volcano', 'g14': 'vortex', 'h14': 'vine', 'i14': 'vulture', 'j14': 'valley', 'k14': 'vodka', 'l14': 'violet', 'm14': 'vault', 'n14': 'vitamin', 'o14': 'viper', 'p14': 'vote',
    'a15': 'walrus', 'b15': 'wombat', 'c15': 'wagon', 'd15': 'whisk', 'e15': 'windmill', 'f15': 'waffle', 'g15': 'watch', 'h15': 'window', 'i15': 'wizard', 'j15': 'waterfall', 'k15': 'kettlebell', 'l15': 'lawnmower', 'm15': 'matchstick', 'n15': 'necktie', 'a16': 'otter', 'p15': 'paintbrush',
    'a16': 'xylophone', 'b16': 'xenon', 'c16': 'x-ray', 'd16': 'xerox', 'e16': 'xenophobia', 'f16': 'xeriscape', 'g16': 'xylem', 'h16': 'xenolith', 'i16': 'xenograft', 'j16': 'xanthan', 'k16': 'xerophyte', 'l16': 'xenocryst', 'm16': 'xiphoid', 'n16': 'xerosis', 'o16': 'xanthophyll', 'p16': 'xoloitzcuintli',
}
overlay_window = None
is_grid_displayed = False

def extract_arguments(command, cmd):
    return re.findall(command_patterns[cmd], command, re.IGNORECASE)

def screen_help():
    print("Screen help requested")
    is_grid_displayed = True
    overlay_window = create_overlay()
    while is_grid_displayed:
        event, values = overlay_window.read(timeout=100)
        if event == sg.WIN_CLOSED or keyboard.is_pressed('ctrl+alt') or recognize_speech() == "screen help":
            overlay_window.close()
            is_grid_displayed = False
        else:
            code_word = recognize_speech()
            if code_word:
                is_grid_displayed = move_mouse_to_grid(code_word, is_grid_displayed)
                if not is_grid_displayed:
                    overlay_window.close()
                        
def create_overlay():
    screen_size = (1920, 1080)  # Set your screen resolution here
    grid_size = (16, 16)
    cell_width, cell_height = screen_size[0] // grid_size[0], screen_size[1] // grid_size[1]

    layout = [[sg.Graph(screen_size, (0, 0), screen_size, key='-GRAPH-', enable_events=True, background_color=None)]]
    window = sg.Window('Overlay', layout, no_titlebar=True, location=(0, 0), keep_on_top=True, alpha_channel=0.5, finalize=True)
    graph = window['-GRAPH-']

    for i in range(1, grid_size[0]):
        graph.draw_line((i * cell_width, 0), (i * cell_width, screen_size[1]), width=1, color='black')
    
    for i in range(1, grid_size[1]):
        graph.draw_line((0, i * cell_height), (screen_size[0], i * cell_height), width=1, color='black')
    
    font = ImageFont.truetype("arial.ttf", 12)
    img = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(img)

    for row in reversed(range(grid_size[0])):
        for col in range(grid_size[1]):
            grid_id = f"{chr(row + ord('a'))}{col + 1}"
            label = code_words.get(grid_id)
            if label is None:
                label = grid_id
            bbox = draw.textbbox((0, 0), label, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x_pos = col * cell_width + (cell_width - text_width) // 2
            y_pos = (grid_size[0] - row - 1) * cell_height + (cell_height - text_height) // 2
            graph.draw_text(label, (x_pos, y_pos), font=("Helvetica", 12), color='black')
    
    return window

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        recognized_text = r.recognize_google(audio).lower()
        # Check if recognized text matches any code word
        for grid_id, code_word in code_words.items():
            if code_word in recognized_text:
                return code_word
        if recognized_text == "screen help":
            return "screen help"
        # If recognized text does not match any code word, print it out
        print("You said: " + recognized_text)
    except sr.UnknownValueError:
        print("Unable to understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    return ""


def move_mouse_to_grid(code_word, is_grid_displayed):
    grid_id = None
    for id, word in code_words.items():
        if word == code_word:
            grid_id = id
            break
    
    if grid_id is None:
        print(f"Invalid code word: {code_word}")
        return is_grid_displayed

    screen_size = (1920, 1080)  # Set your screen resolution here
    grid_size = (16, 16)
    cell_width, cell_height = screen_size[0] // grid_size[0], screen_size[1] // grid_size[1]

    row, col = ord(grid_id[0].lower()) - ord('a'), int(grid_id[1]) - 1
    x, y = col * cell_width + cell_width // 2, row * cell_height + cell_height // 2
    pyautogui.moveTo(x + 5, y + 5) # adjust the mouse alignment by adding 5 pixels to both x and y coordinates
    print(f"Mouse moved to grid: {code_word.upper()} ({grid_id.upper()})")

    return False

# pip install speechrecognition pyautogui pytesseract pillow screeninfo textdistance pyttsx3 fuzzywuzzy python-Levenshtein pywin32
# conda install pywin32

# Set the Tesseract OCR executable path (optional if already in PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Start the speech recognition engine
r = sr.Recognizer()

# Set the Levenshtein distance threshold
levenshtein_threshold = 2

developer_mode = False
api_key = "sk-APIKEY"
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
    pyautogui.keyDown('win')
    pyautogui.press('r')
    pyautogui.keyUp('win')
    pyautogui.typewrite("https://")
    pyautogui.typewrite(domain)
    pyautogui.press('enter')
    print(f"Opened Command Prompt")
    
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
    "screen help": screen_help,
}

def set_developer_mode(mode):
    global developer_mode
    developer_mode = mode
    print(f"Developer mode {'on' if mode else 'off'}")

command_patterns = {
    "locate": r"locate (.*)",
    "switch to": r"switch to (.*)",
    "click there": r"(?:click|pick|put)(?: (?:there|that|it))?",
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
    "open": r"open\s+([a-zA-Z0-9]+\.[a-zA-Z]{2,})",
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
    "ask ai": r"ask ai (.*)",
    "screen help": r"(?:scream|stream|.*\b)screen help",
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
