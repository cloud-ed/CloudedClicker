import threading
import tkinter as tk
from tkinter import ttk
from clicker_controller import ClickerController
from recorder_controller import RecorderController
from pynput.mouse import Controller

def launch_gui():
    mouse = Controller()

    clicker = ClickerController(
        get_interval_callback=lambda: interval_var.get(),
        start_button=None,
        stop_button=None,
        status_label=None
    )
    recorder = RecorderController(mouse)

    root = tk.Tk()
    root.title("CloudedClicker")
    root.geometry("300x180")
    root.resizable(False, False)

    mode_var = tk.StringVar(value="clicker")
    content_frame = ttk.Frame(root, padding="10")
    content_frame.pack(fill="both", expand=True)

    def switch_mode():
        for widget in content_frame.winfo_children():
            widget.destroy()
        if mode_var.get() == "clicker":
            build_clicker_ui(content_frame)
            clicker.update_gui()
        else:
            build_recorder_ui(content_frame)
            recorder.update_gui()

    def toggle_mode():
        mode_var.set("recorder" if mode_var.get() == "clicker" else "clicker")
        switch_mode()

    ttk.Button(root, text="Switch Mode", command=toggle_mode).pack(pady=(10, 0))

    def build_clicker_ui(frame):
        nonlocal interval_var
        ttk.Label(frame, text="Click speed (ms):").grid(row=0, column=0, pady=5, sticky="ew")
        interval_var = tk.StringVar(value="100")
        ttk.Entry(frame, textvariable=interval_var, justify="center").grid(row=1, column=0, padx=10, sticky="ew")

        ttk.Label(frame, text="Hotkey:").grid(row=0, column=1, pady=5, sticky="ew")
        hotkey_var = tk.StringVar(value="`")

        def validate_hotkey_input(char):
            return len(char) <= 1

        validate_hotkey = root.register(validate_hotkey_input)
        hotkey_entry = ttk.Entry(frame, textvariable=hotkey_var, validate="key", validatecommand=(validate_hotkey, '%P'), justify='center')
        hotkey_entry.grid(row=1, column=1, padx=10, sticky="ew")

        start_button = ttk.Button(frame, text="Start (`)", command=lambda: clicker.start_clicking())
        start_button.grid(row=2, column=0, padx=10, pady=10)

        stop_button = ttk.Button(frame, text="Stop (`)", command=lambda: clicker.stop_clicking())
        stop_button.grid(row=2, column=1, padx=10, pady=10)

        status_label = ttk.Label(frame, text="Status: Idle")
        status_label.grid(row=3, column=0, columnspan=2, pady=5)

        def update_clicker_hotkey(*args):
            hotkey = hotkey_var.get().strip()
            if len(hotkey) == 1:
                clicker.set_hotkey(hotkey)
                start_button.config(text=f"Start ({hotkey})")
                stop_button.config(text=f"Stop ({hotkey})")
                hotkey_entry.selection_clear()
                hotkey_entry.icursor("end")
                hotkey_entry.master.focus_set()

        hotkey_var.trace_add("write", update_clicker_hotkey)
        clicker.get_interval = lambda: interval_var.get()
        clicker.start_button = start_button
        clicker.stop_button = stop_button
        clicker.status_label = status_label

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        update_clicker_hotkey()

    def build_recorder_ui(frame):
        ttk.Label(frame, text="Record Hotkey:").grid(row=0, column=0, sticky="ew")
        record_hotkey_var = tk.StringVar(value=recorder.record_hotkey)
        record_entry = ttk.Entry(frame, textvariable=record_hotkey_var, justify="center", width=5)
        record_entry.grid(row=0, column=1, padx=10, sticky="ew")

        ttk.Label(frame, text="Playback Hotkey:").grid(row=1, column=0, sticky="ew")
        playback_hotkey_var = tk.StringVar(value=recorder.playback_hotkey)
        playback_entry = ttk.Entry(frame, textvariable=playback_hotkey_var, justify="center", width=5)
        playback_entry.grid(row=1, column=1, padx=10, sticky="ew")

        def update_hotkeys(*args):
            record_key = record_hotkey_var.get().strip()
            playback_key = playback_hotkey_var.get().strip()

            if len(record_key) == 1:
                recorder.record_hotkey = record_key
                recorder.record_button.config(text=f"Start Recording ({record_key})")
                recorder.stop_record_button.config(text=f"Stop Recording ({record_key})")
            if len(playback_key) == 1:
                recorder.playback_hotkey = playback_key
                playback_button.config(text=f"Playback ({playback_key})")

        record_hotkey_var.trace_add("write", update_hotkeys)
        playback_hotkey_var.trace_add("write", update_hotkeys)

        recorder.record_button = ttk.Button(frame, text=f"Start Recording ({recorder.record_hotkey})", command=recorder.start_recording)
        recorder.record_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        recorder.stop_record_button = ttk.Button(frame, text=f"Stop Recording ({recorder.record_hotkey})", command=recorder.stop_recording)
        recorder.stop_record_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        playback_button = ttk.Button(frame, text=f"Playback ({recorder.playback_hotkey})", command=lambda: threading.Thread(target=recorder.playback, daemon=True).start())
        playback_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        recorder.update_gui()

    def clear_focus(event):
        widget = root.winfo_containing(event.x_root, event.y_root)
        if not isinstance(widget, tk.Entry):
            root.focus_set()

    root.bind("<Button-1>", clear_focus)
    interval_var = tk.StringVar(value="100")
    switch_mode()
    root.mainloop()