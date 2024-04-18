from sklearn.feature_selection import mutual_info_regression
import numpy as np
import pandas as pd

# Load the data
data = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/GSE97154_Cleaned.csv')

treatment_group = data[data['Treatment'] == 1]
control_group = data[data['Treatment'] == 0]

def calculate_mutual_information_with_bootstrap(group, n_iterations=1000):
    t0 = group[group['Timepoint'] == 'T0']
    t8 = group[group['Timepoint'] == 'T8']
    
    miRNAs = group.columns[5:]  # Assuming miRNA expression starts at column 5
    bootstrap_mi_scores = np.zeros((len(miRNAs), n_iterations))
    
    for n in range(n_iterations):
        # Bootstrap resampling
        bootstrap_sample = pd.concat([t0.sample(frac=1, replace=True), t8.sample(frac=1, replace=True)])
        labels = [0]*len(t0) + [1]*len(t8)  # Reusing labels since sample size remains constant
        
        for index, miRNA in enumerate(miRNAs):
            mi_score = mutual_info_regression(bootstrap_sample[[miRNA]], labels, discrete_features=False)
            bootstrap_mi_scores[index, n] = mi_score[0]
    
    # Calculate summary statistic (e.g., mean or median -- using median) across bootstrap iterations for each miRNA
    mi_score_summary = np.median(bootstrap_mi_scores, axis=1)
    
    return pd.DataFrame({'miRNA': miRNAs, 'MI_Score': mi_score_summary})

def perform_mi_analysis_and_categorize():
    treatment_mi = calculate_mutual_information_with_bootstrap(treatment_group)
    control_mi = calculate_mutual_information_with_bootstrap(control_group)

    # Assuming significance is determined, for demonstration, by being in the top X percentile (e.g., top 25%)
    # Adjust the quantile value as needed
    significant_threshold_treatment = treatment_mi['MI_Score'].quantile(0.75)
    significant_threshold_control = control_mi['MI_Score'].quantile(0.75)

    # Identifying significant miRNAs based on the calculated threshold
    significant_miRNAs_treatment = set(treatment_mi[treatment_mi['MI_Score'] > significant_threshold_treatment]['miRNA'])
    significant_miRNAs_control = set(control_mi[control_mi['MI_Score'] > significant_threshold_control]['miRNA'])

    # Categorizing into the five groups
    unique_miRNAs_treatment = significant_miRNAs_treatment - significant_miRNAs_control
    unique_miRNAs_control = significant_miRNAs_control - significant_miRNAs_treatment
    significant_miRNAs_intersection = significant_miRNAs_treatment.intersection(significant_miRNAs_control)

    # Convert sets to DataFrames
    mi_treatment_unique = pd.DataFrame(list(unique_miRNAs_treatment), columns=['miRNA'])
    mi_control_unique = pd.DataFrame(list(unique_miRNAs_control), columns=['miRNA'])
    mi_intersection = pd.DataFrame(list(significant_miRNAs_intersection), columns=['miRNA'])
    mi_treatment = pd.DataFrame(list(significant_miRNAs_treatment), columns=['miRNA'])
    mi_control = pd.DataFrame(list(significant_miRNAs_control), columns=['miRNA'])

    # Save each DataFrame to a CSV file
    mi_treatment_unique.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/mi/mi_treatment_unique.csv', index=False)
    mi_control_unique.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/mi/mi_control_unique.csv', index=False)
    mi_intersection.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/mi/mi_intersection.csv', index=False)
    mi_treatment.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/mi/mi_treatment.csv', index=False)
    mi_control.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/mi/mi_control.csv', index=False)

    print("MI analysis categorized into 5 groups and saved to CSV files.")

    
perform_mi_analysis_and_categorize()
