import time
import threading
import tkinter as tk
from tkinter import ttk
from pynput.mouse import Controller, Button
from pynput.mouse import Listener as mListener
from pynput.keyboard import Listener, KeyCode

# Toggle hotkey
TOGGLE_KEY = None

# Globals
clicking_event = threading.Event()
mouse = Controller()
recording = False
replaying = False
recorded_actions = []

# GUI callback references
start_button = None
stop_button = None
status_label = None
interval_var = None


################################################################
#                       CLICKER SECTION                        #
################################################################

# Main clicker loop
def clicker():
    while True:
        if clicking_event.is_set():
            try:
                interval = float(interval_var.get()) / 1000  # Convert ms to seconds
            except ValueError:
                interval = 100 / 1000  # Default 100ms
            mouse.click(Button.left, 1)
            time.sleep(interval)
        else:
            time.sleep(0.05)

# Update GUI based on current state
def update_gui_state():
    if clicking_event.is_set():
        start_button.config(state='disabled')  # Grey out when clicking
        stop_button.config(state='normal')
        status_label.config(text="Status: Clicking")
    else:
        start_button.config(state='normal')
        stop_button.config(state='disabled')  # Grey out when not clicking
        status_label.config(text="Status: Idle")

def start_clicking():
    clicking_event.set()
    update_gui_state()

def stop_clicking():
    clicking_event.clear()
    update_gui_state()

# Hotkey toggle
def toggle_event(key):
    global clicking
    if TOGGLE_KEY and key == TOGGLE_KEY:
        if clicking_event.is_set():
            clicking_event.clear()  # Stop clicking
        else:
            clicking_event.set()  # Start clicking
        update_gui_state()


################################################################
#                  RECORD/PLAYBACK SECTION                     #
################################################################

def on_click(x, y, button, pressed):
    if recording:
        timestamp = time.time()
        recorded_actions.append(('click', x, y, button, pressed, timestamp))

def on_move(x, y):
    if recording:
        timestamp = time.time()
        recorded_actions.append(('move', x, y, timestamp))

mouse_listener = mListener(on_click=on_click, on_move=on_move)
mouse_listener.start()

def start_recording():
    global recording, recorded_actions
    recorded_actions = []
    recording = True

def stop_recording():
    global recording
    recording = False

def playback_actions():
    if not recorded_actions:
        return
    
    global recording
    replaying = True

    start_time = recorded_actions[0][-1]
    for i, action in enumerate(recorded_actions):
        if not replaying:
            break
        if action[0] == 'move':
            _, x, y, timestamp = action
        else:
            _, x, y, button, pressed, timestamp = action
        
        # Sleep until next action
        if i > 0:
            delay = timestamp - recorded_actions[i - 1][-1]
            time.sleep(delay)
        
        if action[0] == 'move':
            mouse.position = (x, y)
        elif action[0] == 'click' and pressed:
            mouse.position(x, y)
            mouse.click(button)
    
    replaying = False

################################################################
#                         GUI SECTION                          #
################################################################

def launch_gui():
    global start_button, stop_button, status_label, interval_var

    root = tk.Tk()
    root.title("CloudedClicker")

    # Window size
    w_height = 135
    w_width = 250
    root.geometry(f"{w_width}x{w_height}")
    root.resizable(False, False)

    control_frame = ttk.Frame(root, padding="10")
    control_frame.grid(row=0, column=0, sticky="nsew")

    control_frame.grid_columnconfigure(0, weight=1)
    control_frame.grid_columnconfigure(0, weight=1)

   # Interval settings
    ttk.Label(control_frame, text="Click speed (ms):", anchor="center", justify="center").grid(
        column=0, row=0, pady=(0, 5), sticky="ew"
    )

    interval_var = tk.StringVar(value="100")
    interval_entry = ttk.Entry(control_frame, width=10, textvariable=interval_var, justify="center")
    interval_entry.grid(column=0, row=1, pady=(0, 10), sticky="ew", padx=10)

    # Hotkey settings
    ttk.Label(control_frame, text="Hotkey:", anchor="center", justify="center").grid(
        column=1, row=0, pady=(0, 5), sticky="ew"
    )

    hotkey_var = tk.StringVar(value="`")
    hotkey_entry = ttk.Entry(control_frame, width=10, textvariable=hotkey_var, justify="center")
    hotkey_entry.grid(column=1, row=1, pady=(0, 10), sticky="ew", padx=10)


    # No auto-select when tabbing in
    def remove_selection(event):
        event.widget.selection_clear()

    interval_entry.bind("<FocusIn>", remove_selection)
    hotkey_entry.bind("<FocusIn>", remove_selection)

    # Deselect entry when clicking outside
    def clear_focus(event):
        widget = event.widget
        if not isinstance(widget, tk.Entry):
            root.focus()

    root.bind_all("<Button-1>", clear_focus)

    # Start and stop buttons
    start_button = ttk.Button(control_frame, text="Start (`)", command=start_clicking)
    start_button.grid(column=0, row=2, padx=20, sticky="e")

    stop_button = ttk.Button(control_frame, text="Stop (`)", command=stop_clicking)
    stop_button.grid(column=1, row=2, padx=20, sticky="w")

    # Record and playback buttons
    record_button = ttk.Button(control_frame, text="Record", command=start_recording)
    record_button.grid(row=4, column=0, padx=10, pady=(10, 5), sticky="e")

    stop_record_button = ttk.Button(control_frame, text="Stop Record", command=stop_recording)
    stop_record_button.grid(row=4, column=1, padx=10, pady=(10, 5), sticky="w")

    playback_button = ttk.Button(control_frame, text="Playback", command=lambda: threading.Thread(target=playback_actions, daemon=True).start)
    playback_button.grid(row=5, column=0, columnspan = 2, pady=(5, 0))

    # Column weights for even spacing
    control_frame.grid_columnconfigure(0, weight=1)  # Column for click speed
    control_frame.grid_columnconfigure(1, weight=1)  # Column for hotkey

    # Current status
    status_label = ttk.Label(control_frame, text="Status: Idle", anchor="center")
    status_label.grid(column=0, row=3, columnspan=2, pady=(10, 0), sticky="nsew")

    # Update hotkey
    def update_hotkey(*args):
        global TOGGLE_KEY
        hotkey = hotkey_var.get().strip()
        if len(hotkey) == 1:
            TOGGLE_KEY = KeyCode(char=hotkey.lower())
            start_button.config(text=f"Start ({hotkey})")
            stop_button.config(text=f"Stop ({hotkey})")
    hotkey_var.trace_add("write", update_hotkey)

    update_hotkey()
    update_gui_state()
    root.mainloop()

# Threads
click_thread = threading.Thread(target=clicker, daemon=True)
click_thread.start()

hotkey_clicker_thread = threading.Thread(target=lambda: Listener(on_press=toggle_event).run(), daemon=True)
hotkey_clicker_thread.start()

# Start the GUI
launch_gui()