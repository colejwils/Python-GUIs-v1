import tkinter as tk
from tkinter import scrolledtext
# no request handling necessary. use mine or another requests module built for making Connect API requests.
# the module can be found at https://github.com/colejwils/fs-connect-api-requests-v1 (in prog)
# import requests
import json
import os
import connect_api_requests

class PasswordLoginWindow():
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title = 'Authenticate'
        self.width = 600
        self.height = 800
        self.screen_width = self.main_window.winfo_screenwidth()
        self.screen_height = self.main_window.winfo_screenheight()
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)
        self.main_window.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        self.api_ip = tk.StringVar()
        self.api_username = tk.StringVar()
        self.api_password = tk.StringVar()
        self.api_label = tk.Label(self.main_window, text='Connect API IP')
        # old input...
        # self.api_ip_input = tk.Text(self.main_window, height=1, width=20)
        # improved API IP input...
        self.api_ip_input = tk.Entry(self.main_window, textvariable=self.api_ip)
        self.api_username_label = tk.Label(self.main_window, text='Username')
        # old input...
        # self.api_username_input = tk.Text(self.main_window, height=1, width=20)
        # improved input...
        self.api_username_input = tk.Entry(self.main_window, textvariable=self.api_username)
        # password label
        self.api_password_label = tk.Label(self.main_window, text='Password')
        # password input
        self.api_password_input = tk.Entry(self.main_window, textvariable=self.api_password, show='*')
        # login button
        self.login_button = tk.Button(self.main_window, text='Login', command=self.login())
        # success message textbox
        self.success_message_textbox = 
    
    def launch(self):
        self.api_label.pack()
        self.api_ip_input.pack()
        self.api_username_label.pack()
        self.api_username_input.pack()
        self.api_password_label.pack()
        self.api_password_input.pack()
        self.login_button.pack()
        self.main_window.mainloop()
    
    def login(self):
        token = connect_api_requests.get_token()






if __name__ == '__main__':
    os.chdir('PasswordLogin')
    pw_lgn_wndw = PasswordLoginWindow()
    pw_lgn_wndw.launch()