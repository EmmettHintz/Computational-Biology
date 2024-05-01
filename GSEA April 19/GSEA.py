import pandas as pd

# Define file paths
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
combined_genes_union_df = pd.DataFrame()

# Process file pairs and compute the union of significant genes
for group_prefix in ['control_group', 'intersection_group', 'treatment_group', 'unique_control_group']:
    # Initialize sets to store significant genes from each dataset
    genes_tb = set()
    genes_ts = set()

    # Load and filter the miRTarBase (_tb) dataset
    tb_path = f"{group_prefix}_tb"
    data_tb = pd.read_csv(file_paths[tb_path])
    genes_tb.update(data_tb[data_tb['p-value'] <= p_value_significance]['Gene Symbol'].dropna().unique())

    # Load and filter the TargetScan (_ts) dataset
    ts_path = f"{group_prefix}_ts"
    data_ts = pd.read_csv(file_paths[ts_path])
    genes_ts.update(data_ts[data_ts['p-value'] <= p_value_significance]['Gene Symbol'].dropna().unique())

    # Compute the union of significant genes
    genes_union = genes_tb.union(genes_ts)

    # Add the union to the DataFrame
    combined_genes_union_df[group_prefix] = pd.Series(list(genes_union))

# Handle the unique_treatment_group separately as it only has a _tb dataset
data_utg_tb = pd.read_csv(file_paths['unique_treatment_group_tb'])
genes_utg_tb = data_utg_tb[data_utg_tb['p-value'] <= p_value_significance]['Gene Symbol'].dropna().unique()
combined_genes_union_df['unique_treatment_group'] = pd.Series(genes_utg_tb)

# Save the combined DataFrame to a CSV file
output_file = '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/combined_genes_union.xlsx'
combined_genes_union_df.to_excel(output_file, index=False)

print(f"Combined gene list (union) saved to {output_file}")
