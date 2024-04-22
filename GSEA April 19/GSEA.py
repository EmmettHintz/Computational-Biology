import pandas as pd

# Assuming the CSV files contain a column 'Gene Symbol' and are in a folder structure as indicated
file_paths = {
    'control_group_tb': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/control_group/control_genes_miRTarBase.csv',
    'control_group_ts': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/control_group/control_genes_TargetScan.csv',
    'intersection_group_tb': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/intersection_group/intersection_genes_miRTarBase.csv',
    'intersection_group_ts': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/intersection_group/intersection_genes_TargetScan.csv',
    'treatment_group_tb': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/treatment_group/treatment_genes_miRTarBase.csv',
    'treatment_group_ts': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/treatment_group/treatment_genes_TargetScan.csv',
    'unique_control_group_tb': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/unique_control_group/unique_control_genes_miRTarBase.csv',
    'unique_control_group_ts': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/unique_control_group/unique_control_genes_TargetScan.csv',
    'unique_treatment_group_tb': '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/unique_treatment_group/unique_treatment_genes_miRTarBase.csv',
}


# Define the significance level for p-value
p_value_significance = 0.05

# Initialize a DataFrame to store the combined data
combined_genes_df = pd.DataFrame()

# Process each file
for group, path in file_paths.items():
    try:
        # Load the data
        data = pd.read_csv(path)
        # Filter for significant p-values
        significant_data = data[data['p-value'] <= p_value_significance]
        # Extract unique gene symbols
        unique_genes = significant_data['Gene Symbol'].unique().tolist()
        # Add the genes to the DataFrame under the corresponding group
        combined_genes_df[group] = pd.Series(unique_genes)
    except Exception as e:
        print(f"An error occurred while processing {path}: {e}")

# Define the output path for the combined CSV
output_file = '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/combined_genes.xlsx'

# Save the combined genes to a CSV file
combined_genes_df.to_excel(output_file, index=False)

print(f"Combined gene list saved to {output_file}")