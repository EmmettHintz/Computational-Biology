import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier

# Load the data
union = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/union_significant_features.csv')

intersection = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/intersection_significant_features.csv')

features = data.columns[5:]  # Assuming miRNA expression starts at column 5

# Initialize a dictionary to hold the differential expression values
diff_expression_dict = {}

# Calculate differential expression for each feature
for feature in features:
    diff_col_name = f"{feature}_diff"
    diff_expression_dict[diff_col_name] = data.groupby('Participant ID')[feature].transform(lambda x: x.diff().iloc[-1])

# Create the differential expression DataFrame from the dictionary
diff_expression_df = pd.DataFrame(diff_expression_dict)

# Drop rows with NaN values that may result from the diff() operation
diff_expression_df = diff_expression_df.dropna()

# Ensure the response variable is properly aligned with the differential expression DataFrame
response_aligned = data['Response'].loc[diff_expression_df.index]

# Initialize the model to be used in RFE
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Initialize RFE with Random Forest as the estimator
rfe = RFE(estimator=rf_classifier, n_features_to_select=36)  # Adjust as needed

# Fit RFE using the differential expression features and the aligned response
rfe.fit(diff_expression_df, response_aligned)

# Get the ranking of the features and select features accordingly
ranking = rfe.ranking_
selected_features = [diff_expression_df.columns[i] for i in range(len(diff_expression_df.columns)) if ranking[i] == 1]

# Print the selected features
print(f"Selected features based on differential expression: {selected_features}")