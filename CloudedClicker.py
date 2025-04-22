import time
import threading
import tkinter as tk
from tkinter import ttk
from pynput.mouse import Controller, Button
from pynput.mouse import Listener as mListener
from pynput.keyboard import Listener, KeyCode

# Global references
mouse = Controller()

# GUI references
interval_var_global = None
mode_var = None
content_frame = None

# Clicker instance (defined later)
clicker = None

################################################################
#                       CLICKER SECTION                        #
################################################################

class ClickerController:
    def __init__(self, get_interval_callback, start_button, stop_button, status_label):
        self.clicking_event = threading.Event()
        self.get_interval = get_interval_callback
        self.mouse = Controller()
        self.start_button = start_button
        self.stop_button = stop_button
        self.status_label = status_label
        self.hotkey = None

        self.thread = threading.Thread(target=self._run_clicker, daemon=True)
        self.thread.start()

        # Start hotkey listener in a separate thread
        self.hotkey_listener_thread = threading.Thread(target=self._start_hotkey_listener, daemon=True)
        self.hotkey_listener_thread.start()

    def _run_clicker(self):
        while True:
            if self.clicking_event.is_set():
                try:
                    interval = float(self.get_interval()) / 1000 # Convert ms to seconds
                except ValueError:
                    interval = 0.1 # Default 100ms
                self.mouse.click(Button.left)
                time.sleep(interval)
            else:
                time.sleep(0.05)

    def start_clicking(self):
        self.clicking_event.set()
        self.update_gui()

    def stop_clicking(self):
        self.clicking_event.clear()
        self.update_gui()

    def is_clicking(self):
        return self.clicking_event.is_set()

    def update_gui(self):
        if self.is_clicking():
            self.start_button.config(state='disabled') # Grey out when clicking
            self.stop_button.config(state='normal')
            self.status_label.config(text="Status: Clicking")
        else:
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled') # Grey out when not clicking
            self.status_label.config(text="Status: Idle")

    def _start_hotkey_listener(self):
        listener = Listener(on_press=self._on_hotkey_press)
        listener.start()

    def _on_hotkey_press(self, key):
        if self.hotkey and key == self.hotkey:
            if self.is_clicking():
                self.stop_clicking()
            else:
                self.start_clicking()

    def set_hotkey(self, hotkey):
        self.hotkey = KeyCode(char=hotkey.lower())

################################################################
#                  RECORD/PLAYBACK SECTION                     #
################################################################

class RecorderController:
    def __init__(self, mouse_controller):
        self.recording = False
        self.replaying = False
        self.recorded_actions = []
        self.mouse = mouse_controller

        self.record_button = None
        self.stop_record_button = None

        self.listener = mListener(
            on_click=self.on_click,
            on_move=self.on_move
        )
        self.listener.start()

    def on_click(self, x, y, button, pressed):
        if self.recording:
            timestamp = time.time()
            self.recorded_actions.append(('click', x, y, button, pressed, timestamp))

    def on_move(self, x, y):
        if self.recording:
            timestamp = time.time()
            self.recorded_actions.append(('move', x, y, timestamp))

    def start_recording(self):
        self.recorded_actions.clear()
        self.recording = True
        self._update_buttons()

    def stop_recording(self):
        self.recording = False
        self._update_buttons()

    def playback(self):
        if not self.recorded_actions:
            return

        self.replaying = True
        start_time = self.recorded_actions[0][-1]

        for i, action in enumerate(self.recorded_actions):
            if not self.replaying:
                break

            delay = 0
            if i > 0:
                delay = action[-1] - self.recorded_actions[i - 1][-1]
            time.sleep(delay)

            if action[0] == 'move':
                _, x, y, _ = action
                self.mouse.position = (x, y)
            elif action[0] == 'click' and action[4]:  # pressed is True
                _, x, y, button, _, _ = action
                self.mouse.position = (x, y)
                self.mouse.click(button)

        self.replaying = False

    def _update_buttons(self):
        if self.record_button and self.stop_record_button:
            if self.recording:
                self.record_button.config(state='disabled')
                self.stop_record_button.config(state='normal')
            else:
                self.record_button.config(state='normal')
                self.stop_record_button.config(state='disabled')

################################################################
#                         GUI SECTION                          #
################################################################

def launch_gui():
    global interval_var_global, mode_var, content_frame
    global clicker

    root = tk.Tk()
    root.title("CloudedClicker")
    root.geometry("300x180")
    root.resizable(False, False)

    mode_var = tk.StringVar(value="clicker")

    clicker = ClickerController(
        get_interval_callback=lambda: interval_var_global.get(),
        start_button=None,
        stop_button=None,
        status_label=None
    )
    recorder = RecorderController(mouse)

    def switch_mode():
        for widget in content_frame.winfo_children():
            widget.destroy()
        if mode_var.get() == "clicker":
            build_clicker_ui(content_frame)
        else:
            build_recorder_ui(content_frame)

    def toggle_mode():
        mode_var.set("recorder" if mode_var.get() == "clicker" else "clicker")
        switch_mode()

    ttk.Button(root, text="Switch Mode", command=toggle_mode).pack(pady=(10, 0))
    content_frame = ttk.Frame(root, padding="10")
    content_frame.pack(fill="both", expand=True)

    def build_clicker_ui(frame):
        global interval_var_global, start_button, stop_button, status_label

        ttk.Label(frame, text="Click speed (ms):").grid(row=0, column=0, pady=5, sticky="ew")
        interval_var_global = tk.StringVar(value="100")
        ttk.Entry(frame, textvariable=interval_var_global, justify="center").grid(row=1, column=0, padx=10, sticky="ew")

        ttk.Label(frame, text="Hotkey:").grid(row=0, column=1, pady=5, sticky="ew")
        hotkey_var = tk.StringVar(value="`")
        
        # Validate hotkey input
        def validate_hotkey_input(char):
            if len(char) == 1 or char == '':  # Allow one character or empty for backspace
                return True
            return False  # Disallow anything longer than one character
        
        validate_hotkey = root.register(validate_hotkey_input)
        hotkey_entry = ttk.Entry(frame, textvariable=hotkey_var, validate="key", validatecommand=(validate_hotkey, '%P'), justify='center')
        hotkey_entry.grid(row=1, column=1, padx=10, sticky="ew")

        def update_hotkey(*args):
            hotkey = hotkey_var.get().strip()
            if len(hotkey) == 1:
                clicker.set_hotkey(hotkey)
                start_button.config(text=f"Start ({hotkey})")
                stop_button.config(text=f"Stop ({hotkey})")

        hotkey_var.trace_add("write", update_hotkey)

        start_button = ttk.Button(frame, text="Start (`)", command=lambda: clicker.start_clicking())
        start_button.grid(row=2, column=0, padx=10, pady=10)

        stop_button = ttk.Button(frame, text="Stop (`)", command=lambda: clicker.stop_clicking())
        stop_button.grid(row=2, column=1, padx=10, pady=10)

        status_label = ttk.Label(frame, text="Status: Idle")
        status_label.grid(row=3, column=0, columnspan=2, pady=5)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        update_hotkey()

        # Pass the buttons to the controller
        clicker.start_button = start_button
        clicker.stop_button = stop_button
        clicker.status_label = status_label
        clicker.update_gui()

    def build_recorder_ui(frame):
        recorder.record_button = ttk.Button(frame, text="Start Recording", command=recorder.start_recording)
        recorder.record_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        recorder.stop_record_button = ttk.Button(frame, text="Stop Recording", command=recorder.stop_recording)
        recorder.stop_record_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        playback_button = ttk.Button(
            frame, text="Playback",
            command=lambda: threading.Thread(target=recorder.playback, daemon=True).start()
        )
        playback_button.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        recorder._update_buttons()


    switch_mode()
    root.mainloop()

# Launch the GUI
launch_gui()
