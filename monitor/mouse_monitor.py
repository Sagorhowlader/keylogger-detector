from pynput import mouse


class MouseMonitor:
    def __init__(self):
        self.click_count = 0
        self.move_count = 0
        self.listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.click_count += 1

    def on_move(self, x, y):
        self.move_count += 1

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()

    def get_counts(self):
        clicks = self.click_count
        moves = self.move_count
        self.click_count = 0
        self.move_count = 0
        return clicks, moves
