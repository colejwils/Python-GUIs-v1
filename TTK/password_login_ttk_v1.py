from tkinter import *
from tkinter.ttk import *
# import tkinter as tk
from tkinter import scrolledtext
import requests
import json
import subprocess
import runpy
import os

# top level window
# frame = Tk()
# frame.geometry('600x250')
# frame.title('Simple ForeScout API Program')

# trying centered frame here
frame = Tk()
frame.title('Login to Appliance')
# calcuate geometry adjustments...
width = 600
height = 800
screen_width = frame.winfo_screenwidth()
screen_height = frame.winfo_screenheight()
# calculate starting X and Y coordinates for the window
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
# set geometry
frame.geometry('%dx%d+%d+%d' % (width, height, x, y))

# function for getting token 
# from textbox inputs and printing  
# at a scrolled_label widget∂
def getToken():
    inp1 = input_number_1.get(1.0, 'end-1c').strip()
    inp2 = input_number_2.get(1.0, 'end-1c').strip()
    api_ip = api_input.get(1.0, 'end-1c').strip()
    print('Got API IP: {}'.format(api_ip))
    # url = 'https://10.210.20.22/connect/v1/authentication/token'
    url = 'https://{}/connect/v1/authentication/token'.format(api_ip)
    print('Attempting connection to: {}'.format(url))
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    payload = {
        'username': inp1.strip(),
        'password': inp2.strip(),
        'app_name': 'reportingmanager',
        'expiration': '86400'
    }
    print('HEADERS\n{}\nHEADERS'.format(json.dumps(headers)))
    print('PAYLOAD\n{}\nPAYLOAD'.format(json.dumps(payload)))
    try:
        print('Attempting connection...')
        r = requests.post(url=url, headers=headers, data=json.dumps(payload), verify=False)
        print(r.content)
        if r.status_code == 200:
            # print(r.content)
            # token_txt.config(text=(str(r.json()['data']['token']).strip()))
            # scrolled_text_box.insert(text=(str(r.json()['data']['token']).strip()))
            scrolled_text_box.insert(index=1.0, chars=str(r.json()['data']['token']).strip())
            expiration.config(text=str(r.json()['data']['expire_time']).strip())
        else:
            # print(r.content)
            # token_txt.config('Unknown Error with Code: {}'.format(text=str(r.status_code)))
            scrolled_text_box.insert(index=1.0, chars=str('Unknown Error with Code: {}'.format(text=str(r.status_code))))
            # scrolled_text_box.config(str('Unknown Error with Code: {}'.format(text=str(r.status_code))))
    except Exception as e:
        # token_txt.config(text=str(e))
        # scrolled_text_box.config(text=str(e))
        scrolled_text_box.insert(index=1.0, chars=str(e))
    # total = int(inp1) + int(inp2)
    # token_txt.config(text='Total: {}'.format(total))
    # token_txt.config(text = "Provided Input: "+inp1)
# function to save the config to a file 
def saveConfig():
    token_txt = scrolled_text_box.get(1.0, 'end-1c').strip()
    connect_api_ip = api_input.get(1.0, 'end-1c').strip()
    username = input_number_1.get(1.0, 'end-1c').strip()
    passwd = input_number_2.get(1.0, 'end-1c').strip()
    # encrypted pw in prog
    encr_pw = password
    print(encr_pw.get())
    config_dict = {
        'token': str(token_txt),
        'connect_ip': str(connect_api_ip),
        'username': str(username),
        'password': str(password)
    }
    f = open('config.json', 'w')
    json.dump(config_dict, f, sort_keys=True, indent=2)
    f.close()
    save_success_status_msg.pack()
    save_success_status_msg.config(text='Succesfully Saved...')
    

# function to close the window and reload the main program
def closeWindowRelaunch():  
    # subprocess.call('python -m tkinter')
    # cur_dir = (os.getcwd())
    # os.chdir('GUI')
    runpy.run_path(path_name='main_windowv0.py')
    frame.destroy()


# API IP Label
api_label = Label(frame, text='Connect API IP')
api_label.pack()
# API IP Input Label
api_input = Text(frame,
                height=1,
                width=20)
api_input.pack()
# may not work; dev to insert text because laziness is a bitch
api_input.insert(index=1.0, chars=str('10.210.20.22'))
# may not work; dev to insert text because laziness is a bitch
# Username Label Creation
input_label_1 = Label(frame, text='Username')
input_label_1.pack()
# Username Input Creation
input_number_1 = Text(frame,
                   height = 1,
                   width = 20)
input_number_1.pack()
# may not work; dev to insert text because laziness is a bitch
input_number_1.insert(index=1.0, chars=str('localaccount'))
# may not work; dev to insert text because laziness is a bitch
# Label2 Creation
input_label_2 = Label(frame, text='Password')
input_label_2.pack()

# TextBox2 Creation
input_number_2 = Text(frame,
                    height=1,
                    width=20)
input_number_2.pack()
# may not work; dev to insert text because laziness is a bitch
input_number_2.insert(index=1.0, chars=str('localaccount'))
# may not work; dev to insert text because laziness is a bitch

# HiddenPassword Label Creation
input_label_3 = Label(frame, text='Password 2.0 ;)')
input_label_3.pack()
# HiddenPassword Input Creation
password = StringVar()
passwordEntry = Entry(frame, textvariable=password, show='*')
passwordEntry.pack()

# Button Creation
get_token_button = Button(frame,
                        text='Get Token', 
                        command=getToken)
get_token_button.pack()
# Expiration Label Creation
expiration_label = Label(frame, text='Expiration', width=20)
expiration_label.pack()
# Expiration Creation
expiration = Label(frame, text='', width=20)
expiration.pack()
# Token Label Creation
# background='black',
# token_label = Label(frame, text='Token', width=20, height=1, border=10, borderwidth=0, activebackground='gray', padx=10, pady=10)
# token_label.pack()
# Token Creation
# token_txt = Label(frame, text='', width=20, height=20, wraplength=200)
# token_txt.pack()
# ScrolledTextBoxLabel
scrolled_text_box_label = Label(frame, text='Token (Beta Scroll)', width=10)
scrolled_text_box_label.pack()
# ScrolledTextBox
# note: must use the insert() method:
scrolled_text_box = scrolledtext.ScrolledText(frame)
scrolled_text_box.pack()
# SaveConfigButton
save_config_button = Button(frame,
                            text='Save Configuration',
                            command=saveConfig)
save_config_button.pack()
save_success_status_msg = Label(frame, text='', width=20)                        
# save_success_status_msg.pack()

# CloseWindowRelaunchButton
close_window_relaunch_button = Button(frame,
                                    text='Close & Relaunch',
                                    command=closeWindowRelaunch)
close_window_relaunch_button.pack()



frame.mainloop()
