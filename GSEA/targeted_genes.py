import pandas as pd
import os

directory = '/Users/emmetthintz/Documents/Computational-Biology/GSEA'


cutoff = -0.4  # Adjust this value as needed


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
        

# Exploratory Data Analysis
print(combined_filtered_data.head())
print(combined_filtered_data.shape)

# Save the combined data
combined_filtered_data.to_csv('combined_filtered_data.csv', index=False)

# Save just the genes column to a seperate file
gene_df = combined_filtered_data['Target gene']
gene_df.to_csv('filtered_genes.csv', index=False)
