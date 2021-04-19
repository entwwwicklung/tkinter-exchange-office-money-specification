# -*- coding: utf-8 -*-
from datetime import datetime
from error_logger import ErrorLogger

from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize

import tempfile
import tkMessageBox
import win32api

PAGE_WIDTH  = defaultPageSize[0]
PAGE_HEIGHT = defaultPageSize[1]

class Print():

	pdf_file = None
	canvas = None

	def __init__(self):
		self.pdf_file = tempfile.mktemp(".pdf")
		self.canvas = canvas.Canvas(self.pdf_file)

	def _print(self, values):
		self.generate_pdf(values)
		self.print_to_printer()
		return True

	def generate_pdf(self, request):

		date = datetime.strptime(request['date'], "%Y-%m-%d").strftime("%d.%m.%Y.")
		self.canvas.setFont("Helvetica-Bold", 16)
		self.canvas.drawCentredString(PAGE_WIDTH // 2, PAGE_HEIGHT - 50, "Specifikacija za {}".format(date))

		values = request['values']

		start_point_x = 30
		start_point_y = PAGE_HEIGHT - 100

		counter = 1

		for k, v in values.items():
			if counter == 3:
				start_point_x = PAGE_WIDTH // 2 + 30
				start_point_y = PAGE_HEIGHT - 100
			counter += 1
			self.canvas.setFont("Helvetica-Bold", 14)
			self.canvas.drawString(start_point_x, start_point_y, "{}".format(k))
			start_point_y -= 40
			self.canvas.setFont("Helvetica", 14)

			for denomination, quantity, amount in v['specification']:
				if k == '$':
					self.canvas.drawString(start_point_x, start_point_y, "{} {}".format(k, denomination))
					self.canvas.drawString(start_point_x + 50, start_point_y, "x")
					self.canvas.drawString(start_point_x + 70, start_point_y, "{}".format(quantity))
					self.canvas.drawString(start_point_x + 110, start_point_y, "=")
					self.canvas.drawString(start_point_x + 130, start_point_y, "{} {}".format(k, amount))
				elif k == '€':
					self.canvas.drawString(start_point_x, start_point_y, "{} {}".format(denomination, k))
					self.canvas.drawString(start_point_x + 50, start_point_y, "x")
					self.canvas.drawString(start_point_x + 70, start_point_y, "{}".format(quantity))
					self.canvas.drawString(start_point_x + 110, start_point_y, "=")
					self.canvas.drawString(start_point_x + 130, start_point_y, "{} {}".format(amount, k))					
				else:
					self.canvas.drawString(start_point_x, start_point_y, "{} {}".format(denomination, k))
					self.canvas.drawString(start_point_x + 80, start_point_y, "x")
					self.canvas.drawString(start_point_x + 100, start_point_y, "{}".format(quantity))
					self.canvas.drawString(start_point_x + 140, start_point_y, "=")
					self.canvas.drawString(start_point_x + 160, start_point_y, "{} {}".format(amount, k))
				start_point_y -= 20
			start_point_y -= 20
			self.canvas.setFont("Helvetica-Bold", 14)
			if k == '$':
				self.canvas.drawString(start_point_x, start_point_y, "Ukupno: {} {}".format(k, v['total']))
			else:
				self.canvas.drawString(start_point_x, start_point_y, "Ukupno: {} {}".format(v['total'], k))
			start_point_y -= 60

		self.canvas.showPage()
		self.canvas.save()
		return True

	def print_to_printer(self):
		# This only works on 32bit Windows!
		try:
			win32api.ShellExecute (0, "print", self.pdf_file, None, ".", 0)

			return True

		except Exception as error:
			error_description = "Došlo je do greške prilikom štampanja"
			tkMessageBox.showerror("Greška", error_description)
			ErrorLogger().log(error, error_description)

			return False

