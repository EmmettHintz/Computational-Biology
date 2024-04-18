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
- Lasso

## Identified Signifcant Features for GSEA

### From intersection of t-test and MI

- No overlapping features

### From FCBF

- hsa-miR-627-3p
- hsa-miR-3200-3p

### From RFE

- hsa-miR-148b-3p
- hsa-miR-22-3p
- hsa-let-7d-3p
- hsa-miR-6511a-3p
- hsa-miR-151a-5p

### Overview List of GSEA

- hsa-miR-627-3p
- hsa-miR-3200-3p
- hsa-miR-148b-3p
- hsa-miR-22-3p
- hsa-let-7d-3p
- hsa-miR-6511a-3p
- hsa-miR-151a-5p

### Fixed Analysis

- sFCBF:  
    -Treatment Group: Selected miRNAs:  
        - hsa-miR-30e-5p  
    -Control Group: Selected miRNAs:
        - hsa-miR-3615

- RFE:
    -Treatment Group  
        - Selected Features: Index(['hsa-miR-451b'], dtype='object')
    -Control Group  
        - Selected Features: Index(['hsa-let-7d-3p', 'hsa-miR-4742-3p'], dtype='object')

### Treatment

- hsa-miR-30e-5p
- hsa-miR-451b

### Control

- hsa-miR-3615
- hsa-let-7d-3p
- hsa-miR-4742-3p
