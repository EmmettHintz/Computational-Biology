from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

# Load your datasets
train_path = '/Users/emmetthintz/Documents/Computational-Biology/Predictive Data/filtered_train_data.csv'
test_path = '/Users/emmetthintz/Documents/Computational-Biology/Predictive Data/filtered_test_data.csv'

train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)


treatment_group = test_df[test_df['Treatment'] == 1]

# Convert 'Response' to categorical
train_df['Response'] = train_df['Response'].astype('category')
test_df['Response'] = test_df['Response'].astype('category')
# Assuming filtered_train_data and filtered_test_data are ready for use
X_train = train_df.drop(['Response', 'Treatment', 'Participant ID'], axis=1)
y_train = train_df['Response']
X_test_treatment = treatment_group.drop(['Response', 'Treatment', 'Participant ID'], axis=1) 
y_test_treatment = treatment_group['Response']

# Initialize the model
log_reg = LogisticRegression(max_iter=1000)

# Fit the model
log_reg.fit(X_train, y_train)

# Predictions
y_pred_train = log_reg.predict(X_train)
y_pred_test = log_reg.predict(X_test_treatment)

# Evaluate the model
print("Training Accuracy:", accuracy_score(y_train, y_pred_train))
print("Test Accuracy:", accuracy_score(y_test_treatment, y_pred_test))
print("\nTest Classification Report:\n", classification_report(y_test_treatment, y_pred_test))


import numpy as np

# Assuming `log_reg` is your trained LogisticRegression model
odds_ratios = np.exp(log_reg.coef_[0])

# For interpretability, create a DataFrame with the feature names and odds ratios
feature_names = X_test_treatment.columns
odds_ratio_df = pd.DataFrame({'Feature': feature_names, 'OddsRatio': odds_ratios})

# Sort by OddsRatio for better readability
odds_ratio_df = odds_ratio_df.sort_values(by="OddsRatio", ascending=False)

print(odds_ratio_df)

