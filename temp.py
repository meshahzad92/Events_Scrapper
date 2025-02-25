import win32clipboard
import time
from ctypes import windll, create_string_buffer

def get_clipboard_text():
    win32clipboard.OpenClipboard()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            data = win32clipboard.GetClipboardData()
            return data
    except Exception as e:
        print(f"Clipboard error: {e}")
    finally:
        win32clipboard.CloseClipboard()
    return None

def monitor_clipboard():
    last_text = ""
    while True:
        text = get_clipboard_text()
        if text and text != last_text:
            print(f"New copied text: {text}")  # Replace this with your processing function
            last_text = text
        time.sleep(0.1)  # Very fast but avoids CPU overuse

monitor_clipboard()
