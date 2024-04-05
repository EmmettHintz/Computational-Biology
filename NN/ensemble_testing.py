# Import necessary libraries
from fastai.tabular.all import *
from fastai.metrics import accuracy
import pandas as pd
import optuna
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import seaborn as sns
import matplotlib.pyplot as plt

# Load your datasets
train_path = '/Users/emmetthintz/Documents/Computational-Biology/Predictive Data/filtered_train_data.csv'
test_path = '/Users/emmetthintz/Documents/Computational-Biology/Predictive Data/filtered_test_data.csv'

train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

# Convert 'Response' to categorical
train_df['Response'] = train_df['Response'].astype('category')
test_df['Response'] = test_df['Response'].astype('category')

# Filter test_df to only include treatment == 1
test_df_treatment = test_df[test_df['Treatment'] == 1]

# Define your continuous and categorical columns
cont_cols = [col for col in train_df.columns if col not in ['Participant ID', 'Treatment', 'Response']]
cat_cols = []  # Assuming no categorical variables for simplicity

# Define the percentage of data to use for validation
valid_pct = 0.2

# Create DataLoaders outside of the objective function to avoid re-creation for each trial
dls = TabularDataLoaders.from_df(train_df, path=".", procs=[Normalize],
                                 cat_names=cat_cols, cont_names=cont_cols,
                                 y_names="Response", y_block=CategoryBlock(),
                                 bs=32, valid_idx=range(int(len(train_df)*(1-valid_pct)), len(train_df)))

# Objective function for Optuna
def objective(trial):
    lr = trial.suggest_loguniform("lr", 1e-5, 1e-1)
    n_layers = trial.suggest_int("n_layers", 2, 5)
    layers = [trial.suggest_int(f"units_layer_{i}", 50, 200) for i in range(n_layers)]
    dropout = trial.suggest_uniform("dropout", 0.1, 0.5)
    
    config = tabular_config(ps=dropout)
    learn = tabular_learner(dls, layers=layers, metrics=accuracy, config=config)
    
    with learn.no_bar(), learn.no_logging():  # Optional, reduces verbosity
        learn.fit_one_cycle(5, lr)
    
    # Change this line
    validation_accuracy = learn.validate()[1]
    return validation_accuracy


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=10)

best_lr = study.best_params["lr"]
best_dropout = study.best_params["dropout"]
best_layers = [study.best_params[f"units_layer_{i}"] for i in range(study.best_params["n_layers"])]

# Function to train a model with the best parameters
def train_model_with_best_params(dls, lr, layers, dropout):
    config = tabular_config(ps=dropout)
    learn = tabular_learner(dls, layers=layers, metrics=accuracy, config=config)
    learn.fit_one_cycle(5, lr)
    return learn

# Ensemble
num_models = 5
models = [train_model_with_best_params(dls, best_lr, best_layers, best_dropout) for _ in range(num_models)]

# Ensemble predictions
test_dl_treatment = dls.test_dl(test_df_treatment)
preds_list_treatment = [model.get_preds(dl=test_dl_treatment)[0] for model in models]
avg_preds_treatment = torch.mean(torch.stack(preds_list_treatment), dim=0)
final_predictions_treatment = torch.argmax(avg_preds_treatment, dim=1).numpy()

# Actual labels
actual_labels = test_df_treatment['Response'].astype(int).to_numpy()

# Evaluation
accuracy = accuracy_score(actual_labels, final_predictions_treatment)
print(f"Ensemble Test Accuracy: {accuracy}")

precision = precision_score(actual_labels, final_predictions_treatment)
recall = recall_score(actual_labels, final_predictions_treatment)
f1 = f1_score(actual_labels, final_predictions_treatment)
roc_auc = roc_auc_score(actual_labels, avg_preds_treatment.numpy()[:, 1]) 

print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1:.3f}")
print(f"ROC AUC Score: {roc_auc:.3f}")

from sklearn.metrics import confusion_matrix

# Confusion Matrix Visualization
cm = confusion_matrix(actual_labels, final_predictions_treatment)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
