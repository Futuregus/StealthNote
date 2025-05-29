
"""
AssetLoader Module
This module provides a class to locate and load assets from specified directories.
"""


import os

class AssetLoader:
    """
    AssetLoader helps locate assets by searching its own directory first,
    then falling back to common user directories for specified folders.
    """

    def __init__(self, asset_folders=None):
        """
        Initialize the AssetLoader.

        Args:
            asset_folders (list[str], optional): A list of folder names or paths
                where assets might be located. Defaults to ['StealthNoteAssets']
                in the user's home directory.
        """
        if asset_folders is None:
            asset_folders = [os.path.join(os.getenv("USERPROFILE"), "StealthNoteAssets")]
        self.asset_folders = asset_folders

    def find_assets_folder(self):
        """
        Search for any of the specified asset folders.

        First, check if any asset folder exists relative to this script's directory.
        If not found, search in common user directories.

        Returns:
            str or None: Full path to the first found asset folder, or None if not found.
        """
        print("------------------------------------")
        print("\nAssetLoader:\n")

        # 1. Check relative to this script's own directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Searching in script directory: {script_dir}")
        for folder in self.asset_folders:
            candidate = os.path.join(script_dir, folder)
            print(f"Checking: {candidate}")
            if os.path.exists(candidate) and os.path.isdir(candidate):
                print(f"found asset folder ({candidate})\n")
                return candidate

        # 2. Fall back to searching user directories
        user_directories = [
            os.getenv("USERPROFILE"),
            os.path.join(os.getenv("USERPROFILE"), "Documents"),
            os.path.join(os.getenv("USERPROFILE"), "Downloads"),
            os.path.join(os.getenv("USERPROFILE"), "Desktop"),
            os.path.join(os.getenv("USERPROFILE"), "Program Files")
        ]

        for directory in user_directories:
            if directory and os.path.exists(directory):
                print(f"Searching in: {directory}")
                for root, dirs, files in os.walk(directory):
                    for folder in self.asset_folders:
                        if folder in dirs:
                            found_path = os.path.join(root, folder)
                            print(f"found asset folder ({found_path})\n")
                            return found_path

        print("asset folder not found\n")
        return None

    def find_asset(self, asset_name):
        """
        Search for a specific asset file within the discovered asset folder.

        Args:
            asset_name (str): The name of the asset file to search for (e.g., 'logo.png').

        Returns:
            str or None: Full path to the asset file if found, or None if not found.
        """
        assets_folder_path = self.find_assets_folder()

        if assets_folder_path:
            asset_path = os.path.join(assets_folder_path, asset_name)
            print(f"Looking for file: {asset_path}")
            if os.path.exists(asset_path):
                print(f"Found file ({asset_path})")
            else:
                print(f"File not found ({asset_name}) in ({assets_folder_path})")
        else:
            print(f"Asset folder not found, so file ({asset_name}) couldn't be searched")

        print("------------------------------------")
        return asset_path if os.path.exists(asset_path) else None

