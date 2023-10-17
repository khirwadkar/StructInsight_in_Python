# Module to perform analysis of the continuous beam

#from beam_classes.beam import Beam
#from beam_classes.continuousbeam import ContinuousBeam
#from base_classes.loading import *
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from beam_classes.beam import Beam
from base_classes.loading import *



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


        #self.frame1 = ttk.Frame(self)
        #self.frame1.pack(side="top", fill="both", expand = True)
        #self.frame1.grid_rowconfigure(0, weight=1)
        #self.frame1.grid_columnconfigure(0, weight=1)
        #self.init_widgets()

        self.cb = master.cb  # The global ContinuousBeam() object

        self.cb.analyse()
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
        self.cb.calcShearForces(0.05)     # using default value of step_size
        self.cb.calcBendingMoments(0.05)  # using default value of step_size
        self.cb.calcSlopeDeflections()    # step_size of bending moments is used by this function.
        # TODO : After the addition of the three statements above, several functions in
        #        'beam.py' and 'continuousbeam.py' to be modified to avoid redundancy.

        buttonContainerFrame = ttk.Frame(self.canvas)
        self.canvas.create_window(395, 565, window=buttonContainerFrame)

        self.backButton = ttk.Button(buttonContainerFrame, text='Back',
                     command = (lambda: self.on_backButton_click()))
        self.backButton.pack(side=tk.LEFT, padx=5, expand=True)
        self.sfdButton = ttk.Button(buttonContainerFrame, text='S.F. Diagram',
                     command = (lambda: self.on_sfdButton_click(440)))
        self.sfdButton.pack(side=tk.LEFT, padx=5)
        self.bmdButton = ttk.Button(buttonContainerFrame, text='B.M. Diagram',
                     command = (lambda: self.on_bmdButton_click(440)))
        self.bmdButton.pack(side=tk.LEFT, padx=5)
        self.deflectionsButton = ttk.Button(buttonContainerFrame, text='Deflections',
                     command = (lambda: self.on_deflectionsButton_click(440)))
        self.deflectionsButton.pack(side=tk.LEFT, padx=5)
        self.hideGridButton = ttk.Button(buttonContainerFrame, text='Hide Grid',
                     command = (lambda: self.hide_grid()))
        self.hideGridButton.pack(side=tk.LEFT, padx=5)


        # self.test_print()
        self.show_results()



    def on_backButton_click(self):
        self.canvas.delete(tk.ALL)
        self.destroy()


    def hide_grid(self):
        self.canvas.delete('grid')


    def on_deflectionsButton_click(self, y):
        self.canvas.delete('grid')
        self.canvas.delete('sfdbmd')

        str1 = "Note: Exaggerated deflections!! Only suggestive diagram. Do NOT measure slopes."
        self.canvas.create_text(395, 370, text=str1, fill='red', tags=('sfdbmd'))

        drg_scale = 700 / self.cb.getTotal_length()
        self.canvas.create_line(45, y, 745, y, width=2, fill='blue', tags=('sfdbmd'))
        maxDeflection = self.cb.getMaxDeflection()
        try:
            dfln_scale = abs(20 / maxDeflection[2])  # maxDeflection is tuple of (x, slope, deflection)
        except ZeroDivisionError:
            messagebox.showwarning(title='Beam Without Load', parent=self,
                    message='Probably, you have not specified any load on the beam.')
            return

        nSpans = self.cb.getNspans()
        for beamIndex in range(nSpans):
            xStart = 45 + int(self.cb.getJointPosX(beamIndex) * drg_scale)
            L = int(self.cb.getMemberLength(beamIndex) * drg_scale)
            x_deformations_list = self.cb.getMemberSlopeDeflections(beamIndex)
            n = len(x_deformations_list)
            xPrev = xStart
            yPrev = y
            for i in range(n):
                x = x_deformations_list[i][0]
                delta = x_deformations_list[i][2]
                xPos = xStart + int(x * drg_scale)
                pPixels = int(delta * dfln_scale)
                yPos = y - pPixels  # positive deflection is upwards.
                self.canvas.create_line(xPos, y, xPos, yPos, fill='yellow', tags=('sfdbmd'))
                self.canvas.create_line(xPrev, yPrev, xPos, yPos, fill='yellow', tags=('sfdbmd'))
                xPrev = xPos
                yPrev = yPos


    def on_sfdButton_click(self, y):
        self.canvas.delete('grid')
        self.canvas.delete('sfdbmd')
        drg_scale = 700 / self.cb.getTotal_length()
        self.canvas.create_line(45, y, 745, y, width=2, fill='blue', tags=('sfdbmd'))
        maxSF = self.cb.getMaxSF()
        try:
            sf_scale = abs(60 / maxSF[1])  # maxSF is tuple of (x, SF)
        except ZeroDivisionError:
            messagebox.showwarning(title='Beam Without Load', parent=self,
                    message='Probably, you have not specified any load on the beam.')
            return

        nSpans = self.cb.getNspans()
        for beamIndex in range(nSpans):
            xStart = 45 + int(self.cb.getJointPosX(beamIndex) * drg_scale)
            L = int(self.cb.getMemberLength(beamIndex) * drg_scale)
            x_sf_list = self.cb.getMemberShearForces(beamIndex)
            n = len(x_sf_list)
            xPrev = xStart
            yPrev = y
            for i in range(n):
                x = x_sf_list[i][0]
                p = x_sf_list[i][1]
                xPos = xStart + int(x * drg_scale)
                pPixels = int(p * sf_scale)
                yPos = y - pPixels
                self.canvas.create_line(xPos, y, xPos, yPos, fill='green', tags=('sfdbmd'))
                self.canvas.create_line(xPrev, yPrev, xPos, yPos, fill='green', tags=('sfdbmd'))
                xPrev = xPos
                yPrev = yPos
            p = x_sf_list[0][1]
            pPixels = abs(int(p * sf_scale))
            if p > 0:
                self.canvas.create_text(xStart, y-pPixels-2, anchor='sw', text=f"{round(abs(p), 3)} kN", fill='green', tags=('sfdbmd'))
            elif p < 0:
                self.canvas.create_text(xStart, y+pPixels+2, anchor='nw', text=f"{round(abs(p), 3)} kN", fill='green', tags=('sfdbmd'))
            p = x_sf_list[-1][1]
            pPixels = abs(int(p * sf_scale))
            if p > 0:
                self.canvas.create_text(xStart+L-5, y-pPixels-2, anchor='se', text=f"{round(abs(p), 3)} kN", fill='green', tags=('sfdbmd'))
            elif p < 0:
                self.canvas.create_text(xStart+L-5, y+pPixels+2, anchor='ne', text=f"{round(abs(p), 3)} kN", fill='green', tags=('sfdbmd'))

        for pix_level in range(15, 70, 15):
            sf_level = pix_level / sf_scale
            self.canvas.create_line(25, y-pix_level, 755, y-pix_level, fill='grey', tags=('grid'))
            self.canvas.create_text(765, y-pix_level, anchor='w', text=f"+{round(sf_level, 1)} kN", fill='grey', tags=('grid'))
            self.canvas.create_line(25, y+pix_level, 755, y+pix_level, fill='grey', tags=('grid'))
            self.canvas.create_text(765, y+pix_level, anchor='w', text=f"{round(-sf_level, 1)} kN", fill='grey', tags=('grid'))


    def on_bmdButton_click(self, y):
        self.canvas.delete('grid')
        self.canvas.delete('sfdbmd')
        drg_scale = 700 / self.cb.getTotal_length()
        self.canvas.create_line(45, y, 745, y, width=2, fill='blue', tags=('sfdbmd'))
        maxBM = self.cb.getMaxBM()
        try:
            bm_scale = abs(60 / maxBM[1])  # maxBM is tuple of (x, BM)
        except ZeroDivisionError:
            messagebox.showwarning(title='Beam Without Load', parent=self,
                    message='Probably, you have not specified any load on the beam.')
            return

        nSpans = self.cb.getNspans()
        for beamIndex in range(nSpans):
            xStart = 45 + int(self.cb.getJointPosX(beamIndex) * drg_scale)
            L = int(self.cb.getMemberLength(beamIndex) * drg_scale)
            x_bm_list = self.cb.getMemberBendingMoments(beamIndex)
            n = len(x_bm_list)
            xPrev = xStart
            yPrev = y
            for i in range(n):
                x = x_bm_list[i][0]
                p = x_bm_list[i][1]
                xPos = xStart + int(x * drg_scale)
                pPixels = int(p * bm_scale)
                yPos = y - pPixels
                self.canvas.create_line(xPos, y, xPos, yPos, fill='green', tags=('sfdbmd'))
                self.canvas.create_line(xPrev, yPrev, xPos, yPos, fill='green', tags=('sfdbmd'))
                xPrev = xPos
                yPrev = yPos
            p = x_bm_list[0][1]
            pPixels = abs(int(p * bm_scale))
            if p > 0:
                self.canvas.create_text(xStart, y-pPixels-2, anchor='sw', text=f"{round(abs(p), 3)} kN-m", fill='green', tags=('sfdbmd'))
            elif p < 0:
                self.canvas.create_text(xStart, y+pPixels+2, anchor='nw', text=f"{round(abs(p), 3)} kN-m", fill='green', tags=('sfdbmd'))
            p = x_bm_list[-1][1]
            pPixels = abs(int(p * bm_scale))
            if p > 0:
                self.canvas.create_text(xStart+L-5, y-pPixels-2, anchor='se', text=f"{round(abs(p), 3)} kN-m", fill='green', tags=('sfdbmd'))
            elif p < 0:
                self.canvas.create_text(xStart+L-5, y+pPixels+2, anchor='ne', text=f"{round(abs(p), 3)} kN-m", fill='green', tags=('sfdbmd'))

        for pix_level in range(15, 70, 15):
            bm_level = pix_level / bm_scale
            self.canvas.create_line(25, y-pix_level, 755, y-pix_level, fill='grey', tags=('grid'))
            self.canvas.create_text(765, y-pix_level, anchor='w', text=f"+{round(bm_level, 1)} kN-m", fill='grey', tags=('grid'))
            self.canvas.create_line(25, y+pix_level, 755, y+pix_level, fill='grey', tags=('grid'))
            self.canvas.create_text(765, y+pix_level, anchor='w', text=f"{round(-bm_level, 1)} kN-m", fill='grey', tags=('grid'))



    def show_results(self):
        self.draw_separator_line(200)
        self.draw_separator_line(350)
        self.paint_beam_at_y(100)
        self.draw_supports_at_y(100)
        self.draw_joint_pointLoads_at_y(100)
        self.draw_joint_moments_at_y(100)
        self.draw_member_UDLs_at_y(100)
        self.draw_member_PtLoads_at_y(100)
        self.paint_beam_at_y(260)
        self.draw_load_reactions_at_y(260)
        self.draw_moment_reactions_at_y(255)
        pass


    def draw_separator_line(self, y):
        self.canvas.create_line(0, y, 799, y, width=3, fill='blue')
        pass


    def paint_beam_at_y(self, y):
        drawing_scale = 700 / self.cb.getTotal_length()

        depthsInPixelsList = self.getBeamDepthsInDrawingArray()

        nSpans = self.cb.getNspans()
        for i in range(nSpans):
            self.drawBeam(i, y, drawing_scale, depthsInPixelsList)
        self.canvas.create_line(45, y-10, 745, y-10, fill='blue')
        self.canvas.create_line(45, y, 745, y, fill='blue')



    def draw_supports_at_y(self, y):
        drawing_scale = 700 / self.cb.getTotal_length()

        nJoints = self.cb.getNJoints()
        for i in range(nJoints):
            jtType = self.cb.getJointType(i)
            if jtType == Beam.FIXED:
                self.drawFixedSupport(i, y, drawing_scale)
            elif jtType == Beam.HINGE:
                self.drawSimpleSupport(i, y, drawing_scale)
            elif jtType == Beam.FREE:
                self.drawFreeSupportSymbol(i, y, drawing_scale)


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


    def draw_joint_pointLoads_at_y(self, y):
        self.canvas.delete('jointLoads')
        scale = 700 / self.cb.getTotal_length()
        nJoints = self.cb.getNJoints()
        for jtIndex in range(nJoints):
            jtLoad = self.cb.getJtAction(2*jtIndex)
            x = 45 + int(self.cb.getJointPosX(jtIndex) * scale)
            #y = 240
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


    def draw_joint_moments_at_y(self, y):
        self.canvas.delete('jointMoments')
        scale = 700 / self.cb.getTotal_length()
        nJoints = self.cb.getNJoints()
        for jtIndex in range(nJoints):
            jtMoment = self.cb.getJtAction(2*jtIndex + 1)
            x = 45 + int(self.cb.getJointPosX(jtIndex) * scale)
            #y = 250
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


    def draw_member_UDLs_at_y(self, y):
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
            #y = 250
            if udl.p > 0.0:
                for i in range(n):
                    self.canvas.create_arc(x+i*6, y-14, x+i*6+6, y-5, style='arc', outline='orange',
                            start=180, extent=-180, tags=('udLoads')) # 6 x 9 ellipse's arc
                xc = x + L / 2
                yc = y - 20
                self.canvas.create_line(xc, yc, xc, yc-45, arrow='first', fill='orange', tags=('udLoads'))
                self.canvas.create_text(xc, yc-60, text=f"{abs(udl.p)} kN/m", fill='orange', tags=('udLoads'))
            if udl.p < 0.0:
                for i in range(n):
                    self.canvas.create_arc(x+i*6, y, x+i*6+6, y+9, style='arc', outline='orange',
                            start=180, extent=180, tags=('udLoads')) # 6 x 9 ellipse's arc
                xc = x + L / 2
                yc = y + 10
                self.canvas.create_line(xc, yc, xc+20, yc+20, arrow='first', fill='orange', tags=('udLoads'))
                self.canvas.create_line(xc+20, yc+20, xc, yc-75, fill='orange', tags=('udLoads'))
                self.canvas.create_text(xc, yc-90, text=f"{abs(udl.p)} kN/m", fill='orange', tags=('udLoads'))


    def draw_member_PtLoads_at_y(self, y):
        self.canvas.delete('ptLoads')
        str1 = "(Point loads in 'kN' and their distances in 'meters' units.)"
        self.canvas.create_text(395, y+80, text=str1, fill='red', tags=('ptLoads'))

        scale = 700 / self.cb.getTotal_length()
        nSpans = self.cb.getNspans()
        for memberIndex in range(nSpans):
            ptLoadList_unsorted = self.cb.getMemberPtLoads(memberIndex)
            ptLoadList = sorted(ptLoadList_unsorted, key = lambda ob: ob.x) 
            x = 45 + int(self.cb.getJointPosX(memberIndex) * scale)
            L = int(self.cb.getMemberLength(memberIndex) * scale)
            n = len(ptLoadList)
            #y = 240
            for i in range(n):
                posX = x + int(ptLoadList[i].x * scale)

                if ptLoadList[i].p > 0.0:
                    self.canvas.create_line(posX, y-10, posX, y-35, arrow='first', fill='red', tags=('ptLoads'))
                else:
                    self.canvas.create_line(posX, y-10, posX, y-35, arrow='last', fill='red', tags=('ptLoads'))

                if i % 2 == 0:
                    self.canvas.create_text(posX, y-45, text=f"{abs(ptLoadList[i].p)}", fill='red', tags=('ptLoads'))
                else:
                    self.canvas.create_text(posX, y-55, text=f"{abs(ptLoadList[i].p)}", fill='red', tags=('ptLoads'))

                self.canvas.create_line(x, y+15+12*i, x, y+25+12*i, fill='blue', tags=('ptLoads'))
                self.canvas.create_line(posX, y+15+12*i, posX, y+25+12*i, fill='blue', tags=('ptLoads'))
                self.canvas.create_line(x, y+20+12*i, x+12, y+20+12*i, arrow='first', fill='blue', tags=('ptLoads'))
                self.canvas.create_line(posX, y+20+12*i, posX-12, y+20+12*i, arrow='first', fill='blue', tags=('ptLoads'))
                midx = (x + posX) / 2
                self.canvas.create_text(midx, y+20+12*i, text=f"{ptLoadList[i].x}", fill='blue', tags=('ptLoads'))


    def draw_load_reactions_at_y(self, y):
        self.canvas.delete('loadReaction')
        scale = 700 / self.cb.getTotal_length()
        nJoints = self.cb.getNJoints()
        for jtIndex in range(nJoints):
            reaction = self.cb.getSupportReaction(2*jtIndex)
            x = 45 + int(self.cb.getJointPosX(jtIndex) * scale)
            #y = 240
            if reaction > 0.0:        # Upward reaction positive
                self.canvas.create_line(x, y, x, y+50, arrow='first', fill='blue', tags=('loadReaction'))
                if jtIndex % 2 == 0:
                    self.canvas.create_text(x, y+70, text=f"{round(abs(reaction), 3)} kN", fill='blue', tags=('loadReaction'))
                else:
                    self.canvas.create_text(x, y+60, text=f"{round(abs(reaction), 3)} kN", fill='blue', tags=('loadReaction'))
            elif reaction < 0.0:      # Downward reaction negative
                self.canvas.create_line(x, y, x, y+50, arrow='last', fill='blue', tags=('loadReaction'))
                if jtIndex % 2 == 0:
                    self.canvas.create_text(x, y+70, text=f"{round(abs(reaction), 3)} kN", fill='blue', tags=('loadReaction'))
                else:
                    self.canvas.create_text(x, y+60, text=f"{round(abs(reaction), 3)} kN", fill='blue', tags=('loadReaction'))


    def draw_moment_reactions_at_y(self, y):
        self.canvas.delete('momentReaction')
        scale = 700 / self.cb.getTotal_length()
        nJoints = self.cb.getNJoints()
        for jtIndex in range(nJoints):
            reactMoment = self.cb.getSupportReaction(2*jtIndex + 1)
            x = 45 + int(self.cb.getJointPosX(jtIndex) * scale)
            #y = 250
            if reactMoment > 0.0:      # Anti-clockwise moment positive
                self.canvas.create_arc(x-15, y-20, x+25, y+20, style='arc', outline='green',
                        start=70, extent=220, tags=('momentReaction'))
                self.canvas.create_line(x+12, y+19, x+15, y+19, arrow='last', fill='green', tags=('momentReaction'))
                self.canvas.create_text(x, y-30, text=f"{round(abs(reactMoment), 3)} kN-m", fill='green',
                            tags=('momentReaction'))
            elif reactMoment < 0.0:    # clockwise moment negative
                self.canvas.create_arc(x-15, y-20, x+25, y+20, style='arc', outline='green',
                        start=70, extent=220, tags=('momentReaction'))
                self.canvas.create_line(x+12, y-19, x+15, y-19, arrow='last', fill='green', tags=('momentReaction'))
                self.canvas.create_text(x, y-30, text=f"{round(abs(reactMoment), 3)} kN-m", fill='green',
                            tags=('momentReaction'))


    def test_print(self):
        self.cb.calcShearForces(0.1)
        self.cb.calcBendingMoments(0.1)
        print(self.cb)
        nSpans = self.cb.getNspans()
        for memberIndex in range(nSpans):
            print(f"Shear Forces on Beam {memberIndex + 1}:")
            print(f"-----------------------------------------")
            print(self.cb.getMemberShearForces(memberIndex, 0.1))
            print("\nMaximum SF: ", str(self.cb.beamNum[memberIndex].getMaxSF()))
            print('-'*60)
            print()
            print(f"Bending Moments on Beam {memberIndex + 1}:")
            print(f"-----------------------------------------")
            print(self.cb.getMemberBendingMoments(memberIndex, 0.1))
            print("\nMaximum BM: ", str(self.cb.beamNum[memberIndex].getMaxBM()))
            print('='*60)
            print()
        pass

    # Define the function to be called when the window is closed
    def on_closing(self):
        self.destroy()
        #if messagebox.askquestion("Confirm", "Return to Menu for Continuous Beam Analysis?", parent=self) == "yes":
        #    self.destroy()


### All the following lines can be deleted.

"""
def getBeamData(cb, main_window):
    pass

def getLoadData(cb, main_window):
    pass

def analysis(cb, main_window):
    cb.analyse()
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




