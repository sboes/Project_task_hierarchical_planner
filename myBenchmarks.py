# myBenchmarks.py
# KIT-style enlarged planning benchmarks

from shapely.geometry import Polygon, LineString, Point
from Lectures.IPEnvironment import CollisionChecker
from Lectures.IPBenchmark import Benchmark

benchList = []

# --- Benchmark 1: Simple Trap ---
scene = dict()
scene["obs1"] = LineString([(6, 18), (6, 8), (16, 8), (16, 18)]).buffer(1.0)
description = "Trap: Going straight leads into a box."
benchList.append(Benchmark("Trap", CollisionChecker(scene), [[10, 15]], [[10, 1]], description, 2))

# --- Benchmark 2: Bottleneck ---
scene = dict()
scene["obs1"] = LineString([(0, 13), (11, 13)]).buffer(0.5)
scene["obs2"] = LineString([(13, 13), (23, 13)]).buffer(0.5)
description = "Bottleneck: narrow passage must be found."
benchList.append(Benchmark("Bottleneck", CollisionChecker(scene), [[4, 15]], [[18, 1]], description, 2))

# --- Benchmark 3: Fat Bottleneck ---
scene = dict()
scene["obs1"] = Polygon([(0, 8), (11, 8), (11, 15), (0, 15)]).buffer(0.5)
scene["obs2"] = Polygon([(13, 8), (24, 8), (24, 15), (13, 15)]).buffer(0.5)
description = "Fat Bottleneck: long detour in a tight corridor."
benchList.append(Benchmark("Fat Bottleneck", CollisionChecker(scene), [[4, 21]], [[18, 1]], description, 3))

# --- Benchmark 4: LTC Maze (Letters + Robot Face) ---
scene = dict()
scene["L"] = Polygon([(10, 16), (10, 11), (13, 11), (13, 12), (11, 12), (11, 16)])
scene["T"] = Polygon([(14, 16), (14, 15), (15, 15), (15, 11), (16, 11), (16, 15), (17, 15), (17, 16)])
scene["C"] = Polygon([(19, 16), (19, 11), (22, 11), (22, 12), (20, 12), (20, 15), (22, 15), (22, 16)])

scene["Antenna_L"] = Polygon([(3, 12), (1, 16), (2, 16), (4, 12)])
scene["Antenna_Head_L"] = Point(1.5, 16).buffer(1)

scene["Antenna_R"] = Polygon([(7, 12), (9, 16), (8, 16), (6, 12)])
scene["Antenna_Head_R"] = Point(8.5, 16).buffer(1)

scene["Rob_Head"] = Polygon([(2, 13), (2, 8), (8, 8), (8, 13)])
description = "LTC and robot face as obstacles."
benchList.append(Benchmark("LTC Maze", CollisionChecker(scene), [[4, 21]], [[18, 1]], description, 4))

# --- Benchmark 5: Zig-Zag Maze Corridor ---
scene = dict()
scene["maze1"] = LineString([(5, 5), (20, 5)]).buffer(0.6)
scene["maze2"] = LineString([(5, 7), (20, 7)]).buffer(0.6)
scene["maze3"] = LineString([(5, 9), (20, 9)]).buffer(0.6)
scene["maze4"] = LineString([(5, 11), (20, 11)]).buffer(0.6)
scene["walls"] = LineString([(0, 0), (0, 25)]).buffer(0.5).union(LineString([(25, 0), (25, 25)]).buffer(0.5))
description = "Maze corridor with zig-zag lanes."
benchList.append(Benchmark("Maze Corridor", CollisionChecker(scene), [[2, 2]], [[21, 21]], description, 4))

# --- Benchmark 6: Diagonal Wall Detour ---
scene = dict()
scene["diag"] = LineString([(2, 2), (22, 22)]).buffer(0.7)
description = "Diagonal wall splits free space."
benchList.append(Benchmark("Diagonal Wall", CollisionChecker(scene), [[3, 22]], [[22, 3]], description, 3))

# --- Benchmark 7: Center Block Corridor ---
scene = dict()
scene["corridor"] = Polygon([(0, 10), (25, 10), (25, 15), (0, 15)])
scene["block"] = Polygon([(11, 10), (14, 10), (14, 15), (11, 15)])
description = "Planer must decide to go around left or right."
benchList.append(Benchmark("Corridor Split", CollisionChecker(scene), [[3, 12]], [[22, 12]], description, 4))

# --- Helper ---
def getAllBenchmarks():
    return benchList
