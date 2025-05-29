import tkinter as tk
from tkinter import messagebox
import subprocess
import ctypes
import os
import sys

# Function to check if the script is run with admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Get a file in the same directory as the script/exe
def get_local_file(file_name):
    base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, file_name)
    return file_path if os.path.isfile(file_path) else None

# Get a file in the StealthNoteAssets subdirectory
def get_asset_file(file_name):
    base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    asset_path = os.path.join(base_dir, "StealthNoteAssets", file_name)
    return asset_path if os.path.isfile(asset_path) else None

# Function to register the .ectf extension
def register_extension():
    if not is_admin():
        messagebox.showerror("Error", "This script requires administrative privileges. Please run as Administrator.")
        return

    # Locate files
    stealthnote_path = get_local_file("StealthNote_v1.2.1.exe")
    icon_path = get_asset_file("ECTF.ico")

    if not stealthnote_path or not icon_path:
        messagebox.showerror(
            "Error",
            f"Could not find required files:\n"
            f"{'StealthNote_v1.2.1.exe not found' if not stealthnote_path else ''}\n"
            f"{'ECTF.ico not found in StealthNoteAssets' if not icon_path else ''}"
        )
        return

    try:
        # Registry commands
        commands = [
            rf'reg add "HKEY_CLASSES_ROOT\.ectf" /ve /d "StealthNote.ECTF" /f',
            rf'reg add "HKEY_CLASSES_ROOT\StealthNote.ECTF" /ve /d "StealthNote File" /f',
            rf'reg add "HKEY_CLASSES_ROOT\StealthNote.ECTF\shell\open\command" /ve /d "\"{stealthnote_path}\" \"%1\"" /f',
            rf'reg add "HKEY_CLASSES_ROOT\StealthNote.ECTF\DefaultIcon" /ve /d "\"{icon_path}\"" /f'
        ]

        for command in commands:
            subprocess.run(command, shell=True, check=True)

        messagebox.showinfo("Success", "File association for .ectf registered successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to register file association:\n{e}")

# Function to deregister the .ectf extension
def deregister_extension():
    if not is_admin():
        messagebox.showerror("Error", "This script requires administrative privileges. Please run as Administrator.")
        return

    try:
        commands = [
            r'reg delete "HKEY_CLASSES_ROOT\.ectf" /f',
            r'reg delete "HKEY_CLASSES_ROOT\StealthNote.ECTF" /f'
        ]

        for command in commands:
            subprocess.run(command, shell=True, check=True)

        messagebox.showinfo("Success", ".ectf file association has been deregistered successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to deregister file association:\n{e}")

# GUI setup
root = tk.Tk()
root.title(".ECTF File Association Manager")
root.geometry("400x250")
root.resizable(False, False)

label = tk.Label(root, text=".ECTF File Association Manager", font=("Arial", 14))
label.pack(pady=20)

register_button = tk.Button(root, text="Register .ECTF Extension", command=register_extension, font=("Arial", 12), bg="blue", fg="white")
register_button.pack(pady=10)

deregister_button = tk.Button(root, text="Deregister .ECTF Extension", command=deregister_extension, font=("Arial", 12), bg="red", fg="white")
deregister_button.pack(pady=10)

root.mainloop()

