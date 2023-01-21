import tkinter as tk
from tkinter import scrolledtext
import requests
import json
import os

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
        self.web_api_username = tk.StringVar()
        self.web_api_password = tk.StringVar()
        self.api_verify_ssl_cert = tk.BooleanVar()
        self.api_label = tk.Label(self.main_window, text='Connect API IP', pady=10)
        # old input...
        # self.api_ip_input = tk.Text(self.main_window, height=1, width=20)
        # improved API IP input...
        self.api_ip_input = tk.Entry(self.main_window, textvariable=self.api_ip)
        self.api_username_label = tk.Label(self.main_window, text='Username', pady=10)
        # old input...
        # self.api_username_input = tk.Text(self.main_window, height=1, width=20)
        # improved input...
        self.api_username_input = tk.Entry(self.main_window, textvariable=self.api_username)
        # password label
        self.api_password_label = tk.Label(self.main_window, text='Password', pady=10)
        # password input
        self.api_password_input = tk.Entry(self.main_window, textvariable=self.api_password, show='*')
        # web api label
        self.web_api_username_label = tk.Label(self.main_window, text='Web API Username', pady=10)
        # web api username input
        self.web_api_username_input = tk.Entry(self.main_window, textvariable=self.web_api_username)
        # web api password label 
        self.web_api_password_label = tk.Label(self.main_window, text='Web API Password', pady=10)
        # web api password input
        self.web_api_password_input = tk.Entry(self.main_window, textvariable=self.web_api_password, show='*')
        # verify SSL certificate checkbox
        self.verify_ssl_certificate_checkbox = tk.Checkbutton(self.main_window, text='Verify SSL Certificate', variable=self.api_verify_ssl_cert, onvalue=True, offvalue=False, pady=0)
        self.success_message_textbox = tk.Label(self.main_window, text='', width=50, height=2, justify='center')
        # login button
        self.login_button = tk.Button(self.main_window, text='Login', command=self.login)
        # self.login_button = tk.Button(self.main_window, text='Login', command=connect_api_requests.get_token(self.api_ip, self.api_username, self.api_password, self.api_verify_ssl_cert))
        self.run_reports_button = tk.Button(self.main_window, text='Run Reports', command=self.run_reports)
    
    def run_reports(self):
        print('Got to "run_reports" function')

    def launch(self):
        self.api_label.pack()
        self.api_ip_input.pack()
        self.api_username_label.pack()
        self.api_username_input.pack()
        self.api_password_label.pack()
        self.api_password_input.pack()
        self.web_api_username_label.pack()
        self.web_api_username_input.pack()
        self.web_api_password_label.pack()
        self.web_api_password_input.pack()
        self.verify_ssl_certificate_checkbox.pack()
        # success message textbox
        self.success_message_textbox.pack()
        self.login_button.pack()
        self.run_reports_button.pack()
        self.main_window.mainloop()

    def login(self):
        self.api_ip = self.api_ip_input.get()
        self.api_username = self.api_username_input.get()
        self.api_password = self.api_password.get()
        self.web_api_username = self.web_api_username.get()
        self.web_api_password = self.web_api_password.get()
        print(self.api_ip, self.api_username, self.api_password, self.api_verify_ssl_cert)
        url = f'https://{str(self.api_ip)}/connect/v1/authentication/token'
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        payload = {
            'username': str(self.api_username),
            'password': str(self.api_password),
            'app_name': 'reportingmanager',
            'expiration': '86400'
        }
        web_api_req_url = f'https://{self.api_ip}/api/login'
        web_api_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        web_api_payload = f'username={self.web_api_username}&password={self.web_api_password}'
        print('Attempting to authentication to: {}'.format(url))
        try:
            print(self.api_verify_ssl_cert)
            print(type(self.api_verify_ssl_cert))
            r = requests.post(url=url, headers=headers, data=json.dumps(payload), verify=bool(self.api_verify_ssl_cert.get()))
            web_api_req = requests.post(url=web_api_req_url, headers=web_api_headers, data=web_api_payload, verify=bool(self.api_verify_ssl_cert.get()))
            if r.status_code == 200 and web_api_req.status_code == 200:
                # stopping point -- before configuring 
                self.success_message_textbox.config(text='Succesfully authenticated to:\n{}'.format(self.api_ip))
                resp_dict = r.json()
                print(json.dumps(resp_dict, sort_keys=True, indent=2))
        except Exception as e:
            print(str(e))
            print(e.__traceback__)
            self.success_message_textbox.config(text='Failed to authenticate...\n{}'.format(str(e)))
        

    # working code below!! b4 changes
    # def login(self):
    #     self.api_ip = self.api_ip_input.get()
    #     self.api_username = self.api_username_input.get()
    #     self.api_password = self.api_password.get()
    #     print(self.api_ip, self.api_username, self.api_password, self.api_verify_ssl_cert)
    #     url = f'https://{str(self.api_ip)}/connect/v1/authentication/token'
    #     headers = {'Content-Type': 'application/json; charset=utf-8'}
    #     payload = {
    #         'username': str(self.api_username),
    #         'password': str(self.api_password),
    #         'app_name': 'reportingmanager',
    #         'expiration': '86400'
    #     }
    #     print('Attempting to authentication to: {}'.format(url))
    #     try:
    #         print(self.api_verify_ssl_cert)
    #         print(type(self.api_verify_ssl_cert))
    #         r = requests.post(url=url, headers=headers, data=json.dumps(payload), verify=bool(self.api_verify_ssl_cert.get()))
    #         if r.status_code == 200:
    #             self.success_message_textbox.config(text='Succesfully authenticated to:\n{}'.format(url))
    #             resp_dict = r.json()
    #             print(json.dumps(resp_dict, sort_keys=True, indent=2))
    #     except Exception as e:
    #         print(str(e))
    #         print(e.__traceback__)
    #         self.success_message_textbox.config(text='Failed to authenticate...\n{}'.format(str(e)))






if __name__ == '__main__':
    os.chdir('PasswordLogin')
    pw_lgn_wndw = PasswordLoginWindow()
    pw_lgn_wndw.launch()