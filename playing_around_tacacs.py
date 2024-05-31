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


def ssh_function(ip, username, password):
    # open an SSH session with the provided IP, username, and password
    # initial_msg_box = messagebox
    # initial_msg_box.showinfo('SSH Session', 'Opened SSH session with {} using username {}.'.format(ip, username))
    # messagebox.showinfo('SSH Session', f'Opened SSH session with {ip} using username {username}')
    # for trying to pass the ssh session back to the main window?
    outputs, result = execute_commands(hostname=ip, username=username, password=password)
    # working non-passing ssh back
    # outputs = execute_commands(hostname=ip, username=username, password=password)
    # cur_output = ''
    # for output in outputs:
        # cur_output += str(output)
    # messagebox.showinfo('Authentication Result', '{}'.format(outputs))
    if 'Failed:' not in result:
        pop_up_window.login_status_label.config(text="Status: Authenticated")
        pop_up_window.login_status_label.config(foreground="green")
        pop_up_window.login_button.config(state="disabled")
        # messagebox.showinfo('Authentication Result', 'Successful Authentication')

def execute_commands(hostname, username, password, commands_to_exec=None):
    print(hostname, username, password, commands_to_exec)
    # set up SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect to remote server
    ssh.connect(hostname=hostname, username=username, password=password)

    update_status = False
    
    # execute commands
    commands = ['ls -l', 'df -h']
    if commands_to_exec:
        commands = commands_to_exec
        update_status = True
    outputs = []
    for cmd in commands:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        result = 'Successful Authentication'
        if error:
            result = ('Failed: {} \n Error Information: {}\n'.format(cmd, error))
            print(result)
            
        outputs.append(output)

    # print outputs
    for output in outputs:
        print(output)

    global SESSION 
    SESSION = ssh
    global APPLIANCE_IP
    APPLIANCE_IP = hostname
    global HOST
    HOST = None
    global USERNAME
    USERNAME = None
    global PASSWORD
    PASSWORD = None
    
    # close SSH conn
    # ssh.close()
    # wonder if i can pass the ssh session back 
    # return ssh, outputs
    if update_status:
        main_window.command_result_label.config(text=outputs)
    return outputs, result

class PopUpWindow():
    def __init__(self, main_window, title="Pop Up Window", labels=[], entries=[], buttons=[]):
        self.main_window = main_window
        self.pop_up_window = tk.Toplevel()
        self.pop_up_window.title(title)
        self.width = 500
        self.height = 200
        self.screen_width = self.pop_up_window.winfo_screenwidth()
        self.screen_height = self.pop_up_window.winfo_screenheight()
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)
        self.pop_up_window.geometry("%dx%d+%d+%d" % (self.width, self.height, self.x, self.y))
        self.pop_up_window.resizable(False, False)
        self.login_status_label = ttk.Label(self.pop_up_window, text="Status: Unauthenticated")
        self.login_status_label.grid(row=0, column=3, columnspan=2, padx=10, pady=10)
        self.login_status_label.config(foreground="red")
        self.host_label = ttk.Label(self.pop_up_window, text="Host")
        self.host_label.grid(row=0, column=0, padx=10, pady=10)
        self.host_entry = ttk.Entry(self.pop_up_window)
        self.host_entry.grid(row=0, column=1, padx=10, pady=10)
        self.username_label = ttk.Label(self.pop_up_window, text="Username")
        self.username_label.grid(row=1, column=0, padx=10, pady=10)
        self.username_entry = ttk.Entry(self.pop_up_window)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)
        self.password_label = ttk.Label(self.pop_up_window, text="Password")
        self.password_label.grid(row=2, column=0, padx=10, pady=10)
        self.password_entry = ttk.Entry(self.pop_up_window)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)
        self.login_button = ttk.Button(self.pop_up_window, text="Login", command=lambda: ssh_function(self.host_entry.get(), self.username_entry.get(), self.password_entry.get()))
        self.host = self.host_entry.get()
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


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
        self.command_label = ttk.Label(self.inner_frame, text="Commands")
        self.command_label.grid(row=0, column=0, padx=10, pady=10)
        self.command_result_label = ttk.Label(self.inner_frame, text="Command Results")
        self.command_result_label.grid(row=1, column=0, padx=10, pady=10)
        self.command_entry = ttk.Entry(self.inner_frame)
        self.command_entry.grid(row=0, column=1, padx=10, pady=10)
        self.send_button = ttk.Button(self.inner_frame, text="Execute Command", command=lambda: execute_commands(HOST, USERNAME, PASSWORD, self.command_entry.get()))
        self.send_button.grid(row=0, column=3, padx=10, pady=10)

    def start_program(self):
        self.root.mainloop()


main_window = MainWindow('TACACS++ ForeScout Edition PoC')
pop_up_window = PopUpWindow(main_window, title="Login")

# pop_up_window = PopUpWindow(main_window, title="Login")
# host_label = ttk.Label(pop_up_window.pop_up_window, text="Host")
# host_label.grid(row=0, column=0, padx=10, pady=10)
# host_entry = ttk.Entry(pop_up_window.pop_up_window)
# host_entry.grid(row=0, column=1, padx=10, pady=10)
# username_label = ttk.Label(pop_up_window.pop_up_window, text="Username")
# username_label.grid(row=1, column=0, padx=10, pady=10)
# username_entry = ttk.Entry(pop_up_window.pop_up_window)
# username_entry.grid(row=1, column=1, padx=10, pady=10)
# password_label = ttk.Label(pop_up_window.pop_up_window, text="Password")
# password_label.grid(row=2, column=0, padx=10, pady=10)
# password_entry = ttk.Entry(pop_up_window.pop_up_window)
# password_entry.grid(row=2, column=1, padx=10, pady=10)
# login_button = ttk.Button(pop_up_window.pop_up_window, text="Login")
# login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

main_window.start_program()
# print(main_window.host, main_window.username, main_window.password)s