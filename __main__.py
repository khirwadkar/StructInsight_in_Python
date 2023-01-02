#Starting point of the StructInsight software

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import tkinter.messagebox as messagebox
import contibeam_main



class StructInsight(tk.Tk):

    def __init__(self, *args, **kwargs):
        #tk.Tk.__init__(self, *args, **kwargs) # does same job as of the next statement.
        super().__init__(*args, **kwargs)
        self.geometry("800x600")
        self.title("StructInsight")
        # Tell the window to call this function when the close button is clicked
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        root_frame = ttk.Frame(self)
        root_frame.pack(side="top", fill="both", expand = True)
        root_frame.grid_rowconfigure(0, weight=1)
        root_frame.grid_columnconfigure(0, weight=1)

        """
        self.frames = {}

        for F in (MainMenuFrame, contibeam_main.CB_MenuFrame):

            frame = F(root_frame, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenuFrame)
        """
        self.frame1 = MainMenuFrame(root_frame, self)
        self.frame2 = contibeam_main.CB_MenuFrame(root_frame, self)

        self.show_frame(self.frame1)

    def show_frame(self, current_frame):
        #frame = self.frames[current_frame]
        frame = current_frame
        frame.tkraise()

    # Define the function to be called when the window is closed
    def on_closing(self):
        if messagebox.askquestion("Confirm", "Do you really want to exit the application?") == "yes":
            self.destroy()


class MainMenuFrame(ttk.Frame):

    def __init__(self, parent_frame, root_win):
        #ttk.Frame.__init__(self, parent_frame)
        super().__init__(parent_frame)
        #super().__init__(parent_frame, width=600)
        #self.grid(row=0, column=0, sticky="nsew") # This is repeatition; same step in __init__ of StructInsight class
        self.grid(row=0, column=0, sticky="nsew") 
        #self.pack(side="top", padx=10, pady=10)

        self.root_win = root_win

        self.init_widgets()

        # Configure the ttk frame to fill the main window and center the column of buttons
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def init_widgets(self):
        label1 = ttk.Label(self, text="Analysis of Structures", font='helvetica 24 bold', foreground='blue')
        label1.grid(row=0, column=0, pady=20)    # , sticky="ew")

        # Create a ttk style with a blue background and white foreground
        my_style = ttk.Style()
        my_style.configure('Blue.TButton', font='helvetica 18', foreground='white', background='blue')

        # Create the ttk buttons
        #button1 = ttk.Button(self, text="Button 1", style="Blue.TButton", width=30,
        btn1 = ttk.Button(self, text="Continuous Beam", style="Blue.TButton", command=lambda: self.root_win.show_frame(self.root_win.frame2))
        btn2 = ttk.Button(self, text="Plane Frame", style="Blue.TButton", width=30)
        btn3 = ttk.Button(self, text="Space Frame", style="Blue.TButton", width=30)
        btn4 = ttk.Button(self, text="Plane Truss", style="Blue.TButton", width=30)
        btn5 = ttk.Button(self, text="Space Truss", style="Blue.TButton", width=30)
        btn6 = ttk.Button(self, text="General FEM", style="Blue.TButton", width=30)

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


# Place holder class during initial phase of development;
# no longer necessary, may be deleted.
class PageOne(ttk.Frame):

    def __init__(self, parent_frame, root_win):
        ttk.Frame.__init__(self, parent_frame)
        #super(parent_frame)
        #super.__init__(self, parent_frame, width=600)
        self.grid(row=0, column=0, sticky="nsew")
        #self.pack(side="top", padx=10, pady=10)

        LARGE_FONT= ("Verdana", 12)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: root_win.show_frame(MainMenuFrame))
        button1.pack()






# Create an instance of the StructInsight class, i.e. the main window
app = StructInsight()

# Run the main loop
app.mainloop()



