from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from graphics.tree_converter import TreeConverter

from matplotlib.figure import Figure
import matplotlib.image as mpimg

import networkx as nx
from graphviz import Source
from networkx.drawing.nx_pydot import to_pydot

sys.path.insert(0, '../graphics')
import graphics.tree_converter as tree_converter

class TraceViewer(Toplevel):
    def __init__(self, parent, tree):
        Toplevel.__init__(self, parent)

        self.tree = tree

        # set dialog properties
        self.title("Trace Viewer")
        self.transient(parent)
        self.grab_set()
        self.geometry('{}x{}+{}+{}'.format(250, 425, parent.winfo_rootx()+50, parent.winfo_rooty()+50))

        #configure parent frame weights
        parent.grid_columnconfigure(0, weight = 1)
        parent.grid_rowconfigure(0, weight = 1)

        # populate the controls
        self.CreateViewer()

    def CreateViewer(self):
        f = plt.figure(figsize=(5, 4))
        a = f.add_subplot(111)

        src = to_pydot(TreeConverter.to_graphics(self.tree))
        src.write_png('~tree.png')

        # display graph
        image = mpimg.imread('~tree.png')
        plt.imshow(image)

        # create new canvas
        self.canvas = FigureCanvasTkAgg(f, master=self)
        self.canvas.show()

        # toolbar frame
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()

        # positioning
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
