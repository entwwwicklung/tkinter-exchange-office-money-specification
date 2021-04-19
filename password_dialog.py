# -*- coding: utf-8 -*-
from Tkinter import *

class PasswordDialog(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.master = master

        self.withdraw()

        self.title("Provera")

        width = 609
        height = 149

        parent_offset = tuple(int(_) for _ in self.master.geometry().split('x')[1].split('+'))

        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()

        x = parent_width//2 - width//2 + parent_offset[1]
        y = parent_height//2 - height//2 + parent_offset[2]

        self.geometry("+%d+%d" % (x, y))

        self.label_info = Label(self, text="Da bi ste promenili podatke za datume starije od jednog dana neophodno je uneti šifru", pady=10)
        self.label_info.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        self.label_pw = Label(self, text="Unesite šifru:", pady=10)
        self.label_pw.grid(row=1, column=0, padx=(20, 2), sticky="e")

        self.entry = Entry(self, show="*")
        self.entry.bind("<KeyRelease-Return>", self.store_pass_event)
        self.entry.grid(row=1, column=1, padx=(2,20), sticky="w")

        self.button = Button(self, command=self.store_pass, text="Unesi")
        self.button.grid(row=2, column=0, columnspan=2, pady=10)

        self.deiconify()

    def store_pass_event(self, event):
        self.store_pass()

    def store_pass(self):
        self.master.password = self.entry.get()
        self.destroy()
