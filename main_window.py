import tkinter as tk

class WinAmp:

    window_base_size = (275, 116)
    window_title = 'WinAmp Music Player'
    scale = 3

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(self.window_title)
        self.win_width = self.window_base_size[0] * self.scale
        self.win_height = self.window_base_size[1] * self.scale
        self.root.geometry(f"{self.win_width}x{self.win_height}")

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    winamp = WinAmp()
    winamp.start()
