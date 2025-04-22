import unittest
from recorder_controller import RecorderController
from unittest.mock import MagicMock
import time


class TestRecorderController(unittest.TestCase):

    def setUp(self):
        """Set up test environment (called before every test)."""
        self.mouse_controller = MagicMock()
        self.recorder = RecorderController(self.mouse_controller)

    def test_initialization(self):
        """Test if RecorderController is initialized correctly."""
        self.assertFalse(self.recorder.recording)
        self.assertFalse(self.recorder.replaying)

    def test_start_recording(self):
        """Test if start_recording sets the recording flag."""
        self.recorder.start_recording()
        self.assertTrue(self.recorder.recording)

    def test_stop_recording(self):
        """Test if stop_recording clears the recording flag."""
        self.recorder.stop_recording()
        self.assertFalse(self.recorder.recording)

    def test_recording_actions(self):
        """Test if actions are recorded correctly during mouse events."""
        self.recorder.start_recording()
        # Simulate a click action
        self.recorder.on_click(100, 200, 'left', True)
        self.assertEqual(len(self.recorder.recorded_actions), 1)

    def test_playback(self):
        """Test if playback processes recorded actions."""
        self.recorder.start_recording()
        # Simulate a click action
        self.recorder.on_click(100, 200, 'left', True)
        self.recorder.stop_recording()
        # Trigger playback in a separate thread
        self.recorder.playback()
        self.assertFalse(self.recorder.replaying)


if __name__ == '__main__':
    unittest.main()
