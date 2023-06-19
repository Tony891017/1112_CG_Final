from PyQt6 import QtWidgets
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys, time, threading
import numpy as np
import math

from cv2 import convexHull

from transformFunctions import *


def vectorLength(v):
	return math.sqrt(np.dot(v, v))

def refinement(points, thresh_degree=1):
	if len(points) < 3: return points
	cos_thresh = abs(math.cos(math.pi * thresh_degree / 180))
	
	pre_p = points[0]
	p = points[1]
	new_points = [pre_p]

	pre_direct = [p[0] - pre_p[0], p[1] - pre_p[1]]
	pre_p = p
	for p in points[2:]:
		direction = [p[0] - pre_p[0], p[1] - pre_p[1]]
		pre_direct_len = vectorLength(pre_direct)
		if pre_direct_len == 0:
			pre_direct = direction
		else:
			direction_len = vectorLength(direction)
			if direction_len == 0: continue
			
			cos_angle = np.dot(direction, pre_direct) / (direction_len * pre_direct_len)
			if -cos_thresh < cos_angle < cos_thresh:
				new_points.append(pre_p)
				pre_p = p
				pre_direct = direction
	new_points.append(pre_p)
	#new_points.append(points[0])

	return new_points	

class painter(QtWidgets.QWidget):
	def __init__(self, name='CG Final', obj=None):
		super().__init__()

		self.setWindowTitle(name)
		
		# window size
		self.__height = 600
		self.__width = 600
		self.resize(self.__height, self.__width)
		self.setUpdatesEnabled(True)
		# ui
		self.__margin = 20

		# pen settings
		self.__penSize = 1
		self.__penColor = QColor('#000000')

		# projection control
		self.__rotation = [0.0, 0.0, 0.0]
		self.__distance = 50
		self.__pos = np.array([0, -self.__distance, 0])
		self.__look_at = np.array([0, 0, 0])
		self.__up_vector = np.array([0, 0, 1])
		half_width = self.__height / 2
		half_height = self.__width / 2
		self.__view_port = np.array([
			[half_width, 0, 0, half_width],
			[0, -half_height, 0, half_height],
			[0, 0, 1, 0],
			[0, 0, 0, 1]])

		self.__projection_matrix = self.__transformMatrix()
		
		# history progress
		self.__path = []
		self.__history_canvas = []
		
		# obj
		self.__obj = obj

		# start
		self.__thread_on = True
		self.__ui()

	def __ui(self):
		self.__canvas = QPixmap(self.__height, self.__width - self.__margin)
		self.__canvas.fill(QColor('#ffffff'))

		self.__label = QtWidgets.QLabel(self)
		self.__label.setGeometry(0, 0, self.__height, self.__width - self.__margin)
		self.__label.setPixmap(self.__canvas)
	
		self.__upDateView()

	def setPenColor(self, color_code='#000000'):
		self.__penColor = QColor(color_code)

	# MOUSE EVENT
	def mousePressEvent(self, event):
		self.setPenColor('#ffee00')
		self.__history_canvas.append(self.__label.pixmap())
		
	def mouseReleaseEvent(self,event): # 按下後放開
		self.__path = refinement(self.__path)	
		# 把path轉回相機畫面的座標
		path = np.array(self.__path, dtype=np.float32)
		path[:, 0] -= self.__height / 2
		path[:, 1] -= self.__width / 2
		path[:, 0] *= 2 / self.__height
		path[:, 1] *= 2 / self.__width

		if self.__obj is not None:
			success = self.__obj.saveStroke(path.tolist(), self.__pos, 'create') # 要傳入相機位置
			if success:
				self.__upDateView()
			else:
				self.setPenColor('#ff0000')
				self.painting(self.__path)
				self.__undo()
			
		self.setPenColor()
		self.__path = []
	
	def mouseMoveEvent(self, event): # 滑鼠按下後才啟動
		mx = int(QEnterEvent.position(event).x())
		my = int(QEnterEvent.position(event).y())
		if self.__path:
			if [mx, my] == self.__path[-1]: return
			self.painting([self.__path[-1], [mx, my]])
		self.__path.append([mx, my])
			
	def keyPressEvent(self, event):
		key = event.key()
		if key == 82: #r
			self.__undo()
		elif key == 74: #j
			self.__rotation[2] += 15.0
		elif key == 76: #l
			self.__rotation[2] -= 15.0
		elif key == 73: #i
			self.__rotation[0] += 15.0
		elif key == 75: #k
			self.__rotation[0] -= 15.0
		rx, ry, rz = self.__rotation
		self.__pos = rotation(np.array([0, -self.__distance, 0]), rx, ry, rz)

		if key == 48: #0
			self.__pos[0] = 0.0
			self.__pos[1] = -self.__distance
			self.__pos[2] = 0.0
			self.__rotation = [0.0, 0.0, 0.0]
		#elif key == 79: #o
		#elif key == 80: #p
		print(key) 
		self.__upDateView()

	# Painting
	def clearCanvas(self):
		self.__canvas.fill(QColor('#ffffff'))
		self.__label.setPixmap(self.__canvas)

	def painting(self, points, checkPoints=False, connected=False):
		qpainter = QPainter()
		qpainter.begin(self.__canvas)
		qpainter.setPen(QPen(self.__penColor, self.__penSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
		
		try:
			pre_point = points[0]
		except Exception:
			print("Coding Error in [painting]")
			return
		for p in points[1:]:
			if checkPoints:
				qpainter.drawPoint(p[0], p[1])
			else:
				qpainter.drawLine(pre_point[0], pre_point[1], p[0], p[1])
			pre_point = p
		if connected:
			qpainter.drawLine(pre_point[0], pre_point[1], points[0][0], points[0][1])
		qpainter.end()
		self.__label.setPixmap(self.__canvas)
		self.update()
	
	def __undo(self):
		if len(self.__history_canvas) < 1:
			print("[Already the last change.]")
		else:
			print("[Undo]")
			self.__canvas= self.__history_canvas.pop()
			self.__label.setPixmap(self.__canvas)
	
	def __upDateView(self):
		x_axis = np.array([[0, 0, 0], [1, 0, 0]]) * 100
		y_axis = np.array([[0, 0, 0], [0, 1, 0]]) * 100
		z_axis = np.array([[0, 0, 0], [0, 0, 1]]) * 100
		
		self.clearCanvas()
		self.setPenColor("#00ff00")
		self.painting(self.projection(x_axis))
		self.setPenColor("#ff0000")
		self.painting(self.projection(y_axis))
		self.setPenColor("#0000ff")
		self.painting(self.projection(z_axis))
		self.setPenColor()
		
		if self.__obj is not None:
			points, tri_indices = self.__obj.getObj()
			projected = self.projection(points)
			
			#找出最外圍的點就好
			hull = convexHull(projected)
			hull = np.reshape(hull, (len(hull), 2))

			#或用for依次畫三角形
			for tri in tri_indices:
				v0, v1, v2 = projected[tri[0]], projected[tri[1]], projected[tri[2]]
				self.painting(np.array([v0, v1, v2]), connected=True)
			self.setPenColor("#ffff00")
			self.painting(hull, connected=True)


	def projection(self, points):
		points = np.append(points, np.ones((len(points), 1)), axis=1).T
		projected = self.__transformMatrix() @ points
		projected = projected.T
		for p in projected:
			p /= p[3]
			p /= p[2]
		projected = np.int32(projected)[:, :2]
		return projected
			
	def __transformMatrix(self):
		look_at = lookAt(self.__pos, self.__look_at, self.__up_vector)
		perspect = perspective(60, 1, -1, 100)
		transform = self.__view_port @ perspect @ look_at
		return transform
	
	def closeEvent(self, event):
		self.__thread_on = False
	
		
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	user_interface = painter()
	user_interface.show()
	sys.exit(app.exec())
