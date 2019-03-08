from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *

AND_SYM = '∧'
OR_SYM = '∨'

class StateBuilder(Frame):

    def __init__(self, parent, update_handler, state_exprs, start, stop):
        Frame.__init__(self, parent)

        # create data structures
        self.states = {}
        self.states_items = {}

        self.start_state = start
        self.stop_state = stop
        self.alt_var = StringVar()
        self.alt_var.set(AND_SYM)

        #configure parent frame weights
        parent.grid_columnconfigure(0, weight = 1)
        parent.grid_rowconfigure(0, weight = 1)

        # configure own resizing behavior
        self.grid(row = 0, column = 0, sticky = (N, S, E, W))
        self.grid(row = 1, column = 0, sticky = (N, S, E, W))

        self.update_handler = update_handler

        # populate the controls
        self.CreateEditor()
        self.InitTables(state_exprs)
        self.UpdateTables()

    def CreateEditor(self):
        # create input alphabet:
        states_group = LabelFrame(self, text="States")
        states_group.pack(padx=3, pady=3)

        self.states_view = Treeview(states_group)
        self.states_view['columns'] = ('expr')
        self.states_view.heading('#0', text='Expr', anchor='w')
        self.states_view.column('#0', anchor='w', width=225)
        self.states_view.bind("<Double-1>", self.OnViewDoubleClick)
        states_vscroll = Scrollbar(states_group, orient="vertical", command=self.states_view.yview)
        states_hscroll = Scrollbar(states_group, orient="horizontal", command=self.states_view.xview)

        # create entry:
        self.states_var = StringVar()
        self.states_entry = Entry(states_group, textvariable = self.states_var)
        self.states_entry.bind("<Return>", self.OnEntryReturn)
        alt_menu = OptionMenu(states_group, self.alt_var, AND_SYM, AND_SYM, OR_SYM)

        # create button:
        self.states_validate = Button(states_group, text = 'Add', command = self.OnValidateClick)

        # configure resizing behavior:
        states_group.grid_rowconfigure(0, weight = 1)
        states_group.grid_rowconfigure(1, weight = 0)
        states_group.grid_columnconfigure(0, weight = 1)
        states_group.grid_columnconfigure(1, weight = 0)

        # configure grid placement
        self.states_view.grid(row = 0, columnspan = 3, sticky = (N, S, E, W))
        states_vscroll.grid(row = 0, column = 4, sticky = (N, S, E, W))
        states_hscroll.grid(row = 1, columnspan = 3, sticky = (N, S, E, W))
        self.states_entry.grid(row = 2, column = 0, sticky = (N, S, E, W))
        alt_menu.grid(row = 2, column = 1, sticky = (N, S, E, W))
        self.states_validate.grid(row = 2, column = 2, sticky = (N, S, E, W))

        # start/end picker
        reserved_group = LabelFrame(self, text="Reserved States")
        reserved_group.pack(padx=3, pady=3)

        start_state_label = Label(reserved_group, text = "Start:")
        start_state_label.grid(row = 0, column = 0, sticky = (N, W))
        self.start_state_var = StringVar()
        self.start_state_var.set(self.start_state[:-1])
        self.start_state_entry = Entry(reserved_group, textvariable = self.start_state_var)
        self.start_state_entry.bind("<Return>", self.UpdateReservedStates)
        self.start_state_entry.grid(row = 0, column = 1, sticky = (N, S, E, W))
        dir_label = Label(reserved_group, text="Start alt. state:")
        dir_label.grid(row = 1, column = 0, sticky = (N, S, E, W))
        self.start_alt_var = StringVar()
        self.start_alt_var.set(AND_SYM)
        start_alt_menu = OptionMenu(reserved_group, self.start_alt_var, AND_SYM, AND_SYM, OR_SYM)
        start_alt_menu.grid(row = 1, column = 1, sticky = (N, S, E, W))
        stop_state_label = Label(reserved_group, text = "Stop:")
        stop_state_label.grid(row = 2, column = 0, sticky = (N, W))
        self.stop_state_var = StringVar()
        self.stop_state_var.set(self.stop_state[:-1])
        self.stop_state_entry = Entry(reserved_group, textvariable = self.stop_state_var)
        self.stop_state_entry.bind("<Return>", self.UpdateReservedStates)
        self.stop_state_entry.grid(row = 2, column = 1, sticky = (N, S, E, W))
        self.reserved_update = Button(reserved_group, text = 'Update', command = lambda: self.UpdateReservedStates(None))
        self.reserved_update.grid(row = 3, columnspan = 2, sticky = (N, S, E, W))

        # configure resizing
        reserved_group.grid_rowconfigure(0, weight = 1)
        reserved_group.grid_rowconfigure(1, weight = 1)
        reserved_group.grid_columnconfigure(1, weight = 1)

    def InitTables(self, state_exprs):
        self.default_states_row = self.states_view.insert('', 'end', text=u'(Start and Stop states)')

        for expr in state_exprs:
            self.AddExpr(expr)

    def UpdateTables(self):
        max_width = 250
        for k in self.states.keys():
            max_width = max([max_width, len(k) * 10])
        self.states_view.column('#0', width=max_width)
        self.update_handler(self)

    def RemoveExpr(self, expr):
        if expr not in self.states_items:
            return None
        del self.states[expr]
        del self.states_items[expr]
        self.UpdateTables()
        return expr

    def OnViewDoubleClick(self, event):
        if not self.states_view.selection():
            return
        item = self.states_view.selection()[0]
        if item == self.default_states_row:
            tkinter.messagebox.showinfo("Invalid selection", "Cannot remove placeholder rows (start and stop states)")
            return
        expr_ext = self.states_view.item(item, "text")
        expr = expr_ext[:-2]
        t = expr_ext[-1]

        self.RemoveExpr(expr)

        self.states_view.delete(item)
        self.states_var.set(expr)
        self.alt_var.set(t)

    def OnEntryReturn(self, event):
        self.OnValidateClick()

    def AddExpr(self, expr):
        if not all(expr.split(',')):
            tkinter.messagebox.showinfo("Invalid state entry", "Please enter a valid state (found an empty entry)")
            return None
        if expr and expr not in self.states.keys():
            self.states[expr] = [e + self.alt_var.get() for e in expr.split(',')]
            self.states_items[expr] = self.states_view.insert('', 'end', text='%s %s' % (expr, self.alt_var.get()))
            self.UpdateTables()
            return expr

    def OnValidateClick(self):
        if self.AddExpr(self.states_var.get().strip()):
            self.states_var.set('')

    def UpdateReservedStates(self, event):
        if not all([self.start_state_var.get(), self.stop_state_var.get()]):
            tkinter.messagebox.showinfo("Invalid entry", "Please enter a valid state (found an empty entry)")
            self.start_state_var.set(self.start_state[:-1])
            self.stop_state_var.set(self.stop_state)
            self.start_alt_var.set(self.start_state[-1])
            return
        self.start_state = self.start_state_var.get() + self.start_alt_var.get()
        self.stop_state = self.stop_state_var.get() + AND_SYM
        self.update_handler(self)

    def StateExprs(self):
        return list(self.states.keys())

    def DumpStates(self):
        result = set([self.start_state, self.stop_state])
        for k, v in self.states.items():
            result |= set(v)
        return list(sorted(list(result)))

    def ReservedStates(self):
        return (self.start_state, self.stop_state)

def spawn_toolwindow(root, update_handler, state_exprs = [], start='start' + AND_SYM, stop='stop' + AND_SYM):
    root.attributes("-topmost", 1)
    state_builder = StateBuilder(root, update_handler, state_exprs, start, stop)
    state_builder.master.title('State Builder')
    state_builder.master.resizable(width=False, height=False)
    state_builder.master.geometry('{}x{}'.format(250, 400))
    return state_builder

if __name__ == '__main__':
    root = Tk()
    def handler(sb):
        print(sb.DumpStates())
    spawn_toolwindow(root, handler)
    root.mainloop()