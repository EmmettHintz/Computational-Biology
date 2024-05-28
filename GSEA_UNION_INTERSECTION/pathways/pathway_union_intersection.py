import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from scipy.stats import chi2_contingency

# Paths to the data files
control_path = '/Users/emmetthintz/Documents/Computational-Biology/GSEA_UNION_INTERSECTION/pathways/Control_Pathways.xlsx'
treatment_path = '/Users/emmetthintz/Documents/Computational-Biology/GSEA_UNION_INTERSECTION/pathways/Treatment_Pathways.xlsx'

try:
    # Load data
    control_df = pd.read_excel(control_path)
    treatment_df = pd.read_excel(treatment_path)

    # Extract pathway names and scores
    control_pathways = control_df[['SuperPath Name', 'Score']].set_index('SuperPath Name').to_dict()['Score']
    treatment_pathways = treatment_df[['SuperPath Name', 'Score']].set_index('SuperPath Name').to_dict()['Score']

    # Convert dictionaries back to sets for set operations
    control_pathway_names = set(control_pathways.keys())
    treatment_pathway_names = set(treatment_pathways.keys())

    # Perform set operations
    union_names = control_pathway_names.union(treatment_pathway_names)
    intersection_names = control_pathway_names.intersection(treatment_pathway_names)
    control_unique_names = control_pathway_names - intersection_names
    treatment_unique_names = treatment_pathway_names - intersection_names

    # Extract scores for unique and intersection pathways
    union = {name: control_pathways.get(name, 0) + treatment_pathways.get(name, 0) for name in union_names}
    intersection = {name: (control_pathways[name], treatment_pathways[name]) for name in intersection_names}
    control_unique = {name: control_pathways[name] for name in control_unique_names}
    treatment_unique = {name: treatment_pathways[name] for name in treatment_unique_names}

    # Output results to CSV files
    pd.DataFrame(list(union.items()), columns=['Name', 'Combined Score']).to_csv('pathway_union.csv')
    pd.DataFrame([{'Name': name, 'Score_Control': scores[0], 'Score_Treatment': scores[1]} for name, scores in intersection.items()], columns=['Name', 'Score_Control', 'Score_Treatment']).to_csv('pathway_intersection.csv')
    pd.DataFrame(list(control_unique.items()), columns=['Name', 'Score']).to_csv('pathways_control_unique.csv')
    pd.DataFrame(list(treatment_unique.items()), columns=['Name', 'Score']).to_csv('pathways_treatment_unique.csv')

    # Creating a contingency table for chi-squared test
    contingency_table = [
        [len(control_unique), len(control_pathway_names - control_unique_names)],
        [len(treatment_unique), len(treatment_pathway_names - treatment_unique_names)]
    ]

    # Perform chi-squared test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    print(f"Chi-squared Test p-value: {p_value:.4f}")

    # Visualization using a Venn diagram
    plt.figure(figsize=(8, 8))
    venn2(subsets=(len(control_unique), len(treatment_unique), len(intersection)), 
          set_labels=('Control', 'Treatment'))
    plt.title('Pathway Analysis')
    plt.show()

except Exception as e:
    print("An error occurred:", e)
