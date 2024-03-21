from sklearn.feature_selection import RFECV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
import pandas as pd

# Assuming you have a DataFrame `data` and a target variable `target`
data = pd.read_csv('Data/GSE97154_Cleaned.csv')
# Prepare your features and target variable
X = data.drop(columns=['Sample Name', 'Participant ID', 'Timepoint', 'Treatment', 'Response'])
y = data['Response']  # Or any other binary target variable you're interested in

# Initialize a Random Forest classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Initialize RFE with cross-validation
rfecv = RFECV(estimator=rf, step=1, cv=StratifiedKFold(5), scoring='accuracy')

rfecv.fit(X, y)

print("Optimal number of features: %d" % rfecv.n_features_)

# Plot number of features VS. cross-validation scores
import matplotlib.pyplot as plt

# Accessing the scores from the cv_results_
cv_scores = rfecv.cv_results_['mean_test_score']

plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross-validation score (nb of correct classifications)")
plt.plot(range(1, len(cv_scores) + 1), cv_scores)
plt.show()
