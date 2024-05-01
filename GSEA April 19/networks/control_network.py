import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the control data from Excel file
control_data = pd.read_csv('/Users/emmetthintz/Documents/Computational-Biology/GSEA April 19/control_group/control_genes_miRTarBase.csv')

# Filter control data for p-value < 0.05
control_filtered = control_data[control_data['p-value'] < 0.05]

# Initialize a graph for the control network
G_control = nx.Graph()

# Add nodes and edges based on gene-miRNA relationships
for index, row in control_filtered.iterrows():
    gene_node = row['Gene Symbol']
    G_control.add_node(gene_node, type='gene')
    
    # Iterate through microRNA columns to add edges
    for col in control_data.columns[control_data.columns.str.contains('microRNA')]:
        if pd.notna(row[col]):
            miRNA_node = row[col]
            G_control.add_node(miRNA_node, type='miRNA')
            G_control.add_edge(gene_node, miRNA_node)

# Count the number of gene connections for each miRNA
miRNA_gene_connections = {}
for miRNA_node in G_control.nodes():
    if G_control.nodes[miRNA_node]['type'] == 'miRNA':
        gene_connections = sum(1 for neighbor in G_control.neighbors(miRNA_node) if G_control.nodes[neighbor]['type'] == 'gene')
        miRNA_gene_connections[miRNA_node] = gene_connections

# Sort miRNAs by the number of gene connections and get top 10
top_miRNAs = sorted(miRNA_gene_connections.items(), key=lambda x: x[1], reverse=True)[:10]

# Create a DataFrame for top miRNAs
top_miRNAs_df = pd.DataFrame(top_miRNAs, columns=['miRNA', 'Number of Gene Connections'])

# Display the top 10 miRNAs and their number of gene connections using Matplotlib
plt.figure(figsize=(8, 6))
ax = plt.gca()
ax.axis('off')  # Turn off axis
ax.set_title('Top 10 Control miRNAs and Their Number of Gene Connections', fontsize=14, fontweight='bold')

# Plot table with zebra striping
table = ax.table(cellText=top_miRNAs_df.values,
                 colLabels=top_miRNAs_df.columns,
                 cellLoc='center',
                 loc='upper left',
                 colColours=['#166082'] * 2,
                 bbox=[0.1, 0.1, 0.8, 0.8])

# Set column header text color to white
for i, cell in enumerate(table.get_celld().values()):
    row, col = divmod(i, len(top_miRNAs_df.columns))  # Calculate row and column indices
    if row % 2 != 0 and row != 0:
        # Alternate row colors (skip first row)
        cell.set_facecolor('#F5F5F5')  # Light gray background color for odd rows


plt.show()