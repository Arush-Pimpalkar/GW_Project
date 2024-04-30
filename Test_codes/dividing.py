import os
import shutil
import random

# Define paths to the original dataset and destination directories
original_dataset_dir = "/home/arush/GW_Test_1/Data_Generation/DATA_V2/mass_30_30"
base_dir = "/home/arush/GW_Test_1/Model_Training/Data_v3"

# Create directories for train, test, and validation sets
train_dir = os.path.join(base_dir, "train")
test_dir = os.path.join(base_dir, "test")
validation_dir = os.path.join(base_dir, "validation")
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)
os.makedirs(validation_dir, exist_ok=True)

# Define the names of the classes
classes = ["5_to_8", "8_to_11", "11_to_14","14_to_17","17_to_20", "noise"]

# Define the ratio for train, test, and validation sets
train_ratio = 0.8
test_ratio = 0.1
validation_ratio = 0.1

# Loop through each class directory
for cls in classes:
    # If the class is "noise", use "noise" as the directory name
    cls_dir = os.path.join(original_dataset_dir, cls if cls != "noise" else "noise")
    filenames = os.listdir(cls_dir)
    random.shuffle(filenames)  # Shuffle the filenames

    # Calculate the number of images for each set
    num_train = int(len(filenames) * train_ratio)
    num_test = int(len(filenames) * test_ratio)
    num_validation = len(filenames) - num_train - num_test

    # Split the filenames into train, test, and validation sets
    train_filenames = filenames[:num_train]
    test_filenames = filenames[num_train : num_train + num_test]
    validation_filenames = filenames[num_train + num_test :]

    # Create directories for the current class in train, test, and validation sets
    train_cls_dir = os.path.join(train_dir, cls)
    test_cls_dir = os.path.join(test_dir, cls)
    validation_cls_dir = os.path.join(validation_dir, cls)
    os.makedirs(train_cls_dir, exist_ok=True)
    os.makedirs(test_cls_dir, exist_ok=True)
    os.makedirs(validation_cls_dir, exist_ok=True)

    # Move images to the corresponding directories
    for filename in train_filenames:
        src = os.path.join(cls_dir, filename)
        dst = os.path.join(train_cls_dir, filename)
        shutil.copyfile(src, dst)

    for filename in test_filenames:
        src = os.path.join(cls_dir, filename)
        dst = os.path.join(test_cls_dir, filename)
        shutil.copyfile(src, dst)

    for filename in validation_filenames:
        src = os.path.join(cls_dir, filename)
        dst = os.path.join(validation_cls_dir, filename)
        shutil.copyfile(src, dst)

print("Dataset divided into train, test, and validation sets.")
