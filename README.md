# ☁️ CloudedClicker V1.2.0

CloudedClicker is a lightweight, customizeable **autoclicker and macro tool for Windows** - now with full custom keybinds.

<!-- AUTO-PATCH-NOTES-START -->
## 🔧 Known Issues (Automated)
- 🐛 **#1** (bug): The application fails to detect or warn about conflicting keybinds when multiple actions are assigned the same hotkey, leading to silent, unpredictable behavior. <!-- issue-1 -->
- ✨ **#2** (feature): Add functionality to save and load recorded mouse macros to persist recordings across app sessions. <!-- issue-2 -->
- ✨ **#3** (feature): Extend the recorder to capture right and middle mouse clicks in addition to left clicks and movements. <!-- issue-3 -->
- 📄 **#4** (docs): The README lacks specification of the required Python version, causing potential compatibility issues when running the project from source. <!-- issue-4 -->
- 🐛 **#5** (bug): The application may fail silently when simulating mouse input without admin permissions due to OS-level restrictions, and should detect and notify the user to run with elevated privileges. <!-- issue-5 -->
- 🐛 **#6** (bug): Switching between Autoclicker Mode and Recorder Mode resets the click interval to default, losing user-configured values and requiring re-entry each time. <!-- issue-6 -->
- 🐛 **#7** (bug): The application icon fails to appear in the Windows 11 system tray on certain builds despite the app running, likely due to timing issues in tray icon registration. <!-- issue-7 -->
- ✨ **#8** (feature): The recorder mode should display a warning message when no actions are captured to inform the user before attempting playback. <!-- issue-8 -->
- 🐛 **#9** (bug): The issue appears to be a test submission with minimal content, likely intended to verify the triage process rather than report an actual problem. <!-- issue-9 -->
- ✨ **#10** (feature): Request to add a colour blind mode to improve accessibility for colourblind users. <!-- issue-10 -->
<!-- AUTO-PATCH-NOTES-END -->

## 💡 Why I made this

6 weeks ago, I suffered a serious distal humeral fracture, which resulted in radial nerve palsy - a condition that impairs my ability to control my wrist and fingers. After surgery, my nerve was found to be partially severed and surgically re-attached. As it was my dominant hand, everyday tasks became much more challenging and slow. During my recovery, I realized I could use this as an opportunity to create something that would reduce the strain I was experiencing (and play Cookie Clicker). Thus, CloudedClicker was born.

## ✨ Features

- 🖱️ **Simple One-Key Toggle** — Press a single customizable hotkey to toggle clicking on/off.
- ⚙️ **Adjustable Click Interval** — Set how fast it clicks (in milliseconds).
- 🎥 **Record + Playback Mouse Actions** — Automate more complex or repetitive motion with ease.
- 🔁 **Mode Switching** — Instantly switch between autoclicker mode and recording mode with one button.
- 🔑 **Custom Keybinds** — Set your own hotkeys for recording, playback, and clicking actions, making it easy to control the tool the way you want.
- 🎛️ **Clean and Minimal UI** — Lightweight, no fluff. Just click, set, go.

## 📅 Potential Future Features

- 💻 **Keyboard Macro Support** - Integrate the use of the keyboard into the macro function
- 💾 **Save and Re-use Recordings** - Re-use any saved recording to save time

## 🖥️ How to Use

### 🖱 Autoclicker Mode:

1. Open `CloudedClicker.exe`.
2. Choose your **click speed** in milliseconds.
3. Set your preferred **hotkey**.
4. Click **Start**, or use your hotkey to begin auto-clicking.
5. Click **Stop**, or press the hotkey again to disable.

### 🎥 Recorder Mode:

1. Click **Switch Mode** to enter Recorder Mode.
2. Set your preferred **hotkeys**.
3. Press **Start Recording** and perform the mouse actions you want to capture.
4. Press **Stop Recording** once you're done.
5. Click **Playback** to replay your recorded inputs.

## 📦 Download

You can download the latest version from the [Releases](https://github.com/cloud-ed/cloudedclicker/releases) page.  
Just download and unzip — no install required.

## ❗ Notes

- CloudedClicker is built for accessibility and personal use. Please **use responsibly** and in accordance with any software or game policies.
- This app runs quietly in the background. If you accidentally enable it, just press your toggle hotkey again to stop.
- Recording only captures mouse movement and left-clicks for now — keyboard support might come in a future update.

## 🛠️ Built With

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Pynput](https://pynput.readthedocs.io/)
- [PyInstaller](https://pyinstaller.org/en/stable/)
- [Favicon](https://favicon.io/)

## Dev Note

I know it's not the most impressive project, but it's something that helped me when I needed it. Feel free to use it if you want.

Thanks for checking it out 😁

**_clouded_** ☁️
