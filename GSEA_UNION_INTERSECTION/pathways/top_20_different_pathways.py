import pandas as pd
import matplotlib.pyplot as plt

# Load the data from CSV files
intersection_pathways = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/pathway_intersection.csv')

# Ensure the column names are correctly identified
print("Intersection columns:", intersection_pathways.columns)

# Assuming 'Name', 'Score_Control', and 'Score_Treatment' are the column names
intersection_pathways.rename(columns={'Name': 'Pathway'}, inplace=True)

# Calculate the absolute difference in scores
intersection_pathways['Score_Difference'] = (intersection_pathways['Score_Control'] - intersection_pathways['Score_Treatment']).abs()
intersection_pathways['Difference_Direction'] = intersection_pathways.apply(lambda x: 'Decrease' if x['Score_Control'] < x['Score_Treatment'] else 'Increase', axis=1)

# Sort the DataFrame by 'Score_Difference' in descending order
sorted_df = intersection_pathways.sort_values(by='Score_Difference', ascending=False)

# Select the top 20 pathways with the highest score differences
top_20_differences = sorted_df.head(20)

# Print the top 20 pathways with their score difference and direction
print(top_20_differences[['Pathway', 'Score_Difference', 'Difference_Direction']])

# Set a larger figure size for better visibility
plt.figure(figsize=(18, 12))

# Plotting the top 20 differences
ax = top_20_differences.set_index('Pathway')['Score_Difference'].plot(
    kind='bar',
    color=top_20_differences['Difference_Direction'].map({'Increase': 'red', 'Decrease': 'green'}),
    width=0.8  # Adjust bar width for clarity
)

# Set title and labels with increased font sizes
plt.title('Top 20 Pathways by Absolute Score Difference After Treatment', fontsize=16)
plt.ylabel('Absolute Score Difference', fontsize=14)
plt.xlabel('Pathway', fontsize=14)

# Rotate x-ticks for better visibility and set alignment
plt.xticks(rotation=60, ha='right', fontsize=12)  # Adjust rotation and font size

# Add gridlines for better readability
plt.grid(True, which='both', linestyle='-', linewidth=0.5)

# Tight layout for better spacing
plt.tight_layout()

# Show the plot
plt.show()
