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
        self.n_scale = tk.Scale(self.sim_frame, from_=16, to=128, orient=tk.HORIZONTAL, resolution=16, command=self.updateNScale)
        self.n_scale.grid(row=3, column=2)
        self.n_scale.set(64)
        tk.Label(self.sim_frame, text="Detection :").grid(row=4, column=0)
        self.combo_detect = tk.ttk.Combobox(self.sim_frame, state="readonly")
        self.combo_detect['values'] = ('Threshold', 'OS-CFAR', 'CA-CFAR')
        self.combo_detect.current(0)
        self.combo_detect.grid(row=4, column=2)
        self.combo_detect.bind("<<ComboboxSelected>>", self.changeDetectionMode)
        self.label_thresh = tk.Label(self.sim_frame, text="Detection\nThreshold :")
        self.label_thresh.grid(row=5, column=0)
        #self.label_CFAR = tk.Label(self.sim_frame, text="\u03B1 :")
        #self.label_CFAR.grid(row=5, column=0)
        #self.label_CFAR.grid_remove()
        self.detect_thresh = tk.Scale(self.sim_frame, orient=tk.HORIZONTAL, from_=-50, to=-150, resolution=10)
        self.detect_thresh.grid(row=5, column=2)
        self.detect_thresh.set(-90)
        #self.detect_CFAR = tk.Scale(self.sim_frame, orient=tk.HORIZONTAL, from_=0, to=3, resolution=0.1)
        #self.detect_CFAR.grid(row=5, column=2)
        #self.detect_CFAR.set(0.5)
        #self.detect_CFAR.grid_remove()
        self.proba_label = tk.Label(self.sim_frame, text="Pᶠᵃ [log10]:")
        self.proba_label.grid(row=6, column=0)
        self.proba_label.grid_remove()
        self.proba_scale = tk.Scale(self.sim_frame, orient=tk.HORIZONTAL, from_=-1, to=-10, resolution=1)
        self.proba_scale.grid(row=6, column=2)
        self.proba_scale.set(-9)
        self.proba_scale.grid_remove()
        self.NCFAR_label = tk.Label(self.sim_frame, text="Nᶜᶠᵃʳ :")
        self.NCFAR_label.grid(row=7, column=0)
        self.NCFAR_label.grid_remove()
        self.NCFAR_scale = tk.Scale(self.sim_frame, orient=tk.HORIZONTAL, from_=10, to=50, resolution=10)
        self.NCFAR_scale.grid(row=7, column=2)
        self.NCFAR_scale.set(40)
        self.NCFAR_scale.grid_remove()
        self.guard_label = tk.Label(self.sim_frame, text="Guard Cells :")
        self.guard_label.grid(row=8, column=0)
        self.guard_label.grid_remove()
        self.guard_scale = tk.Scale(self.sim_frame, orient=tk.HORIZONTAL, from_=0, to=6, resolution=2)
        self.guard_scale.grid(row=8, column=2)
        self.guard_scale.set(2)
        self.guard_scale.grid_remove()
        self.kCFAR_label = tk.Label(self.sim_frame, text="kᶜᶠᵃʳ :")
        self.kCFAR_label.grid(row=9, column=0)
        self.kCFAR_label.grid_remove()
        self.kCFAR_scale = tk.Scale(self.sim_frame, orient=tk.HORIZONTAL, from_=0, to=10, resolution=1)
        self.kCFAR_scale.grid(row=9, column=2)
        self.kCFAR_scale.set(4)
        self.kCFAR_scale.grid_remove()

        tk.Label(self.sim_frame, text="AoA\nThreshold :").grid(row=10, column=0)
        self.aoa_thresh = tk.Scale(self.sim_frame, orient=tk.HORIZONTAL, from_=0, to=-10, resolution=1)
        self.aoa_thresh.grid(row=10, column=2)
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

    def changeDetectionMode(self, event):
        event.widget.master.focus_set()
        if self.combo_detect.get() == "Threshold":
            #self.label_CFAR.grid_remove()
            #self.detect_CFAR.grid_remove()
            self.proba_label.grid_remove()
            self.proba_scale.grid_remove()
            self.NCFAR_label.grid_remove()
            self.NCFAR_scale.grid_remove()
            self.guard_label.grid_remove()
            self.guard_scale.grid_remove()
            self.kCFAR_label.grid_remove()
            self.kCFAR_scale.grid_remove()
            self.label_thresh.grid()
            self.detect_thresh.grid()

        elif self.combo_detect.get() == "OS-CFAR":
            self.label_thresh.grid_remove()
            self.detect_thresh.grid_remove()
            #self.label_CFAR.grid()
            #self.detect_CFAR.grid()
            self.guard_label.grid()
            self.guard_scale.grid()
            self.proba_label.grid()
            self.proba_scale.grid()
            self.NCFAR_label.grid()
            self.NCFAR_scale.grid()
            self.kCFAR_label.grid()
            self.kCFAR_scale.grid()
        else:
            self.label_thresh.grid_remove()
            self.detect_thresh.grid_remove()
            self.kCFAR_label.grid_remove()
            self.kCFAR_scale.grid_remove()
            self.guard_label.grid()
            self.guard_scale.grid()
            #self.label_CFAR.grid()
            #self.detect_CFAR.grid()
            self.proba_label.grid()
            self.proba_scale.grid()
            self.NCFAR_label.grid()
            self.NCFAR_scale.grid()

    def updateNScale(self, var):
        if int(var) == 16:
            self.NCFAR_scale.configure(from_=10, to=10)
            self.guard_scale.configure(from_=0, to=2)
        elif int(var) == 32:
            self.NCFAR_scale.configure(from_=10, to=20)
            self.guard_scale.configure(from_=0, to=6)
        elif int(var) == 48:
            self.NCFAR_scale.configure(from_=10, to=30)
            self.guard_scale.configure(from_=0, to=6)
        else:
            self.NCFAR_scale.configure(from_=10, to=50)
            self.guard_scale.configure(from_=0, to=6)
