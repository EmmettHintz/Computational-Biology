from sklearn.feature_selection import RFECV
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Function to perform RFECV on a given dataset
def perform_rfecv(data_path):
    # Load the dataset
    data = pd.read_csv(data_path)
    
    # Assuming 'Response' is your target variable and the rest are features
    X = data.drop(['Participant ID', 'Timepoint', 'Treatment', 'Response'], axis=1)
    y = data['Response']
    
    # Initialize the model to be used as the estimator
    model = LogisticRegression(solver='liblinear')
    
    # Initialize RFECV with the logistic regression model
    rfecv = RFECV(estimator=model, step=1, cv=5, scoring='accuracy')  # You can adjust cv and scoring as needed
    
    # Fit RFECV
    rfecv.fit(X, y)
    
    # Selected features
    selected_features = X.columns[rfecv.support_]
    
    # Optimal number of features
    optimal_number_of_features = rfecv.n_features_
    
    return selected_features, optimal_number_of_features

# Paths to your datasets
treatment_data_path = '/Users/emmetthintz/Documents/Computational-Biology/Data/Union_Data.csv'
control_data_path = '/Users/emmetthintz/Documents/Computational-Biology/Data/CONTROL_union_data.csv'  

# Perform RFECV for both treatment and control groups
selected_features_treatment, optimal_features_treatment = perform_rfecv(treatment_data_path)
selected_features_control, optimal_features_control = perform_rfecv(control_data_path)

# Print selected features and optimal number of features for both groups
print("Treatment Group - Selected Features:", selected_features_treatment)
print("Optimal Number of Features (Treatment):", optimal_features_treatment)
print("Control Group - Selected Features:", selected_features_control)
print("Optimal Number of Features (Control):", optimal_features_control)
