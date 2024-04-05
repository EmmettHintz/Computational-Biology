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

def perform_mi_analysis_and_save():
    treatment_mi = calculate_mutual_information_with_bootstrap(treatment_group)
    control_mi = calculate_mutual_information_with_bootstrap(control_group)
        
    # Save the MI scores to CSV files
    treatment_mi.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/treatment_mi_scores.csv', index=False)
    control_mi.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/control_mi_scores.csv', index=False)
    
    # For demonstration, we will print the top 5 miRNAs based on MI score
    print("Top 5 MI Scores in Treatment Group:")
    print(treatment_mi.sort_values(by='MI_Score', ascending=False).head())
    print("\nTop 5 MI Scores in Control Group:")
    print(control_mi.sort_values(by='MI_Score', ascending=False).head())
    
perform_mi_analysis_and_save()
