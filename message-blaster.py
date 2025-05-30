import pyautogui
import pandas
import time
import time
import pyperclip
import random
import webbrowser

pyautogui.FAILSAFE = False
MESSAGE = "Hello!"
def open_deeplink(url):
    """
    Opens a URL/Deeplink in the default web browser or associated application.
    """
    print(f"Attempting to open Deeplink: {url}")
    try:
        webbrowser.open(url)
        print("Deeplink opened successfully. Please check your browser or Telegram app.")
    except Exception as e:
        print(f"Failed to open Deeplink: {e}")

def send_message_with_lag(message_content, message_number):
   """
   Simulates sending a message with realistic, random delays.

   Args:
      message_content (str): The content of the message to "send".
      message_number (int): The sequence number of the message being sent.
   """
   if message_content is not None and message_content == message_content:
      # Print the message number and content to the console for tracking.
      print(f"--- Sending Message {message_number} ---")
      # Simulate human "thinking" or "typing" time before the message is sent.
      # This delay is typically shorter.
      thinking_time = random.uniform(0.5, 30.0) # Random delay between 0.5 and 2.0 seconds
      print(f"Preparing to send: '{message_content}' in {thinking_time:.2f} seconds...")
      time.sleep(3)
      pyautogui.press('esc')
      pyautogui.press('esc')
      pyautogui.press('esc')
      open_deeplink(str(excel_data['Username'][message_number]))      
      time.sleep(3)
      time.sleep(thinking_time)
      pyperclip.copy(MESSAGE) # Copy the text to the clipboard
      time.sleep(0.5) # Give a small moment for the clipboard to update
      pyautogui.hotkey('ctrl', 'v')
      time.sleep(0.5) # Give a small moment for the clipboard to update
      pyautogui.press('enter')
      pyautogui.press('esc')
      print(f"--- Message {message_number} process complete ---")
      print("-" * 30) # Separator for readability
   

# --- Example Usage ---
if __name__ == "__main__":
   excel_data = pandas.read_excel('C:\\\\Users\\hovaness\\Documents\\telegram-automated-bulk-messages-master\\Recipients data.xlsx', sheet_name='Recipients')
   print("Starting message distribution...\n")
   for i, message in enumerate(excel_data['Username'].tolist()):
      send_message_with_lag(message, i )

   print('The script executed successfully.')
   print('All messages sent successfully.')