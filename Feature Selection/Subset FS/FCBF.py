import pandas as pd
import numpy as np
# Assuming su_calculation.py is in the same directory or the path is set
import su_calculation as su
from sklearn.preprocessing import KBinsDiscretizer

def fcbf(X, y, **kwargs):
    """
    Fast Correlation-Based Filter (FCBF) algorithm.
    """
    n_samples, n_features = X.shape
    delta = kwargs.get('delta', 0)
    
    t1 = np.zeros((n_features, 2), dtype='object')
    for i in range(n_features):
        f = X[:, i]
        t1[i, 0] = i
        t1[i, 1] = su.su_calculation(f, y)
    s_list = t1[t1[:, 1] > delta, :]
    
    F = []
    SU = []
    while len(s_list) != 0:
        idx = np.argmax(s_list[:, 1])
        fp = X[:, int(s_list[idx, 0])]
        np.delete(s_list, idx, 0)
        F.append(s_list[idx, 0])
        SU.append(s_list[idx, 1])
        s_list = np.array([i for i in s_list if su.su_calculation(fp, X[:, int(i[0])]) < t1[int(i[0]), 1]])
    return np.array(F, dtype=int), np.array(SU)

# Load the dataset
file_path = '/Users/emmetthintz/Documents/Computational-Biology/Data/union_significant_features.csv'  # Adjust the file path as necessary
data = pd.read_csv(file_path)

# Assuming the last column is the class label
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Discretize the features if they are continuous
# Here, we use KBinsDiscretizer as an example
est = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='uniform')
X_discretized = est.fit_transform(X)

# Apply FCBF
delta = 0.01  # Threshold for feature selection, adjust based on your analysis
F, SU = fcbf(X_discretized, y, delta=delta)

# Print the indices of the selected features and their SU values
print("Selected feature indices:", F)
print("Symmetrical Uncertainty (SU) of selected features:", SU)

# If needed, extract the names of the selected features
selected_feature_names = data.columns[F].tolist()
print("Selected feature names:", selected_feature_names)
