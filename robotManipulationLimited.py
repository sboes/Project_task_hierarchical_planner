import numpy as np
import sympy as sp
from Lectures.IPPlanarManipulator import PlanarRobot, PlanarJoint

class LimitedPlanarJoint(PlanarJoint):
    def __init__(self, a=1.5, init_theta=0, id=0, min_theta=-np.pi, max_theta=np.pi):
        super().__init__(a=a, init_theta=init_theta, id=id)
        self.min_theta = min_theta
        self.max_theta = max_theta

    def move(self, new_theta):
        if not (self.min_theta <= new_theta <= self.max_theta):
            raise ValueError(f"⚠️ Gelenkwinkel {new_theta:.2f} außerhalb der Grenzen [{self.min_theta}, {self.max_theta}]")
        self.theta = new_theta


class LimitedPlanarRobot(PlanarRobot):
    def __init__(self, n_joints=2, joint_limits=None):
        self.dim = n_joints
        if joint_limits is None:
            joint_limits = [(-np.pi, np.pi)] * n_joints
        assert len(joint_limits) == n_joints, "❌ Länge der joint_limits stimmt nicht mit n_joints überein"
        self.joints = [
            LimitedPlanarJoint(id=i, min_theta=joint_limits[i][0], max_theta=joint_limits[i][1])
            for i in range(n_joints)
        ]
        self.Ms = [sp.eye(3)]
        for joint in self.joints:
            self.Ms.append(self.Ms[-1] * joint.M)
