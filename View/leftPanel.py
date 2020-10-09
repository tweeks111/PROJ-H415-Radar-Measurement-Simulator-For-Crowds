import tkinter as tk


class LeftPanel(tk.Frame):
    """
    Configuration Panel
    """
    # Constructor
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.pack(side=tk.LEFT, fill=tk.BOTH)

        # Left Frame Components
        self.width_slider = tk.Scale(self, orient=tk.HORIZONTAL)
        self.height_slider = tk.Scale(self, orient=tk.HORIZONTAL)
        self.lambda_slider = tk.Scale(self, orient=tk.HORIZONTAL)
        self.start_btn = tk.Button(self, text="Start \u25B6")

        # Components Packing
        tk.Label(self, text="Width :").grid(row=0, column=0)#pack(side="top", fill=tk.BOTH)
        self.width_slider.grid(row=0, column=1)#pack(side="top", fill=tk.BOTH)
        tk.Label(self, text="Height :").grid(row=1, column=0)#pack(side="top", fill=tk.BOTH)
        self.height_slider.grid(row=1, column=1)#pack(side="top", fill=tk.BOTH)
        tk.Label(self, text="\u03BB :").grid(row=2, column=0)
        self.lambda_slider.grid(row=2, column=1)
        self.start_btn.grid(row=3, columnspan=2)#pack(side="top", fill=tk.BOTH)

    def blockSliders(self, is_running):
        if is_running:
            self.width_slider.configure(state=tk.DISABLED, )
            self.height_slider.configure(state=tk.DISABLED)
            self.lambda_slider.configure(state=tk.DISABLED)
            self.start_btn.configure(text="Stop \u25A0")
        else:
            self.width_slider.configure(state=tk.ACTIVE)
            self.height_slider.configure(state=tk.ACTIVE)
            self.lambda_slider.configure(state=tk.ACTIVE)
            self.start_btn.configure(text="Start \u25B6")
