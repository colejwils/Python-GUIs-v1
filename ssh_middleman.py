import tkinter as tk
from tkinter import ttk
import paramiko

def ssh_login():
    # Get the SSH credentials from the GUI inputs
    host = host_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    command = command_entry.get()  # Get the command from the text box

    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SSH server
        client.connect(host, username=username, password=password)

        # Run the command on the SSH server
        stdin, stdout, stderr = client.exec_command(command)  # Use the command from the text box

        # Get the command output
        output = stdout.read().decode()

        # Update the GUI with the command output
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, output)

    except paramiko.AuthenticationException:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, 'Authentication failed.')
    except paramiko.SSHException as e:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, f'SSH error: {str(e)}')
    finally:
        # Close the SSH connection
        client.close()

# Create the main window
root = tk.Tk()
root.title('SSH Middleman')

# Create the GUI elements
host_label = ttk.Label(root, text='Host:')
host_entry = ttk.Entry(root)
username_label = ttk.Label(root, text='Username:')
username_entry = ttk.Entry(root)
password_label = ttk.Label(root, text='Password:')
password_entry = ttk.Entry(root, show='*')
command_label = ttk.Label(root, text='Command:')
command_entry = ttk.Entry(root)  # Add a new text box for entering commands
login_button = ttk.Button(root, text='Login', command=ssh_login)
result_text = tk.Text(root, height=10, width=50)

# Grid layout for the GUI elements
host_label.grid(row=0, column=0, sticky=tk.W)
host_entry.grid(row=0, column=1)
username_label.grid(row=1, column=0, sticky=tk.W)
username_entry.grid(row=1, column=1)
password_label.grid(row=2, column=0, sticky=tk.W)
password_entry.grid(row=2, column=1)
command_label.grid(row=3, column=0, sticky=tk.W)
command_entry.grid(row=3, column=1)  # Add the command text box
login_button.grid(row=4, column=0, columnspan=2)
result_text.grid(row=5, column=0, columnspan=2)  # Update the row number

# Start the main event loop
root.mainloop()