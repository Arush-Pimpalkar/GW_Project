import re
import os
import numpy as np
import csv
import random


def extract_snr(filename):
    match = re.search(r"SNR=(\d+\.\d{1,3})", filename)
    if match:
        return float(match.group(1))
    else:
        return 0


# Function to load labels from filenames
def load_labels_from_directory(directory):
    labels = []
    filenames = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".png"):
                try:
                    snr = extract_snr(filename)
                except ValueError:
                    snr = 0  # Label for noise
                labels.append(snr)
                filenames.append(os.path.join(root, filename))
    return np.array(labels), filenames


labels_data, filenames_data = load_labels_from_directory(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/Data"
)

labels_noise, filenames_noise = load_labels_from_directory(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/noise"
)


labels = np.concatenate((labels_data, labels_noise))
filenames = np.concatenate((filenames_data, filenames_noise))

combined = list(zip(labels, filenames))

random.seed(42)
random.shuffle(combined)

labels, filenames = zip(*combined)

labels = np.array(labels)
filenames = np.array(filenames)

print("total dataset: ", len(labels))


# function to find the number of files in train, test and validation set
train_len = int(0.8 * len(labels))
test_len = int(0.1 * len(labels))
val_len = len(labels) - train_len - test_len

print("training dataset length: ", train_len)
print("testing dataset length: ", test_len)
print("validation dataset length: ", val_len)

i = 0
with open(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/cont_data_train.csv",
    "w",
    newline="",
) as file:
    writer = csv.writer(file)
    writer.writerow(["Label", "Path"])
    while i < train_len:
        writer.writerow([labels[i], filenames[i]])
        i += 1

with open(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/cont_data_test.csv",
    "w",
    newline="",
) as file:
    writer = csv.writer(file)
    writer.writerow(["Label", "Path"])
    while i < train_len + test_len:
        writer.writerow([labels[i], filenames[i]])
        i += 1

with open(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/cont_data_val.csv",
    "w",
    newline="",
) as file:
    writer = csv.writer(file)
    writer.writerow(["Label", "Path"])
    while i < len(labels):
        writer.writerow([labels[i], filenames[i]])
        i += 1
