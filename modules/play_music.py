import pyautogui
import time
def play(query):
    if "music" or "play" in query:
        pyautogui.moveTo(5, 750)
        pyautogui.click()
        pyautogui.write("spotify")
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(10)
        pyautogui.moveTo(50, 120)
        pyautogui.click()
        time.sleep(2)
        pyautogui.write(query.split()[-1])
        pyautogui.press("enter")
        time.sleep(5)
        pyautogui.moveTo(765, 410)
        pyautogui.click()
        
query = "Open Spotify and play Perfect"
play(query)

