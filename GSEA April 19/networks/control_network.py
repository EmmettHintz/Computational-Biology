import pandas as pd
import networkx as nx

# Load the control data from Excel file
control_data = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/control_group/control_genes_miRTarBase.csv')

# Filter for p-value < 0.05
control_filtered = control_data[control_data['p-value'] < 0.05]

# Initialize the main graph
G_control = nx.Graph()

# Dictionary to count unique miRNAs per gene
gene_miRNA_count = {}

# First pass: count unique miRNAs for each gene
for index, row in control_filtered.iterrows():
    gene_node = row['Gene Symbol']
    gene_miRNA_count.setdefault(gene_node, set())

    # Check each microRNA column for non-null entries
    for col in control_data.columns[control_data.columns.str.contains('microRNA')]:
        miRNA_node = row[col]
        if pd.notna(miRNA_node):
            gene_miRNA_count[gene_node].add(miRNA_node)

# List to store genes included in the graph
included_genes_control = []

# Second pass: add only genes with >= 3 miRNAs and their miRNAs to the graph
for gene_node, miRNAs in gene_miRNA_count.items():
    if len(miRNAs) >= 3:
        G_control.add_node(gene_node, type='gene')
        included_genes_control.append(gene_node)
        for miRNA_node in miRNAs:
            G_control.add_node(miRNA_node, type='miRNA')
            G_control.add_edge(gene_node, miRNA_node)

# Save the subgraph of the control network to a GraphML file
control_subgraph_graphml_path = '/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/networks/control_gene_subgraph_network.graphml'
nx.write_graphml(G_control, control_subgraph_graphml_path)

pd.DataFrame(included_genes_control, columns=['Gene Symbol']).to_csv('included_genes_control.csv', index=False)