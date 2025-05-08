# StealthNote Theme Maker
# -----------------------------------

# Description: 
# A tool for creating custom themes for StealthNote, allowing users to adjust background, 
# foreground, button colors, and font to match their personal style.

# Author: Futuregus and a lot of help from chatGPT

# Created: May/5th/2025

# Last Updated: May/5th/2025


import tkinter as tk
from tkinter.colorchooser import askcolor

# --- StealthNote Theme ---
theme = {
    "bg": "#0d1b2a",
    "fg": "#ffffff",
    "btn": "#1e3a8a",
    "ft": "Arial"
}

def update_preview(event=None):
    try:
        bg_color = bg_entry.get()
        fg_color = fg_entry.get()
        btn_color = btn_entry.get()
        font_name = font_label.cget("text")

        preview_frame.config(bg=bg_color)
        preview_label.config(bg=bg_color, fg=fg_color, font=(font_name, 14))
        preview_button.config(bg=btn_color, fg=fg_color, font=(font_name, 10))
    except:
        pass  # if someone types garbage like "#xyz", just don't crash lol

def pick_color(entry):
    color = askcolor()[1]
    if color:
        entry.delete(0, tk.END)
        entry.insert(0, color)
        update_preview()

def generate_output():
    theme_title = theme_title_entry.get()
    bg_color = bg_entry.get()
    fg_color = fg_entry.get()
    btn_color = btn_entry.get()
    font_name = font_label.cget("text")
    
    output = f',  "{theme_title}": {{ "bg": "{bg_color}", "fg": "{fg_color}", "btn": "{btn_color}", "ft": "{font_name}" }}'
    
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output)

def get_font():
    font = font_entry.get()
    if font:
        font_label.config(text=font)
        update_preview()

# --- Root Setup ---
root = tk.Tk()
root.title("Theme Customizer")
root.configure(bg=theme["bg"])

# Main Frame
main_frame = tk.Frame(root, bg=theme["bg"])
main_frame.pack(padx=10, pady=10)

# Editor Frame (left)
editor_frame = tk.Frame(main_frame, bg=theme["bg"])
editor_frame.pack(side="left", padx=20)

def styled_label(master, text):
    return tk.Label(master, text=text, bg=theme["bg"], fg=theme["fg"], font=(theme["ft"], 10))

def styled_button(master, text, command):
    return tk.Button(master, text=text, command=command, bg=theme["btn"], fg=theme["fg"], font=(theme["ft"], 10))

def styled_entry(master):
    entry = tk.Entry(master, font=(theme["ft"], 10), bg="#1a2d40", fg=theme["fg"], insertbackground=theme["fg"])
    entry.bind("<KeyRelease>", update_preview)
    return entry

# Theme title
styled_label(editor_frame, "Theme Title:").pack()
theme_title_entry = styled_entry(editor_frame)
theme_title_entry.unbind("<KeyRelease>")  # we don’t want title to trigger preview
theme_title_entry.pack()

# BG Color
styled_label(editor_frame, "Background Color:").pack()
bg_frame = tk.Frame(editor_frame, bg=theme["bg"])
bg_frame.pack()
bg_entry = styled_entry(bg_frame)
bg_entry.pack(side="left")
styled_button(bg_frame, "Pick", lambda: pick_color(bg_entry)).pack(side="left", padx=5)

# FG Color
styled_label(editor_frame, "Foreground Color:").pack()
fg_frame = tk.Frame(editor_frame, bg=theme["bg"])
fg_frame.pack()
fg_entry = styled_entry(fg_frame)
fg_entry.pack(side="left")
styled_button(fg_frame, "Pick", lambda: pick_color(fg_entry)).pack(side="left", padx=5)

# Button Color
styled_label(editor_frame, "Button Color:").pack()
btn_frame = tk.Frame(editor_frame, bg=theme["bg"])
btn_frame.pack()
btn_entry = styled_entry(btn_frame)
btn_entry.pack(side="left")
styled_button(btn_frame, "Pick", lambda: pick_color(btn_entry)).pack(side="left", padx=5)

# Font input
styled_label(editor_frame, "Font Name:").pack()
font_entry = styled_entry(editor_frame)
font_entry.pack()
font_label = styled_label(editor_frame, "No font selected")
font_label.pack()
styled_button(editor_frame, "Pick Font", get_font).pack()

# Generate button
styled_button(editor_frame, "Generate Output", generate_output).pack(pady=10)
styled_label(editor_frame, "Generated Output (Copyable):").pack()

output_text = tk.Text(editor_frame, height=4, width=50, bg="#1a2d40", fg=theme["fg"], font=(theme["ft"], 10), insertbackground=theme["fg"])
output_text.pack()

# Preview Frame (right)
preview_frame = tk.Frame(main_frame, bg=theme["bg"])
preview_frame.pack(side="right", padx=20)

preview_label = tk.Label(preview_frame, text="Preview Text", font=(theme["ft"], 14), fg=theme["fg"], bg=theme["bg"])
preview_label.pack(pady=20)

preview_button = tk.Button(preview_frame, text="Preview Button", font=(theme["ft"], 10), fg=theme["fg"], bg=theme["btn"])
preview_button.pack(pady=5)

# Run the app
root.mainloop()

