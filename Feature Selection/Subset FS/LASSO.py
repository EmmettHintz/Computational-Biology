import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler

union_sigificant_features = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/Union_Data.csv')

# Prepare the data
X = union_sigificant_features.drop(['Participant ID', 'Timepoint', 'Treatment', 'Response'], axis=1)
y = union_sigificant_features['Response']

# Split the data into training and test sets

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# Apply LASSO with cross-validation to find the optimal alpha
lasso_cv = LassoCV(cv=5, random_state=42, max_iter=10000)
lasso_cv.fit(X_scaled, y)

# Get the coefficients of the features
coefficients = lasso_cv.coef_

# Identify the features that were selected by LASSO (non-zero coefficients)
selected_features = X.columns[coefficients != 0]

selected_features, lasso_cv.score(X_scaled, y)

print(selected_features)
