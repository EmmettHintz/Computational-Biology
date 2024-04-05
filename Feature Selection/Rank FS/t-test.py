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
    bootstrap_results['mean_p_value'] = bootstrap_results.median(axis=1)
    
    # Adjust mean p-values using Benjamini-Hochberg
    corrected_p_values = multipletests(bootstrap_results['mean_p_value'], alpha=0.05, method='fdr_bh')[1]
    bootstrap_results['corrected_p_value'] = corrected_p_values
    
    return bootstrap_results[bootstrap_results['corrected_p_value'] < 0.05]

def main():
    significant_treatment = perform_bootstrap_t_tests(treatment_group)
    significant_control = perform_bootstrap_t_tests(control_group)

    # Saving the significant miRNAs to CSV files
    significant_treatment.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/significant_treatment_miRNAs_ttest.csv')
    significant_control.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/significant_control_miRNAs_ttest.csv')

    print("Significant miRNAs in Treatment Group:")
    print(significant_treatment)
    print("\nSignificant miRNAs in Control Group:")
    print(significant_control)

if __name__ == "__main__":
    main()
