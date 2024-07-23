import pygame
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os

# Initialize Pygame mixer
pygame.mixer.init()

# Alphabet mapping in the sprite sheet
size_of_a_character_in_sprite_sheet = (5, 6)
characters_per_row = 26
scale = 1


def load_file():
    """
    Function to load a music file and play it
    """
    file_path = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3 *.wav")])
    if file_path:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        update_text_label(f"Now Playing: {file_path.split('/')[-1]}")


def play_music():
    """
    Function to play music
    """
    pygame.mixer.music.unpause()


def pause_music():
    """
    Function to pause music
    """
    pygame.mixer.music.pause()


def stop_music():
    """
    Function to stop music
    """
    pygame.mixer.music.stop()
    update_text_label("")


def crop_image(name, image, x, y, width, height):
    """
    Function to crop the image and return a PhotoImage object

    Args:
        name: str: Name of the image
        image: PIL.Image: Image to crop
        x: int: x-coordinate of the top-left corner
        y: int: y-coordinate of the top-left corner
        width: int: Width of the cropped image
        height: int: Height of the cropped image

    Returns:
        ImageTk.PhotoImage: Cropped image as a PhotoImage object
    """
    if name == 'load':
        height = 16
    cropped_image = image.crop((x, y, x + width + 1, y + height))
    return ImageTk.PhotoImage(cropped_image)


def text_to_sprite(text, sprite_image):
    """
    Function to convert text to a sprite image

    Args:
        text: str: Text to convert
        sprite_image: PIL.Image: Sprite sheet image

    Returns:
        ImageTk.PhotoImage: Sprite image with the text
    """
    char_width, char_height = size_of_a_character_in_sprite_sheet
    sprite_text = Image.new('RGBA', (len(text) * char_width, char_height), (0, 0, 0, 0))

    for i, char in enumerate(text):
        if char.isalpha():
            char = char.upper()
            idx = ord(char) - ord('A')
        elif char.isdigit():
            idx = ord(char) - ord('0') + 26
        else:
            continue

        x = (idx % characters_per_row) * char_width
        y = (idx // characters_per_row) * char_height
        char_image = sprite_image.crop((x, y, x + char_width, y + char_height))
        sprite_text.paste(char_image, (i * char_width, 0))

    return ImageTk.PhotoImage(sprite_text)


def load_sprite_image(file):
    """
    Function to load a sprite image using OpenCV and convert it to a PIL image

    Args:
        file: str: Path to the sprite image file

    Returns:
        PIL.Image: Loaded sprite image
    """
    try:
        sprite_image = cv2.imread(file, cv2.IMREAD_UNCHANGED)
        if sprite_image is None:
            print(f"Failed to read {file} using OpenCV.")
            return None

        sprite_image_rgb = cv2.cvtColor(sprite_image, cv2.COLOR_BGRA2RGBA)
        pil_image = Image.fromarray(sprite_image_rgb)
        return pil_image
    except FileNotFoundError:
        print(f"File {file} not found.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def update_text_label(new_text):
    """
    Function to update the text label with the new text

    Args:
        new_text: str: New text to display
    """
    global sprite_text_image, text_label_x_offset, current_text, scroll_id
    current_text = new_text
    sprite_text_image = text_to_sprite(new_text, text_image)
    text_label.config(image=sprite_text_image)

    # Check if the text is longer than 30 characters
    if len(new_text) > 30:
        text_label_x_offset = 0
        scroll_text()
    else:
        if scroll_id is not None:
            root.after_cancel(scroll_id)
        text_label.place(x=109, y=25)


def scroll_text():
    """
    Function to scroll the text label
    """
    global text_label_x_offset, scroll_id
    text_label.place(x=109 - text_label_x_offset, y=25)
    text_label_x_offset += 1
    if text_label_x_offset > len(current_text) * size_of_a_character_in_sprite_sheet[0]:
        text_label_x_offset = 0
    scroll_id = root.after(100, scroll_text)


def close_window(event=None):
    """
    Function to close the window
    """
    root.destroy()


def start_move(event):
    """
    Function to start moving the window

    Args:
        event: Event object
    """
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def do_move(event):
    """
    Function to move the window

    Args:
        event: Event object
    """
    x = event.x_root - start_x
    y = event.y_root - start_y
    root.geometry(f"+{x}+{y}")


# Creating the main window
root = tk.Tk()
root.title("Winamp Music Player")
root.geometry("275x116")
root.overrideredirect(True)  # Remove the default title bar

# Define the path to the skin directory
skin_path = "base_skin/"  # Adjust this to the correct path if needed

# Load skin images
background_image = load_sprite_image(os.path.join(skin_path, "MAIN.BMP"))
play_image = load_sprite_image(os.path.join(skin_path, "CBUTTONS.BMP"))
pause_image = load_sprite_image(os.path.join(skin_path, "CBUTTONS.BMP"))
stop_image = load_sprite_image(os.path.join(skin_path, "CBUTTONS.BMP"))
load_image = load_sprite_image(os.path.join(skin_path, "CBUTTONS.BMP"))
text_image = load_sprite_image(os.path.join(skin_path, "TEXT.BMP"))
titlebar_image = load_sprite_image(os.path.join(skin_path, "TITLEBAR.BMP"))

# Set background
if background_image:
    background_tk_image = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_tk_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set title bar
if titlebar_image:
    titlebar_cropped_image = crop_image('titlebar', titlebar_image, 28, 0, 275, 14)
    titlebar_label = tk.Label(root, image=titlebar_cropped_image, borderwidth=0)
    titlebar_label.place(x=0, y=0)
    titlebar_label.bind("<Button-1>", start_move)
    titlebar_label.bind("<B1-Motion>", do_move)

    # Add close area using an invisible Button with a transparent image
    transparent_image = ImageTk.PhotoImage(Image.new('RGBA', (1, 1), (0, 0, 0, 0)))
    close_button = tk.Button(root, image=transparent_image, command=close_window, borderwidth=0, bg='black')
    close_button.place(x=264, y=4, width=7, height=7)

# Create buttons with skin images
if load_image:
    btn_load = crop_image('load', load_image, 112, 0, 22, 18)
    load_button = tk.Button(root, image=btn_load, command=load_file, borderwidth=0)
    load_button.place(x=33, y=88)
if play_image:
    btn_play = crop_image('play', play_image, 23, 0, 22, 18)
    play_button = tk.Button(root, image=btn_play, command=play_music, borderwidth=0)
    play_button.place(x=87, y=88)
if pause_image:
    btn_pause = crop_image('pause', pause_image, 46, 0, 22, 18)
    pause_button = tk.Button(root, image=btn_pause, command=pause_music, borderwidth=0)
    pause_button.place(x=141, y=88)
if stop_image:
    btn_stop = crop_image('stop', stop_image, 69, 0, 22, 18)
    stop_button = tk.Button(root, image=btn_stop, command=stop_music, borderwidth=0)
    stop_button.place(x=195, y=88)

# Label to display the currently playing song
sprite_text_image = text_to_sprite("Now Playing", text_image)
text_label = tk.Label(root, image=sprite_text_image, bg="black")
text_label.place(x=109, y=25)

# Variables for scrolling text
text_label_x_offset = 0
scroll_id = None
current_text = ""

# Run the application
root.mainloop()