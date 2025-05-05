# StealthNote
![result](https://github.com/user-attachments/assets/9706fabc-eb83-4da7-9670-db3e21e43a8c)

StealthNote is a simple, secure, and offline encrypted text editor built with Python. It allows you to write notes and save them in a fully encrypted `.ectf` format using strong password-based encryption (Fernet + PBKDF2HMAC). Your data never leaves your device.

---

## ✨ Features

- 💾 **Encrypted Save/Load**: Secure your notes with password-based encryption.
- 🌙 **Themes**: Choose from a list of themes ([or make your own](https://docs.google.com/document/d/1Spz25jdI6UEGjVUOZ90Up5fQTI3quWvMlBbPqFUWrQs/edit?usp=sharing)) for comfortable writing.
- 🔠 **Adjustable Font Size**: Set your preferred reading/writing size.
- 📂 **Default Save/Open Directory**: Choose a starting folder for file dialogs.
- 🧹 **Clear Text Button**: Quickly wipe the editor clean.
- 🔧 **Persistent Settings**: Your preferences are saved and loaded automatically.
- 🔐 **Password Strength Validation**: Ensure a strong password with criteria like length, uppercase, lowercase, digits, and special characters.

---

## ❓ How To Install
- 1 Download the latest version of `StealthNote.zip`
- 2 Unzip `StealthNote.zip`
- 3 Run `ECTFSetup.exe` in administrator and click `Register .ECTF Extension` to proporly set up `.ectf` on your pc
- 4 You should be all set to open `StealthNote.exe`
---

## 🔐 How It Works

- When you save a note, you're prompted to enter a password.
- Password Strength: Use a strong password to keep it safer.
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

StealthNote is fully open source  the Python code is included so you can read it, run it, or even improve it yourself.

The included `StealthNote.exe` was built directly from the provided Python files using `PyInstaller`. Nothing extra, no funny business.

If you’re still unsure, you can:
Run the `.py` version directly using `Python 3.10+`
View or edit the code to verify exactly how it works
Build your own `.exe` from the same files using `PyInstaller`
If you'd like help building it yourself, feel free to reach out !

---
