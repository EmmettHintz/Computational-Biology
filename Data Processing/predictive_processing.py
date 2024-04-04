from sklearn.model_selection import GroupShuffleSplit
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests

# Import data
import pandas as pd

data = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/GSE97154_Cleaned.csv')

# Adjusting the train-test split to account for participant IDs
# We use GroupShuffleSplit to ensure no participant is split across training and testing sets
gss = GroupShuffleSplit(test_size=0.1, n_splits=1, random_state=42)
for train_idx, test_idx in gss.split(data, groups=data['Participant ID']):
    train_data = data.iloc[train_idx]
    test_data = data.iloc[test_idx]

# Implementing the feature selection process with bootstrap t-tests within the training set
def perform_bootstrap_t_tests(group, n_bootstraps=1000):
    miRNA_columns = group.columns[5:]  # miRNA expression columns start from the 6th column
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
    bootstrap_results['mean_p_value'] = bootstrap_results.mean(axis=1)
    
    # Adjust mean p-values using Benjamini-Hochberg
    corrected_p_values = multipletests(bootstrap_results['mean_p_value'], alpha=0.05, method='fdr_bh')[1]
    bootstrap_results['corrected_p_value'] = corrected_p_values
    
    return bootstrap_results[bootstrap_results['corrected_p_value'] < 0.05]

# Splitting the training data into treatment and control groups for feature selection
treatment_group = train_data[train_data['Treatment'] == 1]
control_group = train_data[train_data['Treatment'] == 0]

# Performing feature selection
significant_treatment = perform_bootstrap_t_tests(treatment_group)
significant_control = perform_bootstrap_t_tests(control_group)


print(f"Significant miRNAs in Treatment Group: {significant_treatment}")
print(f"Significant miRNAs in Control Group: {significant_control}")


# Save to csv 
significant_treatment.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Predictive Data/significant_treatment_miRNAs_ttest.csv')
significant_control.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Predictive Data/significant_control_miRNAs_ttest.csv')