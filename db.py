# -*- coding: utf-8 -*-
from error_logger import ErrorLogger
import sqlite3
import tkMessageBox

class Database():

    conn = None
    c = None

    def __init__(self):
        self.conn = sqlite3.connect('specification.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()

    def get(self, date):

        data = self.c.execute("SELECT * FROM data WHERE date = ?", [date])
        data = data.fetchall()
        return data

    def get_by_date_range(self, start, end):

        data = self.c.execute("""
        SELECT * FROM data WHERE
        date BETWEEN ? AND ?
        """, [start, end])
        data = data.fetchall()

        return data

    def check_if_already_exists(self, data):

        date = data['date']
        already_exist = self.c.execute("SELECT id FROM data WHERE date = ?", [date])
        already_exist = already_exist.fetchall()
        if len(already_exist) == 0:
            return False
        else:
            return True

    def write(self, data, update=False):

        date = data['date']
        values = data['values']
        records = []

        try:
            for k, v in values.items():
                for denomination, quantity, amount in v['specification']:
                    records.append((date, k, denomination, quantity, amount))

            if not update:
                self.c.executemany("INSERT INTO data(date, currency, denomination, quantity, amount) VALUES (?, ?, ?, ?, ?)", records)

                if self.c.rowcount == 0:
                    tkMessageBox.showerror("Greška", "Neki podaci se nisu upisali u bazu")
                else:
                    tkMessageBox.showinfo("Obaveštenje", "Podaci su uspešno sačuvani")

            else:
                row_counts = []
                for date, currency, denomination, quantity, amount in records:
                    self.c.execute("""
                    UPDATE data SET
                    quantity = ?,
                    amount = ?
                    WHERE date = ?
                    and currency = ?
                    and denomination = ?
                    """, [quantity, amount, date, currency, denomination])

                    row_counts.append(self.c.rowcount)

                if 0 in row_counts:
                    tkMessageBox.showerror("Greška", "Neki podaci se nisu upisali u bazu")
                else:
                    tkMessageBox.showinfo("Obaveštenje", "Podaci su uspešno sačuvani")

            self.conn.commit()
            self.conn.close()

            return True

        except Exception as error:
            error_description = "Došlo je do greške prilikom upisivanja podataka u bazu"
            tkMessageBox.showerror("Greška", error_description)
            ErrorLogger().log(error, error_description)

            return False
