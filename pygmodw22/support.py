"""
calc.py : Supplementary methods and calculations necessary for agents
"""
import numpy as np
import matplotlib.cm
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


def distance_infinite(p1, p2, L=500, dim=2):
    """ Returns the distance vector of two position vectors x,y
        by tanking periodic boundary conditions into account.

        Input parameters: L - system size, dim - no. of dimension
    """
    distvec = p2 - p1
    distvec_periodic = np.copy(distvec)
    distvec_periodic[distvec < -0.5*L] += L
    distvec_periodic[distvec > 0.5*L] -= L
    return distvec_periodic


def calculate_color(orientation, velocity, max_velocity=1):
    """Calculates an RGB color from the colormap according to orientation and velocity. Color will be calculated from
    orientation while transparency from the absolute velocity compared to the max velocity."""
    cmap = matplotlib.cm.get_cmap('Spectral')
    rgba = np.array(cmap(orientation / (2*np.pi)))
    # setting transparency according to vel
    rgba[3] = velocity/max_velocity
    # rescaling color for pygame
    rgba[0:3] *= 255
    return rgba


def SigThresh(x, x0=0.5, steepness=10):
    """
    Sigmoid function f(x)=1/2*(tanh(a*(x-x0)+1)

        Input parameters:
        -----------------
        x:  function argument
        x0: position of the transition point (f(x0)=1/2)
        steepness:  parameter setting the steepness of the transition.
                    (positive values: transition from 0 to 1, negative values:
                    transition from 1 to 0)
    """
    return 0.5 * (np.tanh(steepness * (x - x0)) + 1)


def CalcSingleAttForce(r_att, steepness_att, distvec):
    """Calculating the attraction force between a single pair of agents with given distance
    from each other.

    :param r_att: attraction range
    :param steepness_att: attraction steepness when calculating force with sigmoid
    :param distvec: distance vector between the paiir of agents
    :return vec_attr: directional attraction force vector
    """
    dist = np.linalg.norm(distvec)
    F_att = SigThresh(dist, r_att, steepness_att)
    vec_attr = F_att * distvec
    return vec_attr


def CalcSingleAlgForce(r_alg, steepness_alg, distvec, dvel):
    """Calculating the attraction force between a single pair of agents with given distance
        from each other.

        :param r_alg: alignment range
        :param steepness_alg: alignment steepness when calculating force with sigmoid
        :param distvec: distance vector between the paiir of agents
        :param dvec: difference between velcoity vectors
        :return vec_alg: directional alignment force vector
        """
    dist = np.linalg.norm(distvec)
    F_alg = SigThresh(dist, r_alg, steepness_alg)
    vec_alg = F_alg * dvel
    return vec_alg


def CalcSingleRepForce(r_rep, steepness_rep, distvec):
    """Calculating the repulsion force between a single pair of agents with given distance
    from each other.

    :param r_rep: repulsion range
    :param steepness_rep: repulsion steepness when calculating force with sigmoid
    :param distvec: distance vector between the paiir of agents
    :return vec_rep: directional repulsion force vector
    """
    dist = np.linalg.norm(distvec)
    F_rep = SigThresh(dist, r_rep, steepness_rep)
    vec_rep = F_rep * distvec
    return vec_rep
