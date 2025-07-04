# environments.py
from shapely.geometry import Point, Polygon, LineString

def get_environments():
    # Define obstacles for multiple environments
    environment_1_obstacles = [
        LineString([(45, 39), (30, 45), (15, 30), (30, 0), (45, 0), (45, 36)]).buffer(0.2),
        LineString([(30, 0), (30, 12)]).buffer(0.2),
        LineString([(30, 45), (30, 18)]).buffer(0.2)
    ]
    
    environment_2_obstacles = [
        LineString([(20, 30), (40, 50), (10, 60), (30, 80), (60, 80), (50, 40)]).buffer(0.3),
        LineString([(10, 20), (50, 60)]).buffer(0.2)
    ]
    
    environment_3_obstacles = [
        LineString([(15, 15), (30, 25), (25, 45), (10, 55), (5, 35)]).buffer(0.2),
        LineString([(10, 30), (30, 40)]).buffer(0.3)
    ]
    
    environments = [
        {
            'start': (5, 72),
            'goal': (25, 25),
            'obstacles': environment_1_obstacles
        },
        {
            'start': (10, 10),
            'goal': (50, 70),
            'obstacles': environment_2_obstacles
        },
        {
            'start': (15, 45),
            'goal': (50, 10),
            'obstacles': environment_3_obstacles
        }
    ]
    
    return environments
