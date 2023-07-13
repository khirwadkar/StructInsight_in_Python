import sys
sys.path.append('.')
sys.path.append('..')
import numpy as np
try:
    from base_classes.member import Member
    from base_classes.loading import *
except ImportError:
    from ..base_classes.member import Member
    from ..base_classes.loading import *

class Beam(Member):
    FIXED = 1
    HINGE = 2
    FREE  = 3

    def __init__(self, id):
        Member.__init__(self, 'Beam', id)
        self.length = 3.5      # in meters
        self.width = 230       # in mm
        self.depth = 300       # in mm
        # self.I = 0.0005175    # in m^4, 230 x 300 beam
        self.I = self.width * self.depth ** 3 / 12e12    # moment of inertia in m^4
        self.E_MPa = 34500         # in Mega Pascals, concrete
        self.E = self.E_MPa * 1000 # in KN per sq.m.
        self.EI = self.E * self.I  # KN-sq.m.
        # self.sm = self.calc_member_stiffness_matrix()
        self.pLoads = []        # List of PointLoads
        self.udLoads = []       # List of UdLoads TODO
        self.udl = UdLoadFull(0, self.length)  # UdLoadFull. temporary modification 
                                # ultimately 'udLoads' to be considered
        self.jt_displacement = np.zeros(4)
        self.aml = np.zeros(4)          # Actions  at ends of restrained member,
                                        # in direction of member axes, due to loads
        self.points_of_interest = []    # List of points where SF and BM are calculated
        self.is_analysed = False
        self.shearForces = None
        self.bendingMoments = None

    def calc_member_stiffness_matrix(self):
        smt = np.zeros([4, 4])
        scm1 = 4 * self.EI / self.length
        scm2 = 1.5 * scm1 / self.length
        scm3 = 2 * scm2 / self.length
        smt[0][0] = smt[2][2] = scm3
        smt[0][2] = smt[2][0] = -scm3
        smt[0][1] = smt[1][0] = smt[0][3] = smt[3][0] = scm2
        smt[1][2] = smt[2][1] = smt[2][3] = smt[3][2] = -scm2
        smt[1][1] = smt[3][3] = scm1
        smt[1][3] = smt[3][1] = scm1/2
        self.sm = smt

    def __str__(self):
        descr = self.type + " " + str(self.id) + ": \n" \
                + str(self.width) + " X " + str(self.depth) \
                + " X " + str(self.length) + "\n" \
                + "E = " + str(self.E_MPa) + " MPa,  " \
                + "MI = " + str(self.I) + "\n"
        if self.is_analysed:
            descr = descr + f"{'End actions:':15} {'SF_left':^15} {'BM_left':^15} {'SF_right':^15} {'BM_right':^15}\n" 
            descr = descr + f"{'            ':15} {self.aml[0]:^15.3f} {self.aml[1]:^15.3f} {self.aml[2]:^15.3f} {self.aml[3]:^15.3f}\n" 
        return descr

    def setLength(self, beam_length):
        self.length = beam_length

    def getLength(self):
        return self.length

    def setE_in_MPa_units(self, E_MPa):
        self.E_MPa = E_MPa
        self.E = self.E_MPa * 1000 # in KN per sq.m.

    def setI(self, mi):
        """ Moment of Inertia in m^4 units
        """
        self.I = mi
        self.EI = self.E * self.I  # KN-sq.m.

    def getI(self):
        return self.I

    def getEI(self):
        return self.EI

    def setUdl(self, udl):
        self.udl = udl

    def getUdl(self):
        return self.udl

    def addPointLoad(self, P):
        self.pLoads.append(P)
        # sorted(self.pLoads)

    def getPointLoads(self):
        return self.pLoads

    def removeAllPtLoads(self):
        self.pLoads.clear()

    def calc_aml_matrix(self):          # Fixed End Moments due to loads
        self.aml = np.zeros(4)          # Initialized to avoid ill-effects of calling this function twice.
        self.aml += self.udl.calc_end_actions(self.length)
        for P in self.pLoads:
            self.aml += P.calc_end_actions(self.length)

    def setJtDisplacements(self, joint_displacements):
        """ Sets the displacements of this beam's end joints.

        The argument joint_displacements is available after global
        analysis of the continuous beam and is numpy array.
        The 1st element is Y-displacement and the 2nd element is
        Z-displacement of the left end of the beam.
        The 3rd and 4th elements are respectively for the 
        right end of the beam.
        """
        self.jt_displacement = joint_displacements
        # TODO Ensure that self.jt_displacement is numpy array

    def calcFinalAml(self):
        self.calc_aml_matrix()   # Avoids ill-effects of calling calcFinalAml multiple times
        self.calc_member_stiffness_matrix()
        self.aml += self.sm @ self.jt_displacement
        # or self.aml += np.matmul(self.sm, self.jt_displacement)
        self.is_analysed = True

    def find_points_of_interest(self, dx_points=0.05):
        a = np.arange(0.0, self.length, dx_points)
        poi_list = a.tolist()
        poi_list.append(self.length)
        for P in self.pLoads:
            poi_list.append(P.x)
        poi_list.sort()
        return poi_list

    def calcShearForces(self, step_size=0.05): 
        """
        Old logic
        self.points_of_interest = self.find_points_of_interest()
        sf_at_x = []
        for x in self.points_of_interest:
            sf_at_x.append(aml[0] - self.udl * x)
            for P in self.pLoads:
                if P.x <= x:
                    sf_at_x[-1] -= P.p
        self.shearForces = list(zip(self.points_of_interest, sf_at_x))
        """
        self.points_of_interest = self.find_points_of_interest(step_size)
        sf_at_x = np.zeros(len(self.points_of_interest))
        sf_at_x += self.aml[0]
        sf_at_x += self.udl.calcShearForces(self.points_of_interest)
        for P in self.pLoads:
            sf_at_x += P.calcShearForces(self.points_of_interest)
        self.shearForces = list(zip(self.points_of_interest, sf_at_x.tolist()))

    def getShearForces(self, step_size=0.05):
        self.calcShearForces(step_size)
        return self.shearForces

    def getMaxSF(self):
        def sortkey(tup):  # self.shearForces is a list of tuples (point_of_interest, SF)
            return abs(tup[1])
        return max(self.shearForces, key=sortkey)

    def calcBendingMoments(self, step_size=0.05):
        """
        Old logic
        self.points_of_interest = self.find_points_of_interest()
        bm_at_x = []
        for x in self.points_of_interest:
            bm_at_x.append(aml[1] - aml[0] * x + self.udl * x * x / 2)
            for P in self.pLoads:
                if P.x <= x:
                    bm_at_x[-1] += P.p * (x - P.x)
        self.bendingMoments = list(zip(self.points_of_interest, bm_at_x))
        """
        self.points_of_interest = self.find_points_of_interest(step_size)
        bm_at_x = np.zeros(len(self.points_of_interest))
        bm_at_x += self.aml[1]
        bm_due_to_reaction = self.aml[0] * np.array(self.points_of_interest)
        bm_at_x -= bm_due_to_reaction
        bm_at_x += self.udl.calcBendingMoments(self.points_of_interest)
        for P in self.pLoads:
            bm_at_x += P.calcBendingMoments(self.points_of_interest)
        self.bendingMoments = list(zip(self.points_of_interest, bm_at_x.tolist()))

    def getBendingMoments(self, step_size=0.05):
        self.calcBendingMoments(step_size)
        return self.bendingMoments

    def getMaxBM(self):
        def sortkey(tup):  # self.bendingMoments is a list of tuples (point_of_interest, BM)
            return abs(tup[1])
        return max(self.bendingMoments, key=sortkey)

    def getSlopeDeflections(self):
        """ Calculates slopes and deflections by Moment-Area method.

        """
        poi = [i for i, j in self.bendingMoments]
        bending_moments = [j for i, j in self.bendingMoments]
        poi = np.array(poi)
        bending_moments = np.array(bending_moments)
        # bending_moments /= self.EI
        left_end_displacement = self.jt_displacement[0]
        slopes = np.zeros(len(poi))
        slopes[0] = self.jt_displacement[1]   # left_end_slope
        deflections = np.zeros(len(poi))
        deflections[0] = self.jt_displacement[0]  # left_end_deflection
        slope_corrections = slopes[0] * poi  # deflection by 2nd-AreaMoment-theorem is vertical
                                            # distance between poi and tangent to curve at the
                                            # left-most point of the area.
        for i in range(1, len(poi)):
            slope_corrections[i] += deflections[0]
            slopes[i] = slopes[i-1] - (bending_moments[i] + bending_moments[i-1]) * 0.5 * (poi[i] - poi[i-1]) / self.EI
            for j in range(i):
                deflections[i] = deflections[i] - (bending_moments[j] + bending_moments[j+1]) * 0.5 \
                        * (poi[j+1] - poi[j]) * ((poi[j+1] - poi[j])/2 + (poi[i] - poi[j+1])) / self.EI
        deflections += slope_corrections
        slopes[-1] = self.jt_displacement[3]   # right_end_slope to avoid residual error due to numerical integration
        deflections[-1] = self.jt_displacement[2]  # right_end_deflection to avoid residual error due to numerical integration

        # slopes = np.cumsum(bending_moments)
        # slopes /= self.EI
        # slopes += left_end_slope

        self.slope_deflections = list(zip(poi.tolist(), slopes.tolist(), deflections.tolist()))
        return self.slope_deflections











    
