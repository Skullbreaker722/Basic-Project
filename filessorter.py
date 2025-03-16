import os
import shutil

# Define categories for files
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"]
}

# Folder to organize
FOLDER_PATH = "C:/Users/skull/desktop"  # Change this to your target folder

def organize_files():
    if not os.path.exists(FOLDER_PATH):
        print("Invalid folder path!")
        return

    # Get list of files in the directory
    files = os.listdir(FOLDER_PATH)

    for file in files:
        file_path = os.path.join(FOLDER_PATH, file)

        # Skip if it's a folder
        if os.path.isdir(file_path):
            continue

        # Check file extension
        file_ext = os.path.splitext(file)[1].lower()
        
        # Find the matching category
        for category, extensions in FILE_CATEGORIES.items():
            if file_ext in extensions:
                category_folder = os.path.join(FOLDER_PATH, category)

                # Create folder if not exists
                if not os.path.exists(category_folder):
                    os.makedirs(category_folder)

                # Move the file
                shutil.move(file_path, os.path.join(category_folder, file))
                print(f"Moved: {file} → {category}/")
                break  # Stop searching after the first match

    print("✅ File organization complete!")

# Run the function
organize_files()
