# StealthNote
#  ──────────────────────────────────────────────────────────────────────────────

# Description:
# StealthNote is a secure notetaking app that allows users to encrypt notes with a password.
#  designed for, keeping notes secret, making it suitable for people who need to keep their notes private and secure

# Author: Futuregus and a little help from chatGPT

# Created: April / 30th / 2025

# Last Updated: May / 29th / 2025

# Version: 1.2.1

# License: MIT License

#  ──────────────────────────────────────────────────────────────────────────────

# Change Log:



#   - v1.2.1:
#       • Security improvements to .ectf file format
#       • Split the code into multiple files for better organization


#   - v1.2.0:
#       • Added Stealth Mode for quickly hiding notes
#       • Introduced a loading screen for improved UX
#       • Enhanced Find & Replace functionality
#       • Made code follow my CHOP system (Comment Header Organization System for Python)
#       • Optimized code for better performance and readability
#       • Improved logging for easier debugging and tracking
#       • Included a hidden mini game (easter egg)

#   - v1.1.3:
#       • Minor bug fixes
#       • Set StealthNote Theme as the default
#       • Polished Help and About menus
#       • Implemented automatic update checking
#       • Added a hidden mini game

#   - v1.1.2:
#       • Expanded the experimental Change Font feature
#       • Applied AI-assisted code optimization
#       • Fixed several minor bugs

#   - v1.1.1:
#       • Added support for custom themes
#       • Introduced experimental Change Font option
#       • Resolved various bugs

#   - v1.0.1:
#       • Fixed a typo-related bug

#   - v1.0.0:
#       • Initial release

#  ──────────────────────────────────────────────────────────────────────────────


# --- Imports ---
import random
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import os, json
import tkinter.font as tkfont
import urllib.request
from packaging import version
import subprocess
from utils.logtofile import Logger
from utils.assetLoader import AssetLoader
from utils.fileManager import FileManager
from utils.settingsManager import SettingsManager
# ----------------------


# --- Important stuff ---
DATA_DIR = os.path.join(os.getcwd(), "StealthNote Data")
LOG_FILE = os.path.join(DATA_DIR, "StealthNote_Log.txt")
Logger.configure(data_dir=DATA_DIR, log_file="StealthNote_Log.txt")
os.makedirs(DATA_DIR, exist_ok=True)
# ----------------------


# --- Functions ---

# ~~--- text Window Function ---~~
# Description: Creates a text window with a scrollbar and a message.
def create_text_window(parent, title, message, width=50, height=10):

    window = tk.Toplevel(parent)
    window.title(title)
    window.geometry("400x300")
    window.resizable(False, False)
    window.config(bg="#0d1b2a")

    title_label = tk.Label(
        window,
        text=title,
        font=("Lucida Console", 14, "bold"),
        bg="#0d1b2a",
        fg="#ffffff"
    )
    title_label.pack(pady=10)

    # Frame for text + scrollbar
    text_frame = tk.Frame(window, bg="#0d1b2a")
    text_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget = tk.Text(
        text_frame,
        wrap=tk.WORD,
        font=("Lucida Console", 10),
        height=height,
        width=width,
        bg="#0d1b2a",
        fg="#ffffff",
        insertbackground="#ffffff",
        yscrollcommand=scrollbar.set,
        relief=tk.FLAT
    )
    text_widget.insert(tk.END, message)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar.config(command=text_widget.yview)

    close_button = tk.Button(
        window,
        text="Close",
        command=window.destroy,
        font=("Lucida Console", 10),
        bg="#1e3a8a",
        fg="#ffffff",
        activebackground="#274baf",
        activeforeground="#ffffff"
    )
    close_button.pack(pady=10)

    window.grab_set()
    parent.wait_window(window)

    return window, text_widget

# ~~---------------------~~

# ~~--- Loading Screen Function ---~~
# Description: Creates a loading screen with a progress bar and label.
def show_loading_screen():
    splash = tk.Toplevel()
    splash.title("Loading StealthNote...")
    splash.update_idletasks()
    width = 400
    height = 120
    x = (splash.winfo_screenwidth() // 2) - (width // 2)
    y = (splash.winfo_screenheight() // 2) - (height // 2)
    splash.geometry(f"{width}x{height}+{x}+{y}")
    splash.resizable(False, False)

    splash_label = tk.Label(splash, text="Loading StealthNote...", font=("Helvetica", 14))
    splash_label.pack(pady=10)

    progress = ttk.Progressbar(splash, orient="horizontal", mode="determinate", length=300)
    progress.pack(pady=10)
    progress["maximum"] = 100
    splash.update()

    def update_progress(step, text=""):
        progress["value"] = step
        splash_label.config(text=text)
        splash.update_idletasks()

    return splash, update_progress
# ~~---------------------~~

# ----------------------


# --- Start Message ---
Logger.log_action("------------------------------------", separator=True)
Logger.log_action("StealthNote Starting...", tag="INFO")
Logger.log_action("Version: 1.2.1", tag="INFO")
Logger.log_action("------------------------------------", separator=True)
# ----------------------


# %--- Themes Class ---%
class Themes:

    THEMES_FILE = os.path.join(DATA_DIR, "themes.json")

    DEFAULT_THEMES = {
        "StealthNote": { "bg": "#0d1b2a", "fg": "#ffffff", "btn": "#1e3a8a", "ft": "Lucida Console" },
        "Dark": { "bg": "#2e2e2e", "fg": "white", "btn": "#666", "ft": "Arial" },
        "Light": { "bg": "#eaf2f8", "fg": "black", "btn": "#057cfc", "ft": "Arial" },
        "Forest": { "bg": "#2d3e30", "fg": "#e1ffe1", "btn": "#558b2f", "ft": "Gabriola" },
        "Ocean": { "bg": "#021f3f", "fg": "#d0efff", "btn": "#0288d1", "ft": "Comic Sans MS" },
        "Midnight Purple": { "bg": "#1e1b2e", "fg": "#e0d6f5", "btn": "#5e4b8b", "ft": "Palatino Linotype" },
        "Solar Flare": { "bg": "#fff3e0", "fg": "#4e342e", "btn": "#ff8f00", "ft": "Trebuchet MS" },
        "Cyberpunk": { "bg": "#0f0f1f", "fg": "#39ff14", "btn": "#ff007f", "ft": "Courier New" },
        "Desert Sand": { "bg": "#f4e2d8", "fg": "#5c3a21", "btn": "#d4a373", "ft": "Arial" },
        "Arctic Ice": { "bg": "#e0f7fa", "fg": "#01579b", "btn": "#4dd0e1", "ft": "Franklin Gothic Medium" },
        "Retro Pixel": { "bg": "#2d2d2d", "fg": "#fcee09", "btn": "#e60012", "ft": "Small Fonts" },
        "Seafoam Splash": { "bg": "#0082e5", "fg": "#00e563", "btn": "#00e5d6", "ft": "Impact", }
    }

#  +--- Theme Methods ---+
    @staticmethod
    def load_themes():
        if not os.path.exists(Themes.THEMES_FILE) or os.stat(Themes.THEMES_FILE).st_size == 0:
            Themes.save_themes(Themes.DEFAULT_THEMES)
        try:
            with open(Themes.THEMES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            Logger.log_action(f"Failed to load themes: {e}", tag="ERROR")
            return Themes.DEFAULT_THEMES.copy()

    @staticmethod
    def save_themes(themes):
        try:
            with open(Themes.THEMES_FILE, 'w') as f:
                json.dump(themes, f)
        except Exception as e:
            Logger.log_action(f"Failed to save themes: {e}", tag="ERROR")

    @staticmethod
    def get_theme(name):
        themes = Themes.load_themes()
        return themes.get(name, themes.get("StealthNote", list(themes.values())[0]))
#  +----------------------+

# %----------------------%


#* %--- Main App class ---%
# Description: The heart of StealthNote

class StealthNoteApp:

#  +--- Start up app ---+
    def __init__(self, top):

        # Show loading screen
        splash, update_progress = show_loading_screen()


        # Step 1: Load settings
        update_progress(10, "Loading settings...")
        self.settings = SettingsManager.load_settings()
        self.stealthmode_save_path = self.settings.get("stealthmode_save_path", "")


    # Step 2: Load theme & font info
        update_progress(30, "Applying theme...")
        self.current_theme = self.settings.get("theme", "StealthNote")
        self.current_font_size = self.settings.get("font_size", 16)
        self.wrap_mode = tk.WORD if self.settings.get("wrap", True) else tk.NONE
        self.default_dir = self.settings.get("default_dir", "")


        # Step 3: Load assets
        update_progress(50, "Loading assets...")
        asset_loader = AssetLoader(asset_folders=["StealthNoteAssets"])


        # Step 4: Setup main window
        update_progress(70, "Building UI...")
        self.top = top
        self.top.title("StealthNote")
        self.top.geometry("800x600")
        icon_path = asset_loader.find_asset("SNlogo40x40.ico")
        self.top.iconbitmap(icon_path)

        # Step 5: Apply stuff
        update_progress(85, "Finishing setup...")
        self.setup_menus()
        self.setup_ui()
        self.apply_theme()
        self.bind_shortcuts()

        # Step 6: Check for updates
        update_progress(100, "Checking for updates...")
        self.check_for_updates()
        Logger.log_action("StealthNote started successfully.", tag="INFO")
        Logger.log_action("-------------------------------------", separator=True)

        # Done with splash
        splash.destroy()

#  +----------------------+


#  +--- Misc Methods ---+

    def setup_menus(self):

        # === Helpers ===
        def create_menu(parent, label, tearoff=0):
            menu = tk.Menu(parent, tearoff=tearoff)
            parent.add_cascade(label=label, menu=menu)
            return menu

        def add_commands(menu, commands):
            for label, command in commands:
                if label == "SEPARATOR":
                    menu.add_separator()
                else:
                    menu.add_command(label=label, command=command)
        # ======================

        # === Create Menubar ===
        menubar = tk.Menu(self.top)
        self.top.config(menu=menubar)
        # ======================

        # === ⚙️ Settings Menu ===
        settings_menu = create_menu(menubar, "⚙️ Settings")
        themes_menu = tk.Menu(settings_menu, tearoff=0)

        # -- Load Themes --
        loaded_themes = Themes.load_themes()
        for theme_name in loaded_themes:
            themes_menu.add_command(
                label=theme_name,
                command=lambda name=theme_name: self.set_theme(name)
            )
        # ------------------

        self.wrap_var = tk.BooleanVar(value=self.wrap_mode == tk.WORD)
        settings_menu.add_cascade(label="Select Theme", menu=themes_menu)
        settings_menu.add_checkbutton(label="Toggle Word Wrap", variable=self.wrap_var, command=self.toggle_wrap)

        add_commands(settings_menu, [
            ("Change Text Size", self.change_text_size),
            ("Change Font", self.change_font),
            ("SEPARATOR", None),
            ("Set Stealth Mode Save Path", self.set_stealthmode_save_path),
            ("Set Default Save/Open Directory", self.set_default_directory),
            ("SEPARATOR", None),
            ("Reset to Default Settings", self.reset_to_defaults)
        ])
        # ==========================

        # === 🎮 Keybinds Menu ===
        shortcuts_menu = create_menu(menubar, "🎮 Keybinds")
        add_commands(shortcuts_menu, [
            ("💾 Save (Ctrl+S)", self.save_ectf),
            ("📂 Open (Ctrl+O)", self.open_ectf),
            ("SEPARATOR", None),
            ("🧹 Clear (Ctrl+W)", self.clear_text),
            ("🔎 Find (Ctrl+F)", self.find_and_replace),
            ("🆎 Change Text size (Ctrl+R)", self.change_text_size),
            ("SEPARATOR", None),
            ("Stealth Mode (Alt+X)", self.activate_StealthMode),
            ("❓ Help (Ctrl+H)", self.show_help),
            ("❌ Quit (Ctrl+Q)", self.top.quit)
        ])
        # =========================

        # === 📜 About Menu ===
        about_menu = create_menu(menubar, "📜 About")
        add_commands(about_menu, [
            ("About", self.show_about),
            ("Changelog", self.show_changelog),
            ("SEPARATOR", None),
            ("🗣Feedback", self.open_feedback_form),
            ("Open Log File", self.open_log_file)
        ])
        # ======================

        # === 🆘 Help Menu ===
        help_menu = create_menu(menubar, "🆘 Help")
        add_commands(help_menu, [
            ("❓ How to Use StealthNote", self.show_help),
            ("How to Use StealthMode", self.show_stealthmode_help)
        ])

        # =====================

    def setup_ui(self):

        # === Text Editor ===
        self.text = tk.Text(self.top, wrap=self.wrap_mode, font=("", self.current_font_size))
        self.text.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        # ====================

        # === Buttons ===
        self.open_btn = tk.Button(self.top, text="📂 Open", width=10, command=self.open_ectf)
        self.save_btn = tk.Button(self.top, text="💾 Save", width=10, command=self.save_ectf)
        self.clear_btn = tk.Button(self.top, text="🧹 Clear", width=10, command=self.clear_text)

        self.open_btn.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.save_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.clear_btn.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        # =================

        # === Grid Weight Config ===
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_rowconfigure(1, weight=0)

        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_columnconfigure(2, weight=1)
        self.top.grid_columnconfigure(3, weight=0)
        # ==========================

    def apply_theme(self):

        theme = Themes.get_theme(self.current_theme)

        # === Apply Theme to editor ===
        self.top.configure(bg=theme["bg"])
        self.text.configure(
            bg=theme["bg"],
            fg=theme["fg"],
            insertbackground=theme["fg"],
            font=(theme["ft"], self.current_font_size)
        )
        # ======================

        # === Apply Theme to buttons ===
        for btn in [self.open_btn, self.save_btn, self.clear_btn]:
            btn.configure(
                bg=theme["btn"],
                font=(theme["ft"], 10)
            )
        # ======================

    def bind_shortcuts(self):

        # === File Operations ===
        self.top.bind('<Control-s>', lambda e: self.save_ectf())
        self.top.bind('<Control-o>', lambda e: self.open_ectf())
        self.top.bind('<Control-w>', lambda e: self.clear_text())
        # ======================

        # === Help and Quit ===
        self.top.bind('<Control-h>', lambda e: self.show_help())
        self.top.bind('<Control-q>', lambda e: self.top.quit())
        # ======================

        # === Editor Features ===
        self.top.bind('<Control-f>', lambda e: self.find_and_replace())
        self.top.bind('<Control-r>', lambda e: self.change_text_size())
        self.top.bind('<Alt-x>', lambda e: self.activate_StealthMode())
        # ======================

        # === Secret Mini game ===
        self.top.bind('<Control-Shift-Alt-F12>', lambda e: self.launch_stealthnote_type_race())
        # ======================

    def check_for_updates(self):
        current_version = "1.2.1"

        try:
            with urllib.request.urlopen("https://raw.githubusercontent.com/Futuregus/StealthNote/main/latest_version.txt") as response:
                latest_version = response.read().decode('utf-8').strip()

            if version.parse(latest_version) > version.parse(current_version):
                messagebox.showinfo("Update Available", f"🚨 NEW UPDATE AVAILABLE!\nCurrent: {current_version} → New: {latest_version}\nVisit GitHub to download.")
            else:
                Logger.log_action("You're Up to date.", tag="INFO")
        except Exception as e:
            Logger.log_action(f"Failed to check for updates: {e}", tag="ERROR")

    def reset_to_defaults(self):

        Default_Settings = SettingsManager.DEFAULTS.copy() # Load default settings
        self.settings = SettingsManager.DEFAULTS.copy()

        # === Apply default settings ===
        self.current_theme = Default_Settings["theme"]
        self.current_font_size = Default_Settings["font_size"]
        self.wrap_mode = tk.WORD if Default_Settings["wrap"] else tk.NONE
        self.default_dir = Default_Settings["default_dir"]
        self.stealthmode_save_path = Default_Settings["stealthmode_save_path"]
        self.apply_theme()
        self.text.configure(wrap=self.wrap_mode)
        self.text.configure(font=("Lucida Console", self.current_font_size))
        SettingsManager.save_settings(self.settings)
        messagebox.showinfo("Settings Reset", "Settings have been reset to default.")
        Logger.log_action("Settings reset to defaults.", tag="INFO")
        # ============================

    def show_about(self):

        about_message = (
            "StealthNote\n"
            "\nAbout:\n"
            "StealthNote is a secure offline notetaking app that allows users to encrypt notes with a password.\n"
            "It is designed for keeping notes secret, making it suitable for people who need to keep their notes private and secure.\n"
            "\nAuthor: Futuregus\n"
            "\nCreated: April 30th, 2025\n"
            "\nLast Updated: May 27th, 2025\n"
            "\nVersion: 1.2.1\n"
            "\nLicense: MIT License\n"
        )

        create_text_window(self.top, "About StealthNote", about_message)

    def show_changelog(self):
        changelog_message = (
            "StealthNote v1.2.1 Changelog:\n"
            "\n- Security improvements to .ectf file format \n"
            "\n- Split the code into multiple files for better organization\n"
        )
        create_text_window(self.top, "Changelog", changelog_message)

    def show_help(self):
        help_message = (
            "1. To save a file: Click '💾 Save' or press Ctrl+S. Create an encryption password (the longer, the better).\n\n"
            "2. To open a file: Click '📂 Open' or press Ctrl+O. You will be prompted to enter the decryption password (the one entered to encrypt it).\n\n"
            "3. To clear the text: Click '🧹 Clear' or press Ctrl+W to erase all content in the editor.\n\n"
            "4. To search for specific text: Press Ctrl+F, then enter the text you want to find in the document.\n\n"
            "5. Settings can be accessed from the ⚙️ menu.\n"
            "\nPro Tips:\n"
            "- Longer passwords = stronger security 💪\n\n"
            "- Avoid sharing your password with your dog 🐶 (they're bad at remembering it)\n"

        )

        create_text_window(self.top, "StealthNote Help", help_message)

    def show_stealthmode_help(self):
        help_message = (


            "StealthMode allows you to quickly hide your notes and cover them with a calculator app.\n"
            "\n"
            "- WARNING ⚠️: StealthMode saves your notes in plain text format, which is not encrypted.\n"
            "\n"
            "1. Set a save path for StealthMode in the ⚙️ Settings menu.\n\n"
            "2. Activate StealthMode by pressing Alt+X.\n\n"
            "3. The main window will hide, and a calculator will open.\n\n"
            "4. Your notes will be saved to the specified path in plain text format.\n\n"
        )

        create_text_window(self.top, "StealthMode Help", help_message)

    def open_log_file(self):
        try:
            # Check if the log file exists
            if not os.path.exists(LOG_FILE):
                messagebox.showinfo("Info", "Log file doesn't exist yet!")
                return

            # Open the log file in Notepad
            subprocess.Popen(['notepad.exe', LOG_FILE])

            Logger.log_action("==========================", separator=True)
            Logger.log_action("Opened log file in Notepad.\n" \
            "If you want to clear the log file, you can safely delete it, and it will be recreated next time you run StealthNote.", separator=True, tag="INFO")
            Logger.log_action("==========================", separator=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open log file in Notepad:\n{e}")
            Logger.log_action(f"Failed to open log file in Notepad: {e}", tag="ERROR")

    def open_feedback_form(self):
        feedback_url = "https://docs.google.com/forms/d/e/1FAIpQLSeW7fitNl-KFbtdv2LSdwAyxZuJ6_kfiT2m0TcfYJ-KFJoysA/viewform"
        try:
            subprocess.Popen(['start', feedback_url], shell=True)
            Logger.log_action("Opened feedback form in web browser.", tag="INFO")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open feedback form:\n{e}")
            Logger.log_action(f"Failed to open feedback form: {e}", tag="ERROR")

    def set_theme(self, name):
        self.current_theme = name
        self.settings["theme"] = name
        SettingsManager.save_settings(self.settings)
        self.apply_theme()

#  +----------------------+


#  +--- File related methods ---+

    def ask_password(self, prompt="Enter password"):

        # === Strength Evaluator ===
        def evaluate_strength(event=None):
            password = password_entry.get()
            strength = self.password_strength(password)
            strength_label.config(
                text=strength,
                fg={"Weak": "red", "Mid": "orange", "Strong": "green"}.get(strength, "black")
            )
        # =====================

        # === Submit Handler ===
        def submit_password(event=None):
            nonlocal entered_password
            entered_password = password_entry.get()
            password_window.destroy()
        # =====================

        # === Setup Window ===
        entered_password = None
        password_window = tk.Toplevel(self.top)
        password_window.title("🔐 Password Entry")
        password_window.geometry("600x170")
        password_window.resizable(False, False)
        password_window.transient(self.top)
        password_window.grab_set()
        # =====================

        # === Add Widgets ===
        tk.Label(password_window, text=prompt, font=("Arial", 12)).pack(pady=10)
        password_entry = tk.Entry(password_window, show="*", font=("Arial", 12))
        password_entry.pack(pady=5, fill=tk.X, padx=20)
        password_entry.bind("<KeyRelease>", evaluate_strength)
        password_entry.bind("<Return>", submit_password)

        strength_label = tk.Label(password_window, text="Strength: ", font=("Arial", 10))
        strength_label.pack(pady=5)

        submit_button = tk.Button(password_window, text="Submit", command=submit_password)
        submit_button.pack(pady=10)
        # =====================

        # === Await Response ===
        self.top.wait_window(password_window)
        return entered_password
        # =====================

    def password_strength(self, password: str) -> str:
        length = len(password)

        # === Character Checks ===
        has_upper   = bool(re.search(r'[A-Z]', password))
        has_lower   = bool(re.search(r'[a-z]', password))
        has_digit   = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        # =====================

        # === Strength Logic ===
        if length >= 12 and has_upper and has_lower and has_digit and has_special:
            return "Strong"
        elif length >= 8 and (has_upper or has_lower) and (has_digit or has_special):
            return "Mid"
        else:
            return "Weak"
        # =====================

    def open_ectf(self):

        # === File Dialog ===
        path = filedialog.askopenfilename(initialdir=self.default_dir, filetypes=[("ECTF Files", "*.ectf")])
        if not path:
            return
        # ====================

        # === Decrypt File ===
        try:
            password = self.ask_password("Enter password to decrypt")
            decrypted_text = FileManager.open_ectf(path, password)
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, decrypted_text)
            Logger.log_action("Opened file: " + os.path.basename(path), tag="INFO")
            messagebox.showinfo("Success", "Decrypted successfully!")
        # =====================

        # === Error Handling ===
        except ValueError as e:
            Logger.log_action("Failed to open file: " + str(e), tag="ERROR")
            messagebox.showerror("Error", str(e))

        except Exception as e:
            Logger.log_action("Failed to open file: " + str(e), tag="ERROR")
            messagebox.showerror("Error", f"Failed to open or decrypt file:\n{e}")
        # =====================

    def save_ectf(self):

        # === File Dialog ===
        path = filedialog.asksaveasfilename(initialdir=self.default_dir, defaultextension=".ectf", filetypes=[("ECTF Files", "*.ectf")])
        if not path:
            return
        # =====================

        # === Encrypt and Save File ===
        try:
            password = self.ask_password("Enter password to encrypt.\n\nTip: password should be at least 12 characters long,\ncontain uppercase and lowercase letters, a number, and a special character.")
            data = self.text.get("1.0", tk.END).strip()
            FileManager.save_ectf(path, password, data)
            Logger.log_action("Saved file: " + os.path.basename(path), tag="INFO")
            messagebox.showinfo("Success", "Encrypted and saved successfully!")
        # =====================

        # === Error Handling ===
        except Exception as e:
            Logger.log_action("Failed to save file: " + str(e), tag="ERROR")
            messagebox.showerror("Error", f"Failed to encrypt or save file:\n{e}")
        # =====================

    def set_default_directory(self):
        new_dir = filedialog.askdirectory(initialdir=self.default_dir)
        if new_dir:
            self.default_dir = new_dir
            self.settings["default_dir"] = new_dir
            SettingsManager.save_settings(self.settings)
            Logger.log_action(f"Default directory set to: {new_dir}", tag="INFO")

#  +----------------------+


#  +--- Stealth Mode ---+

    def set_stealthmode_save_path(self):
        save_path = filedialog.asksaveasfilename(
            initialdir=os.path.expanduser("~"),
            title="Select StealthMode Save File",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if save_path:
            self.stealthmode_save_path = save_path
            self.settings["stealthmode_save_path"] = save_path
            SettingsManager.save_settings(self.settings)
            Logger.log_action(f"StealthMode save path set to: {save_path}", tag="INFO")
            messagebox.showinfo("Success", f"StealthMode save path set to: {save_path}")
        else:
            messagebox.showerror("Error", "No file selected. StealthMode save path not set.")

    def activate_StealthMode(self):

        if not self.stealthmode_save_path or self.stealthmode_save_path == "BLANK": # Check if save path is set

            messagebox.showerror("Error", "No Stealth Mode save path set!\nPlease set a path in Settings before using Stealth Mode.")
            Logger.log_action("Stealth Mode activation failed: No save path set.", tag="ERROR")

            return
        # === Stealth Mode Activation ===
        Logger.log_action("Stealth Mode activated.", tag="INFO")
        self.top.iconify()  # hide the main window
        subprocess.Popen("calc.exe")  # open calculator
        self.StealthMode_Save()  # save the text content to a file
        # =====================

    def StealthMode_Save(self):
        content = self.text.get("1.0", tk.END).strip()
        save_path = self.stealthmode_save_path or os.path.join(self.stealthmode_save_path)
        try:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(content)
            Logger.log_action(f"Text saved to {save_path} in plain text format.", tag="INFO")
            self.top.quit()
        except Exception as e:
            Logger.log_action(f"StealthMode save failed: {e}", tag="ERROR")
            messagebox.showerror("Error", f"StealthMode save failed: {e}")

#  +----------------------+


#  +--- Secret mini game ---+

    def launch_stealthnote_type_race(self):

        # === Word List Setup ===
        words = [
            "notebook", "encryption", "stealth", "password", "hacker", "secure",
            "python", "window", "keyboard", "secret", "StealthNote", "click", "focus",
            "code", "score", "byte", "binary", "cipher", "ghost", "Vault",
            "Key", "Lock", "Hide", "Escape", "Firewall", "Download", "Override",
            "Supercalifragilisticexpialidocious"
        ]

        def generate_word():
            return random.choice(words)
        # =====================

        # === Game Window Setup ===
        game_window = tk.Toplevel(self.top)
        game_window.title("StealthNote Type Race")
        game_window.geometry("400x200")
        game_window.config(bg="#0d1b2a")
        # =====================

        # === Game State Variables ===
        score = tk.IntVar(value=0)
        target = tk.StringVar(value=generate_word())
        timer = tk.IntVar(value=30)
        # =====================

        # === UI Elements ===
        tk.Label(
            game_window, textvariable=target, font=("Lucida Console", 18),
            fg="white", bg="#0d1b2a"
        ).pack(pady=20)

        entry = tk.Entry(game_window, font=("Lucida Console", 16))
        entry.pack()
        entry.focus()

        score_label = tk.Label(
            game_window, textvariable=score, font=("Lucida Console", 14),
            fg="white", bg="#0d1b2a"
        )
        score_label.pack(pady=10)

        timer_label = tk.Label(
            game_window, textvariable=timer, font=("Lucida Console", 14),
            fg="white", bg="#0d1b2a"
        )
        timer_label.pack(pady=10)
        # =====================

        # === Game Timer Logic ===
        def update_timer():
            current_time = timer.get()
            if current_time > 0:
                timer.set(current_time - 1)
                game_window.after(1000, update_timer)
            else:
                game_window.after(1000, end_game)
        # =====================

        # === End Game Behavior ===
        def end_game():
            game_window.destroy()
            tk.messagebox.showinfo("Time's Up!", f"Your final score: {score.get()}")
        # =====================

        # === Input Checking ===
        def check_input(event):
            if entry.get() == target.get():
                score.set(score.get() + 1)
            target.set(generate_word())
            entry.delete(0, tk.END)
        # =====================

        # === Event Binding & Start ===
        entry.bind("<Return>", check_input)
        update_timer()
        # =====================

#  +----------------------+


#  +--- Text Related Methods ---+

    def change_font(self):

        # === Window Creation ===
        font_window = tk.Toplevel(self.top)
        font_window.title("Select Font")
        font_families = sorted(set(tkfont.families()))
        font_selector = ttk.Combobox(font_window, values=font_families, state="readonly")
        font_selector.set("Select a font")
        font_selector.pack(pady=10)
        tk.Label(font_window, text="Or type a font name:").pack(pady=5)
        font_entry = tk.Entry(font_window)
        font_entry.pack(pady=10)
        # =====================

        def apply_font():

            font_name = font_entry.get().strip() or font_selector.get() # Get font from entry or combobox
            if font_name in font_families:  # Check if font is valid
                self.text.configure(font=(font_name, self.current_font_size)) # Apply selected font
                font_window.destroy() # Close the font selection window

            else: # Invalid font handling
                messagebox.showerror("Invalid Font", "Please select or type a valid font.")

        # === Apply Font Button ===
        apply_button = tk.Button(font_window, text="Apply Font", command=apply_font)
        apply_button.pack(pady=5)
        # =====================

    def find_and_replace(self, event=None):

        # === Popup Window for Find & Replace ===
        popup = tk.Toplevel(self.top)
        popup.title("📝 Find & Replace")
        popup.transient(self.top)
        popup.resizable(False, False)
        popup.grab_set()
        # =====================

        # === Layout for Find & Replace ===
        tk.Label(popup, text="Find:").grid(row=0, column=0, padx=5, pady=5)
        find_entry = tk.Entry(popup, width=30)
        find_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(popup, text="Replace with:").grid(row=1, column=0, padx=5, pady=5)
        replace_entry = tk.Entry(popup, width=30)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)
        # =====================

        # === Text Tag for Found Matches ===
        self.text.tag_config('found', background='yellow', foreground='black')
        # =====================

        def do_find():
        # Description: Finds text in the editor and highlights it.

            # === Find Logic ===
            target = find_entry.get()
            if not target:
                messagebox.showwarning("Input Required", "Please enter text to find.")
                return

            self.text.tag_remove('found', '1.0', tk.END)

            start_pos = '1.0'
            found_any = False

            while True:
                start_pos = self.text.search(target, start_pos, stopindex=tk.END, nocase=True)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(target)}c"
                self.text.tag_add('found', start_pos, end_pos)
                if not found_any:
                    self.text.see(start_pos)
                    self.text.mark_set(tk.INSERT, start_pos)
                start_pos = end_pos
                found_any = True

            if not found_any:
                messagebox.showinfo("No Matches", f"No matches found for '{target}'.")
            # =====================

        def do_replace_all():
        # Description: Replaces all occurrences of text in the editor.

            # === Replace Logic ===
            target = find_entry.get()
            replacement = replace_entry.get()

            if not target:
                messagebox.showwarning("Input Required", "Please enter text to find.")
                return

            self.text.tag_remove('found', '1.0', tk.END)

            start_pos = '1.0'
            count = 0

            while True:
                start_pos = self.text.search(target, start_pos, stopindex=tk.END, nocase=True)
                if not start_pos:
                    break

                end_pos = f"{start_pos}+{len(target)}c"
                self.text.delete(start_pos, end_pos)
                self.text.insert(start_pos, replacement)

                new_end_pos = f"{start_pos}+{len(replacement)}c"
                self.text.tag_add('found', start_pos, new_end_pos)

                start_pos = new_end_pos
                count += 1

            if count == 0:
                messagebox.showinfo("No Matches", f"No matches found for '{target}'.")
            else:
                messagebox.showinfo("Replaced", f"Replaced {count} occurrence(s).")
        # =====================

        # === Buttons for Find & Replace ===
        btn_frame = tk.Frame(popup)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        find_btn = tk.Button(btn_frame, text="Find", command=do_find)
        find_btn.grid(row=0, column=0, padx=5)

        replace_btn = tk.Button(btn_frame, text="Replace All", command=do_replace_all)
        replace_btn.grid(row=0, column=1, padx=5)
        # =====================

        find_entry.focus()

    def clear_text(self):
        self.text.delete("1.0", tk.END)

    def toggle_wrap(self):
        self.wrap_mode = tk.NONE if self.wrap_mode == tk.WORD else tk.WORD
        self.text.configure(wrap=self.wrap_mode)
        self.settings["wrap"] = self.wrap_mode == tk.WORD
        self.wrap_var.set(self.wrap_mode == tk.WORD)
        SettingsManager.save_settings(self.settings)

    def change_text_size(self):
        theme = Themes.get_theme(self.current_theme)
        new_size = simpledialog.askinteger("Change Text Size", "Enter new text size:", minvalue=5, maxvalue=100, initialvalue=self.current_font_size)
        if new_size:
            self.current_font_size = new_size
            self.text.configure(font=(theme["ft"], new_size))
            self.settings["font_size"] = new_size
            SettingsManager.save_settings(self.settings)

#  +----------------------+


# %----------------------%


# Run StealthNote
if __name__ == "__main__":
    root = tk.Tk()
    app = StealthNoteApp(root)
    root.mainloop()