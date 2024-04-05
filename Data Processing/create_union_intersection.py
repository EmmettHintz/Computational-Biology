import pandas as pd

# Define your MI score threshold for significance
mi_score_threshold = 0.01  # Example threshold, adjust as needed

# Load the t-test results
significant_control_miRNAs_ttest = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/significant_control_miRNAs_ttest.csv')
significant_treatment_miRNAs_ttest = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/significant_treatment_miRNAs_ttest.csv')

# Load the MI results
control_mi_scores = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/control_mi_scores.csv')
treatment_mi_scores = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/treatment_mi_scores.csv')

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

# Prepare results
results = {
    "unique_treatment_ttest": list(unique_treatment_ttest),
    "unique_treatment_mi": list(unique_treatment_mi),
    "union_significant_features": list(union_significant_features),
    "intersection_significant_features": list(intersection_significant_features)
}

# Display or save the results as needed
print("\nUnion of Significant Features:", results['union_significant_features'])
print("\nIntersection of Significant Features:", results['intersection_significant_features'])
print("Number of miRNAs in the union:", len(results['union_significant_features']))
print("Number of miRNAs in the intersection:", len(results['intersection_significant_features']))

# Save union and intersection as CSV files
union_df = pd.DataFrame(results['union_significant_features'], columns=['miRNA'])
union_df.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/union_significant_features.csv', index=False)

intersection_df = pd.DataFrame(results['intersection_significant_features'], columns=['miRNA'])
intersection_df.to_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/intersection_significant_features.csv', index=False)
