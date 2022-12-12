
from beam_classes.beam import Beam
from beam_classes.continuousbeam import ContinuousBeam
from base_classes.loading import *
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox


def my_input(prompt, default_value, datatype):
    ans = input(prompt + " [" + str(default_value) + "]: ").strip()
    if not ans:
        return default_value
    return datatype(ans)

def main(root):
    # b1 = Beam(1)
    # print(b1)
    cb = ContinuousBeam()
    main_window = tk.Toplevel(root)
    # main_window = tk.Tk()
    # main_window.state('iconic')
    # main_window.overrideredirect(1)  # to avoid 'flash' due to withdraw()
                                       # gives run time fatal error if we try to deiconify()
    # main_window.withdraw()
    main_window.iconify()
    getBeamData(cb, main_window)
    getLoadData(cb, main_window)
    analysis(cb, main_window)
    main_window.destroy()
    # main_window.iconify() 
    return True

def getBeamData(cb, main_window):
    nSpans = simpledialog.askinteger(parent=main_window, title="Input", 
            prompt="Number of spans:", minvalue=1, initialvalue=3) 
    # nSpans = my_input('Number of spans', 3, int)
    cb.setNspans(nSpans)

    typicalSpan = simpledialog.askfloat(parent=main_window, title='Input', 
            prompt='Typical span', initialvalue=3.5)
    cb.setTypicalSpan(typicalSpan)
    beamLengths = []
    for i in range(nSpans):
        span = simpledialog.askfloat(parent=main_window, title='Input', 
                prompt='Length of beam ' + str(i+1), 
                initialvalue=typicalSpan)
        beamLengths.append(span)
    cb.setAllSpans(beamLengths)

    typicalE = simpledialog.askfloat(title='Input', prompt='Typical Modulus of Elasticity', 
            parent=main_window, initialvalue=34500)
    cb.setTypicalModEla(typicalE)
    E = []
    for i in range(nSpans):
        beamE = simpledialog.askfloat(title='Input', prompt='E for beam ' + str(i+1), 
                parent=main_window, initialvalue=typicalE)
        E.append(beamE)
    cb.setAllE_MPa(E)

    typicalMI = simpledialog.askfloat(title='Input', prompt='Typical Moment of Inertia', 
            parent=main_window, initialvalue=0.0005175)
    cb.setTypicalMomIner(typicalMI)
    mi = []
    for i in range(nSpans):
        beamMI = simpledialog.askfloat(title='Input', prompt='M.I. of beam ' + str(i+1), 
                parent=main_window, initialvalue=typicalMI)
        mi.append(beamMI)
    cb.setAllMomIner(mi)

    # for aBeam in cb.beamNum:   # TODO debug stmnt. Delete after use
    #     print(aBeam)

    # print('Enter support type at each joint, starting from the left end.')
    # print(f'Input {Beam.FIXED} for FIXED jt., {Beam.HINGE} for HINGE, and {Beam.FREE} for FREE jt.')
    msg_support = 'Enter support type at each joint, starting from the left end.\n'
    msg_support += f'Input {Beam.FIXED} for FIXED jt., {Beam.HINGE} for HINGE, and {Beam.FREE} for FREE jt.'
    messagebox.showinfo(parent=main_window, message = msg_support)

    nJoints = cb.getNJoints()
    for jtIndex in range(nJoints):
        supportType = simpledialog.askinteger(title='Input', 
                prompt=f'Support type for joint {jtIndex + 1}', 
                parent=main_window, minvalue=Beam.FIXED, maxvalue=Beam.FREE, initialvalue=Beam.HINGE)
        cb.setJointType(jtIndex, supportType)

def getLoadData(cb, main_window):
    nJoints = cb.getNJoints()
    cb.initJtActionArray()
    print('\n\nEnter vertical joint loads (if any).')
    print('Input positive number for upward loads and negative number for downward loads.')
    print(f'Starting from the left end, the joints are numbered 1 to {nJoints}.')
    print('Input -1 as joint number, after dealing with all the vertical joint loads.')
    print()
    jointNum = simpledialog.askinteger(title='Input', prompt='Enter joint number', 
            parent=main_window, initialvalue=1)
    while jointNum != -1:
        vLoad = simpledialog.askfloat(title='Input', 
                prompt=f'Input vertical load at joint # {jointNum}', 
                parent=main_window, initialvalue=0.0)
        supportIndex = jointNum - 1
        cb.setJtAction(2*supportIndex, vLoad)
        jointNum = simpledialog.askinteger(title='Input', prompt='Enter joint number', 
                parent=main_window, initialvalue=1)

    print('\n\nEnter joint moments (if any).')
    print('Positive number would be considered as anti-clockwise moment and ')
    print('negative number as clockwise moment.')
    print(f'Starting from the left end, the joints are numbered 1 to {nJoints}.')
    print('Input -1 as joint number, after dealing with all the joint moments.')
    print()
    jointNum = simpledialog.askinteger(title='Input', prompt='Enter joint number', 
            parent=main_window, initialvalue=1)
    while jointNum != -1:
        jtMoment = simpledialog.askfloat(title='Input', 
                prompt=f'Input moment at joint # {jointNum}', 
                parent=main_window, initialvalue=0.0)
        supportIndex = jointNum - 1
        cb.setJtAction(2*supportIndex+1, jtMoment)
        jointNum = simpledialog.askinteger(title='Input', prompt='Enter joint number', 
                parent=main_window, initialvalue=1)

    nSpans = cb.getNspans()
    print('\n\nNow input member loads.\nFirst give uniformly distributed loads.')
    print('Give positive number for downward udl and negative for upward udl.')
    print(f'From left to right members are numbered 1 to {nSpans}.')
    print('Input 0.0 as udl, if there is no udl on a member.')
    for memberIndex in range(nSpans):
        p_udl = simpledialog.askfloat(title='Input', 
                prompt=f'Input udl on member # {memberIndex + 1}', 
                parent=main_window, initialvalue=0.0)
        cb.setMemberUDLfull(memberIndex, p_udl)
    # cb.calcNumUDLs()  # TODO why?

    print('\n\nAfter UDLs, now give member point loads.')
    print('Input positive number for downward point load and negative number for upward.')
    print('Input 0 as the value of point load, if there is no further point load on a particular member.')
    for memberIndex in range(nSpans):
        P = simpledialog.askfloat(title='Input', 
                prompt=f'Input point load on member # {memberIndex + 1}', 
                parent=main_window, initialvalue=0.0)
        while P != 0.0:
            x = simpledialog.askfloat(title='Input', 
                    prompt=f'Distance of {P} load from left end of member # {memberIndex + 1}', 
                    parent=main_window, minvalue=0.0) # TODO maxvalue as memberspan
            pL = PointLoad(P, x)
            cb.addMemberPointLoad(memberIndex, pL)
            P = simpledialog.askfloat(title='Input', 
                    prompt=f'Input point load on member # {memberIndex + 1}', 
                    parent=main_window, initialvalue=0.0)


def analysis(cb, main_window):
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
    S"""
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


"""
root = tk.Tk()
# root.state('iconic')
root.overrideredirect(1)  # to avoid 'flash' due to withdraw()
root.withdraw()
"""

"""
thestate = window.state()
window.state('normal')
window.state('iconic')
window.state('withdrawn')
window.iconify()
window.deiconify()   # to restore from iconified or withdrawn state
window.withdraw()
"""

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("200x200+50+50")
    # root.overrideredirect(1)  # to avoid 'flash' due to withdraw()a
    # root.withdraw()
    root.iconify()
    main(root)
    print("Returned from main.")
    root.grab_set()
    root.deiconify()
    root.mainloop()

# root.deiconify()
# root.destroy()
# root.mainloop()


