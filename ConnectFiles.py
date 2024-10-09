import sys
from collections import defaultdict

# Helper function to find connected components in the graph
def find_connected_components(graph):
    visited = set()
    components = []

    def dfs(node, component):
        """ Depth-First Search to explore the component """
        visited.add(node)
        component.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)

    # Loop through each node in the graph and find all connected components
    for node in graph:
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(sorted(component))  # Sort for consistent output

    return components

# Function to build the graph from the parsed groups
def build_similarity_graph(similar_groups):
    """ Build a graph where each file index is a node and edges represent similarity """
    graph = defaultdict(set)
    
    # Add edges between all nodes in the same group
    for group in similar_groups:
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                graph[group[i]].add(group[j])
                graph[group[j]].add(group[i])

    return graph

# Function to read the file and extract the lists of similar files
def read_similar_groups(file_path):
    """ Reads the output file and extracts groups of similar files as lists of integers """
    similar_groups = []
    
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('['):  # Only consider lines that start with '['
                group = list(map(int, line.strip()[1:-1].split(',')))
                similar_groups.append(group)

    return similar_groups

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('\nUsage: python process_similar_files.py found_similar_files.txt\n')
        sys.exit(0)

    output_file = sys.argv[1]

    # Read similar groups from the output text file
    similar_groups = read_similar_groups(output_file)

    # Build a graph where nodes are file indices, and edges represent similarity
    similarity_graph = build_similarity_graph(similar_groups)

    # Find connected components (final groups of similar files)
    final_groups = find_connected_components(similarity_graph)

    # Output final connected groups of similar files
    print("Final groups of similar files (by column index):")
    for group in final_groups:
        print(group)
