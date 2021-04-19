# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import tkMessageBox
from tkcalendar import DateEntry

from collections import OrderedDict
from datetime import datetime, timedelta
from db import Database
from _print import Print
from password_dialog import PasswordDialog
from yes_no_dialog import YesNoDialog

root = Tk()
root.resizable(False, False)
root.title("Specifikacija")

DENOMINATIONS_RSD = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
DENOMINATIONS_EUR = [5, 10, 20, 50, 100, 200, 500]
DENOMINATIONS_USD = [1, 2, 5, 10, 20, 50, 100]
DENOMINATIONS_CHF = [10, 20, 50, 100, 200, 1000]

class Window(Frame):

    inputs = {
        'RSD': [],
        '€': [],
        '$': [],
        'CHF': []
    }

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        root.password = None
        root.yesno = None

        self.render()

    def render(self):
        self.set_up_frames()
        self.render_headers()
        self.render_rsd()
        self.render_eur()
        self.render_usd()
        self.render_chf()
        self.render_treeview()
        self.render_buttons()

    def set_up_frames(self):
        tab_parent = ttk.Notebook(root)
        self.tab_1 = Frame(tab_parent)
        self.tab_1.grid(column=0, row=0, sticky="nsew")

        self.tab_2 = Frame(tab_parent)
        self.tab_2.grid(column=0, row=0, sticky="nsew")
        self.tab_2.rowconfigure(1, weight=1)
        self.tab_2.columnconfigure(0, weight=1)

        tab_parent.add(self.tab_1, text="Specifikacija")
        tab_parent.add(self.tab_2, text="Istorija")

        tab_parent.pack(expand=True, fill='both')

        # tab 1
        self.frame_header_tab_1 = Frame(self.tab_1)
        self.frame_header_tab_1.grid(row=0, column=0, sticky="we", padx=10, pady=10)
        self.frame_header_tab_1.grid_columnconfigure(0, weight=1)

        frame_center_tab_1 = Frame(self.tab_1)
        frame_center_tab_1.grid(row=1, column=0, padx=10, pady=(0,10))

        frame_footer_tab_1 = Frame(self.tab_1)
        frame_footer_tab_1.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0,10))
        frame_footer_tab_1.columnconfigure(0, weight=1)

        self.frame_rsd = Frame(frame_center_tab_1)
        self.frame_rsd.grid(row=0, column=0, sticky="nsew")

        self.frame_eur = Frame(frame_center_tab_1)
        self.frame_eur.grid(row=0, column=1, sticky="nsew")

        self.frame_usd = Frame(frame_center_tab_1)
        self.frame_usd.grid(row=0, column=2, sticky="nsew")

        self.frame_chf = Frame(frame_center_tab_1)
        self.frame_chf.grid(row=0, column=3, sticky="nsew")

        self.frame_menu_tab_1 = Frame(frame_footer_tab_1)
        self.frame_menu_tab_1.grid(row=0, column=1)

        # tab 2
        self.frame_header_tab_2 = Frame(self.tab_2)
        self.frame_header_tab_2.grid(row=0, column=0, sticky="we", padx=10, pady=10)
        self.frame_header_tab_2.grid_columnconfigure(0, weight=1)

        self.frame_center_tab_2 = Frame(self.tab_2)
        self.frame_center_tab_2.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        self.frame_center_tab_2.rowconfigure(0, weight=1)
        self.frame_center_tab_2.columnconfigure(1, weight=1)

        frame_footer_tab_2 = Frame(self.tab_2)
        frame_footer_tab_2.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0,10))
        frame_footer_tab_2.columnconfigure(0, weight=1)

        self.frame_menu_tab_2 = Frame(frame_footer_tab_2)
        self.frame_menu_tab_2.grid(row=0, column=1)


    def render_headers(self):
        # tab 1
        self.title_label_tab_1 = Label(self.frame_header_tab_1, text="Specifikacija")
        self.title_label_tab_1.grid(row=0, column=0, sticky="we")

        self.calendar = DateEntry(self.frame_header_tab_1, width=12, background='darkblue',
                        foreground='white', borderwidth=2)
        self.calendar.grid(row=0, column=1, sticky="e")

        # tab 2
        self.title_label_tab_2 = Label(self.frame_header_tab_2, text="Izaberite period:")
        self.title_label_tab_2.grid(row=0, column=0)

        self.label_start_date = Label(self.frame_header_tab_2, text="Početni datum")
        self.label_start_date.grid(row=0, column=1, padx=(0,2), sticky='e')

        self.history_calendar_start = DateEntry(self.frame_header_tab_2, width=12, background='darkblue',
                        foreground='white', borderwidth=2)
        self.history_calendar_start.grid(row=0, column=2, sticky="e")

        self.label_end_date = Label(self.frame_header_tab_2, text="Završni datum")
        self.label_end_date.grid(row=0, column=3, padx=(8, 2), sticky='e')

        self.history_calendar_end = DateEntry(self.frame_header_tab_2, width=12, background='darkblue',
                        foreground='white', borderwidth=2)
        self.history_calendar_end.grid(row=0, column=4, sticky="e")

    def render_rsd(self):
        for i in range(len(DENOMINATIONS_RSD)):
            label = Label(self.frame_rsd, text="{} RSD".format(DENOMINATIONS_RSD[i]))
            label.grid(row=i, column=0, padx=2, pady=2)
            entry = Entry(self.frame_rsd)
            entry.grid(row=i, column=1, padx=2, pady=2)
            self.inputs['RSD'].append((DENOMINATIONS_RSD[i], entry))


    def render_eur(self):
        for i in range(len(DENOMINATIONS_EUR)):
            label = Label(self.frame_eur, text="{} €".format(DENOMINATIONS_EUR[i]))
            label.grid(row=i, column=0, padx=2, pady=2)
            entry = Entry(self.frame_eur)
            entry.grid(row=i, column=1, padx=2, pady=2)
            self.inputs['€'].append((DENOMINATIONS_EUR[i], entry))

    def render_usd(self):
        for i in range(len(DENOMINATIONS_USD)):
            label = Label(self.frame_usd, text="$ {}".format(DENOMINATIONS_USD[i]))
            label.grid(row=i, column=0, padx=2, pady=2)
            entry = Entry(self.frame_usd)
            entry.grid(row=i, column=1, padx=2, pady=2)
            self.inputs['$'].append((DENOMINATIONS_USD[i], entry))

    def render_chf(self):
        for i in range(len(DENOMINATIONS_CHF)):
            label = Label(self.frame_chf, text="{} CHF".format(DENOMINATIONS_CHF[i]))
            label.grid(row=i, column=0, padx=2, pady=2)
            entry = Entry(self.frame_chf)
            entry.grid(row=i, column=1, padx=2, pady=2)
            self.inputs['CHF'].append((DENOMINATIONS_CHF[i], entry))

    def render_treeview(self):
        # left treeview
        self.treeview_frame_left = ttk.Labelframe(self.frame_center_tab_2, text="Specifikacija po danima")
        self.treeview_frame_left.grid(row=0, column=0, pady=(5, 0), padx=5,  sticky="nsew")
        self.treeview_frame_left.rowconfigure(0, weight=1)

        self.treeview_left = ttk.Treeview(self.treeview_frame_left, selectmode='browse')
        self.treeview_left.grid(row=0, column=0, pady=5, padx=(5, 0), sticky="nsw")

        vertical_scrollbar_left = ttk.Scrollbar(self.treeview_frame_left,
                                            orient='vertical',
                                            command=self.treeview_left.yview)
        vertical_scrollbar_left.grid(row=0, column=1, pady=5, padx=(0, 5), sticky="nsw")

        self.treeview_left.configure(yscrollcommand = vertical_scrollbar_left.set)
        self.treeview_left['columns'] = ('1', '2', '3', '4')
        self.treeview_left['show'] = 'headings'

        self.treeview_left.column("1", width = 110, anchor ='c') 
        self.treeview_left.column("2", width = 110, anchor ='se') 
        self.treeview_left.column("3", width = 110, anchor ='se')
        self.treeview_left.column("4", width = 110, anchor ='se') 

        self.treeview_left.heading("1", text ="Datum") 
        self.treeview_left.heading("2", text ="Denominacija") 
        self.treeview_left.heading("3", text ="Količina")
        self.treeview_left.heading("4", text ="Iznos") 

        # right treeview
        self.treeview_frame_right = ttk.Labelframe(self.frame_center_tab_2, text="Specifikacija po denominaciji")
        self.treeview_frame_right.grid(row=0, column=1, pady=(5, 0), padx=5, sticky="nsew")
        self.treeview_frame_right.rowconfigure(0, weight=1)
        self.treeview_frame_right.columnconfigure(0, weight=1)

        self.treeview_right = ttk.Treeview(self.treeview_frame_right, selectmode='browse')
        self.treeview_right.grid(row=0, column=0, pady=5, padx=(5, 0), sticky="nsew")

        vertical_scrollbar_right = ttk.Scrollbar(self.treeview_frame_right,
                                            orient='vertical',
                                            command=self.treeview_right.yview)
        vertical_scrollbar_right.grid(row=0, column=1, pady=5, padx=(0, 5), sticky="nsw")

        self.treeview_right.configure(yscrollcommand = vertical_scrollbar_right.set)
        self.treeview_right['columns'] = ('1', '2', '3')
        self.treeview_right['show'] = 'headings'

        self.treeview_right.column("1", width = 110, anchor ='se') 
        self.treeview_right.column("2", width = 110, anchor ='se') 
        self.treeview_right.column("3", width = 110, anchor ='se')

        self.treeview_right.heading("1", text ="Denominacija") 
        self.treeview_right.heading("2", text ="Količina") 
        self.treeview_right.heading("3", text ="Iznos")

    def render_buttons(self):
        # tab 1
        button_get = Button(self.frame_menu_tab_1, command=self.get, text="Učitaj")
        button_get.grid(row=0, column=0, sticky="nse", padx=2, pady=2)
        button_save = Button(self.frame_menu_tab_1, command=self.save, text="Sačuvaj")
        button_save.grid(row=0, column=1, sticky="nse", padx=2, pady=2)
        button_print = Button(self.frame_menu_tab_1, command=self._print, text="Štampaj")
        button_print.grid(row=0, column=2, sticky="nse", padx=2, pady=2)
        # tab 2
        button_get_history = Button(self.frame_menu_tab_2, command=self.get_history, text="Učitaj")
        button_get_history.grid(row=0, column=0, sticky='e', padx=2, pady=2)

    def clear_inputs(self):
        for k, v in self.inputs.items():
            for label, _input in v:
                _input.delete(0, 'end')

    def prepare_values(self):
        error = False
        values = {}
        for k, v in self.inputs.items():
            validated_denomination_values = []
            for denomination, entry in v:
                quantity = entry.get()
                if quantity == '':
                    quantity = 0 
                if self.validate_input(quantity):
                    validated_denomination_values.append((denomination, int(quantity)))
                    values[k] = validated_denomination_values
                else:
                    error = True
        if not error:
            date = self.calendar.get_date()
            date = date.strftime("%Y-%m-%d")
            calculated_vales = self.calculate(values)
            request = {
                'date': date,
                'values': calculated_vales
            }
            return request
        else:
            tkMessageBox.showerror("Greška", "A-a, probaj opet")
            return False

    def validate_input(self, quantity):
        try:
            quantity = int(quantity)
            if not 0 <= quantity <= 9999:
                raise ValueError
        except ValueError:
            return False
        else:
            return True

    def calculate(self, values):
        response = {}
        for k, v in values.items():
            response[k] = {}
            total = 0
            calculated_denomination_values = []
            for denomination, quantity in v:
                amount = denomination * quantity
                total += amount    
                calculated_denomination_values.append((denomination, quantity, amount))
                response[k]['specification'] = calculated_denomination_values
            response[k]['total'] = total 
        return response

    def get(self):
        date = self.calendar.get_date()
        date = date.strftime("%Y-%m-%d")
        data = Database().get(date)

        if data:
            for _id, date, currency, denomination, quantity, amount in data:
                for k, v in self.inputs.items():
                    if k == currency:
                        for label, _input in v:
                            if label == denomination:
                                _input.delete(0, 'end')
                                _input.insert(0, quantity) 
        else:
            tkMessageBox.showinfo("Obaveštenje","Nema podataka za izabrani datum")

    def get_history(self):
        start = self.history_calendar_start.get_date()
        start = start.strftime("%Y-%m-%d")
        end = self.history_calendar_end.get_date()
        end = end.strftime("%Y-%m-%d")
        data = Database().get_by_date_range(start, end)

        for _id, date, currency, denomination, quantity, amount in data:
            if currency != '$':
                self.treeview_left.insert("", 'end', text ="L1",  
                            values = (date, "{} {}".format(denomination, currency), quantity, "{} {}".format(amount, currency)))
            else:
                self.treeview_left.insert("", 'end', text ="L1",  
                            values = (date, "{} {}".format(currency, denomination), quantity, "{} {}".format(currency, amount))) 

        self.calculate_total_for_time_period(data)

    def calculate_total_for_time_period(self, data):

        total = {}

        for _id, date, currency, denomination, quantity, amount in data:

            try:
                total[currency]
            except KeyError:
                total[currency] = {}

            try:
                total[currency][denomination]
            except KeyError:
                total[currency][denomination] = {
                    'quantity': 0,
                    'amount': 0
                }

            total[currency][denomination]['quantity'] += quantity
            total[currency][denomination]['amount'] = total[currency][denomination]['quantity'] * denomination

        for currency_key, currency_value in total.items():
            currency_value = OrderedDict(sorted(currency_value.items()))
            for denomination_key, denomination_value in currency_value.items():
                if currency_key != '$':
                    self.treeview_right.insert("", 'end', text ="L1",
                        values = ("{} {}".format(denomination_key, currency_key), denomination_value['quantity'], "{} {}".format(denomination_value['amount'], currency_key)))
                else:
                    self.treeview_right.insert("", 'end', text ="L1",
                        values = ("{} {}".format(currency_key, denomination_key), denomination_value['quantity'], "{} {}".format(currency_key, denomination_value['amount'])))

    def save(self, already_printed=False):
        request = self.prepare_values()
        if request:
            # checking if user is trying to update some older dates
            date = request['date']
            today = datetime.now()
            today = today.date()
            yesterday = today - timedelta(days=1)
            selected_date = datetime.strptime(date, "%Y-%m-%d")
            selected_date = selected_date.date()

            check_if_already_exists = Database().check_if_already_exists(request)
            save = None

            if check_if_already_exists:
                if selected_date not in (today, yesterday):
                    root.wait_window(PasswordDialog(master=root))

                    if root.password == 'metla12345':
                        save = Database().write(request, update=True)
                    else:
                        tkMessageBox.showerror("Greška", "Nemate privilegiju da menjate podatke za datume starije od jednog dana")
                else:
                    save = Database().write(request, update=True)

            else:
                save = Database().write(request)

            if save:
                if not already_printed:
                    root.wait_window(YesNoDialog(master=root, text="Da li želite da odštampate podatke?"))

                    if root.yesno:
                        self._print(already_saved=True)            
                self.clear_inputs()

    def _print(self, already_saved=False):
        request = self.prepare_values()
        if request:
            _print = Print()._print(request)
            if not already_saved:
                root.wait_window(YesNoDialog(master=root, text="Da li želite da sačuvate podatke?"))
                if root.yesno:
                    self.save(already_printed=True)
app = Window(root)
root.mainloop()
