from src import graph
from src.graph import djikstra

nodes = graph.build_fixed()
graph.print_2d(nodes)
djikstra.find_path(nodes)
