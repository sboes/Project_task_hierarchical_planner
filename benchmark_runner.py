
import time
import numpy as np
import pandas as pd
from Lectures.IPEnvironment import CollisionChecker

class BenchmarkRunner:
    def __init__(self, planner_class, outer_class, inner_class, environments, config):
        self.planner_class = planner_class
        self.outer_class = outer_class
        self.inner_class = inner_class
        self.environments = environments
        self.config = config
        self.results = []

    def run(self):
        for name, scene in self.environments.items():
            print(f"Running benchmark: {name}")
            checker = CollisionChecker(scene)
            outer = self.outer_class(checker)
            inner = self.inner_class(checker)
            planner = self.planner_class(outer, inner)

            start = time.time()
            path = planner.planPath([[2, 2]], [[21, 21]], self.config)
            duration = time.time() - start

            success = path is not None
            path_len = len(path) if path else 0

            self.results.append({
                "scene": name,
                "success": success,
                "path_length": path_len,
                "duration_sec": round(duration, 3)
            })

        return pd.DataFrame(self.results)
