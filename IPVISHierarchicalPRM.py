# coding: utf-8

"""
HierarchicalPRM Visualizer (KIT-style)
Compatible with BasicPRM, LazyPRM, VisPRM, etc.
"""

import networkx as nx

def hierarchicalPRMVisualize(planner, solution=None, ax=None, nodeSize=300):
    graph = planner.graph
    collChecker = planner._collisionChecker
    pos = nx.get_node_attributes(graph, 'pos')

    if solution is None:
        solution = planner.solution

    # 1. Obstacles
    collChecker.drawObstacles(ax)

    # 2. All nodes and edges
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color="lightblue", node_size=nodeSize)
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="gray", width=1.0, alpha=0.2)

    # 3. Largest connected component
    Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
    if Gcc:
        G0 = graph.subgraph(Gcc[0])
        nx.draw_networkx_edges(G0, pos, ax=ax, edge_color='b', width=2.0, alpha=0.5)

    # 4. Solution path
    if solution:
        Gsp = nx.subgraph(graph, solution)
        nx.draw_networkx_nodes(Gsp, pos, ax=ax, node_color="green", node_size=nodeSize * 1.2)
        nx.draw_networkx_edges(Gsp, pos, ax=ax, edge_color="green", width=5.0)

    # 5. Start/Goal
    if "start" in graph.nodes():
        nx.draw_networkx_nodes(graph, pos, nodelist=["start"], node_color="#00dd00", node_size=nodeSize, ax=ax)
        nx.draw_networkx_labels(graph, pos, labels={"start": "S"}, ax=ax)
    if "goal" in graph.nodes():
        nx.draw_networkx_nodes(graph, pos, nodelist=["goal"], node_color="#dd0000", node_size=nodeSize, ax=ax)
        nx.draw_networkx_labels(graph, pos, labels={"goal": "G"}, ax=ax)
