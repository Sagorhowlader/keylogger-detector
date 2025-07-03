from pynput import keyboard


class KeyboardMonitor:
    def __init__(self):
        self.keystroke_count = 0
        self.listener = keyboard.Listener(on_press=self.on_key_press)

    def on_key_press(self, key):
        self.keystroke_count += 1

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()

    def get_count(self):
        count = self.keystroke_count
        self.keystroke_count = 0
        return count
