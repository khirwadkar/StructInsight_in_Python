import sys
sys.path.append('.')
sys.path.append('..')
import numpy as np
from .beam import Beam
"""
try:
    from base_classes.loading import *
except ImportError:
    from ..base_classes.loading import *
"""
try:
    from base_classes import PointLoad, UdLoadFull
except ImportError:
    from ..base_classes import PointLoad, UdLoadFull

class ContinuousBeam(object):
    def __init__(self):
        """ The default initial continuous beam
        consists of 5 beam members.
        """
        self.setNspans(5)
        #self.calcJointPosX()   # moved from here to the end of setNspans on 16-Jul-2023


    def setNspans(self, n):
        self.nSpans = n         # No. of members
        self.memberBeamsList = []       # List of member beams
        for i in range(self.nSpans):
            self.memberBeamsList.append(Beam(i+1))
        self.initJoints()
        self.calcJointPosX()
        self.initJtActionArray()

    def getNspans(self):
        return self.nSpans

    def initJoints(self):
        self.nJoints = self.nSpans + 1      # No. of joints
        self.nrj = self.nJoints             # No. of restrained joints

                                            # We are assuming hinge joints, so all
                                            # of them are restrained in translation.
        self.rL = [1, 0] * self.nJoints     # Joint Restraint List
        self.nRestraints = self.rL.count(1) # Total number of support restraints
	                                    # against translation and rotation.

    def calcJointPosX(self):
        self.jointPosX = np.zeros(self.nJoints)     # X position of joint from left-end in meters
        for i in range(1, self.nJoints):
            self.jointPosX[i] = self.jointPosX[i-1] + self.memberBeamsList[i-1].getLength()
        self.total_length = self.jointPosX[-1]      # Total length of the continuous beam

    def getJointPosX(self, jtIndex):
        return self.jointPosX[jtIndex]

    def setTypicalSpan(self, typical_span):
        self.typicalSpan = typical_span
        for aBeam in self.memberBeamsList:
            aBeam.setLength(typical_span)
        self.calcJointPosX()
	
    def getTypicalSpan(self):
        return self.typicalSpan

    def getMemberLength(self, beamIndex):
        return self.memberBeamsList[beamIndex].getLength()

    def getAllSpans(self):
        span_list = []
        for aBeam in self.memberBeamsList:
            span_list.append(aBeam.getLength())
        return span_list

    def setAllSpans(self, span_list):
        for i, beam in enumerate(self.memberBeamsList):
            beam.setLength(span_list[i])
        """ Old logic, un-pythonic
        for i in range(len(self.memberBeamsList)):
            self.memberBeamsList[i].setLength(span_list[i])
        """
        self.calcJointPosX()

    def getTotal_length(self):
        return self.total_length

    def setTypicalModEla(self, ModE_MPa):
        self.typicalE = ModE_MPa
        for aBeam in self.memberBeamsList:
            aBeam.setE_in_MPa_units(ModE_MPa)

    def getTypicalModEla(self):
        return self.typicalE

    def setAllE_MPa(self, E_MPa):
        for i, beam in enumerate(self.memberBeamsList):
            beam.setE_in_MPa_units(E_MPa[i])
        """ Old logic, un-pythonic
        for i in range(len(self.memberBeamsList)):
            self.memberBeamsList[i].setE_in_MPa_units(E_MPa[i])
        """

    def getAllE_MPa(self):
        E_list = [beam.getE_in_MPa_units() for beam in self.memberBeamsList]
        return E_list

    def setTypicalMomIner(self, typical_mi):
        self.typicalMI = typical_mi
        for aBeam in self.memberBeamsList:
            aBeam.setI(typical_mi)

    def getTypicalMomIner(self):
        return self.typicalMI

    def setAllMomIner(self, mi_list):
        for i, beam in enumerate(self.memberBeamsList):
            beam.setI(mi_list[i])
        """ Old logic, un-pythonic
        for i in range(len(self.memberBeamsList)):
            self.memberBeamsList[i].setI(mi_list[i])
        """

    def getAllMomIner(self):
        mi_list = [beam.getI() for beam in self.memberBeamsList]
        return mi_list

    def getAllEI(self):
        ei_list = [beam.getEI() for beam in self.memberBeamsList]
        return ei_list

    def getNJoints(self):
        return self.nJoints

    def setJointType(self, jtIndex, jtType):
        if(jtType == Beam.FIXED):
            self.rL[2*jtIndex] = 1
            self.rL[2*jtIndex+1] = 1
            # self.nRestraints += 2
        if(jtType == Beam.HINGE):
            self.rL[2*jtIndex] = 1
            self.rL[2*jtIndex+1] = 0
            # self.nRestraints += 1
        if(jtType == Beam.FREE):
            self.rL[2*jtIndex] = 0
            self.rL[2*jtIndex+1] = 0
            self.nrj -= 1   # TODO check whether 'self.nrj' is used anywhere in the program.

        self.nRestraints = self.rL.count(1)    # Total number of support restraints


    def getJointType(self, jtIndex):
        if((self.rL[2*jtIndex], self.rL[2*jtIndex+1]) == (1, 1)):
            return Beam.FIXED
        elif((self.rL[2*jtIndex], self.rL[2*jtIndex+1]) == (1, 0)):
            return Beam.HINGE
        else:
            return Beam.FREE

    def calcCumulRestraints(self):
        self.nDOF = 2 * self.nJoints - self.nRestraints     # No. of actual displacements 
                                      # or degrees of freedom = 2 * nJoints - nRestraints
        self.cRL = [0, 0] * self.nJoints   # Cumulative Restraint List
        self.cRL[0] = self.rL[0]
        for k in range(1, len(self.rL)):
            self.cRL[k] = self.cRL[k-1] + self.rL[k]

    def calcNumUDLs(self):
        self.nUDL = 0
        for aBeam in self.memberBeamsList:
            if abs(aBeam.getUdl()) > 0.0:   # TODO rectify, udl is an object
                self.nUDL += 1

    def initJtActionArray(self):
        # Actions (loads) applied at joints, in direction
        # of structure axes. Two per jt.
        self.jtAction = [0, 0] * self.nJoints

    def setJtAction(self, jointIndex, actionValue):
        self.jtAction[jointIndex] = actionValue 

    def getJtAction(self, jointIndex):
        return self.jtAction[jointIndex]

    # def setMemberUDL(self, memberIndex, udl):  # TODO old (Java) name of the function
    def setMemberUDLfull(self, memberIndex, p_udl):
        L = self.memberBeamsList[memberIndex].getLength()
        udl_full = UdLoadFull(p_udl, L)
        self.memberBeamsList[memberIndex].setUdl(udl_full)

    def getMemberUDL(self, memberIndex):       # TODO rectify, udl is an object
        return self.memberBeamsList[memberIndex].getUdl()

    def addMemberPointLoad(self, memberIndex, pointLoad):
        self.memberBeamsList[memberIndex].addPointLoad(pointLoad)

    def removeAllMemberPtLoads(self, memberIndex):
        self.memberBeamsList[memberIndex].removeAllPtLoads()

    def getMemberPtLoads(self, memberIndex):
        return self.memberBeamsList[memberIndex].getPointLoads()

    def getNumMemberPtLoads(self, memberIndex):  # TODO this is redundant
        return len(self.memberBeamsList[memberIndex].getPointLoads())

    def setAmlMatrices(self):
        for aBeam in self.memberBeamsList:
            aBeam.calc_aml_matrix()

    def setStiffnessMatrices(self):
        for aBeam in self.memberBeamsList:
            aBeam.calc_member_stiffness_matrix()

    def setGlobalStiffMatrix(self):     # Global or Overall Stiffness matrix
        self.S = np.zeros([2*self.nJoints, 2*self.nJoints])
        for i in range(self.nSpans):
            j1 = 2*i 
            j2 = 2*i+1 
            k1 = 2*i+2 
            k2 = 2*i+3
            if(self.rL[j1] == 0):  # The joint is not restrained in Y dir.
                j1 = j1 - self.cRL[j1]  # Push the row in Overall stiff. mat. towards beginning
            else:
                j1 = self.nDOF + self.cRL[j1] - 1  # Push it after 'nDOF' rows.

            if(self.rL[j2] == 0):  # The joint is not restrained in Z dir.
                j2 = j2 - self.cRL[j2]
            else:
                j2 = self.nDOF + self.cRL[j2] - 1  # 1 is subtracted because CRL[0] is 1.

            # The same thing for right end of the member
            if(self.rL[k1] == 0):    # The joint is not restrained in Y dir.
                k1 = k1 - self.cRL[k1]  # Push the row in Overall stiff. mat. towards beginning
            else:
                k1 = self.nDOF + self.cRL[k1] - 1  # The first 'nDOF' rows are for unrestrained joints.

            if(self.rL[k2] == 0):   # The joint is not restrained in Z dir.
                k2 = k2 - self.cRL[k2]
            else:
                k2 = self.nDOF + self.cRL[k2] - 1   # 1 is subtracted because CRL[0] is 1.

            # Building overall (global) stiffness matrix
            if(self.rL[2*i] == 0):
                self.S[j1][j1] += self.memberBeamsList[i].sm[0][0]    # First Column
                self.S[j2][j1] += self.memberBeamsList[i].sm[1][0]    # of member stiffness
                self.S[k1][j1] +=  self.memberBeamsList[i].sm[2][0]
                self.S[k2][j1] +=  self.memberBeamsList[i].sm[3][0]

            if(self.rL[2*i+1] == 0):
                self.S[j1][j2] += self.memberBeamsList[i].sm[0][1]    # Second Column
                self.S[j2][j2] += self.memberBeamsList[i].sm[1][1]
                self.S[k1][j2] +=  self.memberBeamsList[i].sm[2][1]
                self.S[k2][j2] +=  self.memberBeamsList[i].sm[3][1]

            if(self.rL[2*i+2] == 0):
                self.S[j1][k1] +=  self.memberBeamsList[i].sm[0][2]   # Third Column
                self.S[j2][k1] +=  self.memberBeamsList[i].sm[1][2]
                self.S[k1][k1] += self.memberBeamsList[i].sm[2][2]
                self.S[k2][k1] += self.memberBeamsList[i].sm[3][2]

            if(self.rL[2*i+3] == 0):
                self.S[j1][k2] +=  self.memberBeamsList[i].sm[0][3]   # Fourth Column
                self.S[j2][k2] +=  self.memberBeamsList[i].sm[1][3]
                self.S[k1][k2] += self.memberBeamsList[i].sm[2][3]
                self.S[k2][k2] += self.memberBeamsList[i].sm[3][3]

    def invertGlobalStiffMatrix(self):
        """ Inverting the nXn part of the overall stiff. mat
             where n means self.nDOF in our program
             inv_S = Inverse of nDOF x nDOF part
             of Global or Overall Stiffness matrix
        """
        S_part = self.S[0:self.nDOF, 0:self.nDOF]
        self.inv_S = np.linalg.inv(S_part)

    def setEquiJointLoads(self):
        # Member loads to Equivalent joint loads
        equi_jt_load = [0, 0] * self.nJoints  #TODO check whether it should be self.equi_jt_load
        for i in range(len(self.memberBeamsList)):
            # beamNum[i].calc_aml_matrix();
            equi_jt_load[2*i+0] -= self.memberBeamsList[i].aml[0]
            equi_jt_load[2*i+1] -= self.memberBeamsList[i].aml[1]
            equi_jt_load[2*i+2] -= self.memberBeamsList[i].aml[2]
            equi_jt_load[2*i+3] -= self.memberBeamsList[i].aml[3]

        # Combined joint loads (arranged like Overall stiff. mat.)
        self.combined_jt_load = [0, 0] * self.nJoints
        for j in range(2 * self.nJoints):
            if self.rL[j] == 0:
                k = j - self.cRL[j]
            else:
                k = self.nDOF + self.cRL[j] - 1   # As CRL[0] is 1.
            self.combined_jt_load[k] = self.jtAction[j] + equi_jt_load[j]

    def calcJtDisplacements(self):
        # Joint Displacements Calculation
        # vector of size nDOF x 1
        relevant_loads = np.array(self.combined_jt_load[0:self.nDOF])
        relevant_jt_displacements = self.inv_S @ relevant_loads
        restrained_jt_displacements = np.zeros(self.nRestraints)
        # TODO change the var name self.jt_displacement to plural
        self.jt_displacement = np.append(relevant_jt_displacements, restrained_jt_displacements)
        # Vector of size (2 * nJoints) x 1

    def calcSupportReactions(self):
        # Calculation of support reactions
        actual_support_reactions = -np.array(self.combined_jt_load[self.nDOF:])
        reactions_due_to_deformations = self.S[self.nDOF:, 0:self.nDOF] @ self.jt_displacement[0:self.nDOF]
        actual_support_reactions += reactions_due_to_deformations
        self.support_reactions = np.append(np.zeros(self.nDOF), actual_support_reactions)
        # Vector of size (2 * nJoints) x 1

    def rearrangeVectors(self):
        # Rearranging displacement vector according to original jt. numbering system
        j = self.nDOF
        last = 2 * self.nJoints - 1    # or = nDOF + nRestraints - 1
        for JE in range(last, -1, -1):  # JE & KE are indices for expanded vectors
            if self.rL[JE] == 0:
                j -= 1
                self.jt_displacement[JE] = self.jt_displacement[j]
            else:
                self.jt_displacement[JE] = 0

        # Rearranging AR vector according to ori. jt. numbering system
        k = self.nDOF - 1
        for KE in range(2 * self.nJoints):
            if self.rL[KE] == 1:
                k += 1
                self.support_reactions[KE] = self.support_reactions[k]
            else:
                self.support_reactions[KE] = 0

        # Copy displacements to members
        for k in range(self.nSpans):
            a = np.array(self.jt_displacement[2*k : 2*k+4])
            self.memberBeamsList[k].setJtDisplacements(a)

    def calcFinalMemberEndActions(self):
        for aBeam in self.memberBeamsList:
            aBeam.calcFinalAml()

    def getSupportReaction(self, reactionIndex):
        return self.support_reactions[reactionIndex]

    def analyse(self):
        """
        Analyses the continuous beam after getting all the data
        about geometry of member beams and loads acting thereupon.

        """
        self.setAmlMatrices()
        self.setStiffnessMatrices()
        self.calcCumulRestraints()
        self.setGlobalStiffMatrix()
        self.invertGlobalStiffMatrix()
        self.setEquiJointLoads()
        self.calcJtDisplacements()
        self.calcSupportReactions()
        self.rearrangeVectors()
        self.calcFinalMemberEndActions()


    def printResults(self):
        # TODO
        pass

    def calcShearForces(self, step_size=0.05):  # TODO 1. this fn. may be redundant.  2. Check whether repeated calling makes any difference
        for aBeam in self.memberBeamsList:              # 12-Oct-2023: Calling this function from 'analysis.py'. It is not redundant.
            aBeam.calcShearForces(step_size)

    def getMemberShearForces(self, memberIndex, step_size=0.05):    # TODO 13-Oct-2023 Check whether this function is redundant.
        return self.memberBeamsList[memberIndex].getShearForces(step_size)

    def getMaxSF(self):
        def sortkey(tup):  # sf_list consists of tuples (point_of_interest, SF)
            return abs(tup[1])
        sf_list = []
        for aBeam in self.memberBeamsList:
            sf_list.append(aBeam.getMaxSF())
        return(max(sf_list, key=sortkey))

    def calcBendingMoments(self, step_size=0.05):   # TODO 1. this fn. may be redundant.  2. Check whether repeated calling makes any difference
        for aBeam in self.memberBeamsList:                  # 12-Oct-2023: Calling this function from 'analysis.py'. It is not redundant.
            aBeam.calcBendingMoments(step_size)

    def getMemberBendingMoments(self, memberIndex, step_size=0.05):  # TODO 13-Oct-2023 Check whether this function is redundant
        return self.memberBeamsList[memberIndex].getBendingMoments(step_size)

    def getMaxBM(self):
        def sortkey(tup):  # bm_list consists of tuples (point_of_interest, BM)
            return abs(tup[1])
        bm_list = []
        for aBeam in self.memberBeamsList:
            bm_list.append(aBeam.getMaxBM())
        return(max(bm_list, key=sortkey))

    def calcSlopeDeflections(self):   # TODO 1. Modify beam.py and write calc fn there to make this consistent with SF and BM funcs
        for aBeam in self.memberBeamsList:    # 12-Oct-2023: Calling this function from 'analysis.py'. It is not redundant.
            aBeam.getSlopeDeflections()

    def getMaxDeflection(self):
        def sortkey(tup):  # deformations_list consists of tuples (point_of_interest, slope, deflection)
            return abs(tup[2])
        deformations_list = []
        for aBeam in self.memberBeamsList:
            deformations_list.append(aBeam.getMaxDeflection())
        return(max(deformations_list, key=sortkey))

    def getMemberSlopeDeflections(self, memberIndex):
        return self.memberBeamsList[memberIndex].getSlopeDeflections()

    def __str__(self):
        descr = '\nContinuous Beam Analysis Results' + \
                '\n----------------------------------------\n'
        for aBeam in self.memberBeamsList:
            descr += str(aBeam)
            descr += '-' * 80
            descr += '\n\n\n'
        descr += f"{'Joint':>10} {'Y-displ':^15} {'Z-displ':^15} {'Y-react':^15} {'Z-react':^15}\n"
        df = self.jt_displacement
        re = self.support_reactions
        for k in range(0, 2*self.nJoints, 2):
            #descr += f"{k/2+1:10} {df[k]*1000:^15.3f} {df[k+1]*1000:^15.3f} {re[k]:^15.3f} {re[k+1]:^15.3f}\n"
            descr += f"{k/2+1:10} {df[k]:^15.4e} {df[k+1]:^15.4e} {re[k]:^15.3f} {re[k+1]:^15.3f}\n"
        return descr




















