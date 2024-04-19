import pandas as pd

# Load the original dataset
data = pd.read_csv('Data/GSE97154_Cleaned.csv')

def process_and_save_filtered_data(group_name, union_sig_features_file, intersection_sig_features_file):
    # Process Union File
    if union_sig_features_file:
        significant_features_union = pd.read_csv(union_sig_features_file)
        significant_miRNAs_union = significant_features_union['miRNA'].tolist()
        filtered_data_union = data[['Participant ID', 'Timepoint', 'Treatment', 'Response'] + significant_miRNAs_union]
        filtered_data_union.to_csv(union_sig_features_file, index=False)
        print(f"Union data for {group_name} has been updated in place.")
    
    # Process Intersection File
    if intersection_sig_features_file:
        significant_features_intersection = pd.read_csv(intersection_sig_features_file)
        significant_miRNAs_intersection = significant_features_intersection['miRNA'].tolist()
        filtered_data_intersection = data[['Participant ID', 'Timepoint', 'Treatment', 'Response'] + significant_miRNAs_intersection]
        filtered_data_intersection.to_csv(intersection_sig_features_file, index=False)
        print(f"Intersection data for {group_name} has been updated in place.")

# Dictionary mapping group names to their union and intersection significant features files
groups_info = {
    'treatment_unique': {
        'union_sig_features': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/treatment_unique/union_treatment_unique.csv',
        'intersection_sig_features': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/treatment_unique/intersection_treatment_unique.csv'
    },
    'control_unique': {
        'union_sig_features': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/control_unique/union_control_unique.csv',
        'intersection_sig_features': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/control_unique/intersection_control_unique.csv'
    },
    'intersection': {
        'union_sig_features': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/intersection/union_intersection.csv',
        'intersection_sig_features': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/intersection/intersection_intersection.csv'
    },
    'treatment': {
        'union_sig_features': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/treatment/union_treatment.csv',
        'intersection_sig_features': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/treatment/intersection_treatment.csv'
    },
    'control': {
        'union_sig_features': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/control/union_control.csv',
        'intersection_sig_features': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/control/intersection_control.csv'
    }
}

# Process and save filtered data for each group
for group_name, paths in groups_info.items():
    process_and_save_filtered_data(group_name, paths.get('union_sig_features'), paths.get('intersection_sig_features'))
