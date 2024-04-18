import pandas as pd

# Load the original dataset
data = pd.read_csv('Data/GSE97154_Cleaned.csv')

# Function to filter and save data for a specific group
def filter_and_save_data(significant_features_file, save_file):
    significant_features = pd.read_csv(significant_features_file)
    significant_miRNAs = significant_features['miRNA'].tolist()
    filtered_data = data[['Participant ID', 'Timepoint', 'Treatment', 'Response'] + significant_miRNAs]
    filtered_data.to_csv(save_file, index=False)

# Define file names for significant features and output files for the 5 groups
groups_files = {
    'treatment_unique': ('Data/treatment_unique_significant_features.csv', 'Data/treatment_unique_data.csv'),
    'control_unique': ('Data/control_unique_significant_features.csv', 'Data/control_unique_data.csv'),
    'intersection': ('Data/intersection_significant_features.csv', 'Data/intersection_data.csv'),
    'treatment': ('Data/treatment_significant_features.csv', 'Data/treatment_data.csv'),
    'control': ('Data/control_significant_features.csv', 'Data/control_data.csv')
}

# Apply the filter_and_save_data function for each group
for group, (features_file, save_file) in groups_files.items():
    filter_and_save_data(features_file, save_file)
    print(f"Filtered data for {group} group saved to {save_file}")
