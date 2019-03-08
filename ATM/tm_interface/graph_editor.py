from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog
from tkinter.ttk import *

import tm_interface.spreadsheet_editor as spreadsheet_editor

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from matplotlib.figure import Figure
import matplotlib.image as mpimg

import networkx as nx
import numpy as np

from graphviz import Source
from networkx.drawing.nx_pydot import to_pydot

AND_SYM = '∧'
OR_SYM = '∨'

def sanitize(v):
    if v[-1] == AND_SYM:
        return v[:-1] + '^'
    elif v[-1] == OR_SYM:
        return v[:-1] + 'v'
    else:
        return v

class GraphEditor(Frame):

    def refresh_graph(self):
        f = plt.figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)

        delta = self.de.DumpDelta()

        # build graph to display
        G = nx.MultiDiGraph()
        for v in self.states:
            G.add_node(sanitize(v))
        for k, v in delta.keys():
            for q, a, d in delta[(k, v)]:
                G.add_edge(sanitize(k), sanitize(q), label=v[0] + '->' + a + ',' + d)

        # layout graph
        src = to_pydot(G)
        src.write_png('~temp.png')
        image = mpimg.imread("~temp.png")

        # display graph
        plt.imshow(image)

        # remove old canvas
        if self.canvas:
            plt.close("all")
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()

        # create new canvas
        self.canvas = FigureCanvasTkAgg(f, master=self.graph_frame)
        self.canvas.show()

        # toolbar frame
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.graph_frame)
        self.toolbar.update()

        # positioning
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def PullDeltaUpdates(self, de):
        self.delta = de.DumpDelta()
        self.refresh_graph()
        self.update_handler(de)

    def UpdateDeltaView(self, states, gamma):
        self.states = states
        self.gamma = gamma
        self.de.UpdateDeltaView(states, gamma)
        self.refresh_graph()

    def __init__(self, root, update_handler, states, gamma, delta = {}):
        Frame.__init__(self, root)

        # create data structures
        self.states = states
        self.gamma = gamma
        self.delta = delta
        self.canvas = None

        self.update_handler = update_handler

        # configure parent frame weights
        self.root = root
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)

        # configure own resizing behavior
        self.grid(row = 0, column = 0, sticky = (N, S, E, W))
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        # initialization
        pane = PanedWindow(self, orient=HORIZONTAL)

        self.graph_frame = Frame(pane)
        self.sheet_frame = Frame(pane)
        self.de = spreadsheet_editor.SpreadsheetEditor(self.sheet_frame, lambda de: self.PullDeltaUpdates(de), self.states, self.gamma, delta = delta)
        self.de.grid(row = 0, column = 0, sticky = (N, S, E, W))

        pane.add(self.graph_frame)
        pane.add(self.sheet_frame)
        pane.grid(row = 0, column = 0, sticky = (N, S, E, W))

        self.UpdateDeltaView(self.states, self.gamma)

    # rebuild delta given keys, values
    def ImportDelta(self, delta_keys, delta_values):
        self.de.ImportDelta(delta_keys, delta_values)

    def DumpDelta(self):
        return self.de.DumpDelta()


def spawn_toolwindow(root, handler, states, gamma, delta = {}):
    root.attributes("-toolwindow", 1)
    graph_editor = GraphEditor(root, handler, states, gamma, delta = {})
    graph_editor.master.title('Graph Editor')
    graph_editor.master.resizable(width=True, height=True)
    graph_editor.master.geometry('{}x{}'.format(500, 500))
    return graph_editor

if __name__ == '__main__':
    root = Tk()
    def handler(de):
        print(de.DumpDelta())
    ge = spawn_toolwindow(root, handler, [], ['|-', '_'])

    root.mainloop()