import pyautogui
import keyboard
import time

clicking = False
delay = 0.1
click_position = None
debounce = 0.2 # Set a delay for inputs to avoid accidental presses
pyautogui.FAILSAFE = False

def get_click_position():
    print("Move your mouse to the target position, then press 'c'")
    while True:
        if keyboard.is_pressed('c'):
            pos = pyautogui.position()
            print(f'Captured position: {pos}')
            time.sleep(debounce)
            return (pos.x, pos.y)

print("Press 'p' to pick a click position.")
print("Press '`' to start/stop clicking. Press 'q' to quit.")

while True:
    if keyboard.is_pressed('p'):
        click_position = get_click_position()
        time.sleep(debounce)

    if keyboard.is_pressed('`'):
        clicking = not clicking
        print('Started clicking...' if clicking else 'Stopped clicking.')
        time.sleep(debounce)
    
    if keyboard.is_pressed('q'):
        print('Exiting program.')
        break

    if clicking:
        pyautogui.click(click_position if click_position else None)
        time.sleep(delay)