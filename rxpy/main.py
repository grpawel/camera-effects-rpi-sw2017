import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from rx import Observable
from frame_observable import CameraFeed
from image_show_observer import show_frames
from rx.concurrency import ThreadPoolScheduler


def setup_gui():
    window = tk.Tk()  # Makes main window
    window.wm_title("Camera feed")
    window.config(background="#FFFFFF")
    # Graphics window
    imageFrame = tk.Frame(window, width=600, height=500)
    imageFrame.grid(row=0, column=0, padx=10, pady=2)
    # Capture video frames
    lmain = tk.Label(imageFrame)
    lmain.grid(row=0, column=0)
    return window, lmain

def main():
    window, lmain = setup_gui()
    scheduler = ThreadPoolScheduler(1)
    observer = Observable.from_(CameraFeed())
    observer.subscribe_on(scheduler)
    show_frames(observer, lmain, window)
    window.mainloop()
    

if __name__ == "__main__":
    main()
