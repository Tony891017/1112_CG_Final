from PyQt6 import QtWidgets
import sys, threading
import numpy as np
import math

from drawing import *

def norm(d):
	return math.sqrt(np.dot(d, d))

class Object:
	def __init__(self):
		self.contour_points = []

	def storePosition(self, x, y):
		if x is None or y is None: return
		if self.contour_points:
			#if x == self.contour_points[-1][0] and y == self.contour_points[-1][1]: return
			if [x, y] == self.contour_points[len(self.contour_points) - 1]: return
			#if math.dist([x, y], self.contour_points[-1]) <= 1: return
		self.contour_points.append([x, y])

	def refinement(self):
		thresh = 0.98#math.cos(math.pi / 180)
		print(self.contour_points)

		#pre_p = self.contour_points[0]
		#p = self.contour_points[1]
		#pre_direct = [p[0] - pre_p[0], p[1] -  pre_p[1]]
		#pre_p = p
		#for p in self.contour_points[2:]:
		#	new_direct = [p[0] - pre_p[0], p[1] -  pre_p[1]]
			#if np.dot(pre_direct, new_direct) / (norm(pre_direct) * norm(new_direct)) > thresh:
			#	self.contour_points.remove(p)
		#	pre_direct = new_direct

		#print(self.contour_points)
		#return self.contour_points
	def getPoints(self):
		return self.contour_points


if __name__ == '__main__':
	obj1 = Object()
	app = QtWidgets.QApplication(sys.argv)
	Form = MyWidget(recorder=obj1)
	Form.show()
	sys.exit(app.exec())
