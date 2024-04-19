from sklearn.feature_selection import RFECV
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Function to perform RFECV on a given dataset and return selected features
def perform_rfecv(group_name, data_path):
    print(f"\nAnalyzing {group_name} Group")
    
    # Load the dataset
    data = pd.read_csv(data_path)
    
    # Assuming 'Response' is your target variable and the rest are features
    X = data.drop(['Participant ID', 'Timepoint', 'Treatment', 'Response'], axis=1)
    y = data['Response']
    
    # Initialize the model to be used as the estimator
    model = LogisticRegression(solver='liblinear')
    
    # Initialize RFECV with the logistic regression model
    rfecv = RFECV(estimator=model, step=1, cv=5, scoring='accuracy')  # Adjust cv and scoring as needed
    
    # Fit RFECV
    rfecv.fit(X, y)
    
    # Selected features
    selected_features = X.columns[rfecv.support_]
    
    # Optimal number of features
    optimal_number_of_features = rfecv.n_features_
    
    # Log selected features and optimal number
    print(f"{group_name} Group - Selected Features:", selected_features.tolist())
    print(f"Optimal Number of Features ({group_name}):", optimal_number_of_features)

# Dictionary mapping group names to their data files
groups_info = {
    'treatment_unique': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/treatment_unique/union_treatment_unique.csv',
    'control_unique': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/control_unique/union_control_unique.csv',
    'intersection': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/intersection/union_intersection.csv',
    'treatment': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/treatment/union_treatment.csv',
    'control': '/Users/emmetthintz/Documents/Computational-Biology/Data/Groups/control/union_control.csv'
}

# Analyze each group with RFECV
for group_name, data_path in groups_info.items():
    perform_rfecv(group_name, data_path)
