# StealthNote
![result](https://github.com/user-attachments/assets/9706fabc-eb83-4da7-9670-db3e21e43a8c)

StealthNote is a simple, secure, and offline-first encrypted text editor built with Python and Tkinter. It allows you to write notes and save them in a fully encrypted `.ectf` format using strong password-based encryption (Fernet + PBKDF2HMAC). Your data never leaves your device.

---

## ✨ Features

- 💾 **Encrypted Save/Load**: Secure your notes with password-based encryption.
- 🌙 **Dark/Light Mode**: Toggle between themes for comfortable writing.
- 📝 **Word Wrap Toggle**: Switch between wrapped or horizontal scrolling.
- 🔠 **Adjustable Font Size**: Set your preferred reading/writing size.
- 📂 **Default Save/Open Directory**: Choose a starting folder for file dialogs.
- 🧹 **Clear Text Button**: Quickly wipe the editor clean.
- 🔧 **Persistent Settings**: Your preferences are saved and loaded automatically.

---

## 🔐 How It Works

- When you save a note, you're prompted to enter a password.
- The note is encrypted with a random salt + Fernet encryption using your password.
- The resulting `.ectf` file contains both the salt and the encrypted message.
- To open a note, you must enter the same password you used to save it.

Your password is the ONLY way to decrypt your notes.  
**Do not lose or forget it — there is no password recovery mechanism.**

## ⚖️ License

This project is licensed under the **GNU General Public License v3.0**.  
See [`LICENSE`](LICENSE) for more details.


## 📷 Screenshots 
- Dark mode
![Darkmode](https://github.com/user-attachments/assets/c811a75f-2f50-451d-b01a-6bee165d7a3d)

- Light mode
![Lightmode](https://github.com/user-attachments/assets/c6c6a9bc-36b2-4d7d-969c-5817b3da06cd)





