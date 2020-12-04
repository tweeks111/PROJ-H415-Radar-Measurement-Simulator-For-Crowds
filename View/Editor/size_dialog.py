import tkinter as tk


class SizeDialog(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.map_width      = tk.IntVar()
        self.map_width.set(20)
        self.map_height     = tk.IntVar()
        self.map_height.set(20)

        width_label         = tk.Label(self, text="Width [m] :")
        self.width_scale    = tk.Scale(self, from_=10, to=30, orient=tk.HORIZONTAL, variable=self.map_width)
        height_label        = tk.Label(self, text="Height [m] :")
        self.height_scale   = tk.Scale(self, from_=10, to=30, orient=tk.HORIZONTAL, variable=self.map_height)

        self.ok_button      = tk.Button(self, text="OK")

        width_label.grid(row=0, column=0)
        self.width_scale.grid(row=0, column=1)
        height_label.grid(row=1, column=0)
        self.height_scale.grid(row=1, column=1)
        self.ok_button.grid(row=2, columnspan=2)

    def getValues(self):
        return [self.width_scale.get(), self.height_scale.get()]
