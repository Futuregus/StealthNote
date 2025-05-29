import os
import json
from utils.logtofile import Logger


DATA_DIR = os.path.join(os.getcwd(), "StealthNote Data")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
Logger.configure(data_dir=DATA_DIR, log_file="StealthNote_Log.txt")


# %--- Settings Manager Class ---%
class SettingsManager:

    DEFAULTS = {
        "theme": "StealthNote",
        "font_size": 16,
        "wrap": True,
        "default_dir": "",
        "stealthmode_save_path": "BLANK"
    }

    @staticmethod
    def load_settings():
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                Logger.log_action(f"Failed to load settings: {e}", tag="ERROR")
        return SettingsManager.DEFAULTS.copy()

    @staticmethod
    def save_settings(settings):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            Logger.log_action(f"Failed to save settings: {e}", tag="ERROR")

# %----------------------%