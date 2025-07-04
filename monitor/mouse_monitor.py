from threading import Timer

from pynput import mouse


class MouseMonitor:
    def __init__(self, interval):
        self.interval = interval
        self.click_count = 0
        self.move_count = 0
        self.listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)
        self.queue = []
        self.running = True

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.click_count += 1

    def on_move(self, x, y):
        self.move_count += 1

    def start(self):
        self.listener.start()
        self.running = True
        self.schedule_log()

    def stop(self):
        self.running = False
        self.listener.stop()

    def get_counts(self):
        clicks = self.click_count
        moves = self.move_count
        self.queue.append([clicks, moves])
        self.click_count = 0
        self.move_count = 0
        if self.running:
            self.schedule_log()

    def schedule_log(self):
        Timer(self.interval, self.get_counts).start()
