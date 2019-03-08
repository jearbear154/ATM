from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *

class AlphabetBuilder(Frame):

    def __init__(self, parent, update_handler, sigma_exprs, gamma_exprs, leftend, blank):
        Frame.__init__(self, parent)

        # create data structures
        self.sigma = {}
        self.sigma_items = {}
        self.gamma = {}
        self.gamma_items = {}

        self.leftend_sym = leftend
        self.blank_sym = blank

        #configure parent frame weights
        parent.grid_columnconfigure(0, weight = 1)
        parent.grid_rowconfigure(0, weight = 1)

        # configure own resizing behavior
        self.grid(row = 0, column = 0, sticky = (N, S, E, W))
        self.grid(row = 1, column = 0, sticky = (N, S, E, W))

        self.update_handler = update_handler

        # populate the controls
        self.CreateEditor()
        self.InitTables(sigma_exprs, gamma_exprs)
        self.UpdateTables()

    def CreateEditor(self):
        # create input alphabet:
        sigma_group = LabelFrame(self, text="Sigma")
        sigma_group.pack(padx=3, pady=3)

        self.sigma_view = Treeview(sigma_group)
        self.sigma_view['columns'] = ('expr')
        self.sigma_view.heading('#0', text='Expr', anchor='w')
        self.sigma_view.column('#0', anchor='w', width=225)
        self.sigma_view.bind("<Double-1>", self.OnSigmaViewDoubleClick)
        sigma_vscroll = Scrollbar(sigma_group, orient="vertical", command=self.sigma_view.yview)
        sigma_hscroll = Scrollbar(sigma_group, orient="horizontal", command=self.sigma_view.xview)

        # create entry:
        self.sigma_var = StringVar()
        self.sigma_entry = Entry(sigma_group, textvariable = self.sigma_var)
        self.sigma_entry.bind("<Return>", self.OnSigmaEntryReturn)

        # create button:
        self.sigma_validate = Button(sigma_group, text = 'Validate', command = self.OnSigmaValidateClick)

        # configure resizing behavior:
        sigma_group.grid_rowconfigure(0, weight = 1)
        sigma_group.grid_rowconfigure(1, weight = 0)
        sigma_group.grid_columnconfigure(0, weight = 1)
        sigma_group.grid_columnconfigure(1, weight = 0)

        # configure grid placement
        self.sigma_view.grid(row = 0, columnspan = 2, sticky = (N, S, E, W))
        sigma_vscroll.grid(row = 0, column = 3, sticky = (N, S, E, W))
        sigma_hscroll.grid(row = 1, columnspan = 2, sticky = (N, S, E, W))
        self.sigma_entry.grid(row = 2, column = 0, sticky = (N, S, E, W))
        self.sigma_validate.grid(row = 2, column = 1, sticky = (N, S, E, W))

        # create tape alphabet:
        gamma_group = LabelFrame(self, text="Gamma")
        gamma_group.pack(padx=3, pady=3)

        self.gamma_view = Treeview(gamma_group)
        self.gamma_view['columns'] = ('expr')
        self.gamma_view.heading('#0', text='Expr', anchor='w')
        self.gamma_view.column('#0', anchor='w', width=225)
        self.gamma_view.bind("<Double-1>", self.OnGammaViewDoubleClick)
        gamma_vscroll = Scrollbar(gamma_group, orient="vertical", command=self.gamma_view.yview)
        gamma_hscroll = Scrollbar(gamma_group, orient="horizontal", command=self.gamma_view.xview)

        # create entry:
        self.gamma_var = StringVar()
        self.gamma_entry = Entry(gamma_group, textvariable = self.gamma_var)
        self.gamma_entry.bind("<Return>", self.OnGammaEntryReturn)

        # create button:
        self.gamma_validate = Button(gamma_group, text = 'Validate', command = self.OnGammaValidateClick)

        # configure resizing behavior:
        gamma_group.grid_rowconfigure(0, weight = 1)
        gamma_group.grid_rowconfigure(1, weight = 0)
        gamma_group.grid_columnconfigure(0, weight = 1)
        gamma_group.grid_columnconfigure(1, weight = 0)

        # configure grid placement
        self.gamma_view.grid(row = 0, columnspan = 2, sticky = (N, S, E, W))
        gamma_vscroll.grid(row = 0, column = 3, sticky = (N, S, E, W))
        gamma_hscroll.grid(row = 1, columnspan = 2, sticky = (N, S, E, W))
        self.gamma_entry.grid(row = 2, column = 0, sticky = (N, S, E, W))
        self.gamma_validate.grid(row = 2, column = 1, sticky = (N, S, E, W))

        # symbol picker
        reserved_group = LabelFrame(self, text="Reserved Gamma Symbols")
        reserved_group.pack(padx=3, pady=3)

        leftend_label = Label(reserved_group, text = "Left End Marker:")
        leftend_label.grid(row = 0, column = 0, sticky = (N, W))
        self.leftend_var = StringVar()
        self.leftend_var.set(self.leftend_sym)
        self.leftend_entry = Entry(reserved_group, textvariable = self.leftend_var)
        self.leftend_entry.bind("<Return>", self.UpdateGammaReserved)
        self.leftend_entry.grid(row = 0, column = 1, sticky = (N, S, E, W))
        blank_label = Label(reserved_group, text = "Blank Symbol:")
        blank_label.grid(row = 1, column = 0, sticky = (N, W))
        self.blank_var = StringVar()
        self.blank_var.set(self.blank_sym)
        self.blank_entry = Entry(reserved_group, textvariable = self.blank_var)
        self.blank_entry.bind("<Return>", self.UpdateGammaReserved)
        self.blank_entry.grid(row = 1, column = 1, sticky = (N, S, E, W))
        # configure resizing
        reserved_group.grid_rowconfigure(0, weight = 1)
        reserved_group.grid_rowconfigure(1, weight = 1)
        reserved_group.grid_columnconfigure(1, weight = 1)

    def InitTables(self, sigma_exprs, gamma_exprs):
        self.default_sigma_row = self.gamma_view.insert('', 'end', text=u'(Contents of Sigma)')

        for expr in sigma_exprs:
            self.AddSigmaExpr(expr)

        # need to construct explicitly to be able to block removal
        self.default_control_row = self.gamma_view.insert('', 'end', text='(Left End Marker, Blank Symbol)')

        for expr in gamma_exprs:
            self.AddGammaExpr(expr)

    def UpdateTables(self):
        max_width = 250
        for k in self.sigma.keys():
            max_width = max([max_width, len(k) * 10])
        self.sigma_view.column('#0', width=max_width)
        max_width = 250
        for k in self.gamma.keys():
            max_width = max([max_width, len(k) * 10])
        self.gamma_view.column('#0', width=max_width)
        self.update_handler(self)

    # sigma interaction
    def RemoveSigmaExpr(self, expr):
        if expr not in self.sigma:
            return None
        del self.sigma[expr]
        del self.sigma_items[expr]
        self.UpdateTables()
        return expr

    def OnSigmaViewDoubleClick(self, event):
        if not self.sigma_view.selection():
            return
        item = self.sigma_view.selection()[0]
        expr = self.sigma_view.item(item, "text")

        self.RemoveSigmaExpr(expr)

        self.sigma_view.delete(item)
        self.sigma_var.set(expr)

    def AddSigmaExpr(self, expr):
        if not all(expr.split(',')):
            tkinter.messagebox.showinfo("Invalid Sigma entry", "Please enter a valid state (found an empty entry)")
            return None
        if expr and expr not in self.sigma:
            self.sigma[expr] = expr.split(',')
            self.sigma_items[expr] = self.sigma_view.insert('', 'end', text=expr)
            self.UpdateTables()
            return expr

    def OnSigmaEntryReturn(self, event):
        self.OnSigmaValidateClick()

    def OnSigmaValidateClick(self):
        if self.AddSigmaExpr(self.sigma_var.get()):
            self.sigma_var.set('')

    # gamma interaction
    def RemoveGammaExpr(self, expr):
        if expr not in self.gamma:
            return None
        del self.gamma[expr]
        del self.gamma_items[expr]
        self.UpdateTables()
        return expr

    def OnGammaViewDoubleClick(self, event):
        if not self.gamma_view.selection():
            return
        item = self.gamma_view.selection()[0]
        if item == self.default_control_row or item == self.default_sigma_row:
            tkinter.messagebox.showinfo("Invalid selection", "Cannot remove placeholder rows (implicit Sigma inclusion and endmarker/blank symbols)")
            return
        expr = self.gamma_view.item(item, "text")
        self.RemoveGammaExpr(expr)
        self.gamma_view.delete(item)
        self.gamma_var.set(expr)

    def AddGammaExpr(self, expr):
        if not all(expr.split(',')):
            tkinter.messagebox.showinfo("Invalid Gamma entry", "Please enter a valid state (found an empty entry)")
            return None
        if expr and expr not in self.gamma:
            self.gamma[expr] = expr.split(',')
            self.gamma_items[expr] = self.gamma_view.insert('', 'end', text=expr)
            self.UpdateTables()
            return expr

    def OnGammaEntryReturn(self, event):
        self.OnGammaValidateClick()

    def OnGammaValidateClick(self):
        if self.AddGammaExpr(self.gamma_var.get()):
            self.gamma_var.set('')

    def UpdateGammaReserved(self, event):
        if not all([self.leftend_var.get(), self.blank_var.get()]):
            tkinter.messagebox.showinfo("Invalid entry", "Please enter a valid state (found an empty entry)")
            self.leftend_var.set(self.leftend_sym)
            self.blank_var.set(self.blank_sym)
            return
        self.leftend_sym = self.leftend_var.get()
        self.blank_sym = self.blank_var.get()
        self.update_handler(self)

    def SigmaExprs(self):
        return list(self.sigma.keys())

    def DumpSigma(self):
        result = set()
        for k, v in self.sigma.items():
            result |= set(v)
        return list(sorted(list(result)))

    def GammaExprs(self):
        return list(self.gamma.keys())

    def DumpGamma(self):
        result = set(self.DumpSigma() + [self.leftend_sym, self.blank_sym])
        for k, v in self.gamma.items():
            result |= set(v)
        return list(sorted(list(result)))

    def ReservedSyms(self):
        return (self.leftend_sym, self.blank_sym)

def spawn_toolwindow(root, update_handler, sigma_exprs = [], gamma_exprs = [], leftend = u'\u22A2', blank = u'\u23b5'):
    root.attributes("-topmost", 1)
    alphabet_builder = AlphabetBuilder(root, update_handler, sigma_exprs, gamma_exprs, leftend, blank)
    alphabet_builder.master.title('Alphabet Builder')
    alphabet_builder.master.resizable(width=False, height=False)
    alphabet_builder.master.geometry('{}x{}'.format(250, 640))
    return alphabet_builder

if __name__ == '__main__':
    root = Tk()
    def handler(ab):
        print(ab.DumpSigma())
    spawn_toolwindow(root, handler)
    root.mainloop()