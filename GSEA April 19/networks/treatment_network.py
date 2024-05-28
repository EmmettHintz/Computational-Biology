import pandas as pd
import networkx as nx

# Load the treatment data from Excel file
treatment_data = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/treatment_group/treatment_genes_miRTarBase.csv')

# Filter for p-value < 0.05
treatment_filtered = treatment_data[treatment_data['p-value'] < 0.05]

# Initialize the main graph
G_treatment = nx.Graph()

# Dictionary to count unique miRNAs per gene
gene_miRNA_count = {}

# First pass: count unique miRNAs for each gene
for index, row in treatment_filtered.iterrows():
    gene_node = row['Gene Symbol']
    gene_miRNA_count.setdefault(gene_node, set())

    # Check each microRNA column for non-null entries
    for col in treatment_data.columns[treatment_data.columns.str.contains('microRNA')]:
        miRNA_node = row[col]
        if pd.notna(miRNA_node):
            gene_miRNA_count[gene_node].add(miRNA_node)

# List to store genes included in the graph
included_genes_treatment = []

# Second pass: add only genes with >= 3 miRNAs and their miRNAs to the graph
for gene_node, miRNAs in gene_miRNA_count.items():
    if len(miRNAs) >= 3:
        G_treatment.add_node(gene_node, type='gene')
        included_genes_treatment.append(gene_node)
        for miRNA_node in miRNAs:
            G_treatment.add_node(miRNA_node, type='miRNA')
            G_treatment.add_edge(gene_node, miRNA_node)

# Save the subgraph of the treatment network to a GraphML file
treatment_subgraph_graphml_path = '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/networks/treatment_subgraph_network.graphml'
nx.write_graphml(G_treatment, treatment_subgraph_graphml_path)

pd.DataFrame(included_genes_treatment, columns=['Gene Symbol']).to_csv('included_genes_treatment.csv', index=False)
