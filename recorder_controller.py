import time
import threading
from pynput.mouse import Listener as mListener
from pynput.keyboard import Listener as kListener, KeyCode

class RecorderController:
    def __init__(self, mouse_controller, record_hotkey='9', playback_hotkey='0'):
        self.recording = False
        self.replaying = False
        self.recorded_actions = []
        self.mouse = mouse_controller

        self.record_button = None
        self.stop_record_button = None

        # Hotkeys
        self.record_hotkey = record_hotkey
        self.playback_hotkey = playback_hotkey

        # Start keyboard and mouse listeners
        self.keyboard_listener = kListener(on_press=self._on_hotkey_press)
        self.keyboard_listener.daemon = True
        self.keyboard_listener.start()

        self.mouse_listener = mListener(on_click=self.on_click, on_move=self.on_move)
        self.mouse_listener.daemon = True
        self.mouse_listener.start()

    def _on_hotkey_press(self, key):
        try:
            if isinstance(key, KeyCode):
                pressed_key = key.char
                if pressed_key == self.record_hotkey:
                    if not self.recording:
                        self.start_recording()
                    else:
                        self.stop_recording()
                    self.update_gui()
                elif pressed_key == self.playback_hotkey and not self.recording:
                    threading.Thread(target=self.playback, daemon=True).start()
        except AttributeError:
            pass

    def update_hotkeys(self, record_hotkey=None, playback_hotkey=None):
        if record_hotkey:
            self.record_hotkey = record_hotkey
        if playback_hotkey:
            self.playback_hotkey = playback_hotkey

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
        self.update_gui()

    def stop_recording(self):
        self.recording = False
        self.update_gui()

    def update_gui(self):
        if self.record_button and self.stop_record_button:
            if self.recording:
                self.record_button.config(state='disabled')
                self.stop_record_button.config(state='normal')
            else:
                self.record_button.config(state='normal')
                self.stop_record_button.config(state='disabled')

    def playback(self):
        if not self.recorded_actions:
            return

        self.replaying = True

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
            elif action[0] == 'click' and action[4]:
                _, x, y, button, _, _ = action
                self.mouse.position = (x, y)
                self.mouse.click(button)

        self.replaying = False
