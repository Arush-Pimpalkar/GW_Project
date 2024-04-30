import os
from PIL import Image


def remove_white_border_and_crop(image_path):
    # Open the image
    image = Image.open(image_path)

    # Convert image to RGBA to handle transparency
    image = image.convert("RGBA")

    # Get the image dimensions
    width, height = image.size

    # Check if the image is already cropped (height <= cropped_height)
    cropped_height = height // 2
    if height <= cropped_height:
        print(f"Skipping {image_path} as it is already cropped.")
        return

    # Remove white border
    left, top, right, bottom = 0, 0, width, height

    # Search for non-white pixels from left
    for x in range(width):
        if not all(
            image.getpixel((x, y))[:3] == (255, 255, 255) for y in range(height)
        ):
            left = x
            break

    # Search for non-white pixels from right
    for x in range(width - 1, -1, -1):
        if not all(
            image.getpixel((x, y))[:3] == (255, 255, 255) for y in range(height)
        ):
            right = x + 1
            break

    # Search for non-white pixels from bottom
    for y in range(height - 1, -1, -1):
        if not all(image.getpixel((x, y))[:3] == (255, 255, 255) for x in range(width)):
            bottom = y + 1
            break

    # Crop off the bottom 50% of the image
    cropped_image = image.crop((left, bottom - cropped_height, right, bottom))

    # Save the cropped image, overwriting the original image
    cropped_image.save(image_path)


# List of folders containing the images
folder_paths = [
    "/home/arush/GW_Test_1/Model_Training/Data_v2/test/High_SNR",
    "/home/arush/GW_Test_1/Model_Training/Data_v2/test/noise",
    "/home/arush/GW_Test_1/Model_Training/Data_v2/test/Low_SNR",
    "/home/arush/GW_Test_1/Model_Training/Data_v2/test/Mid_SNR",
    "/home/arush/GW_Test_1/Model_Training/Data_v2/train/High_SNR",
    "/home/arush/GW_Test_1/Model_Training/Data_v2/train/noise",
    "/home/arush/GW_Test_1/Model_Training/Data_v2/train/Low_SNR",
    "/home/arush/GW_Test_1/Model_Training/Data_v2/train/Mid_SNR",
    "/home/arush/GW_Test_1/Model_Training/Data_v2/validation/High_SNR",
    "/home/arush/GW_Test_1/Model_Training/Data_v2/validation/noise",
    "/home/arush/GW_Test_1/Model_Training/Data_v2/validation/Low_SNR",
    "/home/arush/GW_Test_1/Model_Training/Data_v2/validation/Mid_SNR",

]

# Loop through each folder
for folder_path in folder_paths:
    print(f"Processing files in {folder_path}...")
    total_files = len(os.listdir(folder_path))
    progress_bar_width = 40
    for i, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".png"):  # Process only PNG files
            file_path = os.path.join(folder_path, filename)
            remove_white_border_and_crop(file_path)
            progress = (i + 1) / total_files
            progress_bar = "#" * int(progress * progress_bar_width)
            print(f"\rProgress: [{progress_bar:<{progress_bar_width}}] {int(progress * 100)}%", end="")
    print("\nProcessing completed.")
    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):  # Process only PNG files
            file_path = os.path.join(folder_path, filename)
            remove_white_border_and_crop(file_path)
