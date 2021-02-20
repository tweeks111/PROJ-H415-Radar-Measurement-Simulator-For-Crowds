import tkinter as tk
from tkinter.ttk import Progressbar


class RightPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.map_dim = [0, 0]

        self.sim_frame = tk.LabelFrame(self, text="Simulation")
        self.sim_frame.configure(padx=5, pady=5)
        self.sim_frame.pack(fill=tk.X)
        tk.Label(self.sim_frame, text="Duration :\n[s]").grid(row=0, column=0)
        self.time_scale = tk.Scale(self.sim_frame, from_=1, to=20, orient=tk.HORIZONTAL, resolution=1)
        self.time_scale.grid(row=0, column=2)
        self.time_scale.set(10)
        tk.Label(self.sim_frame, text="RDM Freq. :\n[Hz]").grid(row=1, column=0)
        self.rdm_scale = tk.Scale(self.sim_frame, from_=1, to=4, orient=tk.HORIZONTAL, resolution=1)
        self.rdm_scale.grid(row=1, column=2)
        self.rdm_scale.set(2)
        tk.Label(self.sim_frame, text="M :").grid(row=2, column=0)
        self.m_scale = tk.Scale(self.sim_frame, from_=16, to=128, orient=tk.HORIZONTAL, resolution=16)
        self.m_scale.grid(row=2, column=2)
        self.m_scale.set(64)
        tk.Label(self.sim_frame, text="N :").grid(row=3, column=0)
        self.n_scale = tk.Scale(self.sim_frame, from_=16, to=128, orient=tk.HORIZONTAL, resolution=16)
        self.n_scale.grid(row=3, column=2)
        self.n_scale.set(64)
        tk.Label(self.sim_frame, text="Detection\nThreshold :").grid(row=4, column=0)
        self.detect_thresh = tk.Scale(self.sim_frame, orient=tk.HORIZONTAL, from_=-50, to=-150, resolution=10)
        self.detect_thresh.grid(row=4, column=2)
        self.detect_thresh.set(-90)
        tk.Label(self.sim_frame, text="AoA\nThreshold :").grid(row=5, column=0)
        self.aoa_thresh = tk.Scale(self.sim_frame, orient=tk.HORIZONTAL, from_=0, to=-10, resolution=1)
        self.aoa_thresh.grid(row=5, column=2)
        self.aoa_thresh.set(-6)

        self.progress_bar = Progressbar(self, orient=tk.HORIZONTAL, mode='determinate')
        self.progress_bar.pack(fill=tk.X)
        self.run_btn = tk.Button(self, text="Run Simulation")
        self.run_btn['state'] = 'disabled'
        self.run_btn.pack(fill=tk.X)

        self.analysis_frame = tk.LabelFrame(self, text="Analysis")
        self.analysis_frame.configure(padx=5, pady=5)
        self.analysis_frame.pack(fill=tk.BOTH)

        tk.Label(self.analysis_frame, text="Iteration Nb :").grid(row=0, column=0)
        self.run_scale = tk.Scale(self.analysis_frame, from_=10, to=100, orient=tk.HORIZONTAL, resolution=10)
        self.run_scale.grid(row=0, column=1)
        self.run_scale.set(50)

        self.analysis_btn = tk.Button(self.analysis_frame, text="Run Analysis")
        self.analysis_btn['state'] = 'disabled'
        self.analysis_btn.grid(row=1, column=0, columnspan=2)

    def setMapDim(self, map_dim):
        self.map_dim = map_dim

    def bar(self, value):
        self.progress_bar['value'] = round(100*value/self.time_scale.get())
        self.update_idletasks()
