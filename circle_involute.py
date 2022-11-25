"""
Python program for the calculation of a circular involute,
using mpyplot and tkinter.
"""

import tkinter as tk
from math import sin, cos, sqrt, pi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VarEntry:
    def __init__(self, frame_master:tk.Frame, label_string:str, 
                row_number:int, validation_command):
        """Generates instances of a tk.entry field in a freely selectable frame, 
        with freely selectable label and freely selectable row number

        Args:
            frame_master (tk.Frame): Name of the master frame in which the entry field should be located.
            label_string (str): The displayed name that should appear in front of the entry field.
            row_number (int): The number of the row in which the widget should be located (starting from 0).
            validation_command (_type_): Name of the validation function
        """
        self.label = tk.Label(frame_master, text=label_string)
        self.label.grid(row=row_number, column=0, padx=5, pady=5, sticky='w')
        self.entry = tk.Entry(
            frame_master,
            validate='all',
            validatecommand=(validation_command, "%P")
            )
        self.entry.grid(row=row_number, column=1, padx=5, pady=5, sticky='w')
        

class Involute(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.geometry('800x500')
        self.title('Involute Creator')
        self.resizable(False, False)
        self.vfloat = (self.register(self.validate_float))
        self.vint = (self.register(self.validate_int))
        #
        self.X = []
        self.Y = []
        self.t_of_n = []
        self.r = 1
        # UI
        self._ui()
        

    def _ui(self):
        master = tk.Frame(self)
        master.pack(fill=tk.BOTH)
        
        name_label = tk.Label(master, text='Circle Involute Creator')
        name_label.grid(padx=5, pady=5, row=0, column=0, sticky='nw')
        
        var_frame = tk. LabelFrame(master, text='Variables')
        var_frame.grid(padx=5, pady=5, row=1, column=0, sticky='nw')
        
        changeable_float_vars = ['radius', 'radial distance']
        entrys = [VarEntry(var_frame, var, i, self.vfloat)
                        for i, var in enumerate(changeable_float_vars)]
        col, row = var_frame.grid_size()
        entrys.append(VarEntry(var_frame, 'number of points', row, self.vint))

        col, row = var_frame.grid_size()
        calc_button = tk.Button(var_frame, text="Calculate & Draw", command=lambda: self.calc_draw(entrys, master))
        calc_button.grid(row=row, column=0, columnspan=col, sticky='e', padx=5, pady=5)
        
        self.draw(master)

    def validate_float(self, input):
        if (all(char in "0123456789.-" for char in input) and 
            "-" not in input[1:] 
            and input.count(".") <= 1):
            return True
        else: 
            return False


    def validate_int(self, input):
        if input.isdecimal() or input == "":
            return True
        else:
            return False

    def calc_draw(self, entrys, master:tk.Frame):
        try:
            n = int(entrys[-1].entry.get())
            a = float(entrys[1].entry.get())
            self.r = float(entrys[0].entry.get())
            self.t_of_n = self.calc_t_of_n(n, a)
            self.X = self.calc_xy(self.r, self.t_of_n, type='x')
            self.Y = self.calc_xy(self.r, self.t_of_n, type='y')
            self.draw(master)

        except ValueError:
            pass

    def calc_t_of_n(self, point_number:int, a: float):
        return [sqrt(4*pi*n*a) for n in range(1, point_number+1)]

    def calc_xy(self, r:float, t_of_n:list, **kwargs):
        if kwargs['type'] == 'x':
            return [r * cos(t) + t * r * sin(t)
                    for t in t_of_n]
        if  kwargs['type'] == 'y':
            return [r * sin(t) - t * r * cos(t)
                    for t in t_of_n]

    def draw(self, master):
        fig, ax = plt.subplots()
        circle = plt.Circle((0,0), self.r, color='r', fill=False)
        ax.add_patch(circle)
        ax.plot(self.X, self.Y, '-o')
        ax.grid(True, which='both')
        ax.set_aspect('equal')
        ax.axhline(y=0, color='k')
        ax.axvline(x=0, color='k')
        graph = FigureCanvasTkAgg(fig, master)
        graph.get_tk_widget().grid(padx=5, pady=5, row=0, rowspan=2, column=1, columnspan=3)

def main():
    circle_i = Involute()
    circle_i.mainloop()

if __name__ == '__main__':
    main()