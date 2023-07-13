# Module to input loads on a continuous beam

#from beam_classes.beam import Beam
#from beam_classes.continuousbeam import ContinuousBeam
#from base_classes.loading import *
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox



# The class for obtaining continuous beam load data
class LoadData_Window(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.transient(master)

        # width x height + x_offset + y_offset
        self.geometry("800x600")

        self.title("Input Load Data")

        # Tell the window to call this function when the close button is clicked
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        h = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        v = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(self, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set,
                xscrollcommand=h.set)
        h['command'] = self.canvas.xview
        v['command'] = self.canvas.yview
        self.canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        h.grid(column=0, row=1, sticky=(tk.W, tk.E))
        v.grid(column=1, row=0, sticky=(tk.N, tk.S))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame1 = ttk.Frame(self)
        #self.frame1.pack(side="top", fill="both", expand = True)
        #self.frame1.grid_rowconfigure(0, weight=1)
        #self.frame1.grid_columnconfigure(0, weight=1)
        #self.init_widgets()

        self.cb = master.cb  # The global ContinuousBeam() object

    

    def init_widgets(self):
        pass


    # Define the function to be called when the window is closed
    def on_closing(self):
        self.destroy()
        #if messagebox.askquestion("Confirm", "Return to Menu for Continuous Beam Analysis?", parent=self) == "yes":
        #    self.destroy()


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
    pass






