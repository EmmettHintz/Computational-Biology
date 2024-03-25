from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Load your data
# Note: Update the path to your actual dataset
data_path = '/Users/emmetthintz/Documents/Computational-Biology/Data/Union_Data.csv'
data = pd.read_csv(data_path)

# Assuming 'Response' is your target variable and the rest are features
X = data.drop(['Participant ID', 'Timepoint', 'Treatment', 'Response'], axis=1)
y = data['Response']

# Initialize the model to be used as the estimator
model = LogisticRegression(solver='liblinear')

# Initialize RFE with the logistic regression model
# Here, we aim to select 5 features. You can adjust this number based on your needs
rfe = RFE(estimator=model, n_features_to_select=5)

# Fit RFE
rfe.fit(X, y)

# Get the ranking of the features. The lower the rank, the more important the feature
feature_ranking = rfe.ranking_

# Selected features (where ranking == 1)
selected_features = X.columns[rfe.support_]

print("Selected Features:", selected_features)
