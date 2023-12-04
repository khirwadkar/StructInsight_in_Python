""" Starting point of the continuous beam analysis program.

    This module renders the frontend GUI menu for the various
    options available in the continuous beam analysis.

    The module can be invoked directly from the command prompt
    or it can be imported from some other module.
"""

import sys
sys.path.append('.')
sys.path.append('..')

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox


try:
    from beam_classes import ContinuousBeam
    from base_classes import PointLoad, UdLoadFull
    from beam_data import BeamData_Window
    from load_data import LoadData_Window
    from analysis import Analysis_Window
except ImportError:
    from .beam_data import BeamData_Window
    from .load_data import LoadData_Window
    from .analysis import Analysis_Window

is_direct_call = False   # This module can be directly invoked from the command line.


class ContiBeamMenuWindow(tk.Toplevel):
    """ The class for displaying the main menu of continuous beam program
    """

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
        self.btn2 = ttk.Button(self.frame1, text="Input Load Data", style="Blue.TButton", width=30,
                command=self.open_load_data_window)
        self.btn3 = ttk.Button(self.frame1, text="Analysis", style="Blue.TButton", width=30,
                command=self.open_analysis_window)
        self.btn4 = ttk.Button(self.frame1, text="Exit", style="Blue.TButton", width=30,
                command=self.on_closing)
        """
        if is_direct_call:
            self.btn4 = ttk.Button(self.frame1, text="Exit", style="Blue.TButton", width=30,
                    command=self.on_closing)
        else:
            self.btn4 = ttk.Button(self.frame1, text="Return to Main Menu", style="Blue.TButton",
                    command=self.on_closing)
        """
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



class CB_direct(tk.Tk):
    """ The class to create the root window if this module is invoked
        directly from the command line.
    """

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

def main_gui():
    is_direct_call = True
    app = CB_direct()
    app.mainloop()


def main():
    is_direct_call = True
    app = CB_direct()
    app.mainloop()


if __name__ == '__main__':
    main()



