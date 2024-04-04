import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer

def discretize_data(X, n_bins=3):
    """
    Discretize the continuous data into n_bins equal-width bins.
    
    Parameters:
    - X: {numpy array}, shape (n_samples, n_features)
        Continuous input data to be discretized.
    - n_bins: int, default=3
        The number of bins to use for discretization.
        
    Returns:
    - X_discrete: {numpy array}, shape (n_samples, n_features)
        Discretized input data.
    """
    from sklearn.preprocessing import KBinsDiscretizer
    est = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy='uniform', subsample=200000)
    X_discrete = est.fit_transform(X)
    return X_discrete


def JMI(X, y, k=10):
    """
    Joint Mutual Information (JMI) for feature selection.
    
    Parameters:
    - X: {numpy array}, shape (n_samples, n_features)
        Input data.
    - y: {numpy array}, shape (n_samples,)
        Target labels.
    - k: int, default=10
        Number of features to select.
        
    Returns:
    - F: {numpy array}
        Indices of the selected features.
    """
    from sklearn.feature_selection import mutual_info_classif
    import numpy as np
    
    n_samples, n_features = X.shape
    F = []
    
    # Calculate the MI between each feature and the target
    MI = mutual_info_classif(X, y)
    
    # Select the feature with the highest MI to Y
    F.append(np.argmax(MI))
    
    for _ in range(k-1):
        # Calculate the MI between the selected feature and all other features
        MI = np.array([mutual_info_classif(X[:, i].reshape(-1, 1), X[:, F].T).mean() for i in range(n_features)])
        
        # Select the feature with the highest MI to the selected features
        F.append(np.argmax(MI))
    
    return np.array(F, dtype=int)


data_path = '/Users/emmetthintz/Documents/Computational-Biology/Data/Union_Data.csv'
data = pd.read_csv(data_path)
# print(data.head())
X = data.drop(['Participant ID', 'Timepoint', 'Treatment', 'Response'], axis=1).values
y = data['Response'].values

# Discretize the data
X_discrete = discretize_data(X, n_bins=3)

# Make y into a 1d array
y = y.flatten()

# Apply JMI
F = JMI(X_discrete, y)
print(F)
