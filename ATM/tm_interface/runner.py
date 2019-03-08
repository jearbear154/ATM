from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog
from tkinter.ttk import *

import pickle
import base64

import tm_interface.state_builder as state_builder
import tm_interface.alphabet_builder as alphabet_builder
from tm_interface import machine_controller

import tm_interface.spreadsheet_editor as spreadsheet_editor
import tm_interface.graph_editor as graph_editor

AND_SYM = '∧'
OR_SYM = '∨'

class Runner(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)

        # create data structures
        self.state_exprs = []
        self.sigma_exprs = []
        self.gamma_exprs = []

        self.states = []
        self.sigma = []
        self.gamma = []
        self.delta = {}
        self.t = {}

        self.start_state = 'start' + AND_SYM
        self.stop_state = 'stop' + AND_SYM

        self.leftend_sym = u'|-'
        self.blank_sym = u'_'

        # configure parent frame weights
        self.root = root
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)

        # configure own resizing behavior
        self.grid(row = 0, column = 0, sticky = (N, S, E, W))

        # initialization
        self.CreateEditor()
        self.UpdateSimulation()

    # called by menu item. restarts toolhelper update loops
    def respawn_builders(self):
        self.run = False

    # function to base64 encode the machine
    def export_machine(self):
        obj = (self.state_exprs, self.sigma_exprs, self.gamma_exprs, self.leftend_sym,
            self.blank_sym, list(self.delta.keys()), list(self.delta.values()),
            self.start_state, self.stop_state)
        return base64.b64encode(pickle.dumps(obj))

    # called by menu item. exports machine encoding
    def ExportMachine(self):
        pickle_str = self.export_machine()
        # copy string to clipboard
        self.clipboard_clear()
        self.clipboard_append(pickle_str)
        self.update()
        tkinter.messagebox.showinfo("Machine export", "Machine encoding has been copied to clipboard")

    # rebuilds machine from base64 encoding
    def import_machine(self, encoded_pickle):
        # decode pickle
        unpickled = pickle.loads(base64.b64decode(encoded_pickle))
        (self.state_exprs, self.sigma_exprs, self.gamma_exprs, self.leftend_sym,
            self.blank_sym, delta_keys, delta_values,
            self.start_state, self.stop_state) = unpickled

        self.de.ImportDelta(delta_keys, delta_values)
        self.delta = self.de.DumpDelta()

    # called by menu item. imports machine encoding
    def ImportMachine(self):
        encoded_pickle = tkinter.simpledialog.askstring("Machine import", "Paste machine encoding")
        if not encoded_pickle:
            return

        self.import_machine(encoded_pickle)

        # update ui
        self.respawn_builders()
        self.UpdateSimulation()

    # get the new states from the stored delta
    def GetDelta(self, q, a):
        if (q, a) not in self.delta.keys():
            return []
        return self.delta[(q, a)]

    # get the updated states from the state editor window
    def PullStatesUpdates(self, sb):
        self.state_exprs = sb.StateExprs()
        self.states = sb.DumpStates()
        (self.start_state, self.stop_state) = sb.ReservedStates()
        self.UpdateSimulation()

    # get the updated alphabets from the state editor window
    def PullAlphabetUpdates(self, ab):
        self.sigma_exprs = ab.SigmaExprs()
        self.sigma = ab.DumpSigma()
        self.gamma_exprs = ab.GammaExprs()
        self.gamma = ab.DumpGamma()
        (self.leftend_sym, self.blank_sym) = ab.ReservedSyms()
        self.UpdateSimulation()

    # get the updated delta from the state editor window
    def PullDeltaUpdates(self, de):
        self.delta = de.DumpDelta()
        self.UpdateSimulation()

    # construct all controls and add to window
    def CreateEditor(self):
        # create a toplevel menu
        menubar = Menu(self.root)
        # file
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Export machine...", command=self.ExportMachine)
        filemenu.add_command(label="Import machine...", command=self.ImportMachine)

        def import_sample():
            self.import_machine('gAMoXXEAKFgCAAAAcTVxAVgCAAAAcTRxAlgCAAAAcTJxA1gCAAAAcTNxBGVdcQVYAQAAADBxBmFdcQcoWAEAAAB4cQhoBmVYAgAAAHwtcQlYAQAAACBxCl1xCyhYBQAAAHEy4oincQxoBoZxDVgFAAAAcTPiiKdxDmgKhnEPWAUAAABxNOKIp3EQaAaGcRFYBQAAAHEx4oincRJoCYZxE1gFAAAAcTXiiKdxFGgIhnEVaAxoCoZxFmgMaAiGcRdoDmgIhnEYaBRoBoZxGWgOaAaGcRpoEGgIhnEbaBRoCoZxHGgSaAaGcR1lXXEeKF1xH2gOaAhYAQAAAFJxIIdxIWFdcSJoFGgKWAEAAABMcSOHcSRhXXElaA5oCGggh3EmYV1xJ2gSaAloIIdxKGFdcSloFGgIaCOHcSphXXErWAoAAABxYWNjZXB04oincSxoCmggh3EtYV1xLmgMaAhoIIdxL2FdcTBoDmgIaCCHcTFhXXEyaBRoBmgjh3EzYV1xNGgQaAZoIIdxNWFdcTZoEGgIaCCHcTdhXXE4aAxoCmggh3E5YV1xOlgFAAAAcTLiiKdxO2gKaCCHcTxhZWgSaCx0cT0u')
            self.respawn_builders()
            self.UpdateSimulation()
        filemenu.add_command(label="Import sample machine", command=import_sample)
        menubar.add_cascade(label="File", menu=filemenu)
        # window
        windowmenu = Menu(menubar, tearoff=0)
        windowmenu.add_command(label="Show builders", command=self.respawn_builders)
        menubar.add_cascade(label="Window", menu=windowmenu)
        self.root.config(menu=menubar)

        # create delta editor
        self.de = graph_editor.GraphEditor(self, self.PullDeltaUpdates, self.states, self.gamma, delta = self.delta)

        # create machine controller
        self.mc = machine_controller.MachineController(self, self.states, self.sigma, self.gamma, self.leftend_sym, self.blank_sym, self.delta, self.start_state, self.stop_state)

        # configure resizing behavior:
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 0)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 0)

        # configure grid placement
        self.de.grid(row = 0, column = 0, sticky = (N, S, E, W))
        self.mc.grid(row = 1, column = 0, sticky = (N, S, E, W))

    # rebuild the delta table based on sigma, gamma, and delta
    def UpdateSimulation(self):
        # update delta editor
        self.de.UpdateDeltaView(self.states, self.gamma)
        # recreate machine controller
        self.mc.rebuild(self.states, self.sigma, self.gamma, self.leftend_sym, self.blank_sym, self.delta, self.start_state, self.stop_state)

    # called to run the toolwindows and main window in parallel
    def mainloop(self):
        self.run = True

        # spawn the toolwindows
        sb_control = Toplevel(self.root)
        self.sb = state_builder.spawn_toolwindow(sb_control, self.PullStatesUpdates, self.state_exprs, self.start_state, self.stop_state)
        ab_control = Toplevel(self.root)
        self.ab = alphabet_builder.spawn_toolwindow(ab_control, self.PullAlphabetUpdates, self.sigma_exprs, self.gamma_exprs, self.leftend_sym, self.blank_sym)

        # pull initial state from the toolwindows
        self.PullStatesUpdates(self.sb)
        self.PullAlphabetUpdates(self.ab)

        # the main loop
        while self.run:
            self.root.update_idletasks()
            self.root.update()
            sb_control.update_idletasks()
            sb_control.update()
            ab_control.update_idletasks()
            ab_control.update()

        # need to rerun the tool spawn, destroy existing
        sb_control.destroy()
        ab_control.destroy()


def spawn_window(root):
    sim = Runner(root)
    sim.master.title('TM Simulator')
    sim.master.geometry('{}x{}'.format(500, 500))
    return sim


if __name__ == '__main__':
    root = Tk()
    sim = spawn_window(root)
    while True:
        sim.mainloop()
