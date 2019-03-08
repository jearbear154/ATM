from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *

sys.path.insert(0, '../simulator')
from simulator.atm import ATM
from simulator.advanced_simulator import AdvancedSimulator

import tm_interface.trace_viewer as trace_viewer

AND_SYM = '∧'
OR_SYM = '∨'

class MachineController(Frame):

    def __init__(self, parent, states, sigma, gamma, leftend, blank, delta, start, stop):
        Frame.__init__(self, parent)

        # create data structures
        self.atm = None
        self.sigma = sigma

        #configure parent frame weights
        parent.grid_columnconfigure(0, weight = 1)
        parent.grid_rowconfigure(0, weight = 1)

        # configure own resizing behavior
        self.grid(row = 0, column = 0, sticky = (N, S, E, W))

        # populate the controls
        self.CreateControls()


    def rebuild(self, states_extended, sigma, gamma, leftend, blank, delta_extended, start, stop):
        # create alternation function
        states = [q[:-1] for q in states_extended]
        t_dict = {q[:-1]: q[-1] for q in states_extended}
        t = lambda q: t_dict[q]

        # construct delta
        delta_fixed = {(k[0][:-1], k[1]): [(q[:-1], a, d) for (q, a, d) in vs] for k, vs in delta_extended.items()}
        def delta(q, a):
            return delta_fixed.get((q, a), set())

        # construct the ATM object
        self.atm = ATM(set(states), set(sigma), set(gamma), leftend, blank, delta, start[:-1], t)
        self.sigma = sigma

        # enable the Run button iff the ATM is valid
        if delta_fixed and self.atm.t(stop[:-1]) != OR_SYM:
            self.run_button['state'] = 'normal'
        else:
            self.run_button['state'] = 'disabled'

    def CreateControls(self):
        # create time/space bounds:
        bounds_group = LabelFrame(self, text="Bounds")
        time_label = Label(bounds_group, text="Time:")
        time_label.grid(row = 0, column = 0, sticky = (N, S, E, W))
        self.time_var = StringVar()
        time_entry = Entry(bounds_group, textvariable = self.time_var)
        time_entry.grid(row = 0, column = 1, sticky = (N, S, E, W))
        space_label = Label(bounds_group, text="Space:")
        space_label.grid(row = 1, column = 0, sticky = (N, S, E, W))
        self.space_var = StringVar()
        space_entry = Entry(bounds_group, textvariable = self.space_var)
        space_entry.grid(row = 1, column = 1, sticky = (N, S, E, W))

        # create entry:
        self.input_var = StringVar()
        input_entry = Entry(self, textvariable = self.input_var)
        input_entry.bind("<Return>", self.OnEntryReturn)

        # create button:
        self.run_button = Button(self, text = 'Run', command = self.OnRunClick)

        # configure resizing behavior:
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)

        # configure grid placement
        bounds_group.grid(row = 0, column = 0, sticky = (N, S, E, W))
        input_entry.grid(row = 0, column = 1, sticky = (N, S, E, W))
        self.run_button.grid(row = 0, column = 2, sticky = (N, S, E, W))

    def OnEntryReturn(self, event):
        self.OnRunClick()

    def run_simulation(self, inp_list, time_bound = None, space_bound = None):
        # run simulation and get comp. tree
        if time_bound is not None or space_bound is not None:
            return AdvancedSimulator.simulate(self.atm, inp_list, T = time_bound, S = space_bound)
        else:
            return AdvancedSimulator.simulate(self.atm, inp_list)

    def OnRunClick(self):
        # extract input symbol list
        if not all(self.input_var.get().split(',')):
            tkinter.messagebox.showinfo("Invalid input entry", "Please enter a valid input string (found an empty entry)")
            return
        inp_list = self.input_var.get().split(',')
        if not all([a in self.sigma for a in inp_list]):
            tkinter.messagebox.showinfo("Invalid input entry", "Please enter a valid input string (symbol not found in Sigma)")
            return

        # verify bounds
        time_bound = None
        space_bound = None
        try:
            if self.time_var.get().strip():
                time_bound = int(self.time_var.get().strip())
            if self.space_var.get().strip():
                space_bound = int(self.space_var.get().strip())
        except ValueError:
            tkinter.messagebox.showinfo("Invalid bounds entry", "Please enter valid time/space bounds")
            return

        tree = self.run_simulation(inp_list, time_bound = time_bound, space_bound = space_bound)

        # display result
        if tree is None:
            tkinter.messagebox.showinfo("Input rejected",
                'The encoded machine rejected the input: "%s"' %
                inp_list)
        else:
            tkinter.messagebox.showinfo("Input accepted",
                'The encoded machine accepted the input: "%s" with an accepting computation tree of depth %d' %
                (', '.join(inp_list), tree.depth()))

            # show trace viewer
            trace_viewer.TraceViewer(self, tree)


def spawn_toolwindow(root, states, sigma, gamma, leftend, blank, delta, start, stop):
    root.attributes("-toolwindow", 1)
    machine_controller = MachineController(root, states, sigma, gamma, delta, leftend, blank, start, stop)
    machine_controller.master.title('Machine Controller')
    machine_controller.master.resizable(width=True, height=False)
    machine_controller.master.geometry('{}x{}'.format(500, 50))
    return machine_controller

if __name__ == '__main__':
    root = Tk()
    spawn_toolwindow(root, [], [], [], '|-', '_', {}, 'start', 'stop')
    root.mainloop()