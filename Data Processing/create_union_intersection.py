import pandas as pd

# Define your MI score threshold for significance
mi_score_threshold = 0.01  # Example threshold, adjust as needed

# Load the t-test results
significant_control_miRNAs_ttest = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/significant_control_miRNAs_ttest.csv')
significant_treatment_miRNAs_ttest = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/significant_treatment_miRNAs_ttest.csv')

# Load the MI results
control_mi_scores = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/control_mi_scores.csv')
treatment_mi_scores = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/treatment_mi_scores.csv')
import pandas as pd

# Fix column names for T-test datasets
significant_control_miRNAs_ttest.rename(columns={'Unnamed: 0': 'miRNA'}, inplace=True)
significant_treatment_miRNAs_ttest.rename(columns={'Unnamed: 0': 'miRNA'}, inplace=True)

# Filter miRNAs by MI score threshold
mi_score_threshold = 0.01
mi_treatment_filtered = treatment_mi_scores[treatment_mi_scores['MI_Score'] > mi_score_threshold]
mi_control_filtered = control_mi_scores[control_mi_scores['MI_Score'] > mi_score_threshold]

# Find unique significant miRNAs in the treatment group based on t-test
unique_treatment_ttest = set(significant_treatment_miRNAs_ttest['miRNA']) - set(significant_control_miRNAs_ttest['miRNA'])

# Now use the filtered MI data
unique_treatment_mi = set(mi_treatment_filtered['miRNA']) - set(mi_control_filtered['miRNA'])

# Union of significant features from T-test and MI Scores
union_significant_features = unique_treatment_ttest.union(unique_treatment_mi)

# Intersection of significant features from T-test and MI Scores
intersection_significant_features = unique_treatment_ttest.intersection(unique_treatment_mi)

# Prepare results for treatment
results_treatment = {
    "unique_treatment_ttest": list(unique_treatment_ttest),
    "unique_treatment_mi": list(unique_treatment_mi),
    "union_significant_features": list(union_significant_features),
    "intersection_significant_features": list(intersection_significant_features)
}

# Find unique significant miRNAs in the control group based on t-test
unique_control_ttest = set(significant_control_miRNAs_ttest['miRNA']) - set(significant_treatment_miRNAs_ttest['miRNA'])

# Now use the filtered MI data for control
unique_control_mi = set(mi_control_filtered['miRNA']) - set(mi_treatment_filtered['miRNA'])

# Union of significant features from T-test and MI Scores for control
union_significant_features_control = unique_control_ttest.union(unique_control_mi)

# Intersection of significant features from T-test and MI Scores for control
intersection_significant_features_control = unique_control_ttest.intersection(unique_control_mi)

# Prepare results for control
results_control = {
    "unique_control_ttest": list(unique_control_ttest),
    "unique_control_mi": list(unique_control_mi),
    "union_significant_features": list(union_significant_features_control),
    "intersection_significant_features": list(intersection_significant_features_control)
}

# Save results for treatment
union_df_treatment = pd.DataFrame(results_treatment['union_significant_features'], columns=['miRNA'])
intersection_df_treatment = pd.DataFrame(results_treatment['intersection_significant_features'], columns=['miRNA'])

# Save results for control
union_df_control = pd.DataFrame(results_control['union_significant_features'], columns=['miRNA'])
intersection_df_control = pd.DataFrame(results_control['intersection_significant_features'], columns=['miRNA'])

# Assuming paths are placeholders, replace with actual save locations
union_df_treatment.to_csv('union_significant_features_treatment.csv', index=False)
intersection_df_treatment.to_csv('intersection_significant_features_treatment.csv', index=False)

union_df_control.to_csv('union_significant_features_control.csv', index=False)
intersection_df_control.to_csv('intersection_significant_features_control.csv', index=False)


