
from Lectures.IPPlanerBase import PlanerBase
from Lectures.IPPerfMonitor import IPPerfMonitor
import networkx as nx

class HierarchicalPlanner(PlanerBase):
    def __init__(self, outerPlanner, innerPlanner):
        super(HierarchicalPlanner, self).__init__(outerPlanner._collisionChecker)
        self.outerPlanner = outerPlanner
        self.innerPlanner = innerPlanner
        self.graph = nx.DiGraph()
        self.solutionPath = []       # Node-Namen (optional)
        self.solutionCoords = []     # Echte Koordinaten als Pfad
        self.totalLength = 0
        self.totalTime = 0

    @IPPerfMonitor
    def planPath(self, startList, goalList, config):
        try:
            outer_ntry = config.get("outer_ntry", 100)
            inner_radius = config.get("inner_radius", 5.0)
            inner_nodes = config.get("inner_nodes", 250)

            # Step 1: Outer planner
            outer_config = {"ntry": outer_ntry}
            outer_path = self.outerPlanner.planPath(startList, goalList, outer_config)

            if not outer_path or len(outer_path) < 2:
                print("Outer planner failed.")
                return None

            self.solutionPath = []
            self.solutionCoords = []
            self.totalLength = 0

            pos_attr = nx.get_node_attributes(self.outerPlanner.graph, "pos")
            last_node = None

            for i in range(len(outer_path) - 1):
                start = pos_attr[outer_path[i]]
                goal = pos_attr[outer_path[i + 1]]

                inner_config = {
                    "radius": inner_radius,
                    "numNodes": inner_nodes
                }

                self.innerPlanner.graph.clear()
                sub_path = self.innerPlanner.planPath([start], [goal], inner_config)

                if not sub_path or len(sub_path) < 2:
                    print(f"Inner planner failed at segment {i}: {start} -> {goal}")
                    return None

                coords = [self.innerPlanner.graph.nodes[n]["pos"] for n in sub_path]

                if last_node is not None:
                    self.solutionPath.extend(sub_path[1:])
                    self.solutionCoords.extend(coords[1:])
                else:
                    self.solutionPath.extend(sub_path)
                    self.solutionCoords.extend(coords)
                    last_node = True

                self.totalLength += len(sub_path)

            return self.solutionPath
        except Exception as e:
            print(f"Hierarchical planning failed: {e}")
            return None
