from shapely.geometry import Polygon, LineString, Point
from shapely.affinity import rotate

def env_1_trap():
    obstacles = {
        "trap_wall": LineString([(6, 18), (6, 8), (16, 8), (16,18)]).buffer(1.0)
    }
    start = (10.0, 15.0)
    goal = (10.0, 1.0)
    return {"obstacles": obstacles, "start": start, "goal": goal}

def env_2_bottleneck():
    obstacles = {
        "left": LineString([(0, 13), (11, 13)]).buffer(0.5),
        "right": LineString([(13, 13), (23,13)]).buffer(0.5)
    }
    start = (4.0, 15.0)
    goal = (18.0, 1.0)
    return {"obstacles": obstacles, "start": start, "goal": goal}

def env_3_fat_bottleneck():
    obstacles = {
        "left": Polygon([(0, 8), (11, 8), (11, 15), (0, 15)]).buffer(0.5),
        "right": Polygon([(13, 8), (24, 8), (24, 15), (13, 15)]).buffer(0.5)
    }
    start = (4.0, 21.0)
    goal = (18.0, 1.0)
    return {"obstacles": obstacles, "start": start, "goal": goal}

def env_4_robot_shapes():
    obstacles = {
        "L": Polygon([(10, 16), (10, 11), (13, 11), (13,12), (11,12), (11,16)]),
        "T": Polygon([(14,16), (14,15), (15,15), (15,11), (16,11), (16,15), (17,15), (17,16)]),
        "C": Polygon([(19,16), (19,11), (22,11), (22,12), (20,12), (20,15), (22,15), (22,16)]),
        "Antenna_L": Polygon([(3,12), (1,16), (2,16), (4,12)]),
        "Antenna_Head_L": Point(1.5, 16).buffer(1),
        "Antenna_R": Polygon([(7,12), (9,16), (8,16), (6,12)]),
        "Antenna_Head_R": Point(8.5, 16).buffer(1),
        "Robot_Head": Polygon([(2,13), (2,8), (8,8), (8,13)])
    }
    start = (4.0, 21.0)
    goal = (18.0, 1.0)
    return {"obstacles": obstacles, "start": start, "goal": goal}

def env_5_twist_gap():
    bar = Polygon([(0, 0), (8, 0), (8, 1), (0, 1)])
    rotated_bar = rotate(bar, 45, origin=(11, 11))
    obstacles = {
        "twist_bar": rotated_bar,
        "block_right": Polygon([(15, 15), (19, 15), (19, 19), (15, 19)])
    }
    start = (2.0, 2.0)
    goal = (21.0, 21.0)
    return {"obstacles": obstacles, "start": start, "goal": goal}

def env_6_dense_walls():
    obstacles = {}
    for i in range(5, 21, 2):
        obstacles[f"wall_{i}"] = Polygon([(i, 6), (i+1, 6), (i+1, 18), (i, 18)])
    start = (2.0, 2.0)
    goal = (22.0, 22.0)
    return {"obstacles": obstacles, "start": start, "goal": goal}

def env_7_micro_passages():
    obstacles = {
        "wide": Polygon([(5, 5), (19, 5), (19, 19), (5, 19)])
    }
    # cut narrow holes
    for i in range(6, 19, 2):
        obstacles[f"hole_{i}"] = Polygon([(i, 9), (i+0.5, 9), (i+0.5, 10), (i, 10)])
    start = (6.0, 2.0)
    goal = (18.0, 22.0)
    return {"obstacles": obstacles, "start": start, "goal": goal}

def get_all_environments():
    return {
        "trap": env_1_trap(),
        "bottleneck": env_2_bottleneck(),
        "fat_bottleneck": env_3_fat_bottleneck(),
        "robot_shapes": env_4_robot_shapes(),
        "twist_gap": env_5_twist_gap(),
        "dense_walls": env_6_dense_walls(),
        "micro_passages": env_7_micro_passages()
    }
