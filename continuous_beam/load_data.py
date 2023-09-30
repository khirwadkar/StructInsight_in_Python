# Module to input loads on a continuous beam

#from beam_classes.beam import Beam
#from beam_classes.continuousbeam import ContinuousBeam
#from base_classes.loading import *
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from beam_classes.beam import Beam
from base_classes.loading import *



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


        #self.frame1 = ttk.Frame(self)
        #self.frame1.pack(side="top", fill="both", expand = True)
        #self.frame1.grid_rowconfigure(0, weight=1)
        #self.frame1.grid_columnconfigure(0, weight=1)
        #self.init_widgets()

        self.cb = master.cb  # The global ContinuousBeam() object

        self.qNo = 0
        self.question = [ 
                "Input joint loads, if any ...                         ",
                "Input uniformly distributed loads on members (kN/m)   ",
                "Input point loads on members, if any ...              ",
                "                                                      ",
                "Change the values, if necessary. Then click 'Submit' ",
                ]
        self.supportFlag = True
        self.supportIndex = 0
        self.cb.initJtActionArray()
        self.memberIndex = 0
    


    def get_data(self):
        if self.qNo == 0:     # Input joint loads and joint moments
            # Upward loads are considered positive, while downwards would be negative.
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(100, 10, anchor='nw', window=qL)

            self.previousJtBt = ttk.Button(self.canvas, text='Previous Joint', command = (lambda: self.on_previousJtBt_click()))
            self.canvas.create_window(335, 60, window=self.previousJtBt)
            self.nextJtBt = ttk.Button(self.canvas, text=' Next  Joint ', command = (lambda: self.on_nextJtBt_click()))
            self.canvas.create_window(455, 60, window=self.nextJtBt)

            if self.supportIndex == 0:
                self.previousJtBt.state(['disabled'])
            else:
                self.previousJtBt.state(['!disabled'])
            if self.supportIndex == self.cb.getNJoints() - 1:
                self.nextJtBt.state(['disabled'])
            else:
                self.nextJtBt.state(['!disabled'])

            self.draw_support_pointer()

            buttonContainerFrame = ttk.Frame(self.canvas)
            self.canvas.create_window(395, 110, window=buttonContainerFrame)

            self.icon_up = tk.PhotoImage(file='./MyIcons/up-arrow.gif')
            self.icon_dn = tk.PhotoImage(file='./MyIcons/down-arrow.gif')
            self.icon_clk = tk.PhotoImage(file='./MyIcons/clockwise-moment.gif')
            self.icon_antclk = tk.PhotoImage(file='./MyIcons/anticlockwise-moment.gif')
            



            #self.upJtLoadBt = ttk.Button(buttonContainerFrame, text='  Upward Load  ', command = (lambda: self.on_upJtLoadBt_click()))
            self.upJtLoadBt = ttk.Button(buttonContainerFrame, image=self.icon_up, text=' Upward\n Load  ',
                    compound=tk.LEFT, command = (lambda: self.on_upJtLoadBt_click()))
            self.upJtLoadBt.pack(side=tk.LEFT, padx=5, ipadx=5, expand=True) 
            self.downJtLoadBt = ttk.Button(buttonContainerFrame, image=self.icon_dn, text=' Downward\n Load ', 
                    compound=tk.LEFT, command = (lambda: self.on_downJtLoadBt_click()))
            self.downJtLoadBt.pack(side=tk.LEFT, padx=5) 
            self.clockwiseJtMomentBt = ttk.Button(buttonContainerFrame, image=self.icon_clk, text=' Clockwise\n Moment ', 
                    compound=tk.LEFT, command = (lambda: self.on_clockwiseJtMomentBt_click()))
            self.clockwiseJtMomentBt.pack(side=tk.LEFT, padx=5)
            self.anticlockJtMomentBt = ttk.Button(buttonContainerFrame, image=self.icon_antclk, text='AntiClockwise\nMoment', 
                    compound=tk.LEFT, command = (lambda: self.on_anticlockJtMomentBt_click()))
            self.anticlockJtMomentBt.pack(side=tk.LEFT, padx=5)


            jointLoadSubmitBt = ttk.Button(self.canvas, text='No more Joint Actions', command = (lambda: self.on_jointLoadSubmitBt_click()))
            self.canvas.create_window(395, 450, window=jointLoadSubmitBt)

            self.paint_beam()

        if self.qNo == 1:     # Input uniformly distributed loads
            # Downward udl are considered positive and upward udl as negative.
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(100, 10, anchor='nw', window=qL)

            self.prevMemberBt = ttk.Button(self.canvas, text='Previous Member', command = (lambda: self.on_prevMemberBt_click()))
            self.canvas.create_window(325, 60, window=self.prevMemberBt)
            self.nextMemberBt = ttk.Button(self.canvas, text=' Next  Member ', command = (lambda: self.on_nextMemberBt_click()))
            self.canvas.create_window(465, 60, window=self.nextMemberBt)

            if self.memberIndex == 0:
                self.prevMemberBt.state(['disabled'])
            else:
                self.prevMemberBt.state(['!disabled'])
            if self.memberIndex == self.cb.getNspans() - 1:
                self.nextMemberBt.state(['disabled'])
            else:
                self.nextMemberBt.state(['!disabled'])
            self.draw_member_pointer()


            self.udlUpBt = ttk.Button(self.canvas, text=' Upward UDL ', command = (lambda: self.on_udlUpBt_click()))
            self.canvas.create_window(325, 110, window=self.udlUpBt)
            self.udlDownBt = ttk.Button(self.canvas, text='Downward UDL', command = (lambda: self.on_udlDownBt_click()))
            self.canvas.create_window(465, 110, window=self.udlDownBt)


            udlSubmitBt = ttk.Button(self.canvas, text='No more U. D. Loads', command = (lambda: self.on_udlSubmitBt_click()))
            self.canvas.create_window(395, 450, window=udlSubmitBt)

            self.paint_beam()

        if self.qNo == 2:     # Input Point loads
            # Downward point loads are considered positive and upward as negative.
            qL = ttk.Label(self.canvas)
            qL['text'] = self.question[self.qNo]
            self.canvas.create_window(100, 10, anchor='nw', window=qL)

            self.prevMemberBt = ttk.Button(self.canvas, text='Previous Member', command = (lambda: self.on_prevMemberBt_click()))
            self.canvas.create_window(325, 60, window=self.prevMemberBt)
            self.nextMemberBt = ttk.Button(self.canvas, text=' Next  Member ', command = (lambda: self.on_nextMemberBt_click()))
            self.canvas.create_window(465, 60, window=self.nextMemberBt)

            if self.memberIndex == 0:
                self.prevMemberBt.state(['disabled'])
            else:
                self.prevMemberBt.state(['!disabled'])
            if self.memberIndex == self.cb.getNspans() - 1:
                self.nextMemberBt.state(['disabled'])
            else:
                self.nextMemberBt.state(['!disabled'])
            self.draw_member_pointer()


            self.ptLoadUpBt = ttk.Button(self.canvas, text=' Upward Pt. Load ', command = (lambda: self.on_ptLoadUpBt_click()))
            self.canvas.create_window(315, 110, window=self.ptLoadUpBt)
            self.ptLoadDownBt = ttk.Button(self.canvas, text='Downward Pt. Load', command = (lambda: self.on_ptLoadDownBt_click()))
            self.canvas.create_window(475, 110, window=self.ptLoadDownBt)


            ptLoadSubmitBt = ttk.Button(self.canvas, text='No more Point Loads', command = (lambda: self.on_ptLoadSubmitB_click()))
            self.canvas.create_window(395, 450, window=ptLoadSubmitBt)

            self.paint_beam()



    def on_previousJtBt_click(self):
        self.canvas.delete('support_pointer')
        self.supportIndex -= 1 
        if self.supportIndex == 0:
            self.previousJtBt.state(['disabled'])
        else:
            self.previousJtBt.state(['!disabled'])
        if self.supportIndex == self.cb.getNJoints() - 1:
            self.nextJtBt.state(['disabled'])
        else:
            self.nextJtBt.state(['!disabled'])
        self.draw_support_pointer()


    def on_nextJtBt_click(self):
        self.canvas.delete('support_pointer')
        self.supportIndex += 1 
        if self.supportIndex == 0:
            self.previousJtBt.state(['disabled'])
        else:
            self.previousJtBt.state(['!disabled'])
        if self.supportIndex == self.cb.getNJoints() - 1:
            self.nextJtBt.state(['disabled'])
        else:
            self.nextJtBt.state(['!disabled'])
        self.draw_support_pointer()


    def on_upJtLoadBt_click(self):
        vLoad = simpledialog.askfloat(title='Input Joint Load', 
                prompt=f'Input upward point load in kN units at joint # {self.supportIndex + 1}', 
                parent=self, initialvalue=0.0, minvalue=0.0)
        self.cb.setJtAction(2*self.supportIndex, vLoad)
        self.draw_joint_pointLoads()


    def on_downJtLoadBt_click(self):
        vLoad = simpledialog.askfloat(title='Input Joint Load', 
                prompt=f'Input downward point load in kN units at joint # {self.supportIndex + 1}', 
                parent=self, initialvalue=0.0, minvalue=0.0)
        self.cb.setJtAction(2*self.supportIndex, -vLoad)
        self.draw_joint_pointLoads()
   

    def on_clockwiseJtMomentBt_click(self):
        jtMoment = simpledialog.askfloat(title='Input Joint Moment', 
                prompt=f'Input clockwise moment in kN-m units at joint # {self.supportIndex + 1}', 
                parent=self, initialvalue=0.0, minvalue=0.0)
        self.cb.setJtAction(2*self.supportIndex + 1, -jtMoment)
        self.draw_joint_moments()
   

    def on_anticlockJtMomentBt_click(self):
        jtMoment = simpledialog.askfloat(title='Input Joint Moment', 
                prompt=f'Input counter-clockwise moment in kN-m units at joint # {self.supportIndex + 1}', 
                parent=self, initialvalue=0.0, minvalue=0.0)
        self.cb.setJtAction(2*self.supportIndex + 1, jtMoment)
        self.draw_joint_moments()


    def on_jointLoadSubmitBt_click(self):
        self.qNo += 1
        self.canvas.delete(tk.ALL)
        self.get_data()


    def on_prevMemberBt_click(self):
        self.canvas.delete('member_pointer')
        self.memberIndex -= 1 
        if self.memberIndex == 0:
            self.prevMemberBt.state(['disabled'])
        else:
            self.prevMemberBt.state(['!disabled'])
        if self.memberIndex == self.cb.getNspans() - 1:
            self.nextMemberBt.state(['disabled'])
        else:
            self.nextMemberBt.state(['!disabled'])
        self.draw_member_pointer()


    def on_nextMemberBt_click(self):
        self.canvas.delete('member_pointer')
        self.memberIndex += 1 
        if self.memberIndex == 0:
            self.prevMemberBt.state(['disabled'])
        else:
            self.prevMemberBt.state(['!disabled'])
        if self.memberIndex == self.cb.getNspans() - 1:
            self.nextMemberBt.state(['disabled'])
        else:
            self.nextMemberBt.state(['!disabled'])
        self.draw_member_pointer()


    def on_udlUpBt_click(self):
        udl_value = simpledialog.askfloat(title='Uniformly Distributed Load (UDL)',
                prompt=f'Input upward UDL in kN/m units on member # {self.memberIndex + 1}', 
                parent=self, initialvalue=0.0, minvalue=0.0)
        # TODO : The following statements would be modified after the general
        #        UDL class is developed.
        self.cb.setMemberUDLfull(self.memberIndex, -udl_value)
        self.draw_member_UDLs()


    def on_udlDownBt_click(self):
        udl_value = simpledialog.askfloat(title='Uniformly Distributed Load (UDL)',
                prompt=f'Input downward UDL in kN/m units on member # {self.memberIndex + 1}', 
                parent=self, initialvalue=0.0, minvalue=0.0)
        # TODO : The following statements would be modified after the general
        #        UDL class is developed.
        self.cb.setMemberUDLfull(self.memberIndex, udl_value)
        self.draw_member_UDLs()


    def on_udlSubmitBt_click(self):
        self.qNo += 1
        self.memberIndex = 0
        self.canvas.delete(tk.ALL)
        self.get_data()


    def on_ptLoadUpBt_click(self):
        P = simpledialog.askfloat(title='Input Upward Point Load',
                prompt=f'Upward point load in kN units on member # {self.memberIndex + 1}', 
                parent=self, initialvalue=0.0, minvalue=0.0)
        x = 0.0
        memberLength = self.cb.getMemberLength(self.memberIndex)
        if P > 0.0:
            x = simpledialog.askfloat(title='Input Point Load Position', 
                    prompt=f'Distance in meters of {P} kN load from left end of member # {self.memberIndex + 1}', 
                    parent=self, minvalue=0.0, maxvalue=memberLength)
        else:
            messagebox.showwarning(title='Zero Point Load', parent=self, 
                    message='You have given Zero as the value of point load. Not adding it to the point loads list.')
            return
        """
        if x == 0.0 || x == memberLength:
            messagebox.showwarning(title='Not a Member Load', parent=self, 
                    message='You have placed the load on one of the member ends. Please input it as a joint load.')
            return
        """
        pL = PointLoad(-P, x)
        self.cb.addMemberPointLoad(self.memberIndex, pL)
        self.draw_member_PtLoads()


    def on_ptLoadDownBt_click(self):
        P = simpledialog.askfloat(title='Input Downward Point Load',
                prompt=f'Downward point load in kN units on member # {self.memberIndex + 1}', 
                parent=self, initialvalue=0.0, minvalue=0.0)
        x = 0.0
        memberLength = self.cb.getMemberLength(self.memberIndex)
        if P > 0.0:
            x = simpledialog.askfloat(title='Input Point Load Position', 
                    prompt=f'Distance in meters of {P} kN load from left end of member # {self.memberIndex + 1}', 
                    parent=self, minvalue=0.0, maxvalue=memberLength)
        else:
            messagebox.showwarning(title='Zero Point Load', parent=self, 
                    message='You have given Zero as the value of point load. Not adding it to the point loads list.')
            return
        """
        if x == 0.0 || x == memberLength:
            messagebox.showwarning(title='Not a Member Load', parent=self, 
                    message='You have placed the load on one of the member ends. Please input it as a joint load.')
            return
        """
        pL = PointLoad(P, x)
        self.cb.addMemberPointLoad(self.memberIndex, pL)
        self.draw_member_PtLoads()


    def on_ptLoadSubmitB_click(self):
        self.qNo += 1
        self.memberIndex = 0
        self.canvas.delete(tk.ALL)
        # self.get_data()
        self.destroy()



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


    def drawVertArrow(self, jtIndex, y, scale):
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
        y = 240
        promptLabel = self.canvas.create_text(x+21, y-90, text=f"@ Jt. {jtIndex + 1}?", fill='green', tags=('support_pointer'))
        self.canvas.create_line(x, y-5, x+21, y-75, arrow='first', fill='green', width=2, tags=('support_pointer'))


    def draw_joint_pointLoads(self):
        self.canvas.delete('jointLoads')
        scale = 700 / self.cb.getTotal_length()
        nJoints = self.cb.getNJoints()
        for jtIndex in range(nJoints):
            jtLoad = self.cb.getJtAction(2*jtIndex)
            x = 45 + int(self.cb.getJointPosX(jtIndex) * scale)
            y = 240
            if jtLoad > 0.0:
                self.canvas.create_line(x, y, x, y-50, arrow='last', fill='magenta', tags=('jointLoads'))
                if jtIndex % 2 == 0:
                    self.canvas.create_text(x, y-70, text=f"{abs(jtLoad)} kN", fill='magenta', tags=('jointLoads'))
                else:
                    self.canvas.create_text(x, y-60, text=f"{abs(jtLoad)} kN", fill='magenta', tags=('jointLoads'))
            elif jtLoad < 0.0:
                self.canvas.create_line(x, y, x, y-50, arrow='first', fill='magenta', tags=('jointLoads'))
                if jtIndex % 2 == 0:
                    self.canvas.create_text(x, y-70, text=f"{abs(jtLoad)} kN", fill='magenta', tags=('jointLoads'))
                else:
                    self.canvas.create_text(x, y-60, text=f"{abs(jtLoad)} kN", fill='magenta', tags=('jointLoads'))



    def draw_joint_moments(self):
        self.canvas.delete('jointMoments')
        scale = 700 / self.cb.getTotal_length()
        nJoints = self.cb.getNJoints()
        for jtIndex in range(nJoints):
            jtMoment = self.cb.getJtAction(2*jtIndex + 1)
            x = 45 + int(self.cb.getJointPosX(jtIndex) * scale)
            y = 250
            if jtMoment > 0.0:
                self.canvas.create_arc(x-15, y-20, x+25, y+20, style='arc', outline='magenta',
                        start=70, extent=220, tags=('jointMoments'))
                self.canvas.create_line(x+12, y+19, x+15, y+19, arrow='last', fill='magenta', tags=('jointMoments'))
                self.canvas.create_text(x, y-30, text=f"{abs(jtMoment)} kN-m", fill='magenta',
                            tags=('jointMoments'))
                #if jtIndex % 2 == 0:
                #    self.canvas.create_text(x+17, y-35, text=f"{abs(jtMoment)} kN-m", fill='magenta',
                #            anchor='nw', tags=('jointMoments'))
                #else:
                #    self.canvas.create_text(x+17, y-25, text=f"{abs(jtMoment)} kN-m", fill='magenta',
                #            anchor='nw', tags=('jointMoments'))
            elif jtMoment < 0.0:
                self.canvas.create_arc(x-15, y-20, x+25, y+20, style='arc', outline='magenta',
                        start=70, extent=220, tags=('jointMoments'))
                self.canvas.create_line(x+12, y-19, x+15, y-19, arrow='last', fill='magenta', tags=('jointMoments'))
                self.canvas.create_text(x, y-30, text=f"{abs(jtMoment)} kN-m", fill='magenta',
                            tags=('jointMoments'))


    def draw_member_pointer(self):
        scale = 700 / self.cb.getTotal_length()
        leftJtIndex = self.memberIndex
        x = 45 + int(self.cb.getJointPosX(leftJtIndex) * scale)
        # x = x + int(self.cb.getMemberLength(self.memberIndex) * scale / 2)
        # In stead of pointing at the middle of the beam as in the above commented statement,
        # pointing slightly to the right of the middle, as in the following statement.
        x = x + int(self.cb.getMemberLength(self.memberIndex) * scale * 0.60)
        y = 240
        promptLabel = self.canvas.create_text(x+10, y-85, text=f"on member {self.memberIndex + 1}?", fill='green', tags=('member_pointer'))
        self.canvas.create_line(x, y-8, x+10, y-70, arrow='first', fill='green', width=2, tags=('member_pointer'))


    def draw_member_UDLs(self):
        self.canvas.delete('udLoads')
        scale = 700 / self.cb.getTotal_length()
        nSpans = self.cb.getNspans()
        for memberIndex in range(nSpans):
            # TODO : The following statements would be modified after the general
            #        UDL class is developed.
            udl = self.cb.getMemberUDL(memberIndex)
            udl_p = udl.p
            x = 45 + int(self.cb.getJointPosX(memberIndex) * scale)
            L = int(self.cb.getMemberLength(memberIndex) * scale)
            n = int(L / 6)  # each arc in the drawing to represent UDL is 6 pixels wide.
            m = (L - 6*n) / 2
            x += m
            y = 250
            if udl.p > 0.0:
                for i in range(n):
                    self.canvas.create_arc(x+i*6, y-14, x+i*6+6, y-5, style='arc', outline='magenta',
                            start=180, extent=-180, tags=('udLoads')) # 6 x 9 ellipse's arc
                xc = x + L / 2
                yc = y - 20
                self.canvas.create_line(xc, yc, xc, yc-45, arrow='first', fill='magenta', tags=('udLoads'))
                self.canvas.create_text(xc, yc-60, text=f"{abs(udl.p)} kN/m", fill='magenta', tags=('udLoads'))
            if udl.p < 0.0:
                for i in range(n):
                    self.canvas.create_arc(x+i*6, y, x+i*6+6, y+9, style='arc', outline='magenta',
                            start=180, extent=180, tags=('udLoads')) # 6 x 9 ellipse's arc
                xc = x + L / 2
                yc = y + 10
                self.canvas.create_line(xc, yc, xc+20, yc+20, arrow='first', fill='magenta', tags=('udLoads'))
                self.canvas.create_line(xc+20, yc+20, xc, yc-75, fill='magenta', tags=('udLoads'))
                self.canvas.create_text(xc, yc-90, text=f"{abs(udl.p)} kN/m", fill='magenta', tags=('udLoads'))


    def draw_member_PtLoads(self):
        self.canvas.delete('ptLoads')
        str1 = "(Point loads in 'kN' and their distances in 'meters' units.)"
        self.canvas.create_text(395, 360, text=str1, fill='red', tags=('ptLoads'))

        scale = 700 / self.cb.getTotal_length()
        nSpans = self.cb.getNspans()
        for memberIndex in range(nSpans):
            ptLoadList_unsorted = self.cb.getMemberPtLoads(memberIndex)
            ptLoadList = sorted(ptLoadList_unsorted, key = lambda ob: ob.x) 
            x = 45 + int(self.cb.getJointPosX(memberIndex) * scale)
            L = int(self.cb.getMemberLength(memberIndex) * scale)
            n = len(ptLoadList)
            y = 240
            for i in range(n):
                posX = x + int(ptLoadList[i].x * scale)

                if ptLoadList[i].p > 0.0:
                    self.canvas.create_line(posX, y, posX, y-25, arrow='first', fill='red', tags=('ptLoads'))
                else:
                    self.canvas.create_line(posX, y, posX, y-25, arrow='last', fill='red', tags=('ptLoads'))

                if i % 2 == 0:
                    self.canvas.create_text(posX, y-35, text=f"{abs(ptLoadList[i].p)}", fill='red', tags=('ptLoads'))
                else:
                    self.canvas.create_text(posX, y-45, text=f"{abs(ptLoadList[i].p)}", fill='red', tags=('ptLoads'))

                self.canvas.create_line(x, y+14+12*i, x, y+24+12*i, fill='blue', tags=('ptLoads'))
                self.canvas.create_line(posX, y+14+12*i, posX, y+24+12*i, fill='blue', tags=('ptLoads'))
                self.canvas.create_line(x, y+19+12*i, x+12, y+19+12*i, arrow='first', fill='blue', tags=('ptLoads'))
                self.canvas.create_line(posX, y+19+12*i, posX-12, y+19+12*i, arrow='first', fill='blue', tags=('ptLoads'))
                midx = (x + posX) / 2
                self.canvas.create_text(midx, y+20+12*i, text=f"{ptLoadList[i].x}", fill='blue', tags=('ptLoads'))


    # Define the function to be called when the window is closed
    def on_closing(self):
        self.destroy()
        #if messagebox.askquestion("Confirm", "Return to Menu for Continuous Beam Analysis?", parent=self) == "yes":
        #    self.destroy()







