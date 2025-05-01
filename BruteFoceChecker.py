import os
import base64
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import threading

class DecryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brute Force Decryptor")
        self.root.geometry("600x300")

        # UI Elements
        self.target_file_button = tk.Button(self.root, text="Select Encrypted File", command=self.select_target_file)
        self.target_file_button.pack(pady=20)

        self.wordlist_button = tk.Button(self.root, text="Select Wordlist", command=self.select_wordlist)
        self.wordlist_button.pack(pady=20)

        self.decrypt_button = tk.Button(self.root, text="Start Decryption", state=tk.DISABLED, command=self.start_decryption)
        self.decrypt_button.pack(pady=20)

        self.result_text = tk.Text(self.root, height=5, width=50, wrap=tk.WORD)
        self.result_text.pack(pady=10)

        # Variables to store file paths
        self.target_file = None
        self.wordlist_path = None

    def select_target_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.ectf")])
        if file_path:
            self.target_file = file_path
            messagebox.showinfo("Selected File", f"Selected Encrypted File: {file_path}")
            if self.wordlist_path:
                self.decrypt_button.config(state=tk.NORMAL)

    def select_wordlist(self):
        wordlist_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if wordlist_path:
            self.wordlist_path = wordlist_path
            messagebox.showinfo("Selected Wordlist", f"Selected Wordlist: {wordlist_path}")
            if self.target_file:
                self.decrypt_button.config(state=tk.NORMAL)

    def start_decryption(self):
        if not self.target_file or not self.wordlist_path:
            messagebox.showerror("Error", "Please select both the encrypted file and the wordlist.")
            return

        # Disable the decrypt button to prevent multiple clicks
        self.decrypt_button.config(state=tk.DISABLED)

        # Start the decryption process in a separate thread
        decryption_thread = threading.Thread(target=self.decrypt_file)
        decryption_thread.start()

    def decrypt_file(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Starting brute-force decryption...\n")

        try:
            with open(self.target_file, "rb") as f:
                encrypted_data = f.read()

            salt = encrypted_data[:16]
            encrypted = encrypted_data[16:]

            with open(self.wordlist_path, "r", encoding="latin-1") as f:
                passwords = [line.strip() for line in f]

            backend = default_backend()
            for pwd in passwords:
                self.result_text.insert(tk.END, f"Trying: {pwd}\n")
                self.result_text.yview(tk.END)  # Auto-scroll to latest attempt
                try:
                    # Derive key
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=390000,
                        backend=backend
                    )
                    key = base64.urlsafe_b64encode(kdf.derive(pwd.encode()))
                    decrypted = Fernet(key).decrypt(encrypted).decode()
                    self.result_text.insert(tk.END, f"\n✅ SUCCESS!\nPassword: {pwd}\nDecrypted Content: {decrypted}\n")
                    messagebox.showinfo("Decryption Successful", f"Password: {pwd}\nDecrypted Content: {decrypted}")
                    break
                except InvalidToken:
                    continue
                except Exception as e:
                    self.result_text.insert(tk.END, f"Error: {e}\n")
                    continue
            else:
                self.result_text.insert(tk.END, "\n❌ Failed to decrypt with provided password list.\n")
                messagebox.showerror("Decryption Failed", "Failed to decrypt with the provided wordlist.")
        except Exception as e:
            self.result_text.insert(tk.END, f"\n❌ Error: {e}\n")
            messagebox.showerror("Error", f"An error occurred: {e}")

        # Re-enable the decrypt button after process completion
        self.decrypt_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = DecryptorApp(root)
    root.mainloop()
