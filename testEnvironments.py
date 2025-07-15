from shapely.geometry import Point, Polygon, LineString
from shapely.affinity import rotate
import matplotlib.pyplot as plt
from Lectures.IPEnvironment import CollisionChecker


class TestEnvironments:
    def __init__(self, limits=[[0, 23], [0, 23]]):
        self.limits = limits

    def draw_scene(self, scene, start=None, goal=None, figsize=(10, 10), title="Environment"):
        checker = CollisionChecker(scene=scene, limits=self.limits)
        fig, ax = plt.subplots(figsize=figsize)
        checker.drawObstacles(ax)
        if start:
            ax.plot(start[0], start[1], 'bo', markersize=12, label="Start")
        if goal:
            ax.plot(goal[0], goal[1], 'ro', markersize=12, label="Ziel")
        ax.set_xlim(self.limits[0])
        ax.set_ylim(self.limits[1])
        ax.set_aspect('equal')
        ax.set_title(title)
        ax.grid(True)
        ax.legend()
        plt.show()

    # --- Very Easy: mit Engstelle ---
    def get_very_easy_1(self):
        scene = {
            "bar": Polygon([(10, 10), (13, 10), (13, 13), (10, 13)]),
            "gap": Polygon([(11.4, 10), (11.6, 10), (11.6, 13), (11.4, 13)])
        }
        return scene, (2, 2), (21, 21)

    # --- Easy: Bottleneck ---
    def get_easy_1(self):
        scene = {
            "left": Polygon([(5, 10), (10, 10), (10, 15), (5, 15)]),
            "right": Polygon([(13, 10), (18, 10), (18, 15), (13, 15)]),
            "narrow": Polygon([(10.5, 11), (12.5, 11), (12.5, 14), (10.5, 14)])
        }
        return scene, (2, 2), (21, 21)

    # --- Medium: verschachtelt mit Korridor ---
    def get_medium_1(self):
        scene = {
            "block1": Polygon([(4, 4), (9, 4), (9, 12), (4, 12)]),
            "block2": Polygon([(14, 10), (19, 10), (19, 19), (14, 19)]),
            "middle_gap": Polygon([(9, 8), (14, 8), (14, 10), (9, 10)])
        }
        return scene, (2, 2), (21, 21)

    # --- Hard: Zickzackpassagen ---
    def get_hard_1(self):
        scene = {
            "zig1": Polygon([(3, 5), (18, 5), (18, 6), (3, 6)]),
            "zig2": Polygon([(3, 8), (18, 8), (18, 9), (3, 9)]),
            "zig3": Polygon([(3, 11), (18, 11), (18, 12), (3, 12)]),
            "zig4": Polygon([(3, 14), (18, 14), (18, 15), (3, 15)])
        }
        return scene, (2, 2), (21, 21)

    # --- Very Hard: Rotation + Blockade ---
    def get_very_hard_1(self):
        bar = Polygon([(0, 0), (6, 0), (6, 0.6), (0, 0.6)])
        rotated_bar = rotate(bar, 50, origin=(11, 11))
        scene = {
            "tilt_bar": rotated_bar,
            "cut_block": Polygon([(13, 13), (19, 13), (19, 20), (13, 20)])
        }
        return scene, (2, 2), (21, 21)

    def get_all_scenes(self):
        methods = [m for m in dir(self) if m.startswith("get_") and callable(getattr(self, m))]
        return {m: getattr(self, m)() for m in methods if m != "get_all_scenes"}

    @staticmethod
    def create_environment(env_name="get_easy_1"):
        envs = TestEnvironments()
        if hasattr(envs, env_name):
            scene, start, goal = getattr(envs, env_name)()
            return CollisionChecker(scene, limits=envs.limits), start, goal
        else:
            raise ValueError(f"Umgebung '{env_name}' nicht gefunden.")
