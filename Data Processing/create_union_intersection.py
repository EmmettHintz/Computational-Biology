import pandas as pd
# Load the data
mi_treatment_unique = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/mi/mi_treatment_unique.csv')
mi_control_unique = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/mi/mi_control_unique.csv')
mi_intersection = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/mi/mi_intersection.csv')
mi_treatment = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/mi/mi_treatment.csv')
mi_control = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/mi/mi_control.csv')

# t-test data
t_test_treatment_unique = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/t-test/t_test_treatment_unique.csv')
t_test_control_unique = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/t-test/t_test_control_unique.csv')
t_test_intersection = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/t-test/t_test_intersection.csv')
t_test_treatment = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/t-test/t_test_treatment.csv')
t_test_control = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/t-test/t_test_control.csv')


# Define function to calculate union and intersection for corresponding groups
def analyze_groups(mi_df, t_test_df, group_name):
    # Extract miRNA names from both datasets
    mi_set = set(mi_df['miRNA'])
    t_test_set = set(t_test_df['miRNA'])
    
    # Calculate union and intersection
    union_set = mi_set.union(t_test_set)
    intersection_set = mi_set.intersection(t_test_set)
    
    # Convert sets to DataFrames
    union_df = pd.DataFrame(list(union_set), columns=['miRNA'])
    intersection_df = pd.DataFrame(list(intersection_set), columns=['miRNA'])
    
    # Save to CSV files
    union_df.to_csv(f'/Users/emmetthintz/Documents/Computational-Biology/Data/union_{group_name}.csv', index=False)
    intersection_df.to_csv(f'/Users/emmetthintz/Documents/Computational-Biology/Data/intersection_{group_name}.csv', index=False)
    
    print(f"Saved union and intersection for {group_name}.")

# Apply the function to each pair of groups
analyze_groups(mi_treatment_unique, t_test_treatment_unique, 'treatment_unique')
analyze_groups(mi_control_unique, t_test_control_unique, 'control_unique')
analyze_groups(mi_intersection, t_test_intersection, 'intersection')
analyze_groups(mi_treatment, t_test_treatment, 'treatment')
analyze_groups(mi_control, t_test_control, 'control')
