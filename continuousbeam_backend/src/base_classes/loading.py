""" Contains class definitions for various types of loads.

    Loads that act on the members of a continuous beam.
    The class hierarchy:
      AnyLoad
         PointLoad
         UdLoad
            UdLoadFull
"""

import numpy as np

class AnyLoad(object):
    """ Super class for any type of load.
    """

    def __init__(self, type, id):
        self.type = type    # point load, udl, triangular load etc.
        self.id = id

    def __str__(self):
        return self.type + " " + str(self.id)

class PointLoad(AnyLoad):
    """ Load defined by its magnitude and position.
    """

    def __init__(self, p, x):
        AnyLoad.__init__(self, 'Point Load', 1)
        self.p = p
        self.x = x

    def calc_end_actions(self, beam_length):        # aml_matrix
        L = beam_length
        P = self.p
        a = self.x
        b = L - a
        aml = np.zeros(4)  # end-actions vector
        aml[0] += (P * b**2 * (3*a + b) / (L**3))
        aml[1] += (P * a * b**2 / (L**2))
        aml[2] += (P * a**2 * (a + 3*b) / (L**3))
        aml[3] += (-P * a**2 * b / (L**2))
        return aml

    def calcShearForces(self, points_of_interest):
        sf_at_x = np.zeros(len(points_of_interest))
        for i in range(sf_at_x.size):
            y = points_of_interest[i]
            if self.x <= y: 
                sf_at_x[i] -= self.p
        return sf_at_x

    def calcBendingMoments(self, points_of_interest):
        bm_at_x = np.zeros(len(points_of_interest))
        for i in range(bm_at_x.size):
            y = points_of_interest[i]
            if self.x <= y: 
                bm_at_x[i] += self.p * (y - self.x)
        return bm_at_x


class UdLoad(AnyLoad):
    """ Uniformly Distributed Load

        May span over the entire length of the member beam
        or it may span over part of the length. 
    """

    def __init__(self, p, x1, x2):
        AnyLoad.__init__(self, 'Udl', 1)
        self.p = p
        self.x1 = x1
        self.x2 = x2

    def calc_end_actions(self, beam_length):        # aml_matrix
        L = beam_length
        aml = np.zeros(4)  # end-actions vector
        # TODO


class UdLoadFull(UdLoad):
    """ UDL spanning over entire length of the member beam.
    """

    def __init__(self, p, L):
        UdLoad.__init__(self, p, 0, L)

    def calc_end_actions(self, beam_length):        # aml_matrix
        L = beam_length  # it can be: L = self.x2  also; in that case, no need to pass beam_length
        w = self.p
        aml = np.zeros(4)  # end-actions vector
        aml[0] += (w * L / 2)
        aml[1] += (w * L**2 / 12)
        aml[2] += (w * L / 2)
        aml[3] += (-w * L**2 / 12)
        return aml

    def calcShearForces(self, points_of_interest):
        sf_at_x = np.zeros(len(points_of_interest))
        for i in range(sf_at_x.size):
            y = points_of_interest[i]
            sf_at_x[i] -= self.p * y 
        return sf_at_x

    def calcBendingMoments(self, points_of_interest):
        bm_at_x = np.zeros(len(points_of_interest))
        for i in range(bm_at_x.size):
            y = points_of_interest[i]
            bm_at_x[i] += self.p * y * y / 2
        return bm_at_x








