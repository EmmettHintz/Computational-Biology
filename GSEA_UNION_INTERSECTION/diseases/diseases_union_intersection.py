import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from scipy.stats import chi2_contingency

# Paths to the data files
control_path = '/Users/emmetthintz/Documents/Computational-Biology/GSEA_UNION_INTERSECTION/diseases/Control_Diseases.xlsx'
treatment_path = '/Users/emmetthintz/Documents/Computational-Biology/GSEA_UNION_INTERSECTION/diseases/Treatment_Diseases.xlsx'

try:
    # Load data
    control_df = pd.read_excel(control_path)
    treatment_df = pd.read_excel(treatment_path)

    # Extract disease names and scores
    control_diseases = control_df[['Name', 'Score']].set_index('Name').to_dict()['Score']
    treatment_diseases = treatment_df[['Name', 'Score']].set_index('Name').to_dict()['Score']

    # Convert dictionaries back to sets for set operations
    control_disease_names = set(control_diseases.keys())
    treatment_disease_names = set(treatment_diseases.keys())

    # Perform set operations
    union_names = control_disease_names.union(treatment_disease_names)
    intersection_names = control_disease_names.intersection(treatment_disease_names)
    control_unique_names = control_disease_names - intersection_names
    treatment_unique_names = treatment_disease_names - intersection_names

    # Extract scores for unique and intersection diseases
    union = {name: control_diseases.get(name, 0) + treatment_diseases.get(name, 0) for name in union_names}
    intersection = {name: (control_diseases[name], treatment_diseases[name]) for name in intersection_names}
    control_unique = {name: control_diseases[name] for name in control_unique_names}
    treatment_unique = {name: treatment_diseases[name] for name in treatment_unique_names}

    # Output results to CSV files
    pd.DataFrame(list(union.items()), columns=['Name', 'Combined Score']).to_csv('disease_union.csv')
    pd.DataFrame([{'Name': name, 'Score_Control': scores[0], 'Score_Treatment': scores[1]} for name, scores in intersection.items()], columns=['Name', 'Score_Control', 'Score_Treatment']).to_csv('disease_intersection.csv')
    pd.DataFrame(list(control_unique.items()), columns=['Name', 'Score']).to_csv('diseases_control_unique.csv')
    pd.DataFrame(list(treatment_unique.items()), columns=['Name', 'Score']).to_csv('diseases_treatment_unique.csv')

    # Creating a contingency table for chi-squared test
    contingency_table = [
        [len(control_unique), len(control_disease_names - control_unique_names)],
        [len(treatment_unique), len(treatment_disease_names - treatment_unique_names)]
    ]

    # Perform chi-squared test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    print(f"Chi-squared Test p-value: {p_value:.4f}")

    # Visualization using a Venn diagram
    plt.figure(figsize=(8, 8))
    venn2(subsets=(len(control_unique), len(treatment_unique), len(intersection)), 
          set_labels=('Control', 'Treatment'))
    plt.title('Disease Pathway Analysis')
    plt.show()

except Exception as e:
    print("An error occurred:", e)
