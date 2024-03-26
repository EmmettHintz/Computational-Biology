import pandas as pd

# Define your MI score threshold for significance
mi_score_threshold = 0.01  # Example threshold, adjust as needed

# Load the t-test results
ttest_control = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/significant_control_miRNAs_ttest.csv')
ttest_treatment = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/significant_treatment_miRNAs_ttest.csv')

# Load the MI results
mi_control = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/control_mi_scores.csv')
mi_treatment = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/treatment_mi_scores.csv')

# Filter miRNAs by MI score threshold
mi_treatment_filtered = mi_treatment[mi_treatment['MI_Score'] > mi_score_threshold]
mi_control_filtered = mi_control[mi_control['MI_Score'] > mi_score_threshold]

# Find unique significant miRNAs in the treatment group based on t-test
unique_treatment_ttest = set(ttest_treatment['miRNA']) - set(ttest_control['miRNA'])

# Now use the filtered MI data
unique_treatment_mi = set(mi_treatment_filtered['miRNA']) - set(mi_control_filtered['miRNA'])

print("Unique significant miRNAs in the treatment group based on t-test:")
print(unique_treatment_ttest)

print("\nUnique significant miRNAs in the treatment group based on MI:")
print(unique_treatment_mi)

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
