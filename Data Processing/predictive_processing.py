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
    
    # Select miRNAs with corrected p-values < 0.05
    significant_miRNAs = bootstrap_results[bootstrap_results['corrected_p_value'] < 0.05]
    
    # Return the names (index values) of the significant miRNAs as a list
    return significant_miRNAs.index.tolist()


# Splitting the training data into treatment and control groups for feature selection
treatment_group = train_data[train_data['Treatment'] == 1]
# Assuming control_group is not used for feature selection based on the discussion
# control_group = train_data[train_data['Treatment'] == 0]

# Performing feature selection only on the treatment group
# Correctly obtaining significant miRNA names
significant_miRNAs_treatment = perform_bootstrap_t_tests(treatment_group)

# Confirming the content is as expected
print(f"Sample of significant miRNAs: {significant_miRNAs_treatment[:10]}")

# Assuming this now correctly contains miRNA names
all_significant_miRNAs = significant_miRNAs_treatment

# Constructing columns_to_keep with actual miRNA names
columns_to_keep = ['Participant ID', 'Treatment', 'Response'] + all_significant_miRNAs

# Now attempting to filter with the corrected columns list should work, assuming all names are correct and present in your DataFrame
filtered_train_data = train_data[train_data['Treatment'] == 1][columns_to_keep]
filtered_test_data = test_data[test_data['Treatment'] == 1][columns_to_keep]

# Define paths for saving the filtered datasets
output_dir = '/Users/emmetthintz/Documents/Computational-Biology/Predictive Data'
filtered_train_data_path = output_dir + '/filtered_train_data.csv'
filtered_test_data_path = output_dir + '/filtered_test_data.csv'

# Proceed with saving the filtered datasets
filtered_train_data.to_csv(filtered_train_data_path, index=False)
filtered_test_data.to_csv(filtered_test_data_path, index=False)

print(f"Filtered train data saved to: {filtered_train_data_path}")
print(f"Filtered test data saved to: {filtered_test_data_path}")