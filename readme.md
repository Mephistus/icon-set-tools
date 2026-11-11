# Icon Set Tools: Folder Icon Reroller

This script automatically updates Windows folder icons by picking a random image from within each subfolder. It crops the image to a square, converts it to a high-quality `.ico` file, and handles the `desktop.ini` configuration and file attributes automatically.

## Before
![Before](screenshots/ss1.jpg)
## After
![After](screenshots/ss2.jpg)

## How it Works
1. **Cleanup:** Removes any existing `folder_icon.ico` or `desktop.ini` files.
2. **Selection:** Randomly selects a `.jpg`, `.jpeg`, `.png`, or `.bmp` from the subfolder.
3. **Processing:** Crops the image to 1:1 and resizes to 256x256.
4. **Configuration:** Generates `desktop.ini` and sets Windows System/Hidden attributes.
5. **Refresh:** Triggers a shell notification to update icons immediately.

## Requirements
* **Windows OS**
* **Python 3.x**
* **Pillow (PIL)**

  ```pip install Pillow```

## Usage
1. Place `set_icons.py` in the root directory.
2. Run `run.bat` or `python set_icons.py`.

By default, only immediate subfolders are processed, and existing icons are preserved.

* `python set_icons.py -d` (or `--deep`): process all nested subfolders at every depth.
* `python set_icons.py -r` (or `--reroll`): regenerate existing icons.
* `python set_icons.py -d -r`: regenerate icons throughout the folder tree.

Each folder uses images directly inside it. Folders without supported images are skipped,
but deep mode still visits their subfolders. Deep mode skips symbolic links and directory
junctions to avoid loops.
