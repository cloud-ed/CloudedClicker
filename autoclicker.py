import time
import threading
import tkinter as tk
from tkinter import ttk
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode

# Toggle hotkey
TOGGLE_KEY = None

# Globals
clicking_event = threading.Event()
mouse = Controller()

# GUI callback references
start_button = None
stop_button = None
status_label = None
interval_var = None

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

    # Update column weights for even spacing
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

listener_thread = threading.Thread(target=lambda: Listener(on_press=toggle_event).run(), daemon=True)
listener_thread.start()

# Start the GUI
launch_gui()