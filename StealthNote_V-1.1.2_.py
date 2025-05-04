# StealthNote
# -----------------------------------

# Description: StealthNote is a lightweight, secure notepad app designed for storing passwords or sharing secret messages

# Author: Futuregus

# Created: April/30th/2025

# Last Updated: May/4th/2025

# Version: 1.1.2

# Change Log:

#   - v1.1.2: Expanded on experimental Change Font option, Ran code through a AI code optimizer, fixed some small bugs.

#   - v1.1.1: Added support for making custom themes, Added experimental Change Font option to settings menu, fixed bugs.

#   - v1.0.1: Fixed a small typo causing a bug.

#   - v1.0.0: Initial release.

# -----------------------------------




# --- Imports ---
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64, os, json, datetime
import tkinter.font as tkfont


# --- Important stuff ---
SALT_SIZE = 32
backend = default_backend()
DATA_DIR = os.path.join(os.getcwd(), "StealthNote Data")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
LOG_FILE = os.path.join(DATA_DIR, "StealthNote_log.txt")  # Fixed typo
MAGIC_HEADER = b"ECTFv1.0::"
os.makedirs(DATA_DIR, exist_ok=True)



# %--- Encryption Helper Class ---%
class EncryptionHelper:
    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
            backend=backend
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    @staticmethod
    def encrypt_data(password: str, data: str) -> bytes:
        salt = os.urandom(SALT_SIZE)
        key = EncryptionHelper.derive_key(password, salt)
        encrypted = Fernet(key).encrypt(data.encode())
        return MAGIC_HEADER + salt + encrypted

    @staticmethod
    def decrypt_data(password: str, encrypted_data: bytes) -> str:
        if not encrypted_data.startswith(MAGIC_HEADER):
            raise ValueError("Invalid file format. Not a valid .ectf file.")
        encrypted_data = encrypted_data[len(MAGIC_HEADER):]
        salt = encrypted_data[:SALT_SIZE]
        encrypted = encrypted_data[SALT_SIZE:]
        key = EncryptionHelper.derive_key(password, salt)
        return Fernet(key).decrypt(encrypted).decode()
# %-------------------------------%




# %--- Settings Manager Class ---%
class SettingsManager:
    DEFAULTS = {
        "mode": "dark",
        "font_size": 16,
        "wrap": True,
        "default_dir": ""
    }

    @staticmethod
    def load_settings():
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                Logger.log_action(f"Failed to load settings: {e}")
        return SettingsManager.DEFAULTS.copy()

    @staticmethod
    def save_settings(settings):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            Logger.log_action(f"Failed to save settings: {e}")
# %-------------------------------%



# %--- File Manager Class ---%
class FileManager:
    @staticmethod
    def open_ectf(path, password):
        try:
            with open(path, "rb") as f:
                encrypted_data = f.read()
            return EncryptionHelper.decrypt_data(password, encrypted_data)
        except Exception as e:
            raise ValueError(f"Failed to open or decrypt file: {e}")

    @staticmethod
    def save_ectf(path, password, data):
        try:
            encrypted_data = EncryptionHelper.encrypt_data(password, data)
            with open(path, "wb") as f:
                f.write(encrypted_data)
        except Exception as e:
            raise ValueError(f"Failed to encrypt or save file: {e}")
# %-------------------------------%



# %--- Logger Class ---%
class Logger:
    @staticmethod
    def log_action(action: str):
        try:
            with open(LOG_FILE, 'a') as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {action}\n")
        except Exception:
            pass  # Avoid crashing on logging errors
# %-------------------------------%



# %--- Themes Class ---%
class Themes:
    THEMES_FILE = os.path.join(DATA_DIR, "themes.json")
    DEFAULT_THEMES = {
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
        "Blueprint": { "bg": "#0d1b2a", "fg": "#ffffff", "btn": "#1e3a8a", "ft": "Lucida Consolel" },
        "Seafoam Splash": { "bg": "#0082e5", "fg": "#00e563", "btn": "#00e5d6", "ft": "Impact", }
    }
# %-------------------------------%

    @staticmethod
    def load_themes():
        if not os.path.exists(Themes.THEMES_FILE) or os.stat(Themes.THEMES_FILE).st_size == 0:
            Themes.save_themes(Themes.DEFAULT_THEMES)
        try:
            with open(Themes.THEMES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            Logger.log_action(f"Failed to load themes: {e}")
            return Themes.DEFAULT_THEMES.copy()

    @staticmethod
    def save_themes(themes):
        try:
            with open(Themes.THEMES_FILE, 'w') as f:
                json.dump(themes, f)
        except Exception as e:
            Logger.log_action(f"Failed to save themes: {e}")

    @staticmethod
    def get_theme(name):
        themes = Themes.load_themes()
        return themes.get(name, themes.get("Dark", list(themes.values())[0]))



# %--- Main App Class ---%
class StealthNoteApp:

    def __init__(self, top):
        self.settings = SettingsManager.load_settings()
        self.current_mode = self.settings.get("mode", "dark")
        self.current_font_size = self.settings.get("font_size", 16)
        self.wrap_mode = tk.WORD if self.settings.get("wrap", True) else tk.NONE
        self.default_dir = self.settings.get("default_dir", "")

        self.top = top
        self.top.title("🔐 StealthNote")
        self.top.geometry("800x600")

        self.setup_menu()
        self.setup_ui()
        self.apply_theme()
        self.bind_shortcuts()


# --- Misc Functions ---
    def setup_ui(self):
        self.text = tk.Text(self.top, wrap=self.wrap_mode, font=("", self.current_font_size))
        self.text.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        self.open_btn = tk.Button(self.top, text="📂 Open", width=10, command=self.open_ectf)
        self.save_btn = tk.Button(self.top, text="💾 Save", width=10, command=self.save_ectf)
        self.clear_btn = tk.Button(self.top, text="🧹 Clear", width=10, command=self.clear_text)

        self.open_btn.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.save_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.clear_btn.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_rowconfigure(1, weight=0)
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_columnconfigure(2, weight=1)
        self.top.grid_columnconfigure(3, weight=0)

    def bind_shortcuts(self):
        self.top.bind('<Control-s>', lambda e: self.save_ectf())
        self.top.bind('<Control-o>', lambda e: self.open_ectf())
        self.top.bind('<Control-w>', lambda e: self.clear_text())
        self.top.bind('<Control-h>', lambda e: self.show_help())
        self.top.bind('<Control-q>', lambda e: self.top.quit())
        self.top.bind('<Control-f>', lambda e: self.find_text())
        self.top.bind('<Control-r>', lambda e: self.change_text_size())

    def show_about(self):
        changelog = (
            "StealthNote v1.1.2\n"
            "\nAbout:\n"
            "StealthNote is a lightweight, secure notepad app designed for storing passwords or sharing secret messages.\n"
            "Files are saved with strong AES encryption using your password.\n"
            "\nRecent Updates:\n"
            "- Expanded on experimental Change Font option \n"
            "- Ran code through a AI code optimizer\n"
        )
        messagebox.showinfo("About StealthNote", changelog)

    def apply_theme(self):
        theme = Themes.get_theme(self.current_mode)
        self.top.configure(bg=theme["bg"])
        self.text.configure(bg=theme["bg"], fg=theme["fg"], insertbackground=theme["fg"])
        self.text.configure(font=(theme["ft"], self.current_font_size))
        for btn in [self.open_btn, self.save_btn, self.clear_btn]:
            btn.configure(bg=theme["btn"])
            btn.configure(font=(theme["ft"], 10))

    def setup_menu(self):
        menubar = tk.Menu(self.top)
        self.top.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        themes_menu = tk.Menu(settings_menu, tearoff=0)

        loaded_themes = Themes.load_themes()
        for theme_name in loaded_themes.keys():
            themes_menu.add_command(
                label=theme_name,
                command=lambda name=theme_name: self.set_theme(name)
            )

        self.wrap_var = tk.BooleanVar(value=self.wrap_mode == tk.WORD)
        settings_menu.add_cascade(label="Select Theme", menu=themes_menu)
        settings_menu.add_checkbutton(label="Toggle Word Wrap", variable=self.wrap_var, command=self.toggle_wrap)
        settings_menu.add_command(label="Change Text Size", command=self.change_text_size)
        settings_menu.add_command(label="Change Font", command=self.change_font)
        settings_menu.add_command(label="Set Default Save/Open Directory", command=self.set_default_directory)
        settings_menu.add_separator()
        settings_menu.add_command(label="Reset to Default Settings", command=self.reset_to_defaults)
        menubar.add_cascade(label="⚙️ Settings", menu=settings_menu)

        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Version & Changelog", command=self.show_about)
        menubar.add_cascade(label="📜 About", menu=about_menu)

        shortcuts_menu = tk.Menu(menubar, tearoff=0)
        shortcuts_menu.add_command(label="💾 Save (Ctrl+S)", command=self.save_ectf)
        shortcuts_menu.add_command(label="📂 Open (Ctrl+O)", command=self.open_ectf)
        shortcuts_menu.add_command(label="🧹 Clear (Ctrl+W)", command=self.clear_text)
        shortcuts_menu.add_command(label="🔎 Find (Ctrl+F)", command=self.find_text)
        shortcuts_menu.add_command(label="🆎 Change Text size (Ctrl+R)", command=self.change_text_size)
        shortcuts_menu.add_command(label="❓ Help (Ctrl+H)", command=self.show_help)
        shortcuts_menu.add_command(label="❌ Quit (Ctrl+Q)", command=self.top.quit)
        menubar.add_cascade(label="🎮 Keybinds", menu=shortcuts_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="❓ How to Use StealthNote", command=self.show_help)
        menubar.add_cascade(label="🆘 Help", menu=help_menu)

    def set_theme(self, name):
        self.current_mode = name
        self.settings["mode"] = name
        SettingsManager.save_settings(self.settings)
        self.apply_theme()

    def reset_to_defaults(self):
        self.settings = SettingsManager.DEFAULTS.copy()
        self.current_mode = self.settings["mode"]
        self.current_font_size = self.settings["font_size"]
        self.wrap_mode = tk.WORD if self.settings["wrap"] else tk.NONE
        self.default_dir = self.settings["default_dir"]
        self.apply_theme()
        self.text.configure(wrap=self.wrap_mode)
        self.text.configure(font=("Consolas", self.current_font_size))
        SettingsManager.save_settings(self.settings)
        messagebox.showinfo("Settings Reset", "Settings have been reset to default.")

    def ask_password(self, prompt="Enter password"):
        def evaluate_strength(event=None):
            password = password_entry.get()
            strength = self.password_strength(password)
            strength_label.config(
                text=strength,
                fg={"Weak": "red", "Mid": "orange", "Strong": "green"}.get(strength, "black")
            )

        def submit_password(event=None):
            nonlocal entered_password
            entered_password = password_entry.get()
            password_window.destroy()

        entered_password = None
        password_window = tk.Toplevel(self.top)
        password_window.title("🔐 Password Entry")
        password_window.geometry("600x170")
        password_window.resizable(False, False)
        password_window.transient(self.top)
        password_window.grab_set()

        tk.Label(password_window, text=prompt, font=("Arial", 12)).pack(pady=10)
        password_entry = tk.Entry(password_window, show="*", font=("Arial", 12))
        password_entry.pack(pady=5, fill=tk.X, padx=20)
        password_entry.bind("<KeyRelease>", evaluate_strength)
        password_entry.bind("<Return>", submit_password)
        strength_label = tk.Label(password_window, text="Strength: ", font=("Arial", 10))
        strength_label.pack(pady=5)
        submit_button = tk.Button(password_window, text="Submit", command=submit_password)
        submit_button.pack(pady=10)
        self.top.wait_window(password_window)
        return entered_password

    def password_strength(self, password: str) -> str:
        length = len(password)
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        if length >= 12 and has_upper and has_lower and has_digit and has_special:
            return "Strong"
        elif length >= 8 and (has_upper or has_lower) and (has_digit or has_special):
            return "Mid"
        else:
            return "Weak"
# ------------------------------


# --- File Related Functions ---
    def open_ectf(self):
        path = filedialog.askopenfilename(initialdir=self.default_dir, filetypes=[("ECTF Files", "*.ectf")])
        if not path:
            return
        try:
            password = self.ask_password("Enter password to decrypt")
            decrypted_text = FileManager.open_ectf(path, password)
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, decrypted_text)
            Logger.log_action("Opened file: " + os.path.basename(path))
            messagebox.showinfo("Success", "Decrypted successfully!")
        except ValueError as e:
            Logger.log_action("Failed to open file: " + str(e))
            messagebox.showerror("Error", str(e))
        except Exception as e:
            Logger.log_action("Failed to open file: " + str(e))
            messagebox.showerror("Error", f"Failed to open or decrypt file:\n{e}")

    def save_ectf(self):
        path = filedialog.asksaveasfilename(initialdir=self.default_dir, defaultextension=".ectf", filetypes=[("ECTF Files", "*.ectf")])
        if not path:
            return
        try:
            password = self.ask_password("Enter password to encrypt.\n\nTip: password should be at least 12 characters long,\ncontain uppercase and lowercase letters, a number, and a special character.")
            data = self.text.get("1.0", tk.END).strip()
            FileManager.save_ectf(path, password, data)
            Logger.log_action("Saved file: " + os.path.basename(path))
            messagebox.showinfo("Success", "Encrypted and saved successfully!")
        except Exception as e:
            Logger.log_action("Failed to save file: " + str(e))
            messagebox.showerror("Error", f"Failed to encrypt or save file:\n{e}")

    def set_default_directory(self):
        new_dir = filedialog.askdirectory(initialdir=self.default_dir)
        if new_dir:
            self.default_dir = new_dir
            self.settings["default_dir"] = new_dir
            SettingsManager.save_settings(self.settings)
# ------------------------------


# --- Text Related functions---

    def change_font(self):
        font_window = tk.Toplevel(self.top)
        font_window.title("Select Font")
        font_families = sorted(set(tkfont.families()))
        font_selector = ttk.Combobox(font_window, values=font_families, state="readonly")
        font_selector.set("Select a font")
        font_selector.pack(pady=10)
        tk.Label(font_window, text="Or type a font name:").pack(pady=5)
        font_entry = tk.Entry(font_window)
        font_entry.pack(pady=10)

        def apply_font():
            font_name = font_entry.get().strip() or font_selector.get()
            if font_name in font_families:
                self.text.configure(font=(font_name, self.current_font_size))
                font_window.destroy()
            else:
                messagebox.showerror("Invalid Font", "Please select or type a valid font.")

        apply_button = tk.Button(font_window, text="Apply Font", command=apply_font)
        apply_button.pack(pady=5)
 
    def show_help(self):
        help_message = (
            "StealthNote Help:\n\n"
            "1. To open a file: Click '📂 Open' or press Ctrl+O, and enter the decryption password.\n"
            "2. To save a file: Click '💾 Save' or press Ctrl+S, and create encryption password (longer passwords are better).\n"
            "3. To clear the text: Click '🧹 Clear' or press Ctrl+W.\n"
            "4. Use Ctrl+F to find text in the document.\n"
            "5. Settings can be accessed from the ⚙️ menu."
        )
        messagebox.showinfo("StealthNote Help", help_message)

    def find_text(self):
        target = simpledialog.askstring("🔎 Find Text", "Enter text to find:")
        if target:
            self.text.tag_remove('found', '1.0', tk.END)
            start_pos = '1.0'
            while True:
                start_pos = self.text.search(target, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(target)}c"
                self.text.tag_add('found', start_pos, end_pos)
                self.text.tag_config('found', background='yellow', foreground='black')
                start_pos = end_pos

    def clear_text(self):
        self.text.delete("1.0", tk.END)

    def toggle_wrap(self):
        self.wrap_mode = tk.NONE if self.wrap_mode == tk.WORD else tk.WORD
        self.text.configure(wrap=self.wrap_mode)
        self.settings["wrap"] = self.wrap_mode == tk.WORD
        self.wrap_var.set(self.wrap_mode == tk.WORD)
        SettingsManager.save_settings(self.settings)

    def change_text_size(self):
        theme = Themes.get_theme(self.current_mode)
        new_size = simpledialog.askinteger("Change Text Size", "Enter new text size:", minvalue=5, maxvalue=100, initialvalue=self.current_font_size)
        if new_size:
            self.current_font_size = new_size
            self.text.configure(font=(theme["ft"], new_size))
            self.settings["font_size"] = new_size
            SettingsManager.save_settings(self.settings)
# ------------------------------

# %----------------------%

if __name__ == "__main__":
    root = tk.Tk()
    app = StealthNoteApp(root)
    root.mainloop()

