"""
String question[] =
   {
       "Input number of spans (beam members) (1 to 10):      ",
       "Input typical span (beam length) in meters:          ",
       "Change the spans, if necessary. Then click 'Submit'. ",
       "Typical Mod. of Elasticity(E) of beam material (MPa) ",
       "Change the values, if necessary. Then click 'Submit' ",
       "Moment of Inertia(I) of typical cross-section (m.^4) ",
       "Change the values, if necessary. Then click 'Submit' ",
       "Now, specify support details...                      "
   };

int nSpans = cb.getNSpans()
int nJoints = cb.getNJoints();
	   for(int i=0; i<nJoints; ++i)
	   {
               int jtType = cb.getJointType(i)

Ask number of spans
cb.setNSpans(temp1)
Ask typical span
cb.setTypicalSpan(typicalSpan) 
Ask length of each beam and store it in a local array 'beamLengths'
cb.setAllSpans(beamLengths)
Ask typical mod of E
cb.setTypicalModEla(typicalE)
Ask mod of elasticity of each beam and store to local array 'E'
cb.setAllE_MPa(E)
Ask typical MI
cb.setTypicalMomIner(typicalMI)
Ask MI of each member and store to local array 'mi'
cb.setAllMomIner(mi)


           if(source == fixedBt)
	   {
	       cb.setJointType(supportIndex, Beam.FIXED);
	   }
	   if(source == simpleSupBt)
	   {
	       cb.setJointType(supportIndex, Beam.HINGE);
	   }
	   if(source == freeBt)
	   {
	       cb.setJointType(supportIndex, Beam.FREE);
	   }

"""

"""
String question[] =
		{
			"Input joint loads, if any ...                         ",
			"Input uniformly distributed loads on members (kN/m)   ",
			"Input point loads on members, if any ...              ",
			"                                                      ",
			"Change the values, if necessary. Then click 'Submit'  ",
		};
cb.initJtActionArray()

for(int i=0; i<nJoints; ++i)
	       {
	           double temp = cb.getJtAction(2*i+1);


String str1 = "Upward load on joint # " + (supportIndex +1) + " in kN:"; Positive
String str1 = "Downward load on joint # " + (supportIndex +1) + " in kN:"; Negative
cb.setJtAction(2*supportIndex, tempValue);

String str1 = "Moment on joint # " + (supportIndex+1) + " in kN-m:"; Anticlockwise +ve, Clockwise -ve
cb.setJtAction(2*supportIndex+1, tempValue);

String str1 = "Upward uniformly distributed load on member # " + (memberIndex + 1) + " in kN/m:";
         // Note: upward udl is considered negative
String str1 = "Downward uniformly distributed load on member # " + (memberIndex + 1) + " in kN/m:";  // Positive
cb.setMemberUDL(memberIndex, tempValue)
cb.calcNumUDLs()

String str1 = "Upward point load on member # " + (memberIndex + 1) + " in kN:";
     // Note: upward point load is considered negative
str1 = "Distance in meters, of " + tempP + " kN load from left end of member # " + (memberIndex + 1);
PointLoad temp = new PointLoad(tempP, tempX);
cb.addMemberPointLoad(memberIndex, temp);

String str1 = "Downward point load on member # " + (memberIndex + 1) + " in kN:";

"""



"""
cb.setAmlMatrices();
cb.setStiffnessMatrices();
cb.calcCumulRestraints();
cb.setGlobalStiffMatrix();
cb.invertGlobalStiffMatrix();
cb.setEquiJointLoads();
cb.calcJtDisplacements();
cb.calcSupportReactions();
cb.rearrangeVectors();
cb.calcFinalMemberEndActions();
cb.calcShearForces();
cb.calcBendingMoments();

cb.printResults(out);

"""




from beam_classes.beam import Beam
from beam_classes.continuousbeam import ContinuousBeam
from base_classes.loading import *

def my_input(prompt, default_value, datatype):
    ans = input(prompt + " [" + str(default_value) + "]: ").strip()
    if not ans:
        return default_value
    return datatype(ans)

def main():
    # b1 = Beam(1)
    # print(b1)
    cb = ContinuousBeam()
    # s = my_input("Number of spans", '', int)
    # print(s)
    getBeamData(cb)
    getLoadData(cb)
    analysis(cb)

def getBeamData(cb):
    nSpans = my_input('Number of spans', 3, int)
    cb.setNspans(nSpans)

    typicalSpan = my_input('Typical span', 3.5, float)
    cb.setTypicalSpan(typicalSpan)
    beamLengths = []
    for i in range(nSpans):
        span = my_input('Length of beam ' + str(i+1), typicalSpan, float)
        beamLengths.append(span)
    cb.setAllSpans(beamLengths)

    typicalE = my_input('Typical Modulus of Elasticity', 34500, float)
    cb.setTypicalModEla(typicalE)
    E = []
    for i in range(nSpans):
        beamE = my_input('E for beam ' + str(i+1), typicalE, float)
        E.append(beamE)
    cb.setAllE_MPa(E)

    typicalMI = my_input('Typical Moment of Inertia', 0.0005175, float)
    cb.setTypicalMomIner(typicalMI)
    mi = []
    for i in range(nSpans):
        beamMI = my_input('M.I. of beam ' + str(i+1), typicalMI, float)
        mi.append(beamMI)
    cb.setAllMomIner(mi)

    # for aBeam in cb.beamNum:   # TODO debug stmnt. Delete after use
    #     print(aBeam)

    print('Enter support type at each joint, starting from the left end.')
    print(f'Input {Beam.FIXED} for FIXED jt., {Beam.HINGE} for HINGE, and {Beam.FREE} for FREE jt.')
    nJoints = cb.getNJoints()
    for jtIndex in range(nJoints):
        supportType = my_input(f'Support type for joint {jtIndex + 1}', Beam.HINGE, int)
        cb.setJointType(jtIndex, supportType)

def getLoadData(cb):
    nJoints = cb.getNJoints()
    cb.initJtActionArray()
    print('\n\nEnter vertical joint loads (if any).')
    print('Input positive number for upward loads and negative number for downward loads.')
    print(f'Starting from the left end, the joints are numbered 1 to {nJoints}.')
    print('Input -1 as joint number, after dealing with all the vertical joint loads.')
    print()
    jointNum = my_input('Enter joint number', 1, int)
    while jointNum != -1:
        vLoad = my_input(f'Input vertical load at joint # {jointNum}', 0.0, float)
        supportIndex = jointNum - 1
        cb.setJtAction(2*supportIndex, vLoad)
        jointNum = my_input('Enter joint number', 1, int)

    print('\n\nEnter joint moments (if any).')
    print('Positive number would be considered as anti-clockwise moment and ')
    print('negative number as clockwise moment.')
    print(f'Starting from the left end, the joints are numbered 1 to {nJoints}.')
    print('Input -1 as joint number, after dealing with all the joint moments.')
    print()
    jointNum = my_input('Enter joint number', 1, int)
    while jointNum != -1:
        jtMoment = my_input(f'Input moment at joint # {jointNum}', 0.0, float)
        supportIndex = jointNum - 1
        cb.setJtAction(2*supportIndex+1, jtMoment)
        jointNum = my_input('Enter joint number', 1, int)

    nSpans = cb.getNspans()
    print('\n\nNow input member loads.\nFirst give uniformly distributed loads.')
    print('Give positive number for downward udl and negative for upward udl.')
    print(f'From left to right members are numbered 1 to {nSpans}.')
    print('Input 0.0 as udl, if there is no udl on a member.')
    for memberIndex in range(nSpans):
        p_udl = my_input(f'Input udl on member # {memberIndex + 1}', 0.0, float)
        cb.setMemberUDLfull(memberIndex, p_udl)
    # cb.calcNumUDLs()  # TODO why?

    print('\n\nAfter UDLs, now give member point loads.')
    print('Input positive number for downward point load and negative number for upward.')
    print('Input 0 as the value of point load, if there is no further point load on a particular member.')
    for memberIndex in range(nSpans):
        P = my_input(f'Input point load on member # {memberIndex + 1}', 0.0, float)
        while P != 0.0:
            x = my_input(f'Distance of {P} load from left end of member # {memberIndex + 1}', 1, float)
            pL = PointLoad(P, x)
            cb.addMemberPointLoad(memberIndex, pL)
            P = my_input(f'Input point load on member # {memberIndex + 1}', 0.0, float)


def analysis(cb):
    cb.analyse()
    """
    cb.setAmlMatrices()
    cb.setStiffnessMatrices()
    cb.calcCumulRestraints()
    cb.setGlobalStiffMatrix()
    cb.invertGlobalStiffMatrix()
    cb.setEquiJointLoads()
    cb.calcJtDisplacements()
    cb.calcSupportReactions()
    cb.rearrangeVectors()
    cb.calcFinalMemberEndActions()
    """
    cb.calcShearForces(0.1)
    cb.calcBendingMoments(0.1)
    print(cb)
    nSpans = cb.getNspans()
    for memberIndex in range(nSpans):
        print(f"Shear Forces on Beam {memberIndex + 1}:")
        print(f"-----------------------------------------")
        print(cb.getMemberShearForces(memberIndex, 0.1))
        print("\nMaximum SF: ", str(cb.beamNum[memberIndex].getMaxSF()))
        print('-'*60)
        print()
        print(f"Bending Moments on Beam {memberIndex + 1}:")
        print(f"-----------------------------------------")
        print(cb.getMemberBendingMoments(memberIndex, 0.1))
        print("\nMaximum BM: ", str(cb.beamNum[memberIndex].getMaxBM()))
        print('='*60)
        print()
    #print("\nMaximum of Maximum SFs: ", str(cb.getMaxSF()))
    #print("\nMaximum of Maximum BMs: ", str(cb.getMaxBM()))
    #for memberIndex in range(nSpans):
        sl_dfl = cb.getMemberSlopeDeflections(memberIndex)
        slopes = [(i, j) for i, j, k in sl_dfl]
        deflections = [(i, k) for i, j, k in sl_dfl]
        print(f"Slopes for Beam {memberIndex + 1}:")
        print(f"-----------------------------------------")
        print(slopes)
        print(f"Deflections for Beam {memberIndex + 1}:")
        print(f"-----------------------------------------")
        print(deflections)




if __name__ == '__main__':
    main()


