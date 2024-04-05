# Import necessary libraries
from fastai.tabular.all import *
import pandas as pd
import optuna
from fastai.callback.tracker import EarlyStoppingCallback

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

# Objective function for Optuna
# Define a deeper network architecture
def objective(trial):
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    n_layers = trial.suggest_int("n_layers", 2, 5)  # Number of layers can range from 2 to 5
    layers = [trial.suggest_int(f"units_layer_{i}", 50, 200) for i in range(n_layers)]
    dropout = trial.suggest_float("dropout", 0.1, 0.5)  # Dropout rate between 10% and 50%
    
    dls = TabularDataLoaders.from_df(train_df, path=".", procs=[Normalize],
                                     cat_names=cat_cols, cont_names=cont_cols,
                                     y_names="Response", y_block=CategoryBlock(),
                                     bs=32, valid_idx=valid_idx)
    
    # Use tabular_config to specify model architecture configurations including dropout
    config = tabular_config(ps=dropout, embed_p=0.1)  # embed_p is for embedding dropout, which you might not use if there are no categorical variables
    learn = tabular_learner(dls, layers=layers, metrics=accuracy, config=config)
    
    learn.fit_one_cycle(5, lr)
    
    return learn.validate()[1]  # Returns accuracy for the last epoch



# optimization
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=10)

best_lr = study.best_params["lr"]
n_layers = study.best_params["n_layers"]  # This is how many layers you have

# Construct the best_layers list by iterating through the number of layers and fetching each one's size
best_layers = [study.best_params[f"units_layer_{i}"] for i in range(n_layers)]

# Proceed with recreating DataLoaders and defining the model with the best hyperparameters as before
dls = TabularDataLoaders.from_df(train_df, path=".", procs=[Normalize],
                                 cat_names=cat_cols, cont_names=cont_cols,
                                 y_names="Response", y_block=CategoryBlock(),
                                 bs=32, valid_idx=valid_idx)

learn = tabular_learner(dls, layers=best_layers, metrics=accuracy,
                        config=tabular_config(ps=study.best_params["dropout"]))

learn.fit_one_cycle(5, best_lr)

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
