import os
import random
import argparse
import ctypes
from PIL import Image

# This gets the folder where the script is saved
AUTO_ROOT = os.path.dirname(os.path.abspath(__file__))

def set_folder_icon(folder_path, reroll=False):
    icon_path = os.path.join(folder_path, "folder_icon.ico")

    # By default, preserve thumbnails that were already generated.
    if not reroll and os.path.isfile(icon_path):
        return False

    # Find an image before removing the current icon. This avoids leaving a
    # folder without an icon when it has no supported images.
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]

    if not images:
        return False

    # --- STEP 0: CLEANUP PREVIOUS ICON ---
    for extra_file in ["folder_icon.ico", "desktop.ini"]:
        path = os.path.join(folder_path, extra_file)
        if os.path.exists(path):
            ctypes.windll.kernel32.SetFileAttributesW(path, 0x80) # Reset to Normal
            os.remove(path)

    # --- STEP 1: FIND A NEW RANDOM IMAGE ---
    random_img_path = os.path.join(folder_path, random.choice(images))

    # --- STEP 2: PROCESS IMAGE ---
    with Image.open(random_img_path) as img:
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        
        img = img.crop((left, top, right, bottom))
        img = img.resize((256, 256), Image.Resampling.LANCZOS)
        img.save(icon_path, format="ICO", sizes=[(256, 256)])

    # --- STEP 3: CREATE DESKTOP.INI ---
    ini_path = os.path.join(folder_path, "desktop.ini")
    ini_content = [
        '[.ShellClassInfo]',
        'IconResource=folder_icon.ico,0',
        '[ViewState]',
        'Mode=',
        'Vid=',
        'FolderType=Generic'
    ]
    
    with open(ini_path, 'w') as f:
        f.write('\n'.join(ini_content))

    # --- STEP 4: SET WINDOWS ATTRIBUTES ---
    ctypes.windll.kernel32.SetFileAttributesW(icon_path, 0x02 | 0x04) # Hidden + System
    ctypes.windll.kernel32.SetFileAttributesW(ini_path, 0x02 | 0x04)  # Hidden + System
    ctypes.windll.kernel32.SetFileAttributesW(folder_path, 0x01)      # Read-Only flag

# --- EXECUTION ---
parser = argparse.ArgumentParser(description="Generate icons for folders with images.")
parser.add_argument(
    "-r",
    "--reroll",
    action="store_true",
    help="regenerate thumbnails even when a folder already has one",
)
args = parser.parse_args()

print(f"Working in: {AUTO_ROOT}")
print("Mode: reroll existing thumbnails" if args.reroll else "Mode: preserve existing thumbnails")

for folder in os.listdir(AUTO_ROOT):
    full_path = os.path.join(AUTO_ROOT, folder)
    
    # We ignore the script itself and any other files
    if os.path.isdir(full_path):
        try:
            generated = set_folder_icon(full_path, reroll=args.reroll)
            if generated:
                action = "Rerolled" if args.reroll else "Created"
                print(f"{action} icon for: {folder}")
            else:
                print(f"Skipped (thumbnail already exists or no images): {folder}")
        except Exception as e:
            print(f"Failed {folder}: {e}")

# Final step: Force Windows to refresh the icons
ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
print("Finished! If icons don't update, press F5 in the folder.")
