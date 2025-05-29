import tkinter as tk
from tkinter import messagebox
import subprocess
import ctypes
import os

# Function to check if the script is run with admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to search for a file in common directories
def find_file(file_name):
    # Common directories to search
    search_dirs = [
        os.getenv("ProgramFiles(x86)"),
        os.getenv("ProgramFiles"),
        os.getenv("USERPROFILE") + "\\Downloads",
        os.getenv("USERPROFILE") + "\\Desktop",
        os.getenv("USERPROFILE") + "\\Documents"
    ]

    # Search for the file
    for directory in search_dirs:
        for root, dirs, files in os.walk(directory):
            if file_name in files:
                return os.path.join(root, file_name)
    return None

# Function to register the .ectf extension
def register_extension():
    if not is_admin():
        messagebox.showerror("Error", "This script requires administrative privileges. Please run as Administrator.")
        return

    # Locate the StealthNote executable and ECTF.ico
    stealthnote_path = find_file("StealthNote_v1.2.0.exe")
    icon_path = find_file("ECTF.ico")

    if not stealthnote_path or not icon_path:
        messagebox.showerror(
            "Error",
            f"Could not find required files:\n"
            f"{'StealthNote_v1.2.0.exe not found' if not stealthnote_path else ''}\n"
            f"{'ECTF.ico not found' if not icon_path else ''}"
        )
        return

    try:
        # Registry commands for registration
        commands = [
            rf'reg add "HKEY_CLASSES_ROOT\.ectf" /ve /d "StealthNote.ECTF" /f',
            rf'reg add "HKEY_CLASSES_ROOT\StealthNote.ECTF" /ve /d "StealthNote File" /f',
            rf'reg add "HKEY_CLASSES_ROOT\StealthNote.ECTF\shell\open\command" /ve /d "\"{stealthnote_path}\" \"%1\"" /f',
            rf'reg add "HKEY_CLASSES_ROOT\StealthNote.ECTF\DefaultIcon" /ve /d "\"{icon_path}\"" /f'
        ]

        # Execute each command
        for command in commands:
            subprocess.run(command, shell=True, check=True)

        # Notify the user of success
        messagebox.showinfo("Success", "File association for .ectf registered successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to register file association:\n{e}")

# Function to deregister the .ectf extension
def deregister_extension():
    if not is_admin():
        messagebox.showerror("Error", "This script requires administrative privileges. Please run as Administrator.")
        return

    try:
        # Registry commands for deregistration
        commands = [
            r'reg delete "HKEY_CLASSES_ROOT\.ectf" /f',
            r'reg delete "HKEY_CLASSES_ROOT\StealthNote.ECTF" /f'
        ]

        # Execute each command
        for command in commands:
            subprocess.run(command, shell=True, check=True)

        # Notify the user of success
        messagebox.showinfo("Success", ".ectf file association has been deregistered successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to deregister file association:\n{e}")

# Create the GUI
root = tk.Tk()
root.title(".ECTF File Association Manager")

# GUI Window Size
root.geometry("400x250")
root.resizable(False, False)

# Add a Label
label = tk.Label(root, text=".ECTF File Association Manager", font=("Arial", 14))
label.pack(pady=20)

# Add Buttons for Register and Deregister
register_button = tk.Button(root, text="Register .ECTF Extension", command=register_extension, font=("Arial", 12), bg="blue", fg="white")
register_button.pack(pady=10)

deregister_button = tk.Button(root, text="Deregister .ECTF Extension", command=deregister_extension, font=("Arial", 12), bg="red", fg="white")
deregister_button.pack(pady=10)

# Run the GUI loop
root.mainloop()
