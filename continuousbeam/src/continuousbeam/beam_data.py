""" Module to input data about geometry of a continuous beam
"""

import sys
sys.path.append('.')
sys.path.append('..')

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
"""
try:
    from beam_classes.beam import Beam
except ImportError:
    from .beam_classes.beam import Beam
"""
try:
    from beam_classes import Beam
except ImportError:
    from .beam_classes import Beam



class BeamData_Window(tk.Toplevel):
    """ The class for obtaining continuous beam geometry data
    """

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


        self.cb = master.cb  # The global ContinuousBeam() object

        self.qNo = 0
        self.question = [ 
                "Input number of spans (beam members) (1 to 10): ",
                "Input typical span (beam length) in meters: ",
                "Change the spans, if necessary. Then click 'Submit'. ",
                "Typical Mod. of Elasticity(E) of beam material (MPa) ",
                "Change the values, if necessary. Then click 'Submit' ",
                "Moment of Inertia(I) of typical cross-section (m.^4) ",
                "Change the values, if necessary. Then click 'Submit' ",
                "Specify support type at each joint by clicking appropriate button..."
                ]
        self.supportFlag = True
        self.supportIndex = 0
    

    def get_data(self):
        if self.qNo == 0:     # Get number of spans (beams)
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(100, 10, anchor='nw', window=qL)

            answer_text = tk.StringVar()
            answer_text.set(str(self.cb.getNspans()))
            answer_box = ttk.Entry(self.canvas, width = 7, textvariable=answer_text)
            answer_box.bind("<Return>", lambda e: self.on_getting_nSpans(answer_text.get()))
            self.canvas.create_window(500, 10, anchor='nw', window=answer_box)

            answer_box.focus()

            self.paint_beam()


        if self.qNo == 1:          # Get typical span (beam length)
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(110, 10, anchor='nw', window=qL)

            answer_text = tk.StringVar()
            answer_text.set("3.5")
            answer_box = ttk.Entry(self.canvas, width = 7, textvariable=answer_text)
            answer_box.bind("<Return>", lambda e: self.on_getting_typicalSpan(answer_text.get()))
            self.canvas.create_window(500, 10, anchor='nw', window=answer_box)

            answer_box.focus()

            self.paint_beam()


        if self.qNo == 2:        # Get actual spans (lengths) of all beams
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(110, 10, anchor='nw', window=qL)

            drawing_scale = 700 / self.cb.getTotal_length()
            typical_span = self.cb.getTypicalSpan()
            nSpans = self.cb.getNspans()
            span_list = self.cb.getAllSpans()  # At this stage, their value equals typicalSpan
            span_stringvar_list = []
            answer_box_list = []
            for i in range(nSpans):
                span_stringvar_list.append(tk.StringVar())
                span_stringvar_list[i].set(typical_span)
                answer_box_list.append(ttk.Entry(self.canvas, width = 7, textvariable=span_stringvar_list[i]))
                x = 45 + int(self.cb.getJointPosX(i) * drawing_scale)
                L = int(self.cb.getMemberLength(i) * drawing_scale)
                self.canvas.create_window(x + L/2, 290, window=answer_box_list[i])

            answer_box_list[0].focus()

            self.paint_beam()

            submitButton = ttk.Button(self.canvas, text='Submit', command = (lambda: self.on_getting_allSpans(span_stringvar_list)))
            self.canvas.create_window(395, 360, window=submitButton)


        if self.qNo == 3:        # Get Typical Mod. of Elasticity(E)
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(110, 10, anchor='nw', window=qL)

            answer_text = tk.StringVar()
            answer_text.set("34500")
            answer_box = ttk.Entry(self.canvas, width = 7, textvariable=answer_text)
            answer_box.bind("<Return>", lambda e: self.on_getting_typicalModE(answer_text.get()))
            self.canvas.create_window(500, 10, anchor='nw', window=answer_box)

            answer_box.focus()

            self.paint_beam()


        if self.qNo == 4:        # Get Mod. of Elasticity(E) of all the beams
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(110, 10, anchor='nw', window=qL)

            drawing_scale = 700 / self.cb.getTotal_length()
            typical_modE = self.cb.getTypicalModEla()
            nSpans = self.cb.getNspans()
            modE_stringvar_list = []
            answer_box_list = []
            for i in range(nSpans):
                modE_stringvar_list.append(tk.StringVar())
                modE_stringvar_list[i].set(typical_modE)
                answer_box_list.append(ttk.Entry(self.canvas, width = 7, textvariable=modE_stringvar_list[i]))
                x = 45 + int(self.cb.getJointPosX(i) * drawing_scale)
                L = int(self.cb.getMemberLength(i) * drawing_scale)
                self.canvas.create_window(x + L/2, 290, window=answer_box_list[i])

            answer_box_list[0].focus()

            self.paint_beam()

            submitButton = ttk.Button(self.canvas, text='Submit', command = (lambda: self.on_getting_allModE(modE_stringvar_list)))
            self.canvas.create_window(395, 360, window=submitButton)



        if self.qNo == 5:        # Get Typical Moment of Inertia
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(110, 10, anchor='nw', window=qL)

            answer_text = tk.StringVar()
            answer_text.set("0.0005175")
            answer_box = ttk.Entry(self.canvas, width = 10, textvariable=answer_text)
            answer_box.bind("<Return>", lambda e: self.on_getting_typicalMI(answer_text.get()))
            self.canvas.create_window(495, 10, anchor='nw', window=answer_box)

            answer_box.focus()

            self.paint_beam()



        if self.qNo == 6:        # Get Moment of Inertia of all the beams
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(110, 10, anchor='nw', window=qL)

            drawing_scale = 700 / self.cb.getTotal_length()
            typical_mi = self.cb.getTypicalMomIner()
            nSpans = self.cb.getNspans()
            MI_stringvar_list = []
            answer_box_list = []
            for i in range(nSpans):
                MI_stringvar_list.append(tk.StringVar())
                MI_stringvar_list[i].set(typical_mi)
                answer_box_list.append(ttk.Entry(self.canvas, width = 9, textvariable=MI_stringvar_list[i]))
                x = 45 + int(self.cb.getJointPosX(i) * drawing_scale)
                L = int(self.cb.getMemberLength(i) * drawing_scale)
                self.canvas.create_window(x + L/2, 290, window=answer_box_list[i])

            answer_box_list[0].focus()

            self.paint_beam()

            submitButton = ttk.Button(self.canvas, text='Submit', command = (lambda: self.on_getting_allMI(MI_stringvar_list)))
            self.canvas.create_window(395, 360, window=submitButton)



        if self.qNo == 7:        # Get support details
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(110, 10, anchor='nw', window=qL)

            self.paint_beam()


            self.fixedBt = ttk.Button(self.canvas, text=' Fixed Support ', command = (lambda: self.on_any_supportTypeButton_click(Beam.FIXED)))
            self.canvas.create_window(250, 70, window=self.fixedBt)
            self.freeBt = ttk.Button(self.canvas, text='Free Joint', command = (lambda: self.on_any_supportTypeButton_click(Beam.FREE)))
            self.canvas.create_window(395, 70, window=self.freeBt)
            self.simpleSupBt = ttk.Button(self.canvas, text='Simple Support', command = (lambda: self.on_any_supportTypeButton_click(Beam.HINGE)))
            self.canvas.create_window(540, 70, window=self.simpleSupBt)

            # The syntax to disable and enable a button is as follows-
            # b.state(['disabled']) # set the disabled flag
            # b.state(['!disabled']) # clear the disabled flag
            # b.instate(['disabled']) # true if disabled, else false
            # b.instate(['!disabled']) # true if not disabled, else false
            # b.instate(['!disabled'], cmd) # execute 'cmd' if not disabled

            if self.supportIndex == 0:
                self.draw_support_pointer()

            if self.supportIndex == self.cb.getNJoints() - 1:
                self.fixedBt.state(['!disabled'])
                self.draw_support_pointer()

            if self.supportIndex > 0 and self.supportIndex < self.cb.getNJoints() - 1:
                self.fixedBt.state(['disabled'])
                self.draw_support_pointer()

            if self.supportIndex == self.cb.getNJoints():
                self.fixedBt.state(['disabled'])
                self.freeBt.state(['disabled'])
                self.simpleSupBt.state(['disabled'])
                editButton = ttk.Button(self.canvas, text='Edit', command = (lambda: self.on_editButton_click()))
                self.canvas.create_window(395, 400, window=editButton)
                exitButton = ttk.Button(self.canvas, text='Exit', command = (lambda: self.destroy()))
                self.canvas.create_window(395, 450, window=exitButton)



    def on_getting_nSpans(self, nSpans_txt):
        try:
            nSpans = int(nSpans_txt)
        except ValueError:
            messagebox.showinfo(parent=self, title="Error!",
                    message="Number of spans must be an integer between 1 and 10.")
            self.canvas.delete(tk.ALL)
            self.get_data()
            return
        if nSpans < 1 or nSpans > 10:
            messagebox.showinfo(parent=self, title="Error!",
                    message="Number of spans (beam members) can have value from 1 through 10.")
            self.canvas.delete(tk.ALL)
            self.get_data()
            return
        self.cb.setNspans(nSpans)
        self.qNo += 1
        self.canvas.delete(tk.ALL)
        self.get_data()


    def on_getting_typicalSpan(self, typicalSpan_txt):
        try:
            typicalSpan = float(typicalSpan_txt)
        except ValueError:
            messagebox.showinfo(parent=self, title="Error!",
                    message="Typical span (beam length) must be a positive real number.")
            self.canvas.delete(tk.ALL)
            self.get_data()
            return
        if typicalSpan < 0.0:
            messagebox.showinfo(parent=self, title="Error!",
                    message="Beam length can not be a negative number.")
            self.canvas.delete(tk.ALL)
            self.get_data()
            return
        self.cb.setTypicalSpan(typicalSpan)
        self.qNo += 1
        self.canvas.delete(tk.ALL)
        self.get_data()


    def on_getting_allSpans(self, spanList_of_StringVar):
        span_list_txt = [span.get() for span in spanList_of_StringVar]
        beamLengths = []
        try:
            for i in range(len(span_list_txt)):
                beamLengths.append(float(span_list_txt[i]))
                if beamLengths[i] < 0.0:
                    messagebox.showinfo(parent=self, title="Error!",
                            message=f"Check length of Beam # {i+1}. It can not be a negative number.")
                    #self.canvas.delete(tk.ALL)
                    #self.get_data()
                    return
        except ValueError:
            messagebox.showinfo(parent=self, title="Error!",
                    message=f"Check length of beam # {i+1}. It must be a positive real number.")
            #self.canvas.delete(tk.ALL)
            #self.get_data()
            return
        self.cb.setAllSpans(beamLengths)
        self.qNo += 1
        self.canvas.delete(tk.ALL)
        self.get_data()


    def on_getting_typicalModE(self, typicalModE_txt):
        try:
            typicalModE = float(typicalModE_txt)
        except ValueError:
            messagebox.showinfo(parent=self, title="Error!",
                    message="Typical Modulus of Elasticity must be a positive real number.")
            #self.canvas.delete(tk.ALL)
            #self.get_data()
            return
        if typicalModE < 0.0:
            messagebox.showinfo(parent=self, title="Error!",
                    message="Modulus of Elasticity can not be a negative number.")
            #self.canvas.delete(tk.ALL)
            #self.get_data()
            return
        self.cb.setTypicalModEla(typicalModE)
        self.qNo += 1
        self.canvas.delete(tk.ALL)
        self.get_data()


    def on_getting_allModE(self, modEList_of_StringVar):
        modE_list_txt = [modE.get() for modE in modEList_of_StringVar]
        beamE = []
        try:
            for i in range(len(modE_list_txt)):
                beamE.append(float(modE_list_txt[i]))
                if beamE[i] < 0.0:
                    messagebox.showinfo(parent=self, title="Error!",
                            message=f"Check Modulus of Elasticity of Beam # {i+1}. It can not be a negative number.")
                    #self.canvas.delete(tk.ALL)
                    #self.get_data()
                    return
        except ValueError:
            messagebox.showinfo(parent=self, title="Error!",
                    message=f"Check Modulus of Elasticity of beam # {i+1}. It must be a positive real number.")
            #self.canvas.delete(tk.ALL)
            #self.get_data()
            return
        self.cb.setAllE_MPa(beamE)
        self.qNo += 1
        self.canvas.delete(tk.ALL)
        self.get_data()


    def on_getting_typicalMI(self, typicalMI_txt):
        try:
            typicalMI = float(typicalMI_txt)
        except ValueError:
            messagebox.showinfo(parent=self, title="Error!",
                    message="Typical Moment of Inertia must be a positive real number.")
            #self.canvas.delete(tk.ALL)
            #self.get_data()
            return
        if typicalMI < 0.0:
            messagebox.showinfo(parent=self, title="Error!",
                    message="Moment of Inertia can not be a negative number.")
            #self.canvas.delete(tk.ALL)
            #self.get_data()
            return
        self.cb.setTypicalMomIner(typicalMI)
        self.qNo += 1
        self.canvas.delete(tk.ALL)
        self.get_data()


    def on_getting_allMI(self, MI_List_of_StringVar):
        mi_list_txt = [MI.get() for MI in MI_List_of_StringVar]
        beamMI = []
        try:
            for i in range(len(mi_list_txt)):
                beamMI.append(float(mi_list_txt[i]))
                if beamMI[i] < 0.0:
                    messagebox.showinfo(parent=self, title="Error!",
                            message=f"Check Moment of Inertia of Beam # {i+1}. It can not be a negative number.")
                    #self.canvas.delete(tk.ALL)
                    #self.get_data()
                    return
        except ValueError:
            messagebox.showinfo(parent=self, title="Error!",
                    message=f"Check Moment of Inertia of beam # {i+1}. It must be a positive real number.")
            #self.canvas.delete(tk.ALL)
            #self.get_data()
            return
        self.cb.setAllMomIner(beamMI)
        self.qNo += 1
        self.canvas.delete(tk.ALL)
        self.get_data()


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
                self.drawSimpleSupport(i, 250, drawing_scale)
            elif jtType == Beam.FREE:
                self.drawFreeSupportSymbol(i, 250, drawing_scale)


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


    def drawSimpleSupport(self, jtIndex, y, scale):
        x = 45 + int(self.cb.getJointPosX(jtIndex) * scale)
        self.canvas.create_line(x, y, x, y+40, arrow='first', fill='green')


    def drawFreeSupportSymbol(self, jtIndex, y, scale):
        x = 45 + int(self.cb.getJointPosX(jtIndex) * scale)
        self.canvas.create_rectangle(x-2, y-3, x+2, y+3, fill='green')


    def drawFixedSupport(self, jtIndex, y, scale):
        if int(self.cb.getJointPosX(jtIndex)) == 0:    # left-most end
            x = 45
            self.canvas.create_line(x, y-25, x, y+25, fill='green')
            for i in range(0, 45, 5):
                self.canvas.create_line(x, y-23+i, x-5, y-18+i, fill='green')
        else:                                    # right-most end
            x = 45 + int(self.cb.getJointPosX(jtIndex) * scale)
            self.canvas.create_line(x, y-25, x, y+25, fill='green')
            for i in range(0, 50, 5):
                self.canvas.create_line(x, y-23+i, x+5, y-28+i, fill='green')


    def draw_support_pointer(self):
        scale = 700 / self.cb.getTotal_length()
        jtIndex = self.supportIndex
        x = 45 + int(self.cb.getJointPosX(jtIndex) * scale)
        # promptLabel = self.canvas.create_text(x+7, 180, text=f"For Jt. {jtIndex + 1} ?", fill='red')
        self.canvas.create_text(x+7, 180, text=f"For Jt. {jtIndex + 1} ?", fill='red')
        self.canvas.create_line(x, 235, x+7, 195, arrow='first', fill='red', width=2)


    def on_any_supportTypeButton_click(self, supportType):
        self.cb.setJointType(self.supportIndex, supportType)
        self.supportIndex += 1
        self.canvas.delete(tk.ALL)
        self.get_data()


    def on_editButton_click(self):
        self.supportIndex = 0
        self.canvas.delete(tk.ALL)
        self.get_data()


    # Define the function to be called when the window is closed
    def on_closing(self):
        self.destroy()
        #if messagebox.askquestion("Confirm", "Return to Menu for Continuous Beam Analysis?", parent=self) == "yes":
        #    self.destroy()




