# Module to input data about geometry of a continuous beam

#from beam_classes.beam import Beam
#from beam_classes.continuousbeam import ContinuousBeam
#from base_classes.loading import *
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox



# The class for obtaining continuous beam geometry data
class BeamData_Window(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.transient(master)

        # width x height + x_offset + y_offset
        self.geometry("800x600")

        self.title("Input Beam Data")

        # Tell the window to call this function when the close button is clicked
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        h = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        v = ttk.Scrollbar(self, orient=tk.VERTICAL)
        canvas = tk.Canvas(self, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set,
                xscrollcommand=h.set)
        h['command'] = canvas.xview
        v['command'] = canvas.yview
        canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
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
        label1 = ttk.Label(self.frame1, text="Analysis of Continuous Beam", font='helvetica 24 bold', foreground='blue')
        label1.grid(row=0, column=0, pady=20)    # , sticky="ew")

        # Create a ttk style with a blue background and white foreground
        my_style = ttk.Style()
        my_style.configure('Blue.TButton', font='helvetica 18', foreground='white', background='blue')

        # Create the ttk buttons
        btn1 = ttk.Button(self.frame1, text="Input Beam Data", style="Blue.TButton")
        #   , command=lambda: self.root_win.show_frame(self.root_win.frame2))
        btn2 = ttk.Button(self.frame1, text="Input Load Data", style="Blue.TButton", width=30)
        btn3 = ttk.Button(self.frame1, text="Analysis", style="Blue.TButton", width=30)
        if is_direct_call:
            btn4 = ttk.Button(self.frame1, text="", style="Blue.TButton", width=30)
            btn4.state(['disabled'])
        else:
            btn4 = ttk.Button(self.frame1, text="Return to Main Menu", style="Blue.TButton",
                    command=self.on_closing)
        # dummy buttons to provide for future expansion of the program
        btn5 = ttk.Button(self.frame1, text="", style="Blue.TButton", width=30, state='disabled')
        btn6 = ttk.Button(self.frame1, text="", style="Blue.TButton", width=30, state='disabled')

        # Place the ttk buttons in a vertical column with a gap of 20 pixels in between
        btn1.grid(row=1, column=0, padx=150, pady=20, sticky="ew")
        btn2.grid(row=2, column=0, padx=150, pady=20, sticky="ew")
        btn3.grid(row=3, column=0, padx=150, pady=20, sticky="ew")
        btn4.grid(row=4, column=0, padx=150, pady=20, sticky="ew")
        btn5.grid(row=5, column=0, padx=150, pady=20, sticky="ew")
        btn6.grid(row=6, column=0, padx=150, pady=20, sticky="ew")


    # Define the function to be called when the window is closed
    def on_closing(self):
        self.destroy()
        #if messagebox.askquestion("Confirm", "Return to Menu for Continuous Beam Analysis?", parent=self) == "yes":
        #    self.destroy()


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



