import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
from os import path


class PendulumEnv(gym.Env):
    metadata = {"render.modes": ["human", "rgb_array"], "video.frames_per_second": 30}

    def __init__(self, g=10.0):
        self.max_speed = 8
        self.max_torque = 2
        self.dt = 0.036
        self.g = g
        self.m = 1.0
        self.l = 1.0
        self.viewer = None
        self.th = []
        self.u = [0,0,0,0,0,0,0,0]
        self.i = 1
        high = np.array([1.0, 1.0, self.max_speed], dtype=np.float32)
        self.action_space = spaces.Box(
            low=-self.max_torque, high=self.max_torque, shape=(1,), dtype=np.float32
        )
        self.observation_space = spaces.Box(low=-high, high=high, dtype=np.float32)
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, u):
        u = u*255.0/2.0
        limit = 255.0
        t,thdot = self.state  # th := theta
        #print(t)
        if self.i == 1:
          thdot = 0
          self.th.append(t)
          self.i = 2
          
        self.th.append(t)
        #print(self.th)
        u = np.clip(u, -limit , limit)[0]
        self.u.append(u)
        #print(self.u)
        self.last_u = u  # for rendering
        costs = (10 * self.th[1] ** 2 + 0.01 * thdot ** 2 + 0.00001 * (u ** 2))
        
        newth = 1.611 * self.th[1] - 0.5599*self.th[0] + (-0.001949*self.u[8] + 0.002877*self.u[7] 
                                                          + 0.008892*self.u[6] + 0.01766*self.u[5] 
                                                          + 0.002082*self.u[4] + 0.002943*self.u[3]
                                                          - 0.0019874*self.u[2] - 0.0008178*self.u[1]
                                                          + 0.0001022*self.u[0])*np.pi/180
# =============================================================================
        angle_limit = 70 * np.pi/180        
        if ( newth > angle_limit):
          newth = angle_limit
        if newth <-angle_limit:
          newth = -angle_limit
# =============================================================================
        #newth = angle_normalize(newth)
        newthdot = (newth - self.th[1])/self.dt
        newthdot = np.clip(newthdot, -self.max_speed, self.max_speed)
        self.th.pop(0)
        self.u.pop(0)
        print(u,newth*180/np.pi, newthdot*180/np.pi)
        self.state = np.array([newth, newthdot])
        return self._get_obs(), -costs, False, {}

    def reset(self):
        self.th = []
        self.u = [0,0,0,0,0,0,0,0]
        self.i = 1
        high = np.array([np.pi/2, 1])
        self.state = self.np_random.uniform(low=-high, high=high)
        self.last_u = None
        return self._get_obs()

    def _get_obs(self):
        theta, thetadot = self.state
        return np.array([np.cos(theta), np.sin(theta), thetadot], dtype=np.float32)

    def render(self, mode="human"):
        if self.viewer is None:
            from gym.envs.classic_control import rendering

            self.viewer = rendering.Viewer(500, 500)
            self.viewer.set_bounds(-2.2, 2.2, -2.2, 2.2)
            rod = rendering.make_capsule(1, 0.2)
            rod.set_color(0.8, 0.3, 0.3)
            self.pole_transform = rendering.Transform()
            rod.add_attr(self.pole_transform)
            self.viewer.add_geom(rod)
            axle = rendering.make_circle(0.05)
            axle.set_color(0, 0, 0)
            self.viewer.add_geom(axle)
            fname = path.join(path.dirname(__file__), "assets/clockwise.png")
            self.img = rendering.Image(fname, 1.0, 1.0)
            self.imgtrans = rendering.Transform()
            self.img.add_attr(self.imgtrans)

        self.viewer.add_onetime(self.img)
        self.pole_transform.set_rotation(self.state[0] + np.pi / 2)
        if self.last_u is not None:
            self.imgtrans.scale = (-self.last_u / 2, np.abs(self.last_u) / 2)

        return self.viewer.render(return_rgb_array=mode == "rgb_array")

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None


def angle_normalize(x):
    return ((x + np.pi/2) % (2 * np.pi/2)) - np.pi/2









