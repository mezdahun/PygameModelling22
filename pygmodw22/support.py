"""
calc.py : Supplementary methods and calculations necessary for agents
"""
import numpy as np
from scipy import integrate

### Supplementary Parameters ###
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
LIGHT_BLUE = (173, 216, 230)
GREEN = (50, 150, 50)
PURPLE = (130, 0, 130)
GREY = (230, 230, 230)
DARK_GREY = (210, 210, 210)
YELLOW = (190, 175, 50)
RED = (255, 0, 0)
LIGHT_RED = (255, 180, 180)
BACKGROUND = WHITE


### Supplementary Methods ###
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    if v1_u[0] * v2_u[1] - v1_u[1] * v2_u[0] < 0:
        angle = -angle
    return angle


# Random Walk functions
def random_walk(vmin=2, vmax=1, theta_min=-1, theta_max=1):
    """Pooling a small orientation and absolute velocity increment from some distribution"""
    dvel = np.random.uniform(vmin, vmax)
    dtheta = np.random.uniform(theta_min, theta_max)
    return dvel, dtheta


def distance_coords(x1, y1, x2, y2, vectorized=False):
    """Distance between 2 points in 2D space calculated from point coordinates.
    if vectorized is True, we use multidimensional (i.e. vectorized) form of distance
    calculation that preserved original dimensions of coordinate arrays in the dimensions of the output and the output
    will contain pairwise distance measures according to coordinate matrices."""
    c1 = np.array([x1, y1])
    c2 = np.array([x2, y2])
    if not vectorized:
        distance = np.linalg.norm(c2 - c1)
    else:
        distance = np.linalg.norm(c2 - c1, axis=0)
    return distance


def distance(agent1, agent2):
    """Distance between 2 agent class agents in the environment as pixels"""
    c1 = np.array([agent1.position[0] + agent1.radius, agent1.position[1] + agent1.radius])
    c2 = np.array([agent2.position[0] + agent2.radius, agent2.position[1] + agent2.radius])
    distance = np.linalg.norm(c2 - c1)
    return distance
