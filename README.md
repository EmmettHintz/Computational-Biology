# Computational-Biology

## Description

This repository contains the code for my research in BIOL 481.

## Contents

Feature Selection:

### Rank FS

- t-test
- MI

### Subset FS

- FCBF
- RFE


## April 19 Progress -- 5 Group model

Intersections for each group:

control:
hsa-miR-503-5p,hsa-miR-3615,hsa-miR-425-5p,hsa-miR-3605-3p,hsa-miR-146a-5p,hsa-miR-24-3p,hsa-miR-215-5p,hsa-miR-146b-5p,hsa-miR-3173-5p,hsa-miR-425-3p,hsa-miR-146b-3p,hsa-miR-484,hsa-miR-3909,hsa-miR-4677-3p,hsa-miR-486-5p,hsa-miR-659-5p,hsa-miR-3074-5p,hsa-miR-29b-3p

control_unique:
hsa-miR-3605-3p,hsa-miR-146b-3p,hsa-miR-659-5p,hsa-miR-29b-3p

intersection:
hsa-miR-503-5p,hsa-miR-146a-5p,hsa-miR-24-3p,hsa-miR-215-5p,hsa-miR-146b-5p,hsa-miR-3173-5p,hsa-miR-425-3p,hsa-miR-3909,hsa-miR-4677-3p,hsa-miR-3074-5p

treatment:
hsa-miR-3184-5p,hsa-miR-146a-5p,hsa-miR-324-5p,hsa-miR-6511a-3p,hsa-miR-425-3p,hsa-miR-3909,hsa-miR-4677-3p,hsa-miR-503-5p,hsa-miR-24-3p,hsa-miR-146b-5p,hsa-miR-1180-3p,hsa-miR-3074-5p,hsa-miR-2110,hsa-miR-3173-5p,hsa-miR-191-5p,hsa-miR-6750-3p,hsa-let-7d-3p,hsa-miR-361-3p,hsa-miR-215-5p,hsa-miR-451b,hsa-miR-6741-3p

treatment_unique:
hsa-miR-6750-3p,hsa-miR-361-3p,hsa-miR-6741-3p,hsa-miR-451b

FCBF:
Analyzing treatment_unique Group
Selected Feature Indices: [50]
SU Scores: [0.02040865]
treatment_unique Group - Selected miRNAs:
hsa-miR-26b-3p

Analyzing control_unique Group
Selected Feature Indices: [30]
SU Scores: [0.01270064]
control_unique Group - Selected miRNAs:
hsa-miR-15b-3p

Analyzing intersection Group
Selected Feature Indices: [16]
SU Scores: [0.01000873]
intersection Group - Selected miRNAs:
hsa-miR-146b-5p

Analyzing treatment Group
Selected Feature Indices: [37]
SU Scores: [0.02040865]
treatment Group - Selected miRNAs:
hsa-miR-26b-3p

Analyzing control Group
Selected Feature Indices: [25]
SU Scores: [0.01270064]
control Group - Selected miRNAs:
hsa-miR-15b-3p

RFE:

Analyzing treatment_unique Group
treatment_unique Group - Selected Features: ['hsa-let-7d-3p', 'hsa-miR-26b-3p']
Optimal Number of Features (treatment_unique): 2

Analyzing control_unique Group
control_unique Group - Selected Features: ['hsa-miR-4742-3p']
Optimal Number of Features (control_unique): 1

Analyzing intersection Group
intersection Group - Selected Features: ['hsa-miR-5010-3p', 'hsa-miR-1180-3p']
Optimal Number of Features (intersection): 2

Analyzing treatment Group
treatment Group - Selected Features: ['hsa-let-7d-3p', 'hsa-miR-26b-3p']
Optimal Number of Features (treatment): 2

Analyzing control Group
control Group - Selected Features: ['hsa-miR-4742-3p', 'hsa-miR-423-3p']
Optimal Number of Features (control): 2

1. Control Group Combined List for GSEA:
hsa-miR-503-5p
hsa-miR-3615
hsa-miR-425-5p
hsa-miR-3605-3p
hsa-miR-146a-5p
hsa-miR-24-3p
hsa-miR-215-5p
hsa-miR-146b-5p
hsa-miR-3173-5p
hsa-miR-425-3p
hsa-miR-146b-3p
hsa-miR-484
hsa-miR-3909
hsa-miR-4677-3p
hsa-miR-486-5p
hsa-miR-659-5p
hsa-miR-3074-5p
hsa-miR-29b-3p
hsa-miR-15b-3p
hsa-miR-4742-3p
hsa-miR-423-3p
2. Control Unique Group Combined List for GSEA:
hsa-miR-3605-3p
hsa-miR-146b-3p
hsa-miR-659-5p
hsa-miR-29b-3p
hsa-miR-15b-3p
hsa-miR-4742-3p
3. Intersection Group Combined List for GSEA:
hsa-miR-503-5p
hsa-miR-146a-5p
hsa-miR-24-3p
hsa-miR-215-5p
hsa-miR-146b-5p
hsa-miR-3173-5p
hsa-miR-425-3p
hsa-miR-3909
hsa-miR-4677-3p
hsa-miR-3074-5p
hsa-miR-5010-3p
hsa-miR-1180-3p
4. Treatment Group Combined List for GSEA:
hsa-miR-3184-5p
hsa-miR-146a-5p
hsa-miR-324-5p
hsa-miR-6511a-3p
hsa-miR-425-3p
hsa-miR-3909
hsa-miR-4677-3p
hsa-miR-503-5p
hsa-miR-24-3p
hsa-miR-146b-5p
hsa-miR-1180-3p
hsa-miR-3074-5p
hsa-miR-2110
hsa-miR-3173-5p
hsa-miR-191-5p
hsa-miR-6750-3p
hsa-let-7d-3p
hsa-miR-361-3p
hsa-miR-215-5p
hsa-miR-451b
hsa-miR-6741-3p
hsa-miR-26b-3p
hsa-let-7d-3p
5. Treatment Unique Group Combined List for GSEA:
hsa-miR-6750-3p
hsa-miR-361-3p
hsa-miR-6741-3p
hsa-miR-451b
hsa-miR-26b-3p
hsa-let-7d-3p

## With 'hsa-' removed

1. Control Group Combined List for GSEA:
miR-503-5p
miR-3615
miR-425-5p
miR-3605-3p
miR-146a-5p
miR-24-3p
miR-215-5p
miR-146b-5p
miR-3173-5p
miR-425-3p
miR-146b-3p
miR-484
miR-3909
miR-4677-3p
miR-486-5p
miR-659-5p
miR-3074-5p
miR-29b-3p
miR-15b-3p
miR-4742-3p
miR-423-3p
2. Control Unique Group Combined List for GSEA:
miR-3605-3p
miR-146b-3p
miR-659-5p
miR-29b-3p
miR-15b-3p
miR-4742-3p
3. Intersection Group Combined List for GSEA:
miR-503-5p
miR-146a-5p
miR-24-3p
miR-215-5p
miR-146b-5p
miR-3173-5p
miR-425-3p
miR-3909
miR-4677-3p
miR-3074-5p
miR-5010-3p
miR-1180-3p
4. Treatment Group Combined List for GSEA:
miR-3184-5p
miR-146a-5p
miR-324-5p
miR-6511a-3p
miR-425-3p
miR-3909
miR-4677-3p
miR-503-5p
miR-24-3p
miR-146b-5p
miR-1180-3p
miR-3074-5p
miR-2110
miR-3173-5p
miR-191-5p
miR-6750-3p
let-7d-3p
miR-361-3p
miR-215-5p
miR-451b
miR-6741-3p
miR-26b-3p
let-7d-3p
5. Treatment Unique Group Combined List for GSEA:
miR-6750-3p
miR-361-3p
miR-6741-3p
miR-451b
miR-26b-3p
let-7d-3p