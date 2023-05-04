# Voice Recognition Computer
A simple voice-controlled computer program that allows you to control your computer using your voice. You can open applications, switch between windows, browse the web, and more, all with voice commands.

## Getting started
1. Install the required Python packages: `pip install speechrecognition pyautogui pytesseract pillow screeninfo textdistance pyttsx3 fuzzywuzzy python-Levenshtein pywin32`
2. If you're using Windows, also run `conda install pywin32`
3. Download and install the Tesseract OCR executable from [here](https://github.com/UB-Mannheim/tesseract/wiki) and set the Tesseract OCR executable path in the script.
4. Set up an OpenAI API key [here](https://beta.openai.com/signup/) and set the `api_key` variable in the script.
5. Run the script!

## Usage
The program listens for voice commands and responds accordingly. Some example commands are:

### Voice Commands
- `locate [word]`: locates the position of a word on the screen.
- `click there`: performs a left-click action on the current position of the mouse.
- `full screen`: presses the "F" key to toggle full screen mode.
- `exit fullscreen`: presses the "Esc" key to exit full screen mode.
- `next video`: presses the "Shift" and "N" keys to go to the next video.
- `previous video`: presses the "J" key to go to the previous video.
- `pause`: presses the "K" key to pause the current video.
- `play`: presses the "K" key to resume the current video.
- `mute`: presses the "M" key to mute the audio.
- `unmute`: presses the "M" key to unmute the audio.
- `new tab`: presses the "Ctrl" and "T" keys to open a new tab.
- `close tab`: presses the "Ctrl" and "W" keys to close the current tab.
- `scroll down [n]`: scrolls down by n pixels (default is 1).
- `scroll up [n]`: scrolls up by n pixels (default is 1).
- `zoom in`: presses the "Ctrl" and "+" keys to zoom in.
- `zoom out`: presses the "Ctrl" and "-" keys to zoom out.
- `open run`: presses the "Win" and "R" keys to open the Run dialog box.
- `copy`: presses the "Ctrl" and "C" keys to copy selected text.
- `paste`: presses the "Ctrl" and "V" keys to paste copied text.
- `select all`: presses the "Ctrl" and "A" keys to select all text.
- `type string [text]`: types the specified text on the screen.
- `search`: presses the "Enter" key to perform a search.
- `tab`: presses the "Tab" key to switch to the next field.
- `backspace`: presses the "Backspace" key to delete the previous character.
- `space`: presses the "Space" key to insert a space.
- `alt tab`: presses the "Alt" and "Tab" keys to switch to the next window.
- `maximise`: maximizes the current window.
- `minimise`: minimizes the current window.
- `switch tab next`: presses the "Ctrl" and "Tab" keys to switch to the next tab.
- `switch tab previous`: presses the "Ctrl", "Shift", and "Tab" keys to switch to the previous tab.


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
