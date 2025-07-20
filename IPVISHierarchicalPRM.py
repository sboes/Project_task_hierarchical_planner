import networkx as nx
import matplotlib.pyplot as plt

def _drawStatsCloud(statsGraph, ax, nodeSize):
    pos = nx.get_node_attributes(statsGraph, 'pos')
    nx.draw_networkx_nodes(statsGraph, pos=pos, ax=ax, alpha=0.1, node_size=nodeSize, node_color='skyblue')
    nx.draw_networkx_edges(statsGraph, pos=pos, ax=ax, alpha=0.1, edge_color='orange')

def _drawGraph(graph, collChecker, ax, title, nodeSize=100, solution=None):
    pos = nx.get_node_attributes(graph, 'pos')
    collChecker.drawObstacles(ax)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color="lightblue", node_size=nodeSize)
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="gray", width=1.0, alpha=0.4)

    if solution:
        Gsp = graph.subgraph(solution)
        nx.draw_networkx_nodes(Gsp, pos, ax=ax, node_color="green", node_size=nodeSize * 1.2)
        nx.draw_networkx_edges(Gsp, pos, ax=ax, edge_color="green", width=4.0)

    if "start" in graph.nodes():
        nx.draw_networkx_nodes(graph, pos, nodelist=["start"], node_color="#00dd00", node_size=nodeSize, ax=ax)
        nx.draw_networkx_labels(graph, pos, labels={"start": "S"}, ax=ax)
    if "goal" in graph.nodes():
        nx.draw_networkx_nodes(graph, pos, nodelist=["goal"], node_color="#dd0000", node_size=nodeSize, ax=ax)
        nx.draw_networkx_labels(graph, pos, labels={"goal": "G"}, ax=ax)

    ax.set_title(title)
    ax.grid(True)

def hierarchicalPRMVisualizeLazySteps(planner, axList, nodeSize=100):
    import networkx as nx

    # Step 1: Sichtbarkeits-Wolke
    if planner.statsHandler and axList[0]:
        pos = nx.get_node_attributes(planner.statsHandler.graph, 'pos')
        nx.draw_networkx_nodes(planner.statsHandler.graph, pos=pos, ax=axList[0],
                               alpha=0.1, node_size=nodeSize, node_color='skyblue')
        nx.draw_networkx_edges(planner.statsHandler.graph, pos=pos, ax=axList[0],
                               alpha=0.1, edge_color='orange')
        axList[0].set_title("Step 1: Sichtbarkeits-Wolke")
        axList[0].grid(True)

    # Step 2: Roadmap nach MainPlanner (klassisch)
    if planner.graphMain and axList[1]:
        pos = nx.get_node_attributes(planner.graphMain, 'pos')
        planner._collisionChecker.drawObstacles(axList[1])
        nx.draw_networkx_nodes(planner.graphMain, pos=pos, ax=axList[1], node_color="lightblue", node_size=nodeSize)
        nx.draw_networkx_edges(planner.graphMain, pos=pos, ax=axList[1])
        axList[1].set_title("Step 2: PRM (vor Validierung)")
        axList[1].grid(True)

    # Step 3: Finaler Graph + Lazy-Farben
    if planner.graph and axList[2]:
        graph = planner.graph
        pos = nx.get_node_attributes(graph, 'pos')
        color = nx.get_node_attributes(graph, 'color')
        planner._collisionChecker.drawObstacles(axList[2])

        # Nodes
        nx.draw_networkx_nodes(graph, pos, ax=axList[2], nodelist=list(color.keys()),
                               node_color=list(color.values()), node_size=nodeSize)

        # Standard-Kanten
        nx.draw_networkx_edges(graph, pos, ax=axList[2])

        # Größte Komponente
        try:
            G0 = graph.subgraph(max(nx.connected_components(graph), key=len))
            nx.draw_networkx_edges(G0, pos, edge_color='b', width=3.0, style='dashed', alpha=0.5, ax=axList[2])
        except:
            pass

        # Kollision / Nicht-Kollision aus LazyPRM
        if hasattr(planner.subPlanner, 'collidingEdges'):
            for edges, color, alpha in [
                (planner.subPlanner.collidingEdges, 'r', 0.2),
                (planner.subPlanner.nonCollidingEdges, 'yellow', 0.8)
            ]:
                if edges:
                    tmpG = nx.Graph()
                    tmpG.add_nodes_from(graph.nodes(data=True))
                    for u, v in edges:
                        tmpG.add_edge(u, v)
                    nx.draw_networkx_edges(tmpG, pos, edge_color=color, width=5, alpha=alpha, ax=axList[2])

        # Pfad
        if planner.solution:
            Gsp = nx.subgraph(graph, planner.solution)
            nx.draw_networkx_edges(Gsp, pos, edge_color='g', width=10, alpha=0.8, ax=axList[2])

        # Start / Goal
        if "start" in graph.nodes():
            nx.draw_networkx_nodes(graph, pos, nodelist=["start"], node_color="#00dd00", node_size=nodeSize, ax=axList[2])
            nx.draw_networkx_labels(graph, pos, labels={"start": "S"}, ax=axList[2])
        if "goal" in graph.nodes():
            nx.draw_networkx_nodes(graph, pos, nodelist=["goal"], node_color="#dd0000", node_size=nodeSize, ax=axList[2])
            nx.draw_networkx_labels(graph, pos, labels={"goal": "G"}, ax=axList[2])

        axList[2].set_title("Step 3: Final mit Lazy-Farben + Pfad")
        axList[2].grid(True)



def hierarchicalPRMVisualizeBasicSteps(planner, axList, nodeSize=100):
    import networkx as nx

    # Step 1: Sichtbarkeitswolke
    if planner.statsHandler and axList[0]:
        pos = nx.get_node_attributes(planner.statsHandler.graph, 'pos')
        nx.draw_networkx_nodes(planner.statsHandler.graph, pos=pos, ax=axList[0],
                               alpha=0.1, node_size=nodeSize, node_color='skyblue')
        nx.draw_networkx_edges(planner.statsHandler.graph, pos=pos, ax=axList[0],
                               alpha=0.1, edge_color='orange')
        axList[0].set_title("Step 1: Sichtbarkeitswolke")
        axList[0].grid(True)

    # Step 2: PRM nach MainPlanner (wie basic)
    if planner.graphMain:
        graph = planner.graphMain
        pos = nx.get_node_attributes(graph, 'pos')
        planner._collisionChecker.drawObstacles(axList[1])
        nx.draw_networkx_nodes(graph, pos, cmap=plt.cm.Blues, ax=axList[1], node_size=nodeSize)
        nx.draw_networkx_edges(graph, pos, ax=axList[1])
        try:
            G0 = graph.subgraph(max(nx.connected_components(graph), key=len))
            nx.draw_networkx_edges(G0, pos, edge_color='b', width=3.0, ax=axList[1])
        except:
            pass
        axList[1].set_title("Step 2: PRM (vor Validierung)")

    # Step 3: Finaler Graph + Pfad (wie basic)
    if planner.graph:
        graph = planner.graph
        pos = nx.get_node_attributes(graph, 'pos')
        planner._collisionChecker.drawObstacles(axList[2])
        nx.draw_networkx_nodes(graph, pos, cmap=plt.cm.Blues, ax=axList[2], node_size=nodeSize)
        nx.draw_networkx_edges(graph, pos, ax=axList[2])

        # Pfad
        if planner.solution:
            Gsp = graph.subgraph(planner.solution)
            nx.draw_networkx_nodes(Gsp, pos, node_size=nodeSize * 1.5, node_color='g', ax=axList[2])
            nx.draw_networkx_edges(Gsp, pos, edge_color='g', width=10, alpha=0.8, ax=axList[2])

        # Start/Goal
        if "start" in graph.nodes():
            nx.draw_networkx_nodes(graph, pos, nodelist=["start"], node_color="#00dd00",
                                   node_size=nodeSize * 1.5, ax=axList[2])
            nx.draw_networkx_labels(graph, pos, labels={"start": "S"}, ax=axList[2])
        if "goal" in graph.nodes():
            nx.draw_networkx_nodes(graph, pos, nodelist=["goal"], node_color="#dd0000",
                                   node_size=nodeSize * 1.5, ax=axList[2])
            nx.draw_networkx_labels(graph, pos, labels={"goal": "G"}, ax=axList[2])
        axList[2].set_title("Step 3: Final + Pfad")
        axList[2].grid(True)

