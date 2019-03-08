from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog
from tkinter.ttk import *

import tm_interface.transition_prompt as transition_prompt

class SpreadsheetEditor(Frame):
    def __init__(self, root, update_handler, states, gamma, delta = {}):
        Frame.__init__(self, root)

        # create data structures
        self.states = states
        self.gamma = gamma
        self.delta = delta

        self.update_handler = update_handler

        # configure parent frame weights
        self.root = root
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)

        # configure own resizing behavior
        self.grid(row = 0, column = 0, sticky = (N, S, E, W))

        # initialization
        self.CreateEditor()
        self.UpdateDeltaView(self.states, self.gamma)

    def DumpDelta(self):
        return self.delta

    # get the new states from the stored delta
    def GetDelta(self, q, a):
        if (q, a) not in self.delta.keys():
            return []
        return self.delta[(q, a)]

    # construct all controls and add to window
    def CreateEditor(self):
        # create delta editor
        self.delta_view = Treeview(self)
        self.delta_view.bind("<Double-1>", self.OnDeltaViewDoubleClick)
        delta_vscroll = Scrollbar(self, orient="vertical", command=self.delta_view.yview)
        delta_hscroll = Scrollbar(self, orient="horizontal", command=self.delta_view.xview)

        # configure resizing behavior:
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 0)
        self.grid_rowconfigure(2, weight = 0)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 0)

        # configure grid placement
        self.delta_view.grid(row = 0, column = 0, sticky = (N, S, E, W))
        delta_vscroll.grid(row = 0, column = 1, sticky = (N, S, E, W))
        delta_hscroll.grid(row = 1, column = 0, sticky = (N, S, E, W))

    # on double click row, remove the row from table and populate the
    # edit box with the removed state information
    def OnDeltaViewDoubleClick(self, event):
        row = self.delta_view.identify_row(event.y)
        q = self.delta_view.item(row, option='text')
        # have to manually iterate thru column widths because table dosen't supply it
        col = 0
        total_width = 0
        while True:
            total_width += self.delta_view.column(col, option='width')
            col += 1
            if total_width > event.x or col >= len(self.delta_view['columns']):
                break
        i = col - 2
        if i < 0 or i >= len(self.gamma):
            return
        a = self.gamma[i]
        self.EditTransition(q, a)

    # fetch the transition in question and spawn transition_prompt window
    def EditTransition(self, q, a):
        # get the existing transitions
        if (q, a) in self.delta.keys():
            prefilled_states = self.delta[(q, a)]
        else:
            self.delta[(q, a)] = []
            prefilled_states = []

        # spawn window with transitions
        prompt = transition_prompt.TransitionPrompt(self, "Edit transition", "Choose a new state, symbol, and head direction.", self.states, self.gamma, prefilled_states)
        if prompt.result is None:
            return

        # update based on result
        self.delta[(q, a)] = prompt.result
        self.UpdateDeltaView(self.states, self.gamma)
        self.update_handler(self)

    # rebuild the delta table based on states, gamma
    def UpdateDeltaView(self, states, gamma):
        self.states = states
        self.gamma = gamma

        # clear existing rows
        self.delta_view.delete(*self.delta_view.get_children())

        # create base column
        self.delta_view['columns'] = tuple(['state/input'] + self.gamma)
        self.delta_view.heading('#0', text='State / Input', anchor='w')
        self.delta_view.column('#0', anchor='w', width=75)
        # create column for every item in gamma
        for i in range(len(self.gamma)):
            a = self.gamma[i]
            self.delta_view.heading('#%d' % (i + 1), text=a, anchor='w')
            self.delta_view.column('#%d' % (i + 1), anchor='w', width=75)

        # add row for every state in Q
        for q in self.states:
            row = self.delta_view.insert('', 'end', text=q, values=tuple([self.GetDelta(q, a) for a in self.gamma]))

    # rebuild delta given keys, values
    def ImportDelta(self, delta_keys, delta_values):
        self.delta = {}
        for k, v in zip(delta_keys, delta_values):
            self.delta[k] = v

def spawn_toolwindow(root, handler, states, gamma, delta = {}):
    root.attributes("-toolwindow", 1)
    spreadsheet_editor = SpreadsheetEditor(root, handler, states, gamma, delta = {})
    spreadsheet_editor.master.title('Spreadsheet Editor')
    spreadsheet_editor.master.resizable(width=True, height=False)
    spreadsheet_editor.master.geometry('{}x{}'.format(500, 500))
    return spreadsheet_editor


if __name__ == '__main__':
    root = Tk()
    def handler(de):
        print(de.DumpDelta())
    spawn_toolwindow(root, handler, [], ['|-', '_'])
    root.mainloop()