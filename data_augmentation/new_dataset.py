"""
Once, prompts have been used to generate graphs in the form of an output.csv file, this script trnasform the output.csv file into a new dataset folder with:
    - a description folder: containing a valid prompt for each graph stored in a .txt file
    - a graph folder: containing a .edgelist file for each new graph describing the edges of the graph
"""

import os
import argparse
import pandas as pd
import csv
import networkx as nx
import ast  # Safer alternative to eval
from tqdm import tqdm

# Argument parser
parser = argparse.ArgumentParser(description='DataAugmentation')
parser = argparse.ArgumentParser(description='Transforms a CSV set of graphs into a new dataset')
parser.add_argument('--input', type=str, default='output.csv', help="CSV containing the graphs.")
parser.add_argument('--output-dir', type=int, default='train_augmented', help="New folder which will contain the new dataset.")

args = parser.parse_args()

# Replace with your output CSV file name
input_csv_filename = args.input
n = pd.read_csv(input_csv_filename).shape[0]

# Create folders for individual text and edge list files
base_output_folder = args.output_dir
description_folder = os.path.join(base_output_folder, "description")
edgelist_folder = os.path.join(base_output_folder, "graph")

os.makedirs(description_folder, exist_ok=True)
os.makedirs(edgelist_folder, exist_ok=True)

with open(input_csv_filename, "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header
    
    for row in tqdm(reader, total=n, desc=base_output_folder):
        graph_id = row[0]
        edge_list_text = row[1]  # Edge list is stored as a string
        
        # Convert edge list string back to tuples
        edge_list = ast.literal_eval(edge_list_text)  # Use ast.literal_eval instead of eval for safety
        G = nx.Graph()
        G.add_edges_from(edge_list)
        
        # Calculate graph characteristics
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        avg_degree = sum(dict(G.degree()).values()) / num_nodes
        triangles = sum(nx.triangles(G).values()) // 3
        clustering_coeff = nx.average_clustering(G)
        max_k_core = max(nx.core_number(G).values())
        num_communities = len(list(nx.algorithms.community.greedy_modularity_communities(G)))
        
        # Create the prompt for the graph
        prompt = (
            f"This graph comprises {num_nodes} nodes and {num_edges} edges. "
            f"The average degree is {avg_degree}, there are {triangles} triangles. "
            f"The global clustering coefficient is {clustering_coeff}, the maximum k-core is {max_k_core}. "
            f"The graph consists of {num_communities} communities."
        )
        
        # Save the prompt to an individual text file
        description_filename = os.path.join(description_folder, f"{graph_id}.txt")
        with open(description_filename, "w") as txtfile:
            txtfile.write(prompt)
        
        # Save the edge list to an individual .edgelist file
        edgelist_filename = os.path.join(edgelist_folder, f"{graph_id}.edgelist")
        nx.write_edgelist(G, edgelist_filename, data=False)
