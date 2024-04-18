from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
import pandas as pd
import numpy as np

# Load the data
data = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/GSE97154_Cleaned.csv')

treatment_group = data[data['Treatment'] == 1]
control_group = data[data['Treatment'] == 0]

def perform_bootstrap_t_tests(group, n_bootstraps=1000):
    miRNA_columns = group.columns[5:]  # miRNA expression columns
    bootstrap_results = pd.DataFrame(index=miRNA_columns, columns=range(n_bootstraps))
    
    for i in range(n_bootstraps):
        # Create bootstrap sample for each group
        bootstrap_sample_t0 = group[group['Timepoint'] == 'T0'].sample(frac=1, replace=True)
        bootstrap_sample_t8 = group[group['Timepoint'] == 'T8'].sample(frac=1, replace=True)
        
        for miRNA in miRNA_columns:
            t0_values = bootstrap_sample_t0[miRNA].values
            t8_values = bootstrap_sample_t8[miRNA].values
            
            # Perform t-test
            t_stat, p_val = ttest_ind(t0_values, t8_values, equal_var=False, nan_policy='omit')
            bootstrap_results.loc[miRNA, i] = p_val
    
    # Calculate the mean p-value across all bootstraps for each miRNA
    # Experiment with mean/median
    bootstrap_results['median_p_value'] = bootstrap_results.median(axis=1)
    
    # Adjust mean p-values using Benjamini-Hochberg
    corrected_p_values = multipletests(bootstrap_results['median_p_value'], alpha=0.05, method='fdr_bh')[1]
    bootstrap_results['corrected_p_value'] = corrected_p_values
    
    return bootstrap_results[bootstrap_results['corrected_p_value'] < 0.05]


significant_treatment = perform_bootstrap_t_tests(treatment_group)
significant_control = perform_bootstrap_t_tests(control_group)

# Finding the significant miRNAs in both treatment and control groups
significant_miRNAs_treatment = set(significant_treatment.index)
significant_miRNAs_control = set(significant_control.index)

# Intersection: miRNAs significant in both groups
significant_miRNAs_intersection = significant_miRNAs_treatment.intersection(significant_miRNAs_control)

# Unique to Treatment: miRNAs significant in treatment but not in control
unique_miRNAs_treatment = significant_miRNAs_treatment - significant_miRNAs_control

# Unique to Control: miRNAs significant in control but not in treatment
unique_miRNAs_control = significant_miRNAs_control - significant_miRNAs_treatment

# Preparing summary dictionary for all groups:
summary = {
    "Group 1 (Unique to Treatment)": list(unique_miRNAs_treatment),
    "Group 2 (Unique to Control)": list(unique_miRNAs_control),
    "Group 3 (Intersection)": list(significant_miRNAs_intersection),
    "Group 4 (All significant in Treatment)": list(significant_miRNAs_treatment),
    "Group 5 (All significant in Control)": list(significant_miRNAs_control)
}

# Printing summary information
print(f'There are {len(significant_miRNAs_treatment)} significant miRNAs in the treatment group.')
print(f'There are {len(significant_miRNAs_control)} significant miRNAs in the control group.')
print(f'There are {len(significant_miRNAs_intersection)} miRNAs that are significant in both the treatment and control groups.')
print("\nSummary:")
for group, miRNAs in summary.items():
    print(f"{group}: {len(miRNAs)} miRNAs")
    
# Create pd DataFrame for each of the 5 groups, then save to csv
# Convert lists to Pandas DataFrames
t_test_treatment_unique = pd.DataFrame(list(summary["Group 1 (Unique to Treatment)"]), columns=['miRNA'])
t_test_control_unique= pd.DataFrame(list(summary["Group 2 (Unique to Control)"]), columns=['miRNA'])
t_test_intersection = pd.DataFrame(list(summary["Group 3 (Intersection)"]), columns=['miRNA'])
t_test_treatment= pd.DataFrame(list(summary["Group 4 (All significant in Treatment)"]), columns=['miRNA'])
t_test_control = pd.DataFrame(list(summary["Group 5 (All significant in Control)"]), columns=['miRNA'])

# Save each DataFrame to a CSV file
t_test_treatment_unique.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/t-test/t_test_treatment_unique.csv', index=False)
t_test_control_unique.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/t-test/t_test_control_unique.csv', index=False)
t_test_intersection.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/t-test/t_test_intersection.csv', index=False)
t_test_treatment.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/t-test/t_test_treatment.csv', index=False)
t_test_control.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/t-test/t_test_control.csv', index=False)

print("All groups have been saved to CSV files.")
