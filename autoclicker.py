import pyautogui
import keyboard
import time
import tkinter as tk
import threading
import queue

clicking = False
delay_ms = 100  # Delay in milliseconds, default to 100ms
click_position = None
pyautogui.FAILSAFE = False
click_queue = queue.Queue()  # Use a queue to manage clicks

# Tkinter setup
root = tk.Tk()
root.title("cloudedAutoclicker")

# Start/Stop Clicking
def toggle_clicking():
    global clicking
    clicking = not clicking
    status_label.config(text="Clicking..." if clicking else "Stopped")

# Capture Click Position
def capture_position():
    global click_position
    print("Move your mouse to the target position, then press 'c'")
    while True:
        if keyboard.is_pressed('c'):
            pos = pyautogui.position()
            click_position = (pos.x, pos.y)
            print(f"Captured position: {click_position}")
            break

# Delay Entry (convert to milliseconds)
def set_delay():
    global delay_ms
    try:
        delay_ms = int(delay_entry.get())  # Expecting milliseconds
    except ValueError:
        print("Invalid delay value.")

# Main clicking loop with queue-based timing
def autoclicker_loop():
    delay_seconds = delay_ms / 1000  # Convert milliseconds to seconds
    next_click_time = time.time()  # Next time we should click

    while True:
        if clicking:
            current_time = time.time()
            if current_time >= next_click_time:  # If enough time has passed
                # Push the click event to the queue
                click_queue.put(click_position if click_position else None)
                next_click_time = current_time + delay_seconds  # Reset the time after clicking

        # Process clicks from the queue
        while not click_queue.empty():
            pos = click_queue.get()
            pyautogui.click(pos)
        time.sleep(0.001)  # Prevent CPU overload

# Listen for hotkey press in a separate thread
def listen_for_hotkeys():
    global clicking
    while True:
        if keyboard.is_pressed('F8'):  # Set F8 to toggle clicking
            toggle_clicking()
            time.sleep(0.5)  # Debounce the hotkey press

# Start Tkinter mainloop and hotkey listener in separate threads
def start_gui():
    thread = threading.Thread(target=autoclicker_loop, daemon=True)
    thread.start()

    hotkey_thread = threading.Thread(target=listen_for_hotkeys, daemon=True)
    hotkey_thread.start()

    root.mainloop()

# Tkinter UI components
label = tk.Label(root, text="Autoclicker")
label.pack()

toggle_button = tk.Button(root, text="Start/Stop Clicking", command=toggle_clicking)
toggle_button.pack(pady=10)

delay_label = tk.Label(root, text="Delay (milliseconds):")
delay_label.pack()
delay_entry = tk.Entry(root)
delay_entry.insert(0, str(delay_ms))  # Default to 100ms
delay_entry.pack(pady=5)

capture_button = tk.Button(root, text="Capture Position", command=capture_position)
capture_button.pack(pady=10)

status_label = tk.Label(root, text="Stopped")
status_label.pack(pady=10)

# Start the GUI and hotkey listener
start_gui()
