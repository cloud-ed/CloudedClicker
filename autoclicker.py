import pyautogui
import keyboard
import time

clicking = False
delay = 0.05

print("Press '`' to start/stop clicking. Press 'q' to quit.")

while True:
    if keyboard.is_pressed('`'):
        clicking = not clicking
        print('Started clicking...' if clicking else 'Stopped clicking.')
        time.sleep(0.5) # Debounce the button to avoid accidentally pressing multiple times
    
    if keyboard.is_pressed('q'):
        print('Exiting program.')
        break

    if clicking:
        pyautogui.click()
        time.sleep(delay)