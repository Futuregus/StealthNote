# fileLogger.py
"""
This module allows you to log actions to a file and optionally print them to the console.
It will create a directory for logs if it doesn't exist.
You MUST provide both data_dir and log_file when configuring.
"""

import datetime
import os

# Default paths (used until configure() is called)
DATA_DIR = os.path.join(os.getcwd(), "Placeholder_Data")
LOG_FILE = os.path.join(DATA_DIR, "Placeholder_Log.txt")


class Logger:
    _data_dir = DATA_DIR
    _log_file = LOG_FILE

    @classmethod
    def configure(cls, data_dir: str = None, log_file: str = None):
        """
        Set custom paths for logging.
        Both data_dir and log_file must be provided.
        The log_file must be a relative filename (not an absolute path).
        """
        if not data_dir or not log_file:
            print("Logger not configured: both data_dir and log_file must be provided.")
            return

        if os.path.isabs(log_file):
            print("Logger not configured: absolute paths for log_file are not allowed.")
            return

        cls._data_dir = data_dir
        cls._log_file = os.path.join(cls._data_dir, log_file)

        os.makedirs(cls._data_dir, exist_ok=True)

    @classmethod
    def log_action(cls, action: str, print_to_console: bool = True, separator: bool = False, tag: str = None):
        """
        Logs a message to the log file.
        - print_to_console: whether to also print it to the terminal
        - separator: logs a message with no timestamp (like dividers)
        - tag: optional string tag like "INFO", "ERROR", etc.
        """
        message = action
        if tag:
            message = f"[{tag}] {message}"

        if print_to_console:
            print(message)

        try:
            with open(cls._log_file, 'a') as f:
                if separator:
                    f.write(f"{message}\n")
                else:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass  # Don’t crash on logging errors



# --- Example Usage ---

# Uncomment the following lines to test the Logger functionality.

#if __name__ == "__main__":

    # CORRECT CONFIG

#        Logger.configure(data_dir="ExampleLogs", log_file="Example_Log.txt")
#        Logger.log_action("System boot complete.", tag="SYSTEM")
#        Logger.log_action("----------", separator=True)
#        Logger.log_action("This is a test log message", print_to_console=True, tag="INFO")


    # INCORRECT CONFIG TEST

#        Logger.configure(log_file="Log.txt")  # Won’t do anything
#        Logger.configure(data_dir="OnlyDir")  # Won’t do anything
#        Logger.configure(data_dir="Logs", log_file="C:/log.txt")  # Absolute path = denied!