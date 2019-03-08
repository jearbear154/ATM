from tkinter import *
from tkinter.ttk import *

class TransitionPrompt(Toplevel):
    def __init__(self, parent, title, message, states, gamma, prefilled_states):
        Toplevel.__init__(self)

        # set dialog properties
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.resizable(width=False, height=False)
        self.geometry('{}x{}+{}+{}'.format(250, 425, parent.winfo_rootx()+50, parent.winfo_rooty()+50))
        self.protocol("WM_DELETE_WINDOW", self.Cancel)

        # create data structures
        self.states_items = {}

        # create state list group:
        states_group = LabelFrame(self, text="States")
        states_group.pack(padx=3, pady=3)

        # state list table
        self.states_view = Treeview(states_group)
        self.states_view['columns'] = ('expr')
        self.states_view.heading('#0', text='Expr', anchor='w')
        self.states_view.column('#0', anchor='w', width=225)
        self.states_view.bind("<Double-1>", self.OnViewDoubleClick)
        states_vscroll = Scrollbar(states_group, orient="vertical", command=self.states_view.yview)
        states_hscroll = Scrollbar(states_group, orient="horizontal", command=self.states_view.xview)
        self.states_view.grid(row = 0, columnspan = 2, sticky = (N, S, E, W))
        states_vscroll.grid(row = 0, column = 3, sticky = (N, S, E, W))
        states_hscroll.grid(row = 1, columnspan = 2, sticky = (N, S, E, W))

        # apply button (send results to main window)
        apply_button = Button(states_group, text="Apply", command=self.Submit)
        apply_button.grid(row = 4, columnspan = 3, sticky = (N, S, E, W))

        # configure resizing behavior:
        states_group.grid_rowconfigure(0, weight = 1)
        states_group.grid_rowconfigure(1, weight = 0)
        states_group.grid_columnconfigure(0, weight = 1)
        states_group.grid_columnconfigure(1, weight = 0)

        # new state editor
        edit_group = LabelFrame(self, text="Edit")
        edit_group.pack(padx=3, pady=3)

        # info label
        main_label = Label(edit_group, text=message)
        main_label.grid(row = 0, columnspan = 2, sticky = (N, S, E, W))

        # q label
        state_label = Label(edit_group, text="Output state:")
        state_label.grid(row = 1, column = 0, sticky = (N, S, E, W))
        # q edit
        self.state_var = StringVar()
        self.state_var.set(states[0])
        state_menu = OptionMenu(edit_group, self.state_var, states[0], *states)
        state_menu.grid(row = 1, column = 1, sticky = (N, S, E, W))

        # a label
        symbol_label = Label(edit_group, text="Output symbol:")
        symbol_label.grid(row = 2, column = 0, sticky = (N, S, E, W))
        # a edit
        self.symbol_var = StringVar()
        self.symbol_var.set(gamma[0])
        symbol_menu = OptionMenu(edit_group, self.symbol_var, gamma[0], *gamma)
        symbol_menu.grid(row = 2, column = 1, sticky = (N, S, E, W))

        # d label
        dir_label = Label(edit_group, text="Head direction:")
        dir_label.grid(row = 3, column = 0, sticky = (N, S, E, W))
        # d edit
        self.dir_var = StringVar()
        self.dir_var.set('R')
        dir_menu = OptionMenu(edit_group, self.dir_var, 'R', 'R', 'L')
        dir_menu.grid(row = 3, column = 1, sticky = (N, S, E, W))

        # button add state to the state list
        add_button = Button(edit_group, text="Add", command=self.ButtonClick)
        add_button.grid(row = 4, columnspan = 2, sticky = (N, S, E, W))

        # run initialization
        self.InitTables(prefilled_states)

        # don't return to main part till you close this MsgBox
        self.wait_window()

    # edit actions
    def AddTransition(self, state):
        table_text = "{%s %s %s}" % state
        item = self.states_view.insert('', 'end', text=table_text)
        self.states_items[item] = state
        self.UpdateTables()

    def ButtonClick(self):
        self.AddTransition((self.state_var.get(), self.symbol_var.get(), self.dir_var.get()))

    def InitTables(self, prefilled_states):
        for state in prefilled_states:
            self.AddTransition(state)

    def UpdateTables(self):
        max_width = 250
        for state in self.states_items.values():
            table_text = "{%s %s %s}" % state
            max_width = max([max_width, len(table_text) * 10])
        self.states_view.column('#0', width=max_width)

    # on double click row, remove the row from table and populate the
    # edit box with the removed state information
    def OnViewDoubleClick(self, event):
        # get selection
        if not self.states_view.selection():
            return
        item = self.states_view.selection()[0]

        # populate edit boxes
        (q, a, d) = self.states_items[item]
        self.state_var.set(q)
        self.symbol_var.set(a)
        self.dir_var.set(d)

        # remove selection
        self.states_view.delete(item)
        del self.states_items[item]

    # global actions
    def Cancel(self):
        self.result = None
        self.destroy()

    def Submit(self):
        self.result = list(self.states_items.values())
        self.destroy()