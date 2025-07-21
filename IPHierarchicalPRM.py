# Erweiterung deiner HierarchicalPRM-Klasse mit adaptiver lokaler Subplanung
import networkx as nx
import copy
from scipy.spatial import cKDTree
import numpy as np

class HierarchicalPRM:
    def __init__(self, collisionChecker, mainPlannerFactory, subPlannerFactory=None):
        self._collisionChecker = collisionChecker
        self.mainPlannerFactory = mainPlannerFactory
        self.subPlannerFactory = subPlannerFactory
        self.solution = None

        self.graphMain = None
        self.graphValidated = None
        self.graph = None
        self.statsHandler = None
        self.subPlanner = None

        self.local_planning_config = None
        self.failed_edges = []  # für Visualisierung
        self.local_nodes = []   # hinzugefügte lokale Knoten zur Visualisierung

    def planPath(self, startList, goalList, config):
        checkedStartList, checkedGoalList = self._checkStartGoal(startList, goalList)

        self._setLocalPlanningConfig(config)

        mainPlanner = self.mainPlannerFactory(self._collisionChecker)
        mainPlanner._learnRoadmap(config["ntry"])
        self.graphMain = copy.deepcopy(mainPlanner.graph)
        self.statsHandler = getattr(mainPlanner, "statsHandler", None)

        self.graphValidated = copy.deepcopy(self.graphMain)
        if self.subPlannerFactory:
            self.subPlanner = self.subPlannerFactory(self._collisionChecker)
            for u, v in list(self.graphValidated.edges()):
                pos_u = self.graphValidated.nodes[u]["pos"]
                pos_v = self.graphValidated.nodes[v]["pos"]
                if not self._edgeValidOrRepair(pos_u, pos_v):
                    self.graphValidated.remove_edge(u, v)
                    self.failed_edges.append((u, v))

        self.graph = copy.deepcopy(self.graphValidated)
        self._connectStartGoal(self.graph, checkedStartList[0], checkedGoalList[0])

        try:
            self.solution = nx.shortest_path(self.graph, "start", "goal")
        except:
            self.solution = []

        return self.solution

    def _setLocalPlanningConfig(self, config):
        def clamp(val, minval, maxval):
            return max(minval, min(val, maxval))

        self.local_planning_config = {
            "initial_num_nodes": int(clamp(config.get("initial_num_nodes", 20), 1, 1000)),
            "max_num_nodes": int(clamp(config.get("max_num_nodes", 100), 10, 5000)),
            "increment_step": int(clamp(config.get("increment_step", 20), 1, 1000)),
            "region_margin": float(clamp(config.get("region_margin", 0.1), 0.01, 5.0))
        }

    def _edgeValidOrRepair(self, pos1, pos2):
        if hasattr(self.subPlanner, "_edgeValid") and self.subPlanner._edgeValid(pos1, pos2):
            return True

        num_nodes = self.local_planning_config["initial_num_nodes"]
        max_nodes = self.local_planning_config["max_num_nodes"]
        step = self.local_planning_config["increment_step"]
        margin = self.local_planning_config["region_margin"]

        while num_nodes <= max_nodes:
            if hasattr(self.subPlanner, "reset"):
                self.subPlanner.reset()
            if hasattr(self.subPlanner, "setSamplingRegion"):
                self.subPlanner.setSamplingRegion(pos1, pos2, margin)
            if hasattr(self.subPlanner, "buildRoadmap"):
                self.subPlanner.buildRoadmap(num_nodes)
            if hasattr(self.subPlanner, "query"):
                success, path = self.subPlanner.query(pos1, pos2)
                if success:
                    self._injectLocalPath(pos1, pos2, path)
                    return True
            num_nodes += step

        return False

    def _injectLocalPath(self, pos1, pos2, path):
        prev_node = None
        for i, p in enumerate(path):
            node_id = f"local_{hash(tuple(p))}_{i}"
            self.local_nodes.append((node_id, p))
            if not self.graphValidated.has_node(node_id):
                self.graphValidated.add_node(node_id, pos=p)
            if prev_node:
                self.graphValidated.add_edge(prev_node, node_id)
            prev_node = node_id
        # Optional: direkter Anschluss an Endpunkte
        if not self.graphValidated.has_node("endpoint2"):
            self.graphValidated.add_node("endpoint2", pos=pos2)
        self.graphValidated.add_edge(prev_node, "endpoint2")

    def _checkStartGoal(self, startList, goalList):
        return startList, goalList

    def _connectStartGoal(self, graph, start, goal):
        pos = nx.get_node_attributes(graph, "pos")
        if not pos:
            return
        tree = cKDTree(list(pos.values()))
        keys = list(pos.keys())
        for label, pt in zip(["start", "goal"], [start, goal]):
            _, idxs = tree.query(pt, k=min(5, len(keys)))
            if not isinstance(idxs, (list, np.ndarray)):
                idxs = [idxs]
            for i in idxs:
                if i >= len(keys):
                    continue
                if not self._collisionChecker.lineInCollision(pt, pos[keys[i]]):
                    graph.add_node(label, pos=pt)
                    graph.add_edge(label, keys[i])
                    break