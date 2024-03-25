import pandas as pd

data = pd.read_csv('Data/GSE97154_Cleaned.csv')

union_significant_features = pd.read_csv('Data/Union_Significant_Features.csv')

significant_miRNAs = union_significant_features['miRNA'].tolist()

# Filter the origional dataset to include only the significant miRNAs
# Keep only necessary columns
filtered_data = data[['Participant ID', 'Timepoint', 'Treatment', 'Response'] + significant_miRNAs]

# Save as a csv
filtered_data.to_csv('Data/Union_Data.csv', index=False)