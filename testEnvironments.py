from shapely.geometry import Point, Polygon, LineString
from shapely.affinity import rotate
import matplotlib.pyplot as plt
from Lectures.IPEnvironment import CollisionChecker


class TestEnvironments:
    def __init__(self, limits=[[0, 23], [0, 23]]):
        self.limits = limits

    def draw_scene(self, content, figsize=(10, 10), title="Environment"):
        """
        Visualisiert die Szene über CollisionChecker.drawObstacles (wie in der Vorlesung).
        """
        checker = CollisionChecker(scene=content, limits=self.limits)
        fig, ax = plt.subplots(figsize=figsize)
        checker.drawObstacles(ax)

        # Optional: Start/Ziel explizit markieren
        if "start" in content:
            start_center = content["start"].centroid
            ax.plot(start_center.x, start_center.y, 'bo', markersize=12, label="Start")
        if "goal" in content:
            goal_center = content["goal"].centroid
            ax.plot(goal_center.x, goal_center.y, 'ro', markersize=12, label="Ziel")

        ax.set_xlim(self.limits[0])
        ax.set_ylim(self.limits[1])
        ax.set_aspect('equal')
        ax.set_title(title)
        ax.grid(True)
        ax.legend()
        plt.show()

    # --- Very Easy ---
    def get_very_easy_1(self):
        return {
            "start": Point(2, 2).buffer(0.8),
            "goal": Point(21, 21).buffer(0.8)
        }

    def get_very_easy_2(self):
        return {
            "block": Polygon([(10, 10), (11, 10), (11, 11), (10, 11)]),
            "start": Point(2, 2).buffer(0.8),
            "goal": Point(21, 21).buffer(0.8)
        }

    # --- Easy ---
    def get_easy_1(self):
        return {
            "block1": Polygon([(5, 5), (7, 5), (7, 7), (5, 7)]),
            "start": Point(2, 2).buffer(0.8),
            "goal": Point(21, 21).buffer(0.8)
        }

    def get_easy_2(self):
        return {
            "block1": Polygon([(6, 4), (9, 4), (9, 8), (6, 8)]),
            "block2": Polygon([(13, 10), (16, 10), (16, 14), (13, 14)]),
            "start": Point(3, 3).buffer(0.8),
            "goal": Point(21, 21).buffer(0.8)
        }

    # --- Medium ---
    def get_medium_1(self):
        return {
            "L1": Polygon([(5, 5), (10, 5), (10, 10), (5, 10)]),
            "R1": Polygon([(13, 5), (18, 5), (18, 10), (13, 10)]),
            "middle": Polygon([(10.5, 6), (12.5, 6), (12.5, 9), (10.5, 9)]),
            "start": Point(2, 2).buffer(0.8),
            "goal": Point(21, 21).buffer(0.8)
        }

    def get_medium_2(self):
        return {
            "L2": Polygon([(4, 13), (8, 13), (8, 18), (4, 18)]),
            "R2": Polygon([(15, 13), (19, 13), (19, 18), (15, 18)]),
            "trap": Polygon([(10.5, 14), (12.5, 14), (12.5, 15), (10.5, 15)]),
            "start": Point(2, 2).buffer(0.8),
            "goal": Point(21, 21).buffer(0.8)
        }

    # --- Hard ---
    def get_hard_2(self):
        return {
            "maze1": Polygon([(5, 5), (15, 5), (15, 6), (5, 6)]),
            "maze2": Polygon([(5, 7), (15, 7), (15, 8), (5, 8)]),
            "maze3": Polygon([(5, 9), (15, 9), (15, 10), (5, 10)]),
            "maze4": Polygon([(5, 11), (15, 11), (15, 12), (5, 12)]),
            "wall_left": LineString([(0, 0), (0, 23)]).buffer(0.5),
            "wall_right": LineString([(23, 0), (23, 23)]).buffer(0.5),
            "start": Point(2, 2).buffer(0.8),
            "goal": Point(21, 21).buffer(0.8)
        }

    def get_hard_3(self):
        return {
            "trap1": Polygon([(8, 11), (9, 11), (9, 12), (8, 12)]),
            "trap2": Polygon([(14, 11), (15, 11), (15, 12), (14, 12)]),
            "bar1": Polygon([(10, 0), (11, 0), (11, 10), (10, 10)]),
            "bar2": Polygon([(12, 13), (13, 13), (13, 23), (12, 23)]),
            "start": Point(2, 2).buffer(0.8),
            "goal": Point(21, 21).buffer(0.8)
        }

    # --- Very Hard ---
    def get_very_hard_1(self):
        scene = {
            f"maze_{i}": Polygon([(3, i*2), (20, i*2), (20, i*2+1), (3, i*2+1)])
            for i in range(1, 9, 2)
        }
        scene["gap_left"] = Polygon([(6, 4), (7, 4), (7, 5), (6, 5)])
        scene["gap_right"] = Polygon([(16, 6), (17, 6), (17, 7), (16, 7)])
        scene["start"] = Point(2, 2).buffer(0.8)
        scene["goal"] = Point(21, 21).buffer(0.8)
        return scene

    def get_very_hard_2(self):
        bar = Polygon([(0, 0), (8, 0), (8, 1), (0, 1)])
        rotated_bar = rotate(bar, 45, origin=(11, 11))
        return {
            "twist_bar": rotated_bar,
            "side_block": Polygon([(15, 15), (19, 15), (19, 19), (15, 19)]),
            "start": Point(2, 2).buffer(0.8),
            "goal": Point(21, 21).buffer(0.8)
        }

    # --- Zugriff auf alles ---
    def get_all_scenes(self):
        methods = [m for m in dir(self) if m.startswith("get_") and callable(getattr(self, m))]
        return {m: getattr(self, m)() for m in methods}
