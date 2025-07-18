# coding: utf-8

"""
HierarchicalPRM: Combines a main planner (e.g., VisPRM) with a sub-planner (e.g., BasicPRM)
Course: Innovative Programmiermethoden für Industrieroboter (KIT)
"""

from Lectures.IPPRMBase import PRMBase
import networkx as nx
from Lectures.IPPerfMonitor import IPPerfMonitor

class HierarchicalPRM(PRMBase):

    def __init__(self, _collChecker):
        super(HierarchicalPRM, self).__init__(_collChecker)
        self.graph = nx.Graph()
        self.solution = []

    @IPPerfMonitor
    def planPath(self, startList, goalList, config):
        """
        config["mainPlanner"]: class reference to global planner (e.g., VisPRM)
        config["mainConfig"]: config dict for global planner
        config["subPlanner"]: class reference to sub-planner (e.g., BasicPRM)
        config["subConfig"]: config dict for sub-planner
        """
        # 0. extract planner classes and configs
        mainClass = config["mainPlanner"]
        mainConfig = config["mainConfig"]
        subClass = config["subPlanner"]
        subConfig = config["subConfig"]

        # 1. reset graph
        self.graph.clear()

        # 2. check start/goal validity
        checkedStartList, checkedGoalList = self._checkStartGoal(startList, goalList)

        # 3. build main planner roadmap
        mainPlanner = mainClass(self._collisionChecker)
        mainPlanner._learnRoadmap(mainConfig["ntry"])
        self.graph = mainPlanner.graph.copy()
        posList = nx.get_node_attributes(self.graph, 'pos')

        # 4. prune edges using sub-planner
        for u, v in list(self.graph.edges()):
            posU = self.graph.nodes[u]['pos']
            posV = self.graph.nodes[v]['pos']
            subPlanner = subClass(self._collisionChecker)
            path = subPlanner.planPath([posU], [posV], subConfig)
            if not path:
                self.graph.remove_edge(u, v)

        # 5. connect start/goal
        for name, pos in [("start", checkedStartList[0]), ("goal", checkedGoalList[0])]:
            self.graph.add_node(name, pos=pos)
            for node, nodePos in posList.items():
                if not self._collisionChecker.lineInCollision(pos, nodePos):
                    self.graph.add_edge(name, node)
                    break

        # 6. plan final path
        try:
            self.solution = nx.shortest_path(self.graph, "start", "goal")
        except:
            self.solution = []

        return self.solution
