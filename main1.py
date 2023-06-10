from PyQt6 import QtWidgets
from scipy import spatial

import sys, threading
import numpy as np
import math
import cv2

import objFile

from drawing import *
from glFunctions import *

from creation import elevation
from creation import incenter


class Object:
	def __init__(self):
		self.contour_points = []
		self.triangle_indices = []

	def saveStroke(self, stroke_points, mode):
		if not self.__validStroke(stroke_points): return False
		if mode == 'create':
			self.__createObj(stroke_points)
		return True

	def getObj(self):
		return self.contour_points, self.triangle_indices
	
	def storeObj(self, contour_points, triangle_indices):
		self.contour_points = contour_points.tolist()
		self.triangle_indices = contour_points.tolist()
		

	def __validStroke(self, stroke):
		if len(stroke) < 3: return False
		head_index = 1
		tail_index = len(stroke) - 2

		while head_index < tail_index:
			head_index += 1
			tail_index -= 1
		return True
	
	def __createObj(self, stroke):
		contour_lines = np.int32(elevation(np.array(stroke), 20, 50))

		segs, nps, dim = contour_lines.shape
		elevated_points = np.reshape(contour_lines, (segs * nps, dim))

		tri = spatial.Delaunay(elevated_points[:, 0:2])
		triangle_indices = self.__removeRedundantTriangles(elevated_points[:, :2], tri.simplices, nps)

		mirror_points = elevated_points
		mirror_points[:, 2] *= -1
		mirror_tri = triangle_indices + elevated_points.shape[0]

		# Store
		contour_points = np.append(elevated_points, mirror_points, axis=0)
		triangle_indices = np.append(triangle_indices, mirror_tri, axis=0)
		self.storeObj(elevated_points, triangle_indices)
		
		#objFile.objFileWriter(self.contour_points, self.triangle_indices, "./test_file.obj")
	
	def __removeRedundantTriangles(self, points, triangle_indices, edge_nps):
		contour_img = np.zeros((max(points[:, 1] + 1), max(points[:, 0] + 1), 3), dtype=np.uint8)

		points = np.array(points)
		cnt_ps = np.reshape(points[:edge_nps], (1, edge_nps, 2))
		contour_img = cv2.fillPoly(contour_img, pts=cnt_ps, color=(255, 255, 255))
		contour_img = cv2.cvtColor(contour_img, cv2.COLOR_BGR2GRAY)

		clean_indices = []
		for tri in triangle_indices:
			i0, i1, i2 = tri
			v0, v1, v2 = points[i0], points[i1], points[i2]
			mid_01 = (v0 + v1) // 2
			mid_12 = (v1 + v2) // 2
			mid_20 = (v2 + v0) // 2
			#x, y = incenter(points[v0], points[v1], points[v2])
			valid = True
			for x, y in [mid_01, mid_12, mid_20]:
				if contour_img[y][x] < 1: valid = False
			if valid: clean_indices.append(tri)
		return np.array(clean_indices)


if __name__ == '__main__':
	obj1 = Object()
	app = QtWidgets.QApplication(sys.argv)
	painter_ui = painter(obj=obj1)
	painter_ui.show()
	
	glui = view3D(obj=obj1)
	sys.exit(app.exec())
