# Module to perform analysis of the continuous beam

#from beam_classes.beam import Beam
#from beam_classes.continuousbeam import ContinuousBeam
#from base_classes.loading import *
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox



# The class to display the results of analysis of continuous beam
class Analysis_Window(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.transient(master)

        # width x height + x_offset + y_offset
        self.geometry("800x600")

        self.title("Analysis Results")

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
    pass


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




