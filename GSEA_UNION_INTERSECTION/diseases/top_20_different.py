import pandas as pd
import matplotlib.pyplot as plt

# Load the data from Excel files
control_diseases = pd.read_excel('/Users/emmetthintz/Documents/Computational-Biology/GSEA_UNION_INTERSECTION/diseases/Control_diseases.xlsx')
treatment_diseases = pd.read_excel('/Users/emmetthintz/Documents/Computational-Biology/GSEA_UNION_INTERSECTION/diseases/Treatment_diseases.xlsx')

# Check column names
print("Control columns:", control_diseases.columns)
print("Treatment columns:", treatment_diseases.columns)

# Ensure correct column names are used
control_score_column = 'Score'  # Adjust if necessary
treatment_score_column = 'Score'  # Adjust if necessary

# Merge the two dataframes on the disease names with an indicator to track the source of each row
merged_df = pd.merge(control_diseases, treatment_diseases, on='Name', how='outer', suffixes=('_Control', '_Treatment'), indicator=True)

# Fill missing values with 0 or appropriate value before subtraction
merged_df[control_score_column + '_Control'].fillna(0, inplace=True)
merged_df[treatment_score_column + '_Treatment'].fillna(0, inplace=True)

# Calculate the difference in scores and indicate direction
merged_df['Score_Difference'] = merged_df[control_score_column + '_Control'] - merged_df[treatment_score_column + '_Treatment']
merged_df['Difference_Direction'] = merged_df['Score_Difference'].apply(lambda x: 'Increase' if x < 0 else 'Decrease')

# Sort the DataFrame by the absolute 'Score_Difference' column in descending order
sorted_df = merged_df.sort_values(by='Score_Difference', key=abs, ascending=False)

# Select the top 20 diseases with the highest score differences
top_20_differences = sorted_df.head(20)

# Print the top 20 diseases with their score difference and direction
print(top_20_differences[['Name', 'Score_Difference', 'Difference_Direction']])

import matplotlib.pyplot as plt

# Set a larger figure size for better visibility
plt.figure(figsize=(18, 12))

# Plotting the top 20 differences
ax = top_20_differences.set_index('Name')['Score_Difference'].plot(
    kind='bar',
    color=top_20_differences['Difference_Direction'].map({'Increase': 'red', 'Decrease': '#166082'}),
    width=0.8  # Adjust bar width for clarity
)

# Set title and labels with increased font sizes
plt.title('Top 20 Diseases by Score Difference After Treatment', fontsize=16)
plt.ylabel('Score Difference', fontsize=14)
plt.xlabel('Disease', fontsize=14)

# Rotate x-ticks for better visibility and set alignment
plt.xticks(rotation=60, ha='right', fontsize=12)  # Adjust rotation and font size

# Add gridlines for better readability
plt.grid(True, which='both', linestyle='', linewidth=0.5)

# Tight layout for better spacing
plt.tight_layout()

# Show the plot
plt.show()
