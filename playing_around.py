import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import paramiko
import ipaddress
import requests
import json
import csv
import constants
import urllib3
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PopUpWindow():
    def __init__(self, main_window, title="Pop Up Window", labels=[], entries=[], buttons=[]):
        self.pop_up_window = tk.Toplevel()
        self.pop_up_window.title(title)
        self.width = 400
        self.height = 200
        self.screen_width = self.pop_up_window.winfo_screenwidth()
        self.screen_height = self.pop_up_window.winfo_screenheight()
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)
        self.pop_up_window.geometry("%dx%d+%d+%d" % (self.width, self.height, self.x, self.y))
        self.pop_up_window.resizable(False, False)


class MainWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Playing Around")
        self.width = 1150
        self.height = 600
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)
        self.root.geometry("%dx%d+%d+%d" % (self.width, self.height, self.x, self.y))
        self.root.resizable(True, True)
        self.canvas = tk.Canvas(self.root, width=1150, height=600)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.inner_frame = ttk.Frame(self.canvas)
        self.inner_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas.create_window(0, 0, window=self.inner_frame, anchor="nw")

    def start_program(self):
        self.root.mainloop()


main_window = MainWindow()
pop_up_window = PopUpWindow(main_window)
test_label = ttk.Label(pop_up_window.pop_up_window, text="Test Label")
main_window.start_program()