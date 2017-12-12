from queue import Queue

import cv2
import thread
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

frames = Queue()

def read_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        frames.put(frame)

def main():
    root = tk.Tk()
    root.wm_title("Camera")
    imageFrame = tk.Frame(root, width=600, height=600)
    imageFrame.grid(row=0, column=0, padx=10, pady=2)
    # Capture video frames
    lmain = tk.Label(imageFrame)
    lmain.grid(row=0, column=0)
    thread.start_new_thread(read_camera, ())

    def task():
        cv2img = frames.get()
        img = Image.fromarray(cv2img)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        root.update()

    while True:
        task()




if __name__ == "__main__":
    main()