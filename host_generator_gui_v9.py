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

"""
Copyright 2023 (C)
Cole Wilson
cole@colejwils.com
"""

SESSION = None
CONNECT_TOKEN = None
APPLIANCE_IP = None
HOSTS = None

def run_function(commands=['ls -l', 'df -h']):
    # add the code to call functions based on this template and return its output
    # commands = ['ls -l', 'df -h']
    cmd_output = run_commands_with_session(commands)
    output = 'Executed successfully.'
    output_label.config(text='{}\n\n{}'.format(str(output), str(''.join(cmd_output))))
    
def create_connect_host(update_data):
    print(update_data)
    pass    

def fstool_commands(ip, hosts):
    base_command = 'fstool hostinfo_update -P '
    print(hosts)
    print(hosts.keys())
    outputs = []
    for tag in hosts.keys():
        val = hosts.get(tag)
        print(tag, val)
        if len(val) == 1:
            rand_val = val[0]
        
        elif isinstance(val, list):
            rand_val = random.choice(val)
        
        print(tag, rand_val)
        cmd = '{}{} -O {} {}'.format(base_command, str(tag), str(rand_val), str(ip))
        print(cmd)
        # outputs = []
        stdin, stdout, stderr = SESSION.exec_command(cmd)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        outputs.append(output)
        if error:
            print('{} {}'.format(cmd, error))
            outputs.append(error)
            outputs.append(cmd)
    return outputs
    
def fstool_commands_v2(host, ip):
    outputs = []
    for cmd in host:
        cmd = (cmd.replace('<IP_MAC>', str(ip)))
        # outputs = []
        stdin, stdout, stderr = SESSION.exec_command(cmd)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        outputs.append(output)
        print(output)
        if error:
            print('{} {}'.format(cmd, error))
            outputs.append(error)
            outputs.append(cmd)
    return outputs

def generate_hosts_function_v2(ip_cidr, start_mac='020000000000'):
    mac_iterator = 0
    ip_net = ipaddress.IPv4Network(ip_cidr)
    # TO DO: function to create connect hosts
    # create_connect_host(update_data)
    use_real_data = (use_real_data_var.get())
    if use_real_data:
        for host in HOSTS:
            ip = None
            mac = None
            host_lines = []
            for line in host:
                if '-N -P "ip" -O' in line:
                    ip = line.split('-N -P "ip" -O ')[1].split(' ')[0].replace('"', '')
                elif '-N -P "mac" -O' in line:
                    mac = line.split('-N -P "mac" -O ')[1].split(' ')[0].replace('"', '')
            for line in host:
                # host_lines.append(line.replace('<IP_MAC>', str(ip)))
                host_lines.append(line)
            fstool_commands_v2(host_lines, str(ip))
            # fstool_commands_v2(host_lines, str('192.168.0.233'))
    else:
        host_iterator = 0
        for ip in ip_net:
            if str(ip)[-2:] != '.0' and str(ip)[-2:] != '.255':
                mac_iterator += 1
                mac_iterator_len = len(str(mac_iterator))
                mac = '{}{}'.format(start_mac[:-mac_iterator_len], str(mac_iterator))
                # print(len(HOSTS[host_iterator]))
                host = HOSTS[host_iterator]
                fstool_commands_v2(host, str(ip))
                # for line in host:
                    # print(line.replace('<IP_MAC>', str(ip)))
                    
                if host_iterator >= len(HOSTS):
                    host_iterator = 0
                else:
                    host_iterator += 1
                # TO DO: function to use fstool hostinfo_update to update the host's properties
                    # outputs = fstool_commands(ip, hosts)
                    # for output in outputs:
                        # print(output)
            
            
    output_label.config(text='{}\n\n{}'.format(str(len(HOSTS)), str(ip_cidr)))
    print(APPLIANCE_IP)
    
def login():
    # window for the login prompt
    login_window = tk.Toplevel(root)
    login_window.title('SSH Login')

    # labels and entry fields for the appliance IP, username, and password
    ip_label = ttk.Label(login_window, text='Appliance IP: ')
    ip_label.grid(column=0, row=0, padx=5, pady=5)
    ip_entry = ttk.Entry(login_window)
    ip_entry.grid(column=1, row=0, padx=5, pady=5)

    username_label = ttk.Label(login_window, text='Username: ')
    username_label.grid(column=0, row=1, padx=5, pady=5)
    username_entry = ttk.Entry(login_window)
    username_entry.grid(column=1, row=1, padx=5, pady=5)

    password_label = ttk.Label(login_window, text='Password: ')
    password_label.grid(column=0, row=2, padx=5, pady=5)
    password_entry = ttk.Entry(login_window, show='*')
    password_entry.grid(column=1, row=2, padx=5, pady=5)

    # Create a login button that calls the ssh_function with the provided IP, username, and password
    login_button = ttk.Button(login_window, text='Login', command=lambda: ssh_function(ip_entry.get(), username_entry.get(), password_entry.get()))
    login_button.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

def execute_commands(hostname, username, password):
    # set up SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect to remote server
    ssh.connect(hostname=hostname, username=username, password=password)

    # execute commands
    commands = ['ls -l', 'df -h']
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
    
    # close SSH conn
    # ssh.close()
    # wonder if i can pass the ssh session back 
    # return ssh, outputs
    return outputs, result

def run_commands_with_session(commands):
    # messagebox classes pop up separately and can get annoying.
    # initial_msg_box = messagebox
    # initial_msg_box.showinfo('Running', 'Commands are executing. Cole is a superhero :)')
    if SESSION != None:
        outputs = []
        for cmd in commands:
            stdin, stdout, stderr = SESSION.exec_command(cmd)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            if error:
                print('Some kind of error during execution: {} \n Error Information: {}\n'.format(cmd, error))
            outputs.append(output)
        
        for output in outputs:
            print(output)
        
        # better to just create 
        result_msg_box = messagebox
        result_msg_box.showinfo('Result', '{}'.format(''.join(outputs)))
        
        return outputs
           
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
        result_msg_box = messagebox
        # result_msg_box.showinfo('Authentication Result', '{}'.format(''.join(outputs)))
        # ****** to change the connect status label add this code to wherever you need it **********
        # connect_status_label.config(text='Authenticated')
        appliance_label.config(text='{}{}'.format('Appliance: ', str(APPLIANCE_IP)))
        ssh_status_label.config(text='SSH Status: Authenticated')
        root.update()
        # result_msg_box.askokcancel('Authentication Successful', 'Sucessfully authenticated to appliance: {}\nInformation:\n{}'.format(ip, result))
        
    elif 'Failed:' in result:
        result_msg_box = messagebox
        # result_msg_box.showinfo('Authentication Result', '{}'.format(''.join(outputs)))
        # ****** to change the connect status label add this code to wherever you need it **********
        # connect_status_label.config(text='Authenticated')
        ssh_status_label.config(text='SSH Status: Unathenticated')
        root.update()
        # result_msg_box.askokcancel(title='Authentication Failed', message='Failed to authenticate to: {}\nInformation:\n{}'.format(ip, result))
        
def add_row():
    # determine the row number for the new row
    row_num = len(data_entries)
    
    # create the key and value labels and entry fields for the new row
    tag_row_num = row_num + 1
    key_label = ttk.Label(inner_frame, text='ForeScout Continuum Tag: ')
    key_label.grid(column=0, row=tag_row_num, padx=5, pady=5)
    key_label_entries.append(key_label)
    data_labels.append(key_label)
    
    key_entry = ttk.Entry(inner_frame)
    key_entry.grid(column=1, row=tag_row_num, padx=5, pady=5)
    data_entries.append(key_entry)
    key_data_entries.append(key_entry)
    
    value_row_num = row_num + 1
    value_label = ttk.Label(inner_frame, text='Comma-Separated Values: ')
    value_label.grid(column=2, row=value_row_num, padx=5, pady=5)
    data_labels.append(value_label)
    value_label_entries.append(value_label)
    
    value_entry = ttk.Entry(inner_frame)
    value_entry.grid(column=3, row=value_row_num, padx=5, pady=5)
    data_entries.append(value_entry)
    value_data_entries.append(value_entry)
   
    canvas.config(scrollregion=canvas.bbox('all'))
    
    # # configures the root window to expand vertically as new rows are added
    # root.grid_rowconfigure(row_num+2, weight=1)

def remove_row():
    if (len(key_data_entries) == 1) or (len(key_label_entries) == 1) or (len(value_data_entries) == 1) or (len(value_label_entries) == 1):
        pass
    else:
        
        # remove the last entry
        key_entry_len = len(key_data_entries)
        print(key_entry_len)
        key_entry = key_data_entries.pop(key_entry_len-1)
        key_entry.destroy()
        
        key_label_len = len(key_label_entries)
        key_label = key_label_entries.pop(key_label_len-1)
        key_label.destroy()
        
        value_label_len = len(value_label_entries)
        value_label = value_label_entries.pop(value_label_len-1)
        value_label.destroy()
        
        value_entry_len = len(value_data_entries)
        value_entry = value_data_entries.pop(value_entry_len-1)
        value_entry.destroy()
        
    

# Update the canvas scroll region to exclude the removed row
def load_from_csv():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            lines = [i for i in reader]
            hosts = []
            for line in lines:
                host_commands = []
                for key, value in line.items():
                    if constants.WEB_API_FIELDS.get(key) and value:
                        host_command = ('fstool hostinfo_update -N -P "{}" -O "{}" <IP_MAC>'.format(constants.WEB_API_FIELDS.get(key), value))
                        host_commands.append(host_command)
                hosts.append(host_commands)
            global HOSTS
            HOSTS = hosts
            # print(HOSTS)
            csv_status_label.config(text='Loaded from Data File: {}'.format(str(file_path)))
            # return hosts
        

root = tk.Tk()
root.title('Upstart Cyber ForeScout Host Generator v0.0.1')


# create the IP CIDR network label and entry field
ip_label = ttk.Label(root, text='IPv4 Network (CIDR): ')
ip_label.grid(column=0, row=0, padx=5, pady=5)
ip_entry = ttk.Entry(root)
ip_entry.grid(column=1, row=0, padx=5, pady=5)

# create the canvas and inner fame for the key and value text boxes
canvas = tk.Canvas(root, width=1150, height=300)
canvas.grid(column=0, row=1, columnspan=8, padx=5, pady=5)

inner_frame = ttk.Frame(canvas)


scrollbar = ttk.Scrollbar(root, orient='vertical', command=canvas.yview)
# scrollbar = ttk.Scrollbar(inner_frame, orient='vertical', command=canvas.yview)

scrollbar.grid(column=9, row=1, sticky='NS', padx=5, pady=5)
canvas.config(yscrollcommand=scrollbar.set)
canvas.create_window((0,0), window=inner_frame, anchor='nw')
inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

data_entries = []
data_labels = []

key_data_entries = []
key_label_entries = []
value_data_entries = []
value_label_entries = []

# Create the key and value labels and entry fields for the first row
key_label = ttk.Label(inner_frame, text='ForeScout Continuum Tag:')
key_label.grid(column=0, row=0, padx=5, pady=5)
data_labels.append(key_label)
key_label_entries.append(key_label)

key_entry = ttk.Entry(inner_frame)
key_entry.grid(column=1, row=0, padx=5, pady=5)
data_entries.append(key_entry)
key_data_entries.append(key_entry)

value_label = ttk.Label(inner_frame, text='Comma-Separated Values:')
value_label.grid(column=2, row=0, padx=5, pady=5)
data_labels.append(value_label)
value_label_entries.append(value_label)

value_entry = ttk.Entry(inner_frame)
value_entry.grid(column=3, row=0, padx=5, pady=5)
data_entries.append(value_entry)
value_data_entries.append(value_entry)



# Add the plus and minus buttons for adding and removing rows
plus_button = ttk.Button(inner_frame, text='+', command=add_row)
plus_button.grid(column=7, row=0, padx=5, pady=5)

minus_button = ttk.Button(inner_frame, text='-', command=lambda: remove_row())
minus_button.grid(column=6, row=0, padx=5, pady=5)

# create the load from CSV file button
load_from_csv_button = ttk.Button(root, text='Load from CSV', command=load_from_csv)
load_from_csv_button.grid(column=0, row=2, 
columnspan=4, padx=5, pady=5)

# create the run button
generate_hosts_button = ttk.Button(root, text='Generate Hosts', command=lambda: generate_hosts_function_v2(ip_entry.get()))
generate_hosts_button.grid(column=0, row=3, columnspan=4, padx=5, pady=5)

# create the run button
run_button = ttk.Button(root, text='Run', command=run_function)
run_button.grid(column=0, row=4, columnspan=4, padx=5, pady=5)

# create the SSH login button
login_button = ttk.Button(root, text='Login to SSH', command=login)
login_button.grid(column=0, row=5, columnspan=4, padx=5, pady=5)

# create the Connect login button
# connect_login_button = ttk.Button(root, text='Connect Login', command=connect_login)
# connect_login_button.grid(column=0, row=6, columnspan=4, padx=5, pady=5)

# create the output label
output_label = ttk.Label(root, text='')
output_label.grid(column=0, row=7, columnspan=4, padx=5, pady=5)


appliance_label = ttk.Label(root, text='Appliance: ')
appliance_label.grid(column=3, row=4, columnspan=4, padx=5, pady=5)

ssh_status_label = ttk.Label(root, text='SSH Status: Unauthenticated')
ssh_status_label.grid(column=3, row=5, columnspan=4, padx=5, pady=5)

# create the Connect Authentication Status label
# connect_status_label = ttk.Label(root, text='Connect Status: Unauthenticated')
# connect_status_label.grid(column=3, row=6, columnspan=4, padx=5, pady=5)

# create the CSV file loaded status label
csv_status_label = ttk.Label(root, text='Loading from Data File: None')
csv_status_label.grid(column=3, row=6, columnspan=4, padx=5, pady=5)

# create the "Use Real Data" checkbox
use_real_data_var = tk.BooleanVar()
use_real_data_checkbox = ttk.Checkbutton(root, text="Use Real Data", variable=use_real_data_var)
use_real_data_checkbox.grid(column=3, row=7, columnspan=4, padx=5, pady=5)

# set window size
width = 1150
height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

root.geometry('{}x{}+{}+{}'.format(width, height, x, y))



# root.geometry=('1280x720')
root.resizable(True, True)
root.mainloop()
