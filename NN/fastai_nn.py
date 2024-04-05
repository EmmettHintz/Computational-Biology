# Import necessary libraries
from fastai.tabular.all import *
import pandas as pd

# Load your datasets
train_path = '/Users/emmetthintz/Documents/Computational-Biology/Predictive Data/filtered_train_data.csv' 
test_path = '/Users/emmetthintz/Documents/Computational-Biology/Predictive Data/filtered_test_data.csv'

train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

# Convert 'Response' to categorical
train_df['Response'] = train_df['Response'].astype('category')
test_df['Response'] = test_df['Response'].astype('category')

# Define your continuous and categorical columns
cont_cols = [col for col in train_df.columns if col not in ['Participant ID', 'Response']]
cat_cols = []  # Assuming no categorical variables for simplicity

# Define the percentage of data to use for validation
valid_pct = 0.2

# Adjusted approach to ensure validation set is correctly defined
valid_idx = range(len(train_df) - int(len(train_df) * valid_pct), len(train_df))

dls = TabularDataLoaders.from_df(train_df, path=".", procs=[Normalize],
                                 cat_names=cat_cols,
                                 cont_names=cont_cols,
                                 y_names="Response",
                                 y_block=CategoryBlock(),
                                 bs=32,  # Consider adjusting based on dataset size
                                 valid_idx=valid_idx)

# Before proceeding, let's ensure we have data loaded correctly
print(f"Training Set Size: {len(dls.train_ds)}")
print(f"Validation Set Size: {len(dls.valid_ds)}")

# Assuming the above sizes are printed and look reasonable, proceed to model training
learn = tabular_learner(dls, layers=[200,100], metrics=accuracy)

# It might be safer to skip lr_find if your dataset is very small or if you continue encountering errors
# learn.lr_find()

# If skipping lr_find, use a manually chosen learning rate
learn.fit_one_cycle(5, 1e-2)

# Continue with model evaluation and testing as before...


# Evaluate the model
learn.show_results()
interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()

# Prepare test DataLoader
test_dl = dls.test_dl(test_df)

# Get predictions
preds, _ = learn.get_preds(dl=test_dl)

# Convert predictions to labels
predicted_labels = preds.argmax(dim=1)

# import accuracy score
from sklearn.metrics import accuracy_score

# Evaluate on test data
actual_labels = test_df['Response'].astype(int).to_numpy()  # Ensure correct data type
accuracy = accuracy_score(actual_labels, predicted_labels.numpy())
print(f'Test Accuracy: {accuracy}')

# Visualize the confusion matrix
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(actual_labels, predicted_labels.numpy())
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

# Calculate additional metrics
precision = precision_score(actual_labels, predicted_labels.numpy())
recall = recall_score(actual_labels, predicted_labels.numpy())
f1 = f1_score(actual_labels, predicted_labels.numpy())
roc_auc = roc_auc_score(actual_labels, preds[:,1])

print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1:.3f}")
print(f"ROC AUC Score: {roc_auc:.3f}")
