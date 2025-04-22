import threading
import time
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode

class ClickerController:
    def __init__(self, get_interval_callback, start_button, stop_button, status_label):
        self.get_interval = get_interval_callback
        self.start_button = start_button
        self.stop_button = stop_button
        self.status_label = status_label
        self.clicking_event = threading.Event()
        self.mouse = Controller()
        self.hotkey = None

        self.thread = threading.Thread(target=self._run_clicker, daemon=True)
        self.thread.start()

        self.hotkey_listener_thread = threading.Thread(target=self._start_hotkey_listener, daemon=True)
        self.hotkey_listener_thread.start()

    def _run_clicker(self):
        while True:
            if self.clicking_event.is_set():
                try:
                    interval = float(self.get_interval()) / 1000
                except ValueError:
                    interval = 0.1
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
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self.status_label.config(text="Status: Clicking")
        else:
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
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
