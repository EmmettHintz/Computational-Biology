import pandas as pd

control_path = '//Users/emmetthintz/Documents/Computational-Biology/GSEA_UNION_INTERSECTION/diseases/Control_diseases.xlsx'
treatment_path = '/Users/emmetthintz/Documents/Computational-Biology/GSEA_UNION_INTERSECTION/diseases/Treatment_Diseases.xlsx'

control_df = pd.read_excel(control_path)
treatment_df = pd.read_excel(treatment_path)

control_pathways = set(control_df['Name'])
treatment_pathways = set(treatment_df['Name'])

# Find the union of the two sets
union = control_pathways.union(treatment_pathways)

# Find the intersection of the two sets
intersection = control_pathways.intersection(treatment_pathways)

# Find the unique pathways in the control set
control_unique = control_pathways - intersection

# Find the unique pathways in the treatment set
treatment_unique = treatment_pathways - intersection

# Print the results
# print('Union:', union)
# print('Intersection:', intersection)
print('Control Unique:', control_unique)
print('Treatment Unique:', treatment_unique)
