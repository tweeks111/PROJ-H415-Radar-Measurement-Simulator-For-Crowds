import tkinter as tk
from tkinter.ttk import Progressbar


class RightPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.map_dim = [0, 0]
        self.param_frame = tk.LabelFrame(self, text="Parameters")
        self.param_frame.configure(padx=5, pady=5)
        self.param_frame.pack(fill=tk.X)
        tk.Label(self.param_frame, text="M :").grid(row=2, column=0, sticky='sw')
        self.m_scale = tk.Scale(self.param_frame, from_=16, to=128, orient=tk.HORIZONTAL, resolution=16)
        self.m_scale.grid(row=2, column=2, sticky='nsew', columnspan=2)
        self.m_scale.set(64)
        tk.Label(self.param_frame, text="N :").grid(row=3, column=0, sticky='sw')
        self.n_scale = tk.Scale(self.param_frame, from_=16, to=128, orient=tk.HORIZONTAL, resolution=16)
        self.n_scale.grid(row=3, column=2, sticky='nsew')
        self.n_scale.set(64)
        tk.Label(self.param_frame, text="Detection :").grid(row=4, column=0, sticky='sw')
        self.combo_detect = tk.ttk.Combobox(self.param_frame, state="readonly")
        self.combo_detect['values'] = ('Peak Detection', 'OS-CFAR', 'CA-CFAR')
        self.combo_detect.current(0)
        self.combo_detect.grid(row=4, column=2, sticky='nsew')
        self.combo_detect.bind("<<ComboboxSelected>>", self.changeDetectionMode)
        self.label_thresh = tk.Label(self.param_frame, text="Detection\nThreshold :")
        self.label_thresh.grid(row=5, column=0, sticky='sw')
        # self.label_CFAR = tk.Label(self.sim_frame, text="\u03B1 :")
        # self.label_CFAR.grid(row=5, column=0)
        # self.label_CFAR.grid_remove()
        self.detect_thresh = tk.Scale(self.param_frame, orient=tk.HORIZONTAL, from_=-50, to=-150, resolution=10)
        self.detect_thresh.grid(row=5, column=2, sticky='nsew')
        self.detect_thresh.set(-90)
        # self.detect_CFAR = tk.Scale(self.sim_frame, orient=tk.HORIZONTAL, from_=0, to=3, resolution=0.1)
        # self.detect_CFAR.grid(row=5, column=2)
        # self.detect_CFAR.set(0.5)
        # self.detect_CFAR.grid_remove()
        self.proba_label = tk.Label(self.param_frame, text="Pᶠᵃ [log10]:")
        self.proba_label.grid(row=6, column=0, sticky='sw')
        self.proba_label.grid_remove()
        self.proba_scale = tk.Scale(self.param_frame, orient=tk.HORIZONTAL, from_=-1, to=-10, resolution=1)
        self.proba_scale.grid(row=6, column=2, sticky='nsew')
        self.proba_scale.set(-9)
        self.proba_scale.grid_remove()
        self.NCFAR_label = tk.Label(self.param_frame, text="Nᶜᶠᵃʳ :")
        self.NCFAR_label.grid(row=7, column=0, sticky='sw')
        self.NCFAR_label.grid_remove()
        self.NCFAR_scale = tk.Scale(self.param_frame, orient=tk.HORIZONTAL, from_=10, to=50, resolution=10)
        self.NCFAR_scale.grid(row=7, column=2, sticky='nsew')
        self.NCFAR_scale.set(40)
        self.NCFAR_scale.grid_remove()
        self.guard_label = tk.Label(self.param_frame, text="Guard Cells :")
        self.guard_label.grid(row=8, column=0, sticky='sw')
        self.guard_label.grid_remove()
        self.guard_scale = tk.Scale(self.param_frame, orient=tk.HORIZONTAL, from_=0, to=6, resolution=2)
        self.guard_scale.grid(row=8, column=2, sticky='nsew')
        self.guard_scale.set(2)
        self.guard_scale.grid_remove()
        self.kCFAR_label = tk.Label(self.param_frame, text="kᶜᶠᵃʳ :")
        self.kCFAR_label.grid(row=9, column=0, sticky='sw')
        self.kCFAR_label.grid_remove()
        self.kCFAR_scale = tk.Scale(self.param_frame, orient=tk.HORIZONTAL, from_=0, to=10, resolution=1)
        self.kCFAR_scale.grid(row=9, column=2, sticky='nsew')
        self.kCFAR_scale.set(4)
        self.kCFAR_scale.grid_remove()

        tk.Label(self.param_frame, text="AoA\nThreshold :").grid(row=10, column=0, sticky='sw')
        self.aoa_thresh = tk.Scale(self.param_frame, orient=tk.HORIZONTAL, from_=0, to=-10, resolution=1)
        self.aoa_thresh.grid(row=10, column=2, sticky='nsew')
        self.aoa_thresh.set(-6)

        self.sim_frame = tk.LabelFrame(self, text="Simulation")
        self.sim_frame.configure(padx=5, pady=5)
        self.sim_frame.pack(fill=tk.X)
        tk.Label(self.sim_frame, text="Duration [s]:").grid(row=0, column=0, sticky='sw')
        self.time_scale = tk.Scale(self.sim_frame, from_=1, to=20, orient=tk.HORIZONTAL, resolution=1)
        self.time_scale.grid(row=0, column=2, sticky='nsew')
        self.time_scale.set(10)

        tk.Label(self.sim_frame, text="RDM Freq. [Hz]:").grid(row=1, column=0, sticky='sw')
        self.rdm_scale = tk.Scale(self.sim_frame, from_=1, to=4, orient=tk.HORIZONTAL, resolution=1)
        self.rdm_scale.grid(row=1, column=2, sticky='nsew')
        self.rdm_scale.set(2)

        self.run_btn = tk.Button(self.sim_frame, text="Run Simulation")
        self.run_btn['state'] = 'disabled'
        self.run_btn.grid(row=2, column=2, columnspan=3)

        self.analysis_frame = tk.LabelFrame(self, text="Analysis")
        self.analysis_frame.configure(padx=5, pady=5)
        self.analysis_frame.pack(fill=tk.Y)

        yScroll = tk.Scrollbar(self.analysis_frame, orient=tk.VERTICAL)

        self.param_listbox = tk.Listbox(self.analysis_frame, yscrollcommand=yScroll.set, activestyle='none',
                                        exportselection=False, height=5)
        self.param_listbox.grid(row=1, column=0, columnspan=2, sticky='nsew')
        yScroll.grid(row=1, column=2, sticky='ns')
        yScroll.config(command=self.param_listbox.yview)

        self.add_btn = tk.Button(self.analysis_frame, text="Add")
        self.add_btn.grid(row=2, column=2)
        self.remove_btn = tk.Button(self.analysis_frame, text="Remove")
        self.remove_btn['state'] = 'disabled'
        self.remove_btn.grid(row=2, column=1, sticky='e')

        tk.Label(self.analysis_frame, text="Nb. of iteration for\neach parameter :").grid(row=3, column=0, sticky='sw')
        self.run_scale = tk.Scale(self.analysis_frame, from_=10, to=100, orient=tk.HORIZONTAL, resolution=10)
        self.run_scale.grid(row=3, column=1, sticky='nsew')
        self.run_scale.set(50)

        self.analysis_btn = tk.Button(self.analysis_frame, text="Run Analysis")
        self.analysis_btn['state'] = 'disabled'
        self.analysis_btn.grid(row=4, column=0, columnspan=2)

        self.progress_bar = Progressbar(self, orient=tk.HORIZONTAL, mode='determinate')
        self.progress_bar.pack(fill=tk.X)

    def setMapDim(self, map_dim):
        self.map_dim = map_dim

    def bar(self, value):
        self.progress_bar['value'] = round(100 * value / self.time_scale.get())
        self.progress_bar.update_idletasks()

    def barAnalysis(self, value):
        self.progress_bar['value'] = round(100 * value / self.run_scale.get())
        self.progress_bar.update_idletasks()

    def addParam(self, param):

        if param[2] == "Peak Detection":
            self.param_listbox.insert('end', str(param[2]) + " "+   # Detection
                                      str(param[0]) + "|" +         # N
                                      str(param[1]) + "|" +         # M
                                      str(param[3]) + "|" +         # Threshold
                                      str(param[4]))                # AoA
        elif param[2] == "OS-CFAR":
            self.param_listbox.insert('end', str(param[2]) + " " +  # Detection
                                      str(param[0]) + "|" +         # N
                                      str(param[1]) + "|" +         # M
                                      str(param[3]) + "|" +         # Pfa
                                      str(param[4]) + "|" +         # Ncfar
                                      str(param[5]) + "|" +         # Guard cells
                                      str(param[6]) + "|" +         # kcfar
                                      str(param[7]))                # AoA
        else:
            self.param_listbox.insert('end', str(param[2]) + " " +  # Detection
                                      str(param[0]) + "|" +         # N
                                      str(param[1]) + "|" +         # M
                                      str(param[3]) + "|" +         # Pfa
                                      str(param[4]) + "|" +         # Ncfar
                                      str(param[5]) + "|" +         # Guard cells
                                      str(param[6]))                # AoA

        self.param_listbox.select_clear(0, 'end')
        self.param_listbox.select_set('end')
        self.param_listbox.event_generate("<<ListboxSelect>>")

    def removeParam(self, index):

        self.param_listbox.delete(index)
        self.param_listbox.select_clear(0, 'end')
        self.param_listbox.select_set('end')

        if not self.param_listbox.curselection():
            self.remove_btn['state'] = "disabled"


    def changeDetectionMode(self, event):
        event.widget.master.focus_set()
        if self.combo_detect.get() == "Peak Detection":
            # self.label_CFAR.grid_remove()
            # self.detect_CFAR.grid_remove()
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
            # self.label_CFAR.grid()
            # self.detect_CFAR.grid()
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
            # self.label_CFAR.grid()
            # self.detect_CFAR.grid()
            self.proba_label.grid()
            self.proba_scale.grid()
            self.NCFAR_label.grid()
            self.NCFAR_scale.grid()

    def updateNScale(self, N):
        if N == 16:
            self.NCFAR_scale.configure(from_=10, to=10)
            self.guard_scale.configure(from_=0, to=2)
        elif N == 32:
            self.NCFAR_scale.configure(from_=10, to=20)
            self.guard_scale.configure(from_=0, to=6)
        elif N == 48:
            self.NCFAR_scale.configure(from_=10, to=30)
            self.guard_scale.configure(from_=0, to=6)
        else:
            self.NCFAR_scale.configure(from_=10, to=50)
            self.guard_scale.configure(from_=0, to=6)
