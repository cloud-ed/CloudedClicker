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
interval_var_global = None
mode_var = None
content_frame = None
record_button = None
stop_record_button = None

################################################################
#                       CLICKER SECTION                        #
################################################################

# Main clicker loop
def clicker():
    while True:
        if clicking_event.is_set():
            try:
                interval = float(interval_var_global.get()) / 1000  # Convert ms to seconds
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
    global recording
    recorded_actions.clear()
    recording = True
    update_recorder_state()

def stop_recording():
    global recording
    recording = False
    update_recorder_state()

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

        if i > 0:
            delay = timestamp - recorded_actions[i - 1][-1]
            time.sleep(delay)

        if action[0] == 'move':
            mouse.position = (x, y)
        elif action[0] == 'click' and pressed:
            mouse.position = (x, y)
            mouse.click(button)

    replaying = False


def update_recorder_state():
    if record_button and stop_record_button:
        if recording:
            record_button.config(state='disabled')
            stop_record_button.config(state='normal')
        else:
            record_button.config(state='normal')
            stop_record_button.config(state='disabled')

################################################################
#                         GUI SECTION                          #
################################################################

def launch_gui():
    global start_button, stop_button, status_label, interval_var_global, mode_var, content_frame, record_button, stop_record_button

    root = tk.Tk()
    root.title("CloudedClicker")
    root.geometry("300x180")
    root.resizable(False, False)

    mode_var = tk.StringVar(value="clicker")

    def switch_mode():
        for widget in content_frame.winfo_children():
            widget.destroy()
        if mode_var.get() == "clicker":
            build_clicker_ui(content_frame)
        else:
            build_recorder_ui(content_frame)

    toggle_button = ttk.Button(root, text="Switch Mode", command=lambda: toggle_mode())
    toggle_button.pack(pady=(10, 0))

    content_frame = ttk.Frame(root, padding="10")
    content_frame.pack(fill="both", expand=True)

    def toggle_mode():
        mode_var.set("recorder" if mode_var.get() == "clicker" else "clicker")
        switch_mode()

    def build_clicker_ui(frame):
        global interval_var_global, start_button, stop_button, status_label

        ttk.Label(frame, text="Click speed (ms):").grid(row=0, column=0, pady=5, sticky="ew")
        interval_var_global = tk.StringVar(value="100")
        interval_entry = ttk.Entry(frame, textvariable=interval_var_global, justify="center")
        interval_entry.grid(row=1, column=0, padx=10, sticky="ew")

        ttk.Label(frame, text="Hotkey:").grid(row=0, column=1, pady=5, sticky="ew")
        hotkey_var = tk.StringVar(value="`")
        hotkey_entry = ttk.Entry(frame, textvariable=hotkey_var, justify="center")
        hotkey_entry.grid(row=1, column=1, padx=10, sticky="ew")

        start_button = ttk.Button(frame, text="Start (`)", command=start_clicking)
        start_button.grid(row=2, column=0, padx=10, pady=10)

        stop_button = ttk.Button(frame, text="Stop (`)", command=stop_clicking)
        stop_button.grid(row=2, column=1, padx=10, pady=10)

        status_label = ttk.Label(frame, text="Status: Idle")
        status_label.grid(row=3, column=0, columnspan=2, pady=5)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

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

    def build_recorder_ui(frame):
        global record_button, stop_record_button

        record_button = ttk.Button(frame, text="Start Recording", command=start_recording)
        record_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        stop_record_button = ttk.Button(frame, text="Stop Recording", command=stop_recording)
        stop_record_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        playback_button = ttk.Button(frame, text="Playback", command=lambda: threading.Thread(target=playback_actions, daemon=True).start())
        playback_button.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        update_recorder_state()

    switch_mode()
    root.mainloop()

# Threads
click_thread = threading.Thread(target=clicker, daemon=True)
click_thread.start()

hotkey_clicker_thread = threading.Thread(target=lambda: Listener(on_press=toggle_event).run(), daemon=True)
hotkey_clicker_thread.start()

# Start the GUI
launch_gui()