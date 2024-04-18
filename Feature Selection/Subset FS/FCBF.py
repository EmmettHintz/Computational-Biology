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

# Treatment Group Analysis
treatment_data_path = '/Users/emmetthintz/Documents/Computational-Biology/Data/Union_Data.csv'  # Adjust path as necessary
treatment_data = pd.read_csv(treatment_data_path)
X_treatment = treatment_data.drop(['Participant ID', 'Timepoint', 'Treatment', 'Response'], axis=1).values
y_treatment = treatment_data['Response'].values
X_discrete_treatment = discretize_data(X_treatment, n_bins=3)
F_treatment, SU_treatment = fcbf(X_discrete_treatment, y_treatment)
print("Treatment Group - Selected Features:", F_treatment)
print("SU Scores:", SU_treatment)

# Assuming the features and response for the control group are similarly structured
# Control Group Analysis
control_data_path = '/Users/emmetthintz/Documents/Computational-Biology/Data/CONTROL_union_data.csv'  # Adjust this path to where your control data is located
control_data = pd.read_csv(control_data_path)
X_control = control_data.drop(['Participant ID', 'Timepoint', 'Treatment', 'Response'], axis=1).values
y_control = control_data['Response'].values
X_discrete_control = discretize_data(X_control, n_bins=3)
F_control, SU_control = fcbf(X_discrete_control, y_control)
print("Control Group - Selected Features:", F_control)
print("SU Scores:", SU_control)

# Display selected features by name for both groups
print("\nTreatment Group - Selected miRNAs:")
for index in F_treatment:
    print(treatment_data.columns[index+4])  # Adjust the index offset as necessary based on your dataset structure

print("\nControl Group - Selected miRNAs:")
for index in F_control:
    print(control_data.columns[index+4])  # Adjust the index offset as necessary based on your dataset structure