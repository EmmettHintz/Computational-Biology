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
