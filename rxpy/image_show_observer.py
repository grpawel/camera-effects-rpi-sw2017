import tkinter as tk
from PIL import Image, ImageTk
from rx import Observer


def show_frames(observable, lmain):
    class ShowingObserver(Observer):
        def on_next(self, value):
            img = Image.fromarray(value)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)

        def on_completed(self):
            # assume frame stream never ends
            pass;

        def on_error(self, error):
            raise Exception("")

    observable.subscribe(ShowingObserver())
