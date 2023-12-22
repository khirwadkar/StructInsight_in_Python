""" StructInsight software's main menu.

    Starting point of the package for analysis of all types of structures.
    Provides framework for the future development of the project.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import tkinter.messagebox as messagebox
from continuousbeam import contibeam_main


class StructInsight(tk.Tk):
    """ Class to create graphics window for displaying the main menu.
    """

    def __init__(self, *args, **kwargs):
        #tk.Tk.__init__(self, *args, **kwargs) # does same job as of the next statement.
        super().__init__(*args, **kwargs)

        # width x height + x_offset + y_offset
        self.geometry("800x600")

        self.title("StructInsight")

        # Tell the window to call this function when the close button is clicked
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        self.root_frame = ttk.Frame(self)
        self.root_frame.pack(side="top", fill="both", expand = True)
        self.root_frame.grid_rowconfigure(0, weight=1)
        self.root_frame.grid_columnconfigure(0, weight=1)

        self.init_widgets()

        #self.frame2 = ttk.Frame(self)


    def init_widgets(self):
        label1 = ttk.Label(self.root_frame, text="Analysis of Structures", font='helvetica 24 bold', foreground='blue')
        label1.grid(row=0, column=0, pady=20) 

        # Create a ttk style with a blue background and white foreground
        my_style = ttk.Style()
        my_style.configure('Blue.TButton', font='helvetica 18', foreground='white', background='blue')

        # Create the ttk buttons
        btn1 = ttk.Button(self.root_frame, text="Continuous Beam", style="Blue.TButton", command=self.start_continuous_beam_module)
        btn2 = ttk.Button(self.root_frame, text="Plane Frame", style="Blue.TButton", width=30)
        btn3 = ttk.Button(self.root_frame, text="Space Frame", style="Blue.TButton", width=30)
        btn4 = ttk.Button(self.root_frame, text="Plane Truss", style="Blue.TButton", width=30)
        btn5 = ttk.Button(self.root_frame, text="Space Truss", style="Blue.TButton", width=30)
        btn6 = ttk.Button(self.root_frame, text="General FEM", style="Blue.TButton", width=30)
        btn7 = ttk.Button(self.root_frame, text="Exit", style="Blue.TButton", width=30, command=self.on_closing)

        # Disable the unprogrammed buttons
        btn2.state(['disabled'])
        btn3.state(['disabled'])
        btn4.state(['disabled'])
        btn5.state(['disabled'])
        btn6.state(['disabled'])

        # Place the ttk buttons in a vertical column with a gap of 10 pixels in between
        btn1.grid(row=1, column=0, padx=150, pady=20, sticky="ew")
        btn2.grid(row=2, column=0, padx=150, pady=20, sticky="ew")
        btn3.grid(row=3, column=0, padx=150, pady=20, sticky="ew")
        btn4.grid(row=4, column=0, padx=150, pady=20, sticky="ew")
        btn5.grid(row=5, column=0, padx=150, pady=20, sticky="ew")
        btn6.grid(row=6, column=0, padx=150, pady=20, sticky="ew")
        btn7.grid(row=7, column=0, padx=150, pady=20, sticky="ew")

    def show_frame(self, current_frame):
        #frame = self.frames[current_frame]
        frame = current_frame
        frame.tkraise()

    def start_continuous_beam_module(self):
        new_window = contibeam_main.ContiBeamMenuWindow(self)
        self.wait_window(new_window) # Wait for the child window to close



    # Define the function to be called when the window is closed
    def on_closing(self):
        if messagebox.askquestion("Confirm", "Do you really want to exit the application?") == "yes":
            self.destroy()




# Create an instance of the StructInsight class, i.e. the main window
app = StructInsight()

# Run the main loop
app.mainloop()



