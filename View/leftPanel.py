import tkinter as tk


class LeftPanel(tk.Frame):
    """
    Configuration Panel
    """
    # Constructor
    def __init__(self, root):
        # Inheritance
        tk.Frame.__init__(self, root)
        self.pack(side=tk.LEFT, fill=tk.BOTH)

        # Variables
        self.clusters_on = tk.BooleanVar()
        self.clusters_on.set(False)
        self.points_txt = tk.StringVar()

        # Left Frame Components
        self.width_slider = tk.Scale(self, orient=tk.HORIZONTAL)
        self.height_slider = tk.Scale(self, orient=tk.HORIZONTAL)
        self.lambda_slider = tk.Scale(self, orient=tk.HORIZONTAL)
        self.clusters_check = tk.Checkbutton(self, text="Random clusters", var=self.clusters_on)
        self.start_btn = tk.Button(self, text="Start \u25B6")

        # Components Packing
        tk.Label(self, text="Width :").grid(row=0, column=0)
        self.width_slider.grid(row=0, column=1)
        tk.Label(self, text="Height :").grid(row=1, column=0)
        self.height_slider.grid(row=1, column=1)
        tk.Label(self, text="\u03BB :").grid(row=2, column=0)
        self.lambda_slider.grid(row=2, column=1)
        self.clusters_check.grid(row=3, columnspan=2)
        self.start_btn.grid(row=4, columnspan=2)
        self.points_label = tk.Label(self, textvariable=self.points_txt)

    def blockSliders(self, *args):
        if args[0]:
            self.width_slider.configure(state=tk.DISABLED)
            self.height_slider.configure(state=tk.DISABLED)
            self.lambda_slider.configure(state=tk.DISABLED)
            self.clusters_check.configure(state=tk.DISABLED)
            self.start_btn.configure(text="Stop \u25A0")

            self.points_txt.set(str(args[1])+" points")
            self.points_label.grid(row=5, columnspan=2)
        else:
            self.width_slider.configure(state=tk.ACTIVE)
            self.height_slider.configure(state=tk.ACTIVE)
            self.lambda_slider.configure(state=tk.ACTIVE)
            self.clusters_check.configure(state=tk.ACTIVE)
            self.start_btn.configure(text="Start \u25B6")

            self.points_label.grid_forget()

    # Get Functions
    def getClustersCheck(self):
        return self.clusters_on.get()
