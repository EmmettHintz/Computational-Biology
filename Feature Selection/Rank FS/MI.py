from sklearn.feature_selection import mutual_info_regression
import numpy as np
import pandas as pd

# Load the data
data = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/GSE97154_Cleaned.csv')

treatment_group = data[data['Treatment'] == 1]
control_group = data[data['Treatment'] == 0]

def calculate_mutual_information(group):
    t0 = group[group['Timepoint'] == 'T0']
    t8 = group[group['Timepoint'] == 'T8']
    
    miRNAs = group.columns[5:]  # Assuming miRNA expression starts at column 5
    mi_scores = np.zeros(len(miRNAs))
    
    # Combining T0 and T8 samples for MI calculation
    combined_data = pd.concat([t0, t8])
    for index, miRNA in enumerate(miRNAs):
        # MI expects a continuous target, hence we'll use timepoints as binary labels (0 for T0, 1 for T8)
        labels = [0]*len(t0) + [1]*len(t8)
        mi_score = mutual_info_regression(combined_data[[miRNA]], labels, discrete_features=False)
        mi_scores[index] = mi_score[0]
        
    return pd.DataFrame({'miRNA': miRNAs, 'MI_Score': mi_scores})

def perform_mi_analysis():
    treatment_mi = calculate_mutual_information(treatment_group)
    control_mi = calculate_mutual_information(control_group)
    
    # For demonstration, we will print the top 5 miRNAs based on MI score
    print("Top 5 MI Scores in Treatment Group:")
    print(treatment_mi.sort_values(by='MI_Score', ascending=False).head())
    print("\nTop 5 MI Scores in Control Group:")
    print(control_mi.sort_values(by='MI_Score', ascending=False).head())
    
perform_mi_analysis()