import csv


def chirp_mass(m1, m2):
    """Calculate the chirp mass of two masses."""
    try:   
        chirp_m = ((m1 * m2) ** (3 / 5)) / ((m1 + m2) ** (1 / 5))
        return chirp_m
    except:
        return 0


# Define the path to the CSV file
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
    m1 = int(row[1])
    m2 = int(row[2])
    chirp_m = chirp_mass(m1, m2)
    row.append(f"{chirp_m:.2f}")

# Write the updated content back to the same file
with open(filename, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(rows)
