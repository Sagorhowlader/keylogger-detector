from threading import Timer

from pynput import keyboard


class KeyboardMonitor:
    def __init__(self, interval):
        """
        :param interval: Time in seconds between logging intervals
        """
        self.interval = interval
        self.keystroke_count = 0
        self.queue = []  # Stores time-series data (keystrokes per interval)
        self.running = True  # Stop flag for terminating logging loop
        self.listener = keyboard.Listener(on_press=self.on_press)

    def on_press(self, key):
        """Callback function triggered on each keypress"""
        self.keystroke_count += 1
        print(f"[KEY DETECTED] {key}")

    def start(self):
        """Starts the keyboard listener and logging loop"""
        self.running = True
        self.listener.start()
        self.schedule_log()

    def stop(self):
        """Stops the keyboard listener and logging loop"""
        self.running = False
        self.listener.stop()

    def log(self):
        # Store current count in queue
        self.queue.append(self.keystroke_count)

        # Reset count for next interval
        self.keystroke_count = 0

        # Continue scheduling if not stopped
        if self.running:
            self.schedule_log()

    def schedule_log(self):
        """Schedules the next log after 'interval' seconds"""
        Timer(self.interval, self.log).start()
