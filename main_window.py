import tkinter as tk
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] [%(name)s] [%(funcName)s] %(message)s'
)
_log = logging.getLogger(__name__)

class WinAmp:

    window_base_size = (275, 116)
    window_title = 'WinAmp Music Player'
    scale = 3

    def __init__(self, debug=False):
        self.debug = debug
        if self.debug:
            _log.setLevel(logging.DEBUG)
        self.root = tk.Tk()
        if hasattr(self.root, 'applicationSupportsSecureRestorableState_'):
            self.root.applicationSupportsSecureRestorableState_ = lambda: True
        self.win_width = self.window_base_size[0] * self.scale
        self.win_height = self.window_base_size[1] * self.scale

    def draw_window(self):
        """
        Function to draw the main window
        """
        self.root.title(self.window_title)
        self.root.geometry(f"{self.win_width}x{self.win_height}")


    def start(self):
        self.draw_window()
        self.root.mainloop()


if __name__ == '__main__':
    _log.info('Starting WinAmp')
    winamp = WinAmp(debug=True)
    winamp.start()
