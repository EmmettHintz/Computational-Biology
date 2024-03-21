# Perform a t-test on the data to determine which features are most important for Gene Set
# Enrichment Analysis (GSEA)
# Will not perform a split here because I am not using this for training
import pandas as pd
from scipy.stats import ttest_ind


def main():
    # Load the data
    data = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/Data/GSE97154_Cleaned.csv')

    print('this is working ')
    
    # Perform the t-test
    t_test = ttest_ind(data['feature1'], data['feature2'])

    # Print the results
    print(t_test)
    
if __name__ == '__main__':
    main()