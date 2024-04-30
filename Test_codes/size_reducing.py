from PIL import Image
import os

# Directory path where the images are stored
directory = '/home/arush/GW_Test_1/Data_Generation/Data/Noise'

# New resolution for the images
new_width = 640
new_height = 480

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Open the image
        image_path = os.path.join(directory, filename)
        image = Image.open(image_path)

        # Resize the image
        resized_image = image.resize((new_width, new_height))

        # Save the resized image
        resized_image.save(image_path)

        # Close the image
        image.close()