import os


def add_suffix_to_files_in_directory(directory):
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Check if the current item is a file
        if os.path.isfile(filepath):
            # Add "__" suffix to the filename
            new_filename =  "_"+filename
            new_filepath = os.path.join(directory, new_filename)
            # Rename the file
            os.rename(filepath, new_filepath)
            print(f"Renamed: {filename} -> {new_filename}")
        # If it's a directory, recursively call the function
        elif os.path.isdir(filepath):
            add_suffix_to_files_in_directory(filepath)


# Specify the directory containing the data
root_directory = "/home/arush/GW_Test_1/Data_Generation/DATA_V2/mass_30_30"

# Call the function to add "__" suffix to filenames in all directories
add_suffix_to_files_in_directory(root_directory)
