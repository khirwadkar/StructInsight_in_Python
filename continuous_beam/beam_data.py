# Module to input data about geometry of a continuous beam

#from beam_classes.beam import Beam
#from beam_classes.continuousbeam import ContinuousBeam
#from base_classes.loading import *
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from beam_classes.beam import Beam



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
        self.canvas = tk.Canvas(self, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set,
                xscrollcommand=h.set)
        h['command'] = self.canvas.xview
        v['command'] = self.canvas.yview
        self.canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        h.grid(column=0, row=1, sticky=(tk.W, tk.E))
        v.grid(column=1, row=0, sticky=(tk.N, tk.S))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


        #self.frame1 = ttk.Frame(self)
        #self.frame1.pack(side="top", fill="both", expand = True)
        #self.frame1.grid_rowconfigure(0, weight=1)
        #self.frame1.grid_columnconfigure(0, weight=1)
        #self.init_widgets()

        self.cb = master.cb  # The global ContinuousBeam() object

        self.qNo = 0
        self.question = [ 
                "Input number of spans (beam members) (1 to 10):      ",
                "Input typical span (beam length) in meters:          ",
                "Change the spans, if necessary. Then click 'Submit'. ",
                "Typical Mod. of Elasticity(E) of beam material (MPa) ",
                "Change the values, if necessary. Then click 'Submit' ",
                "Moment of Inertia(I) of typical cross-section (m.^4) ",
                "Change the values, if necessary. Then click 'Submit' ",
                "Now, specify support details...                      "
                ]
    

    def test(self):
        self.canvas.create_line(10, 5, 200, 50)

    def get_data(self):
        if self.qNo == 0:
            question_label = tk.StringVar()
            # qL = ttk.Label(self.canvas, textvariable=question_label)
            # qL = ttk.Label(self.canvas, text=self.question[self.qNo])
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(100, 10, anchor='nw', window=qL)
            question_label.set(self.question[self.qNo])

            answer_text = tk.StringVar()
            # answer_box = ttk.Entry(self.canvas, width = 7, textvariable=answer_text)
            answer_box = ttk.Entry(self.canvas, width = 7, text=str(self.cb.getNspans()))
            answer_box.insert(0, str(self.cb.getNspans()))
            answer_box.bind("<Return>", lambda e: self.on_getting_nSpans(answer_box.get()))
            self.canvas.create_window(500, 10, anchor='nw', window=answer_box)
            answer_text.set(self.cb.getNspans())

            answer_box.focus()

            self.paint_beam()

        elif self.qNo == 1:
            pass

    def on_getting_nSpans(self, nSpans):
        print(nSpans)

        self.qNo += 1

    def paint_beam(self):
        drawing_scale = 700 / self.cb.getTotal_length()

        depthsInPixelsList = self.getBeamDepthsInDrawingArray()

        nSpans = self.cb.getNspans()
        for i in range(nSpans):
            self.drawBeam(i, 250, drawing_scale, depthsInPixelsList)
        self.canvas.create_line(45, 240, 745, 240, fill='blue')
        self.canvas.create_line(45, 250, 745, 250, fill='blue')

        nJoints = self.cb.getNJoints()
        for i in range(nJoints):
            jtType = self.cb.getJointType(i)
            if jtType == Beam.FIXED:
                self.drawFixedSupport(i, 250, drawing_scale)
            elif jtType == Beam.HINGE:
                self.drawVertArrow(i, 250, drawing_scale)


    def getBeamDepthsInDrawingArray(self):    # in pixel units
        ei_list = self.cb.getAllEI()
        ei_set = set(ei_list)
        nSizes = len(ei_set)
        leastThickness = int(10 / nSizes)    # maximum 10 pixels
        if leastThickness < 1:
            leastThickness = 1
        ei_set_sorted = sorted(ei_set)       # this is now list actually
        depthsInPixels = [(ei_set_sorted.index(ei) + 1) * leastThickness for ei in ei_list]
        return depthsInPixels
                
    def drawBeam(self, beamIndex, y, scale, depthsInPixelsList):
        x = 45 + int(self.cb.getJointPosX(beamIndex) * scale)
        L = int(self.cb.getMemberLength(beamIndex) * scale)
        t = depthsInPixelsList[beamIndex] 
        if t == 1:
            return
        self.canvas.create_rectangle(x, y-t, x+L, y, fill='black')

    def drawVertArrow(self, jtIndex, y, scale):
        x = 45 + int(self.cb.getJointPosX(jtIndex) * scale)
        self.canvas.create_line(x, y, x, y+40, arrow='first')

    def drawFixedSupport(self, jtIndex, y, scale):
        if int(self.cb.getJointPosX(jtIndex)) == 0:    # left-most end
            x = 45
            self.canvas.create_line(x, y-25, x, y+25)
            for i in range(0, 45, 5):
                self.canvas.create_line(x, y-23+i, x-5, y-18+i)
        else:                                    # right-most end
            x = 45 + int(self.cb.getJointPosX(jtIndex)) * scale
            self.canvas.create_line(x, y-25, x, y+25)
            for i in range(0, 50, 5):
                self.canvas.create_line(x, y-23+i, x+5, y-28+i)




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



