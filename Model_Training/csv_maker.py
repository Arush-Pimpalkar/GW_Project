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
    np.random.shuffle(labels)
    return np.array(labels), filenames


labels_data, filenames_data = load_labels_from_directory(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/Data"
)

labels_noise, filenames_noise = load_labels_from_directory(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/noise"
)


labels = np.concatenate((labels_data, labels_noise))
filenames = np.concatenate((filenames_data, filenames_noise))

# Shuffle the data
np.random.shuffle(labels)
np.random.shuffle(filenames)

print(len(labels))
print(len(filenames))

i = 0
with open(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/cont_data_train.csv",
    "a",
    newline="",
) as file:
    writer = csv.writer(file)
    writer.writerow(["Label", "Path"])
    while i < 7071:
        writer.writerow([labels[i], filenames[i]])
        i += 1

with open(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/cont_data_test.csv",
    "a",
    newline="",
) as file:
    writer = csv.writer(file)
    writer.writerow(["Label", "Path"])
    while i < 7955:
        writer.writerow([labels[i], filenames[i]])
        i += 1

with open(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/cont_data_val.csv",
    "a",
    newline="",
) as file:
    writer = csv.writer(file)
    writer.writerow(["Label", "Path"])
    while i < 8839:
        writer.writerow([labels[i], filenames[i]])
        i += 1
