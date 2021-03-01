import tkinter as tk
import View.Analysis
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class Window(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.resizable(False, False)
        self.title("Analysis")

        style = ttk.Style()
        style.configure("mystyle.Treeview", background='white')
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 10, 'bold'), background='lightgray')

        self.thresh_label_frame = tk.LabelFrame(self, text="Threshold :")
        self.thresh_label_frame.grid(row=1, column=0)
        yScroll_1 = tk.Scrollbar(self.thresh_label_frame, orient=tk.VERTICAL)
        self.thresh_tree = ttk.Treeview(self.thresh_label_frame, selectmode='extended', yscrollcommand=yScroll_1.set, style="mystyle.Treeview")
        yScroll_1.config(command=self.thresh_tree.yview)

        self.OSCFAR_label_frame = tk.LabelFrame(self, text="OS-CFAR :")
        self.OSCFAR_label_frame.grid(row=1, column=1)
        yScroll_2 = tk.Scrollbar(self.OSCFAR_label_frame, orient=tk.VERTICAL)
        self.OSCFAR_tree = ttk.Treeview(self.OSCFAR_label_frame, selectmode='extended', yscrollcommand=yScroll_2.set, style="mystyle.Treeview")
        yScroll_2.config(command=self.OSCFAR_tree.yview)

        self.CACFAR_label_frame = tk.LabelFrame(self, text="CA-CFAR :")
        self.CACFAR_label_frame.grid(row=1, column=2)
        yScroll_3 = tk.Scrollbar(self.CACFAR_label_frame, orient=tk.VERTICAL)
        self.CACFAR_tree = ttk.Treeview(self.CACFAR_label_frame, selectmode='extended', yscrollcommand=yScroll_3.set, style="mystyle.Treeview")
        yScroll_3.config(command=self.CACFAR_tree.yview)

        self.configureTrees()

        self.thresh_tree.grid(row=0, column=0, columnspan=2)
        yScroll_1.grid(row=0, column=2, sticky='ns')
        self.OSCFAR_tree.grid(row=0, column=0, columnspan=2)
        yScroll_2.grid(row=0, column=2, sticky='ns')
        self.CACFAR_tree.grid(row=0, column=0, columnspan=2)
        yScroll_3.grid(row=0, column=2, sticky='ns')

        self.combo_thresh = tk.ttk.Combobox(self.thresh_label_frame, state="readonly")
        self.combo_thresh['values'] = ('Peak Detection', 'AoA Threshold')
        self.combo_thresh.current(0)
        self.combo_thresh_param = tk.ttk.Combobox(self.thresh_label_frame, state="readonly")
        self.combo_thresh_param['values'] = ('', 'N, M', 'AoA Threshold')
        self.combo_thresh.current(0)
        self.combo_thresh.bind('<<ComboboxSelected>>', self.changeThreshGroup)
        self.combo_thresh.grid(row=1, column=0, sticky='nsew')
        self.combo_thresh_param.grid(row=2, column=0, sticky='nsew')

        self.plot_thresh_btn = tk.Button(self.thresh_label_frame, text="Plot", command=self.plotThresh)
        self.plot_thresh_btn.grid(row=1, column=1, columnspan=2, sticky='nsew')

        self.combo_OSCFAR = tk.ttk.Combobox(self.OSCFAR_label_frame, state="readonly")
        self.combo_OSCFAR['values'] = ('Pfa', 'Ncfar', 'Kcfar')
        self.combo_OSCFAR.current(0)
        self.combo_OSCFAR.grid(row=1, column=0, sticky='nsew')
        self.plot_OSCFAR_btn = tk.Button(self.OSCFAR_label_frame, text="Plot", command=self.plotOSCFAR)
        self.plot_OSCFAR_btn.grid(row=1, column=1, columnspan=2, sticky='nsew')

        self.combo_CACFAR = tk.ttk.Combobox(self.CACFAR_label_frame, state="readonly")
        self.combo_CACFAR['values'] = ('Pfa', 'Ncfar')
        self.combo_CACFAR.current(0)
        self.combo_CACFAR.grid(row=1, column=0, sticky='nsew')
        self.plot_CACFAR_btn = tk.Button(self.CACFAR_label_frame, text="Plot", command=self.plotCACFAR)
        self.plot_CACFAR_btn.grid(row=1, column=1, columnspan=2, sticky='nsew')

    def setTrees(self, index_param, est):
        self.thresh_label_frame.grid()
        self.CACFAR_label_frame.grid()
        self.OSCFAR_label_frame.grid()
        count = [0, 0, 0]
        for i in range(len(index_param)):
            for j in range(len(index_param[i])):
                if index_param[i][j][2] == "Peak Detection":
                    self.thresh_tree.insert(parent='', index='end', values=(index_param[i][j][0], index_param[i][j][1], index_param[i][j][3], index_param[i][j][4], est[i+j]))
                    count[0] = count[0] + 1
                elif index_param[i][j][2] == "OS-CFAR":
                    self.OSCFAR_tree.insert(parent='', index='end',  values=(index_param[i][j][0], index_param[i][j][1], index_param[i][j][3], index_param[i][j][4], index_param[i][j][5], index_param[i][j][6], index_param[i][j][7], est[i+j]))
                    count[1] = count[1] + 1
                else:
                    self.CACFAR_tree.insert(parent='', index='end', values=(index_param[i][j][0], index_param[i][j][1], index_param[i][j][3], index_param[i][j][4], index_param[i][j][5], index_param[i][j][6], est[i+j]))
                    count[2] = count[2] + 1
        if count[0] == 0:
            self.thresh_label_frame.grid_remove()
        if count[1] == 0:
            self.OSCFAR_label_frame.grid_remove()
        if count[2] == 0:
            self.CACFAR_label_frame.grid_remove()

    def configureTrees(self):
        # Threshold :
        self.thresh_tree['columns'] = ('N', 'M', 'thresh', 'AoA', 'est')
        self.thresh_tree['show'] = 'headings'
        self.thresh_tree['height'] = 7
        self.thresh_tree['selectmode'] = None
        self.thresh_tree.column('N', width=30, anchor='c')
        self.thresh_tree.column('M', width=30, anchor='c')
        self.thresh_tree.column('thresh', width=90, anchor='c')
        self.thresh_tree.column('AoA', width=90, anchor='c')
        self.thresh_tree.column('est', width=90, anchor='c')

        self.thresh_tree.heading("N", text="N")
        self.thresh_tree.heading("M", text="M")
        self.thresh_tree.heading("thresh", text="RDM Threshold")
        self.thresh_tree.heading("AoA", text="AoA Threshold")
        self.thresh_tree.heading('est', text="Detect. Ratio")

        # OS-CFAR
        self.OSCFAR_tree['columns'] = ('N', 'M', 'Pfa', 'Ncfar', 'Guard Cells', 'kcfar', 'AoA', 'est')
        self.OSCFAR_tree['show'] = 'headings'
        self.OSCFAR_tree['height'] = 7
        self.OSCFAR_tree['selectmode'] = None
        self.OSCFAR_tree.column('N', width=30, anchor='c')
        self.OSCFAR_tree.column('M', width=30, anchor='c')
        self.OSCFAR_tree.column('Pfa', width=30, anchor='c')
        self.OSCFAR_tree.column('Ncfar', width=40, anchor='c')
        self.OSCFAR_tree.column('Guard Cells', width=40, anchor='c')
        self.OSCFAR_tree.column('kcfar', width=40, anchor='c')
        self.OSCFAR_tree.column('AoA', width=90, anchor='c')
        self.OSCFAR_tree.column('est', width=90, anchor='c')

        self.OSCFAR_tree.heading('N', text='N')
        self.OSCFAR_tree.heading('M', text='M')
        self.OSCFAR_tree.heading('Pfa', text='Pfa')
        self.OSCFAR_tree.heading('Ncfar', text='Ncfar')
        self.OSCFAR_tree.heading('Guard Cells', text='Guard')
        self.OSCFAR_tree.heading('kcfar', text='Kcfar')
        self.OSCFAR_tree.heading('AoA', text='AoA Threshold')
        self.OSCFAR_tree.heading('est', text='Detect. Ratio')

        # CA-CFAR
        self.CACFAR_tree['columns'] = ('N', 'M', 'Pfa', 'Ncfar', 'Guard Cells', 'AoA', 'est')
        self.CACFAR_tree['show'] = 'headings'
        self.CACFAR_tree['height'] = 7
        self.CACFAR_tree['selectmode'] = None
        self.CACFAR_tree.column('N', width=30, anchor='c')
        self.CACFAR_tree.column('M', width=30, anchor='c')
        self.CACFAR_tree.column('Pfa', width=30, anchor='c')
        self.CACFAR_tree.column('Ncfar', width=40, anchor='c')
        self.CACFAR_tree.column('Guard Cells', width=40, anchor='c')
        self.CACFAR_tree.column('AoA', width=90, anchor='c')
        self.CACFAR_tree.column('est', width=90, anchor='c')

        self.CACFAR_tree.heading('N', text='N')
        self.CACFAR_tree.heading('M', text='M')
        self.CACFAR_tree.heading('Pfa', text='Pfa')
        self.CACFAR_tree.heading('Ncfar', text='Ncfar')
        self.CACFAR_tree.heading('Guard Cells', text='Guard')
        self.CACFAR_tree.heading('AoA', text='AoA Threshold')
        self.CACFAR_tree.heading('est', text='Detect. Ratio')

    def clearAnalysis(self):
        self.thresh_tree.delete(*self.thresh_tree.get_children())
        self.CACFAR_tree.delete(*self.CACFAR_tree.get_children())
        self.OSCFAR_tree.delete(*self.OSCFAR_tree.get_children())

    def plotThresh(self):
        plot_type = self.combo_thresh.get()
        param_type = self.combo_thresh_param.get()
        plot_window = tk.Toplevel(self)
        plot_window.resizable(False, False)
        fig = Figure(figsize=(5, 5))
        a = fig.add_subplot(111)
        fig.subplots_adjust(wspace=0.5)
        a.set_ylabel('Detection Ratio')
        data = self.getAllData(self.thresh_tree)

        if plot_type == "Peak Detection":
            plot_window.title("Detect. Ratio - RDM Threshold [dB]")
            a.set_xlabel('Peak Detection')
            if param_type == '':
                thresh = self.getColumn(self.thresh_tree, 2)
                est = self.getColumn(self.thresh_tree, 4)
                sort_idx = np.argsort(thresh)
                thresh = thresh[sort_idx]
                est = est[sort_idx]
                a.plot(thresh, est)
            elif param_type == 'N, M':
                list_of_NM = ['16', '32', '48', '64', '80', '96', '112', '128']
                group_list = []
                for N in list_of_NM:
                    for M in list_of_NM:
                        group_list.append([item for item in data if (item['N'] == N and item['M'] == M)])
                group_list = [i for i in group_list if i != []]

                for elem in group_list:
                    N = elem[0]['N']
                    M = elem[0]['M']
                    est = np.array([float(item['est']) for item in elem])
                    thresh = np.array([float(item['thresh']) for item in elem])
                    sort_idx = np.argsort(thresh)
                    thresh = thresh[sort_idx]
                    est = est[sort_idx]
                    a.plot(thresh, est, label="N = "+N+" M = "+M)
                a.legend(loc="upper right")

            elif param_type == 'AoA Threshold':
                list_of_AoA = np.arange(-10, 1, 1)
                group_list = []
                for AoA in list_of_AoA:
                        group_list.append([item for item in data if (int(item['AoA']) == AoA)])
                group_list = [i for i in group_list if i != []]

                for elem in group_list:
                    AoA = elem[0]['AoA']
                    est = np.array([float(item['est']) for item in elem])
                    thresh = np.array([float(item['thresh']) for item in elem])
                    sort_idx = np.argsort(thresh)
                    thresh = thresh[sort_idx]
                    est = est[sort_idx]
                    a.plot(thresh, est, label="AoA Tresh. = " + AoA)
                a.legend(loc="upper right")
        elif plot_type == "AoA Threshold":
            plot_window.title("Detect. Ratio - AoA Threshold [dB]")
            a.set_xlabel('AoA Threshold')
            if param_type == '':
                AoA = self.getColumn(self.thresh_tree, 3)
                est = self.getColumn(self.thresh_tree, 4)
                sort_idx = np.argsort(AoA)
                AoA = AoA[sort_idx]
                est = est[sort_idx]
                a.plot(AoA, est)
            elif param_type == 'N, M':
                list_of_NM = ['16', '32', '48', '64', '80', '96', '112', '128']
                group_list = []
                for N in list_of_NM:
                    for M in list_of_NM:
                        group_list.append([item for item in data if (item['N'] == N and item['M'] == M)])
                group_list = [i for i in group_list if i != []]

                for elem in group_list:
                    N = elem[0]['N']
                    M = elem[0]['M']
                    est = np.array([float(item['est']) for item in elem])
                    AoA = np.array([float(item['AoA']) for item in elem])
                    sort_idx = np.argsort(AoA)
                    AoA = AoA[sort_idx]
                    est = est[sort_idx]
                    a.plot(AoA, est, label="N = " + N + " M = " + M)
                a.legend(loc="upper right")
            elif param_type == "Peak Detection":
                list_of_thresh = np.arange(-150, -40, 10)
                group_list = []
                for thresh in list_of_thresh:
                    group_list.append([item for item in data if (int(item['thresh']) == thresh)])
                group_list = [i for i in group_list if i != []]

                for elem in group_list:
                    thresh = elem[0]['thresh']
                    est = np.array([float(item['est']) for item in elem])
                    AoA = np.array([float(item['AoA']) for item in elem])
                    sort_idx = np.argsort(AoA)
                    AoA = AoA[sort_idx]
                    est = est[sort_idx]
                    a.plot(AoA, est, label="RDM Tresh. = " + thresh)
                a.legend(loc="upper right")
        canvas = FigureCanvasTkAgg(fig, plot_window)
        canvas.get_tk_widget().pack()

    def plotCACFAR(self):
        plot_type = self.combo_CACFAR.get()
        print('plot CACFAR')

    def plotOSCFAR(self):
        plot_type = self.combo_OSCFAR.get()
        print('plot OSCFAR')

    def getColumn(self, tree, index):
        col = []
        rows = tree.get_children()
        for row in rows:
            col.append(float(tree.set(row, index)))
        return np.array(col)

    def getAllData(self, tree):
        rows = tree.get_children()
        data = []
        for row_idx in range(len(rows)):
            data.append(tree.set(rows[row_idx]))
        return data

    def changeThreshGroup(self, event):
        if self.combo_thresh.get() == "Peak Detection":
            self.combo_thresh_param['values'] = ('', 'N, M', 'AoA Threshold')
        elif self.combo_thresh.get() == "AoA Threshold":
            self.combo_thresh_param['values'] = ('', 'N, M', 'Peak Detection')
        self.combo_thresh_param.current(0)
