# IPEnvironmentKinLimited.py

from IPEnvironmentKin import KinChainCollisionChecker
import numpy as np

class LimitedKinChainCollisionChecker(KinChainCollisionChecker):
    def __init__(self, kin_chain, scene, joint_limits, **kwargs):
        super().__init__(kin_chain, scene, **kwargs)
        self.joint_limits = joint_limits
        self.dim = len(joint_limits)

    def _sampleWithinLimits(self):
        return [np.random.uniform(low, high) for (low, high) in self.joint_limits]

    def getRandomConfiguration(self):
        return self._sampleWithinLimits()

    def pointInCollision(self, pos):
        # Prüfe erst, ob die Konfiguration in den zulässigen Grenzen liegt
        for i, (low, high) in enumerate(self.joint_limits):
            if not (low <= pos[i] <= high):
                return True
        return super().pointInCollision(pos)

    def lineInCollision(self, startPos, endPos):
        # Beide Endpunkte auf Gültigkeit prüfen
        for pos in [startPos, endPos]:
            for i, (low, high) in enumerate(self.joint_limits):
                if not (low <= pos[i] <= high):
                    return True
        return super().lineInCollision(startPos, endPos)
