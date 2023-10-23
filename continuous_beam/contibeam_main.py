# Starting point of the continuous beam analysis program.
# This module comprises the graphics classes for user interface.

import sys
sys.path.append('.')
sys.path.append('..')

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox

try:
    from beam_classes.beam import Beam
    from beam_classes.continuousbeam import ContinuousBeam
    from base_classes.loading import *
    from beam_data import BeamData_Window
    from load_data import LoadData_Window
    from analysis import Analysis_Window
except ImportError:
    from .beam_classes.beam import Beam
    from .beam_classes.continuousbeam import ContinuousBeam
    from .base_classes.loading import *
    from .beam_data import BeamData_Window
    from .load_data import LoadData_Window
    from .analysis import Analysis_Window

is_direct_call = False   # This module can be directly invoked from the command line.

# The following function was created to facilitate console input while testing the 
# correctness of analysis calculations during the initial stage of 
# development; now it is redundant and may be deleted.
def my_input(prompt, default_value, datatype):
    ans = input(prompt + " [" + str(default_value) + "]: ").strip()
    if not ans:
        return default_value
    return datatype(ans)


# The class for displaying the main menu of continuous beam program
class ContiBeamMenuWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.transient(master)

        # width x height + x_offset + y_offset
        self.geometry("800x600")

        self.title("Continuous Beam Analysis")

        # Tell the window to call this function when the close button is clicked
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        self.frame1 = ttk.Frame(self)
        self.frame1.pack(side="top", fill="both", expand = True)
        self.frame1.grid_rowconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)

        self.init_widgets()

        self.cb = ContinuousBeam()  # This will be shared with beam_data, load_data, and analysis modules.
    

    def init_widgets(self):
        label1 = ttk.Label(self.frame1, text="Analysis of Continuous Beam", font='helvetica 24 bold', foreground='blue')
        label1.grid(row=0, column=0, pady=20)    # , sticky="ew")

        # Create a ttk style with a blue background and white foreground
        my_style = ttk.Style()
        my_style.configure('Blue.TButton', font='helvetica 18', foreground='white', background='blue')

        # Create the ttk buttons
        self.btn1 = ttk.Button(self.frame1, text="Input Beam Data", style="Blue.TButton", 
                command=self.open_beam_data_window)
        #   , command=lambda: self.root_win.show_frame(self.root_win.frame2))
        self.btn2 = ttk.Button(self.frame1, text="Input Load Data", style="Blue.TButton", width=30,
                command=self.open_load_data_window)
        self.btn3 = ttk.Button(self.frame1, text="Analysis", style="Blue.TButton", width=30,
                command=self.open_analysis_window)
        if is_direct_call:
            self.btn4 = ttk.Button(self.frame1, text="Exit", style="Blue.TButton", width=30,
                    command=self.on_closing)
            #self.btn4.state(['disabled'])
        else:
            self.btn4 = ttk.Button(self.frame1, text="Return to Main Menu", style="Blue.TButton",
                    command=self.on_closing)
        # dummy buttons to provide for future expansion of the program
        self.btn5 = ttk.Button(self.frame1, text="", style="Blue.TButton", width=30, state='disabled')
        self.btn6 = ttk.Button(self.frame1, text="", style="Blue.TButton", width=30, state='disabled')

        # Place the ttk buttons in a vertical column with a gap of 20 pixels in between
        self.btn1.grid(row=1, column=0, padx=150, pady=20, sticky="ew")
        self.btn2.grid(row=2, column=0, padx=150, pady=20, sticky="ew")
        self.btn3.grid(row=3, column=0, padx=150, pady=20, sticky="ew")
        self.btn4.grid(row=4, column=0, padx=150, pady=20, sticky="ew")
        self.btn5.grid(row=5, column=0, padx=150, pady=20, sticky="ew")
        self.btn6.grid(row=6, column=0, padx=150, pady=20, sticky="ew")


    # Define the function to be called when the window is closed
    def on_closing(self):
        if messagebox.askquestion("Confirm", "Want to quit the Continuous Beam Module?", parent=self) == "yes":
            self.destroy()

    def open_beam_data_window(self):
        new_window = BeamData_Window(self)

        self.btn1.state(['disabled'])
        self.btn2.state(['disabled'])
        self.btn3.state(['disabled'])
        if not is_direct_call:
            self.btn4.state(['disabled'])

        new_window.get_data()
        self.wait_window(new_window) # Wait for the child window to close
        
        self.btn1.state(['!disabled'])
        self.btn2.state(['!disabled'])
        self.btn3.state(['!disabled'])
        if not is_direct_call:
            self.btn4.state(['!disabled'])

    def open_load_data_window(self):
        new_window = LoadData_Window(self)

        self.btn1.state(['disabled'])
        self.btn2.state(['disabled'])
        self.btn3.state(['disabled'])
        if not is_direct_call:
            self.btn4.state(['disabled'])

        new_window.get_data()
        self.wait_window(new_window) # Wait for the child window to close

        self.btn1.state(['!disabled'])
        self.btn2.state(['!disabled'])
        self.btn3.state(['!disabled'])
        if not is_direct_call:
            self.btn4.state(['!disabled'])

    def open_analysis_window(self):
        new_window = Analysis_Window(self)

        self.btn1.state(['disabled'])
        self.btn2.state(['disabled'])
        self.btn3.state(['disabled'])
        if not is_direct_call:
            self.btn4.state(['disabled'])

        self.wait_window(new_window) # Wait for the child window to close

        self.btn1.state(['!disabled'])
        self.btn2.state(['!disabled'])
        self.btn3.state(['!disabled'])
        if not is_direct_call:
            self.btn4.state(['!disabled'])



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
    # main_window.iconify() 
    root.wait_window(main_window)
    main_window.destroy()
    # return True

def getBeamData(cb, main_window):
    pass

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


# The class to create the root window if this module is invoked
# directly from the command line.
class CB_direct(tk.Tk):

    def __init__(self, *args, **kwargs):
        #tk.Tk.__init__(self, *args, **kwargs)
        super().__init__(*args, **kwargs)
        self.geometry("800x600")
        self.title("StructInsight")

        root_frame = ttk.Frame(self)
        root_frame.pack(side="top", fill="both", expand = True)
        root_frame.grid_rowconfigure(0, weight=1)
        root_frame.grid_columnconfigure(0, weight=1)

        new_window = ContiBeamMenuWindow(self)
        self.wait_window(new_window) # Wait for the child window to close
        self.destroy()



if __name__ == '__main__':
    is_direct_call = True
    app = CB_direct()
    app.mainloop()



