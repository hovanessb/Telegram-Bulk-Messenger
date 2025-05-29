import pyautogui
import csv
import time
import pyperclip
def scroll_down():
   ""

def copy_username():
   """
   Simulates sending a message with realistic, random delays.

   Args:
      message_content (str): The content of the message to "send".
      message_number (int): The sequence number of the message being sent.
   """
   time.sleep(0.5)  # Give a small moment for the clipboard to update
   # Print the message number and content to the console for tracking.
   pyautogui.click('username.png')
   search = pyautogui.locateOnScreen('username.png')  # Ensure the 'at' symbol is visible
   pyautogui.moveTo( search[0]+ 25, search[1] - 15)
   pyautogui.click()
   time.sleep(0.5)  # Give a small moment for the clipboard to update
   userName = pyperclip.paste()  # Get the current clipboard content
   time.sleep(0.5)  # Give a small moment for the clipboard to update
   return userName

def setup():
   pyautogui.click('members.png')  # Click on the 'Members' button
   time.sleep(1)  # Wait for the members list to load
   pyautogui.click('groupmembers.png')  # Click on the 'Members' button
   time.sleep(1)  # Wait for the members list to load 
   
   

def get_clipboard_and_write_to_csv(filename="usernames.csv", names_count=2097):
    """
    Continuously gets clipboard contents and writes them to a CSV file.
    The loop continues until the user clicks 'Cancel' in a PyAutoGUI confirm box.
    """
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
         csv_writer = csv.writer(csvfile)
         #csv_writer.writerow(['Timestamp', 'Clipboard Content']) # Write header row
         for i in range(names_count):
            search = pyautogui.locateOnScreen('search.png')  # Ensure the 'at' symbol is visible
            pyautogui.moveTo( search[0]+ 100, search[1] + 75)  # Move the mouse to a safe position
            pyautogui.click()
            try:
               clipboard_content = copy_username()
               timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
               csv_writer.writerow([timestamp, clipboard_content])
               print(f"Saved: [{timestamp}] {clipboard_content[:50]}...") # Print first 50 chars
            except Exception as e:
               print(f"An error occurred while pasting: {e}")
               # You might want to handle specific paste errors here
            pyautogui.keyDown('esc')  # Press 'Esc' to cancel the paste operation
            pyautogui.PAUSE = 0.5
            pyautogui.scroll(-100) 
            time.sleep(1.3)        
           

if __name__ == "__main__":
   print("Launching in 3 seconds... \n" \
         "1. Make sure the Telegram app is visible and open on the screen." \
         "2. Ensure you have a group selected.")
   time.sleep(3)  # Give a small moment for the clipboard to update
   print("Launching...")    
   setup()
   get_clipboard_and_write_to_csv()
   print("CSV writing complete.")