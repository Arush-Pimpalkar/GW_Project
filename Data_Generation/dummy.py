import os
from PIL import Image


def check_corrupt_images(folder_path):
    corrupt_images = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    img.verify()  # Verify the image is intact
            except (IOError, SyntaxError) as e:
                print(f"Corrupt image found: {file_path} - {e}")
                corrupt_images.append(file_path)

    return corrupt_images


folder_path = "/home/arush/GW_Project_1/Data_Generation/Continous_Check/noise"  # Replace with the path to your folder
corrupt_images = check_corrupt_images(folder_path)

if corrupt_images:
    print("Corrupt images found:")
    for img in corrupt_images:
        print(img)
else:
    print("No corrupt images found.")
