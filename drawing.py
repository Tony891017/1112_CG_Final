from PyQt6 import QtWidgets
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys, time, threading
import numpy as np
import math

def vectorLength(v):
	return math.sqrt(np.dot(v, v))

def refinement(points, thresh_degree=1):
	if len(points) < 2: return points
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

	return new_points	
			
			

class painter(QtWidgets.QWidget):
	def __init__(self, name='CG Final'):
		super().__init__()

		self.setWindowTitle(name)
		
		# window size
		self.__height = 750
		self.__width = 500
		self.resize(self.__height, self.__width)
		self.setUpdatesEnabled(True)
		# ui
		self.__margin = 20

		# pen settings
		self.__penSize = 1
		self.__penColor = QColor('#000000')

		# io controler
		
		# history progress
		self.__recorder = []
		self.__path = []
		self.__history_canvas = []
		
		# start
		self.__ui()

	def __ui(self):
		self.__canvas = QPixmap(self.__height, self.__width - self.__margin)
		self.__canvas.fill(QColor('#ffffff'))

		self.__label = QtWidgets.QLabel(self)
		self.__label.setGeometry(0, 0, self.__height, self.__width - self.__margin)
		self.__label.setPixmap(self.__canvas)


	def setPenColor(self, color_code='#000000'):
		self.__penColor = QColor(color_code)

	def mousePressEvent(self, event):
		self.__history_canvas.append(self.__label.pixmap())
		
	def mouseReleaseEvent(self,event): # 按下後放開
		self.__path = refinement(self.__path)
		self.__recorder.append(self.__path)
		#print(len(self.__recorder))

		self.setPenColor('#ffee00')
		self.painting(self.__path)
		#self.setPenColor('#ff0000')
		#self.painting(self.__path, checkPoints=True)
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
		if event.key() == 82:
			self.__undo()

	def painting(self, points, checkPoints=False):
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
			
	
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	user_interface = painter()
	user_interface.show()
	sys.exit(app.exec())
