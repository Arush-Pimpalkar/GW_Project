import re
import csv


def chirp_mass(m1, m2):
    chirp_m = ((m1 * m2) ** (3 / 5)) / ((m1 + m2) ** (1 / 5))
    return chirp_m

# while True:
#     m1 = input("enter m1: ")
#     m2 = input("enter m2: ")

#     chirp_m = chirp_mass(int(m1), int(m2))
#     print(chirp_m)

def get_chirp_masses(filename):
    m1_match = re.search(r"m1=(\d+)", filename)
    m2_match = re.search(r"m2=(\d+)", filename)
    if m1_match and m2_match:
        m1 = int(m1_match.group(1))
        m2 = int(m2_match.group(1))
        chirp_m = chirp_mass(m1, m2)
        return chirp_m
    return None


filename = "/home/arush/GW_Project_1/Data_Generation/Continous_Check/cont_data_val.csv"

# Read the CSV content
with open(filename, "r") as infile:
    reader = csv.reader(infile)
    rows = list(reader)

# Process and update the rows
header = rows[0]
if "ChirpMass" not in header:
    header.append("ChirpMass")

for row in rows[1:]:
    filenames = row[1]
    chirp_m = get_chirp_masses(filenames)
    if chirp_m is not None:
        row.append(chirp_m)
    else:
        row.append("0.00")  # If chirp mass could not be calculated, append an empty string

# Write the updated content back to the same file
with open(filename, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(rows)
