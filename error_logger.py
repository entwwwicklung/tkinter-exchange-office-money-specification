# -*- coding: utf-8 -*-
import tkMessageBox
from datetime import datetime

class ErrorLogger:

    def log(self, error, error_description):

        try:
            with open("specifikacija_error_log.txt", "a") as f:

                f.write("{}: {} --- {}".format(datetime.now(), error, error_description))

        except Exception:

            tkMessageBox.showerror("Greška", "Greška prilikom logovanja")
