import pandas as pd
import os

treatment_directory = '/Users/emmetthintz/Documents/Computational-Biology/GSEA2/Treatment'
control_directory = '/Users/emmetthintz/Documents/Computational-Biology/GSEA2/Control'


cutoff = -0.4  # Adjust this value as needed

def process_directory(directory, cutoff):
    """
    Process all .txt files in the specified directory, filtering rows based on the given cutoff,
    and combining filtered data from all files into a single DataFrame.
    
    Parameters:
    - directory: Path to the directory containing the .txt files
    - cutoff: The cutoff value for filtering rows based on 'Cumulative weighted context++ score'
    
    Returns:
    - DataFrame containing the combined filtered data from all files in the directory
    """
    combined_filtered_data = pd.DataFrame()
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Ensure you're only processing .txt files
            file_path = os.path.join(directory, filename)
            # Read each file
            data = pd.read_csv(file_path, sep='\t', header=0)  # Adjust header=0 if your files have headers
            # Filter based on the cutoff
            filtered_data = data[data['Cumulative weighted context++ score'] <= cutoff]
            # Combine filtered data
            combined_filtered_data = pd.concat([combined_filtered_data, filtered_data], ignore_index=True)
    
    return combined_filtered_data

# Directories containing your data
treatment_directory = '/Users/emmetthintz/Documents/Computational-Biology/GSEA2/Treatment'
control_directory = '/Users/emmetthintz/Documents/Computational-Biology/GSEA2/Control'

cutoff = -0.4  # Adjust this value as needed

# Process each directory
combined_filtered_treatment = process_directory(treatment_directory, cutoff)
combined_filtered_control = process_directory(control_directory, cutoff)

# Exploratory Data Analysis on combined data (optional here)
print(combined_filtered_treatment.head())
print(combined_filtered_treatment.shape)
print(combined_filtered_control.head())
print(combined_filtered_control.shape)

# Save the combined data for treatment and control groups
combined_filtered_treatment.to_csv('combined_filtered_treatment_data.csv', index=False)
combined_filtered_control.to_csv('combined_filtered_control_data.csv', index=False)

# If needed, save just the genes column to separate files for treatment and control
gene_df_treatment = combined_filtered_treatment['Target gene']
gene_df_treatment.to_csv('filtered_genes_treatment.csv', index=False)

gene_df_control = combined_filtered_control['Target gene']
gene_df_control.to_csv('filtered_genes_control.csv', index=False)