import unittest
from clicker_controller import ClickerController
from unittest.mock import MagicMock


class TestClickerController(unittest.TestCase):

    def setUp(self):
        """Set up test environment (called before every test)."""
        # Mock the necessary parts
        self.get_interval_callback = MagicMock(return_value="100")
        self.start_button = MagicMock()
        self.stop_button = MagicMock()
        self.status_label = MagicMock()

        # Initialize ClickerController with mock components
        self.clicker = ClickerController(
            self.get_interval_callback,
            self.start_button,
            self.stop_button,
            self.status_label
        )

    def test_initialization(self):
        """Test if the ClickerController is initialized properly."""
        self.assertEqual(self.clicker.get_interval(), "100")
        self.assertFalse(self.clicker.is_clicking())

    def test_start_clicking(self):
        """Test if start_clicking sets the clicking event."""
        self.clicker.start_clicking()
        self.assertTrue(self.clicker.is_clicking())

    def test_stop_clicking(self):
        """Test if stop_clicking clears the clicking event."""
        self.clicker.stop_clicking()
        self.assertFalse(self.clicker.is_clicking())

    def test_update_gui_when_clicking(self):
        """Test if GUI is updated when clicking starts."""
        self.clicker.start_clicking()
        self.clicker.update_gui()
        self.start_button.config.assert_called_with(state='disabled')
        self.stop_button.config.assert_called_with(state='normal')

    def test_update_gui_when_idle(self):
        """Test if GUI is updated when clicking stops."""
        self.clicker.stop_clicking()
        self.clicker.update_gui()
        self.start_button.config.assert_called_with(state='normal')
        self.stop_button.config.assert_called_with(state='disabled')


if __name__ == '__main__':
    unittest.main()
