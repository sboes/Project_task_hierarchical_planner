import networkx as nx
import copy
from Lectures.IPPerfMonitor import IPPerfMonitor
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

    @IPPerfMonitor
    def planPath(self, startList, goalList, config):
        checkedStartList, checkedGoalList = self._checkStartGoal(startList, goalList)

        print("\n📌 [Step 3] Creating MainPlanner and learning roadmap")
        mainPlanner = self.mainPlannerFactory(self._collisionChecker)
        mainPlanner._learnRoadmap(config["ntry"])
        self.graphMain = copy.deepcopy(mainPlanner.graph)
        self.statsHandler = getattr(mainPlanner, "statsHandler", None)
        print(f"🧠 MainPlanner learned: {self.graphMain.number_of_nodes()} nodes, {self.graphMain.number_of_edges()} edges")

        print("🔍 [Step 4] Validating with SubPlanner...")
        self.graphValidated = copy.deepcopy(self.graphMain)
        removed = 0
        if self.subPlannerFactory:
            self.subPlanner = self.subPlannerFactory(self._collisionChecker)
            for u, v in list(self.graphValidated.edges()):
                pos_u = self.graphValidated.nodes[u]["pos"]
                pos_v = self.graphValidated.nodes[v]["pos"]
                if not self._edgeValidWithSubPlanner(pos_u, pos_v):
                    self.graphValidated.remove_edge(u, v)
                    removed += 1
        print(f"⚠️ {removed} edges removed by SubPlanner.")
        print(f"📊 Validated Graph: {self.graphValidated.number_of_nodes()} nodes, {self.graphValidated.number_of_edges()} edges")

        print("🔗 [Step 5] Connecting start/goal")
        self.graph = copy.deepcopy(self.graphValidated)
        self._connectStartGoal(self.graph, checkedStartList[0], checkedGoalList[0])
        print(f"🧷 Start/Goal verbunden. Finaler Graph: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")

        try:
            self.solution = nx.shortest_path(self.graph, "start", "goal")
            print("✅ Pfad gefunden!")
        except:
            print("❌ Kein Pfad gefunden.")
            self.solution = []

        return self.solution

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

    def _edgeValidWithSubPlanner(self, pos1, pos2):
        if hasattr(self.subPlanner, "_edgeValid"):
            return self.subPlanner._edgeValid(pos1, pos2)
        else:
            return not self._collisionChecker.lineInCollision(pos1, pos2)
