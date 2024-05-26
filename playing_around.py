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
    def __init__(self, title='Playing Around'):
        self.root = tk.Tk()
        self.root.title(title)
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


main_window = MainWindow('Policy Parser')

pop_up_window = PopUpWindow(main_window, title="Login")
username_label = ttk.Label(pop_up_window.pop_up_window, text="Username")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = ttk.Entry(pop_up_window.pop_up_window)
username_entry.grid(row=0, column=1, padx=10, pady=10)
password_label = ttk.Label(pop_up_window.pop_up_window, text="Password")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = ttk.Entry(pop_up_window.pop_up_window)
password_entry.grid(row=1, column=1, padx=10, pady=10)
login_button = ttk.Button(pop_up_window.pop_up_window, text="Login")
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

main_window.start_program()