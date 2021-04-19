# -*- coding: utf-8 -*-
from Tkinter import *

class YesNoDialog(Toplevel):

    def __init__(self, master=None, text=None):
        Toplevel.__init__(self, master)
        self.master = master

        self.withdraw()

        self.title("")

        width = 280
        height = 100

        parent_offset = tuple(int(_) for _ in self.master.geometry().split('x')[1].split('+'))

        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()

        x = parent_width//2 - width//2 + parent_offset[1]
        y = parent_height//2 - height//2 + parent_offset[2]

        self.geometry("%dx%d+%d+%d" % (width, height, x, y))

        self.label_info = Label(self, text=text, pady=10)
        self.label_info.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        self.button_yes = Button(self, command=self.yes, text="Da")
        self.button_yes.grid(row=1, column=0, pady=5, padx=2, sticky="e")

        self.button_no = Button(self, command=self.no, text="Ne")
        self.button_no.grid(row=1, column=1, pady=5, padx=2, sticky="w")

        self.deiconify()

    def yes(self):
        self.master.yesno = True
        self.destroy()

    def no(self):
        self.master.yesno = False
        self.destroy()
