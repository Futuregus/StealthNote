# 🕵️‍♂️ StealthNote

![result](https://github.com/user-attachments/assets/9706fabc-eb83-4da7-9670-db3e21e43a8c)

**StealthNote** is a simple, secure, and offline encrypted text editor built in Python. It lets you write private notes and save them in a fully encrypted `.ectf` format using strong password-based encryption (Fernet + PBKDF2HMAC).  
⚠️ Your data never leaves your device. Ever.

---

## ✨ Features

- 💾 **Encrypted Save/Load** – Secure your notes with password-based encryption.
- 🌙 **Themes** – Choose from pre-made themes ([or make your own](https://docs.google.com/document/d/1Spz25jdI6UEGjVUOZ90Up5fQTI3quWvMlBbPqFUWrQs/edit?usp=sharing)).
- 🔠 **Adjustable Font Size** – Set the font to your perfect writing vibe.
- 📂 **Default Save/Open Folder** – Set your favorite folder as the starting point.
- 🧹 **Clear Text Button** – Wipe your text instantly.
- 🔧 **Persistent Settings** – Remembers your preferences every time you open it.
- 🛡️ **Password Strength Check** – Warns you if your password is weak sauce.

---

## 🛠️ How To Install

1. Download the latest `StealthNote.zip`
2. Unzip it
3. Run `ECTFSetup.exe` as administrator and click **Register .ECTF Extension**
4. You're all set — launch `StealthNote.exe` and start writing!

---

## 🔐 How It Works

- When saving a note, you’ll be prompted to enter a password.
- The app uses your password + a random salt to encrypt your data using Fernet.
- The `.ectf` file contains both the salt and the encrypted content.
- You’ll need to enter the same password to open it again.

---

## ⚠️ Important Security Info

The encryption is **strong**, but it’s only as strong as your password.  
A weak password = easy target for brute-force attacks.

💡 Tips:
- Use a **unique**, strong password (at least 12+ characters)
- Mix UPPER/lowercase, numbers, and symbols
- Test it out with the included `BruteForceChecker.py`

🧠 Reminder: There’s **no recovery** if you forget your password. Seriously. Don’t lose it.

---

## 👀 Is It Safe?

Yep — the Python code is fully open source and included with every release.

The `.exe` file was made straight from that code using `PyInstaller`. No tracking, no sketchy stuff, no mystery meat.

Still skeptical? Here's what you can do:

- Run the `.py` version with Python 3.10+
- Read or edit the code yourself
- Use `PyInstaller` to build your own `.exe` from the exact same files
- Need help? Just ask — I got you.

---

## 🤔 Why Is the `.exe` So Big?

Yeah, I know — the `.py` file is like 20 KB, but the `.exe` is over 14 MB. What gives?

📦 That’s because the `.exe` bundles:

- Python itself (so you don’t need to install anything)
- All the required libraries
- The actual StealthNote app code

Think of it like a **self-contained backpack**: everything it needs to run is already zipped up inside. That’s why it “just works” even on a clean Windows PC.

It’s chunky so *you* don’t have to do anything extra. Just unzip and double-click ✅
