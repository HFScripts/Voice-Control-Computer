# Voice Control Computer
A simple voice-controlled computer program that allows you to control your computer using your voice. You can open applications, switch between windows, browse the web, and more, all with voice commands.

## Basics
So for this project, you must use Anaconda/Conda for windows. The reason for this is library access and ease of use. There are a number of long winded reasons as to why it wont work with other setups, so just trust me - Use conda. 

## Installation

1. Download and install Anaconda: https://www.anaconda.com/
2. Setup the conda environment with python 3.9:
    ```
    conda create --name tts_control_system python=3.9
    conda activate tts_control_system
    ```
3. Download the github repository and enter it:
    ```
    git clone https://github.com/HFScripts/Voice-Control-Computer.git
    cd Voice-Control-Computer
    ```
4. Install the requirements for this project:
    ```
    pip install -r requirements.txt
    ```
5. Generate the initial audio file for testing:
    ```
    tts --text "Fetching that for you now" --model_name tts_models/en/ljspeech/vits--neon --out_path fetching.wav
    ```
6. Download Tesseract OCR for Windows: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe
7. Get your API key for ChatGPT: https://platform.openai.com/account/api-keys
8. Edit the \`start.py\` file with your API key on line 42.

## Usage
To run the script, enter the following command in your terminal:
```
python start.py
```

The program listens for voice commands and responds accordingly. Some example commands are:

### Voice Commands
- `locate [word]`: Locates the position of a word on the screen.
- `click there`: Clicks at the current mouse position or where the last locate command found a word.
- `full screen`: Presses the 'f' key to toggle full-screen mode.
- `exit fullscreen`: Presses the 'esc' key to exit full-screen mode.
- `next video`: Presses 'shift' + 'n' keys to move to the next video.
- `previous video`: Presses the 'j' key to go to the previous video.
- `pause`: Presses the 'k' key to pause the video.
- `play`: Presses the 'k' key to play the video.
- `mute`: Presses the 'm' key to mute the volume.
- `unmute`: Presses the 'm' key to unmute the volume.
- `new tab`: Presses 'ctrl' + 't' keys to open a new tab.
- `close tab`: Presses 'ctrl' + 'w' keys to close the current tab.
- `scroll down`: Scrolls down by a specified number (default is 1).
- `scroll up`: Scrolls up by a specified number (default is 1).
- `zoom in`: Presses 'ctrl' + '+' keys to zoom in.
- `zoom out`: Presses 'ctrl' + '-' keys to zoom out.
- `open run`: Presses 'win' + 'r' keys to open the Run dialog.
- `copy`: Presses 'ctrl' + 'c' keys to copy the selected content.
- `paste`: Presses 'ctrl' + 'v' keys to paste the copied content.
- `select all`: Presses 'ctrl' + 'a' keys to select all content.
- `type string [text]`: Types the specified text.
- `search`: Presses the 'enter' key to initiate a search.
- `tab`: Presses the 'tab' key to navigate between elements.
- `backspace`: Presses the 'backspace' key to delete a character.
- `space`: Presses the 'space' key to input a space character.
- `alt tab`: Presses 'alt' + 'tab' keys to switch between open windows.
- `maximise`: Maximizes the current window.
- `minimise`: Minimizes the current window.
- `switch tab next`: Presses 'ctrl' + 'tab' keys to switch to the next tab.
- `switch tab previous`: Presses 'ctrl' + 'shift' + 'tab' keys to switch to the previous tab.
- `switch to [window_name]`: Switches to the specified window.
- `open [domain]`: Opens the specified domain.
- `switch tab [number]`: Switches to the specified tab number.
- `refresh page`: Presses 'ctrl' + 'r' keys to refresh the current page.
- `cut`: Presses 'ctrl' + 'x' keys to cut the selected content.
- `open file explorer`: Presses 'win' + 'e' keys to open File Explorer.
- `create new folder`: Presses 'ctrl' + 'shift' + 'n' keys to create a new folder.
- `undo`: Presses 'ctrl' + 'z' keys to undo the last action.
- `redo`: Presses 'ctrl' + 'y' keys to redo the last undone action.
- `save`: Presses 'ctrl' + 's' keys to save the current file.
- `save as`: saves the current document with a new name by simulating the "Ctrl + Shift + S" hotkey.
- `double click`: performs a double-click action at the current mouse position.
- `open command prompt`: opens the command prompt (Windows) or terminal (Linux/Mac) on your system.
- `send text`: simulates pressing the "Enter" key, sending the text currently typed.
- `stop command`: stops the currently running command by simulating the "Ctrl + C" hotkey.
- `developer mode on`: enables the developer mode in the application.
- `developer mode off`: disables the developer mode in the application.
- `ping`: pings a specified domain to check network connectivity.
- `ask ai`: listens for user input through the microphone and processes it as an audio command.

Dependencies
Python 3.7 or later
speechrecognition
pyautogui
pytesseract
pillow
screeninfo
textdistance
pyttsx3
fuzzywuzzy
python-Levenshtein
pywin32
License
This project is licensed under the MIT License - see the LICENSE.md file for details.
