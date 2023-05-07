import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import contibeam_main

def continuous_beam():
    root.iconify()
    is_main_over = None
    contibeam_main.main(root)
    # is_main_over = contibeam_main.main(root)
    # print(is_main_over)
    root.deiconify()
    root.destroy()

def plane_frame():
    pass   

def space_frame():
    pass   

def plane_truss():
    pass   

def space_truss():
    pass   

def general_FEM():
    pass   

root = tk.Tk()

root.title("StructInsight")
root.geometry("700x500+50+50")

mainframe = ttk.Frame(root) 
mainframe.grid(column=0, row=0, padx=5, pady=5)
#mainframe.pack(padx=20, pady=10, side="top", fill=tk.X, expand=True) 

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

my_style = ttk.Style()
my_style.configure('blue.TButton', font='helvetica 18', foreground='white', background='blue', padding=10)

btn1 = ttk.Button(mainframe, text="Continuous Beam", command=continuous_beam, padding=(10,5)) # internal padding, i.e. around the text
btn1.grid(row = 0, column = 0, sticky=tk.W+tk.E, pady=20) # padx and pady are external paddings, i.e. between button and frame
btn1['style'] = 'blue.TButton'

btn2 = ttk.Button(mainframe, text="Plane Frame", command=plane_frame, padding=(10,5))
btn2.state(['disabled'])
btn2.grid(row = 1, column = 0, sticky=(tk.W, tk.E), pady=20)
btn2['style'] = 'blue.TButton'

btn3 = ttk.Button(mainframe, text="Space Frame", command=space_frame, padding=(10,5))
btn3.state(['disabled'])
btn3.grid(row = 2, column = 0, sticky=(tk.W, tk.E), pady=20)
btn3['style'] = 'blue.TButton'

btn4 = ttk.Button(mainframe, text="Plane Truss", command=space_frame, padding=(10,5))
btn4.state(['disabled'])
btn4.grid(row = 3, column = 0, sticky=(tk.W, tk.E), pady=20)
btn4['style'] = 'blue.TButton'

btn5 = ttk.Button(mainframe, text="Space Truss", command=space_frame, padding=(10,5))
btn5.state(['disabled'])
btn5.grid(row = 4, column = 0, sticky=(tk.W, tk.E), pady=20)
btn5['style'] = 'blue.TButton'

btn6 = ttk.Button(mainframe, text="General FEM", command=space_frame, padding=(10,5))
btn6.state(['disabled'])
btn6.grid(row = 5, column = 0, sticky=(tk.W, tk.E), pady=20)
btn6['style'] = 'blue.TButton'

root.mainloop()


