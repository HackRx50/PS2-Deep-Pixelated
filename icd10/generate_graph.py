import pandas as pd
import networkx as nx

def build_graph_from_csv(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Initialize a directed graph
    G = nx.DiGraph()

    for idx, row in df.iterrows():
        # Extract codes and descriptions
        level1_code = row['LEVEL-1 Code']
        level1_desc = row['Level-1 Desc']

        level2_code = row['Level-2 Code']
        level2_desc = row['Level-2 Desc']

        level3_code = row['Level-3 Code']
        level3_desc = row['Level-3 Desc']

        icd_code = row['ICD_CODE']
        ped_description = row['PED_DESCRIPTION']

        ailment_group = row['Ailment Group']

        # Add nodes with attributes
        G.add_node(level1_code, description=level1_desc, level='Level 1')
        G.add_node(level2_code, description=level2_desc, level='Level 2')
        G.add_node(level3_code, description=level3_desc, level='Level 3')
        G.add_node(icd_code, description=ped_description, level='ICD Code')
        G.add_node(ailment_group, level='Ailment Group')

        # Add edges with 'relation' attribute
        G.add_edge(level1_code, level2_code, relation='parent_of')
        G.add_edge(level2_code, level3_code, relation='parent_of')
        G.add_edge(level3_code, icd_code, relation='parent_of')
        G.add_edge(icd_code, ailment_group, relation='has_ailment_group')

    return G

if __name__ == "__main__":
    # Replace with the path to your actual CSV file
    csv_file = 'C:/Users/Kartikey/Desktop/projects/LLM_rag/icd10/ICD.csv'
    graph = build_graph_from_csv(csv_file)

    # Save the graph to a GML file
    nx.write_gml(graph, 'icd10_graph.gml')

    # Print out some information about the graph
    print(f"Graph has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")
