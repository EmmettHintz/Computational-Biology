import pandas as pd
import os

# Define your directories for each group
directories = {
    'treatment': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/treatment_group',
    'treatment_unique': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/unique_treatment_group',
    'control': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/control_group',
    'control_unique': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/unique_control_group',
    'intersection': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/intersection_group'
}

cutoff = -0.05  # Adjust this value as needed

def process_directory(directory, cutoff):
    combined_filtered_data = pd.DataFrame()
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            data = pd.read_csv(file_path, sep='\t', header=0)
            filtered_data = data[data['Cumulative weighted context++ score'] <= cutoff]
            combined_filtered_data = pd.concat([combined_filtered_data, filtered_data], ignore_index=True)
    return combined_filtered_data

# Dictionary to hold the combined data for all groups
combined_filtered_data_all_groups = {}

# Process each directory and store the combined data in the dictionary
for group_name, directory_path in directories.items():
    combined_filtered_data_all_groups[group_name] = process_directory(directory_path, cutoff)

# Perform any exploratory data analysis as needed
for group_name, combined_data in combined_filtered_data_all_groups.items():
    print(f"{group_name} Group - Data Head:")
    print(combined_data.head())
    print(f"{group_name} Group - Data Shape:")
    print(combined_data.shape)
    # Save the combined data for each group
    combined_data.to_csv(f'combined_filtered_{group_name}_data.csv', index=False)
    # Save just the genes column to separate files for each group
    combined_data['Gene Symbol'].to_csv(f'filtered_{group_name}_genes.txt', index=False, header=False)
