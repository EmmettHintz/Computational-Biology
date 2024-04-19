import numpy as np
import pandas as pd
# Placeholder for su_calculation module
import su_calculation as su

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

def fcbf(X, y, delta=0):
    n_samples, n_features = X.shape
    t1 = np.array([[i, su.su_calculation(X[:, i], y)] for i in range(n_features) if su.su_calculation(X[:, i], y) > delta])
    
    # Sort by SU in descending order
    t1 = t1[t1[:, 1].argsort()[::-1]]
    
    F = []
    SU = []
    
    while t1.shape[0] > 0:
        # Select the feature with the highest SU to Y
        F.append(int(t1[0, 0]))
        SU.append(t1[0, 1])
        
        # Remove selected feature from consideration
        t1 = np.delete(t1, 0, 0)
        
        # Remove redundant features
        t1 = np.array([t for t in t1 if su.su_calculation(X[:, int(t[0])], X[:, F[-1]]) < t[1]])
    
    return np.array(F, dtype=int), np.array(SU)

def analyze_group(group_name, data_path):
    print(f"Analyzing {group_name} Group")
    data = pd.read_csv(data_path)
    X = data.drop(['Participant ID', 'Timepoint', 'Treatment', 'Response'], axis=1).values
    y = data['Response'].values
    X_discrete = discretize_data(X, n_bins=3)
    F, SU = fcbf(X_discrete, y)
    # Display selected features and SU scores
    print("Selected Features:", F)
    print("SU Scores:", SU)
    # Display selected miRNAs by name
    print(f"\n{group_name} Group - Selected miRNAs:")
    for index in F:
        print(data.columns[index+4])  # Adjust the index offset as necessary
        
## Dictionary mapping group names to their data files
groups_info = {
    'treatment_unique': '/path/to/treatment_unique_data.csv',
    'control_unique': '/path/to/control_unique_data.csv',
    'intersection': '/path/to/intersection_data.csv',
    'treatment': '/path/to/treatment_data.csv',
    'control': '/path/to/control_data.csv'
}

# Analyze each group
for group_name, data_path in groups_info.items():
    analyze_group(group_name, data_path)