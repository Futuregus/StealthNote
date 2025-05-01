# StealthNote
![result](https://github.com/user-attachments/assets/9706fabc-eb83-4da7-9670-db3e21e43a8c)

StealthNote is a simple, secure, and offline-first encrypted text editor built with Python and Tkinter. It allows you to write notes and save them in a fully encrypted `.ectf` format using strong password-based encryption (Fernet + PBKDF2HMAC). Your data never leaves your device.

---

## ✨ Features

- 💾 **Encrypted Save/Load**: Secure your notes with password-based encryption.
- 🌙 **Themes**: Choose from a list of themes for comfortable writing.
- 🔠 **Adjustable Font Size**: Set your preferred reading/writing size.
- 📂 **Default Save/Open Directory**: Choose a starting folder for file dialogs.
- 🧹 **Clear Text Button**: Quickly wipe the editor clean.
- 🔧 **Persistent Settings**: Your preferences are saved and loaded automatically.
- 🔐 **Password Strength Validation**: Ensure a strong password with criteria like length, uppercase, lowercase, digits, and special characters.

---

## 🔐 How It Works

- When you save a note, you're prompted to enter a password.
- **Password Strength**: Your password must be at least 12 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character. This ensures your note is securely encrypted.
- The note is encrypted with a random salt + Fernet encryption using your password.
- The resulting `.ectf` file contains both the salt and the encrypted message.
- To open a note, you must enter the same password you used to save it.

---

## ❗ Disclaimer

The `.ectf` files are **not secure against brute-force attacks** if you choose a weak password. StealthNote uses strong encryption (Fernet + PBKDF2HMAC), but its security entirely depends on the strength of the password you provide.

Always choose a **strong, unique password** — at least 12 characters long, with a mix of uppercase and lowercase letters, numbers, and special characters.

You can test how secure your password is against brute-force attacks by:

- Downloading the included `BruteForceChecker.py` script.
- Trying it with tools like [`RockYou.txt`](https://github.com/brannondorsey/naive-hashcat/releases) to simulate a real-world brute-force attempt.

Your password is the **ONLY** way to decrypt your notes.  
**Do not lose or forget it — there is no password recovery mechanism.**

---
