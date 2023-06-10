import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class view3D:
	def __init__(self, name="View 3D", obj=None):
		self.view_radius = -90.0
		self.theta = 3.14159 * self.view_radius / 180.0
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0

		self.obj = obj

		glutInit()
		glutCreateWindow(name)
		self.initGL()
		glutKeyboardFunc(self.keydown)
		glutDisplayFunc(self.display)
		glutIdleFunc(self.display)
		glutMainLoop()

	def drawTriangle(self, vertices, color):
		glBegin(GL_TRIANGLES)
		glColor3f(color[0], color[1], color[2])
		for v in vertices:
			glVertex3f(v[0], v[1], v[2])
		glEnd()

	def drawGrid(self, size=10):
		glBegin(GL_LINES)
		glColor3f(0.3, 0.3, 0.3)
		for i in range(1, size):
			glVertex3f(i, -size, 0)
			glVertex3f(i, size, 0)
			glVertex3f(-i, -size, 0)
			glVertex3f(-i, size, 0)

			glVertex3f(-size, i, 0)
			glVertex3f(size, i, 0)
			glVertex3f(-size, -i, 0)
			glVertex3f(size, -i, 0)
		glEnd()

		glBegin(GL_LINES)
		glColor3f(1, 0, 0)
		glVertex3f(0, 0, 0)
		glVertex3f(size, 0, 0)
		glColor3f(0.4, 0, 0)
		glVertex3f(0, 0, 0)
		glVertex3f(-size, 0, 0)

		glColor3f(0, 1, 0)
		glVertex3f(0, 0, 0)
		glVertex3f(0, size, 0)
		glColor3f(0, 0.4, 0)
		glVertex3f(0, 0, 0)
		glVertex3f(0, -size, 0)

		glColor3f(0, 0, 1)
		glVertex3f(0, 0, 0)
		glVertex3f(0, 0, size)
		glEnd()

	def display(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	   
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(60, 1, 0.1, 50)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		#gluLookAt(10 * math.cos(self.theta), -10 * math.sin(self.theta), 10, 0, 0, 0, 0, 0, 1)
		gluLookAt(self.x, self.y, 10.0, 10 * math.cos(self.theta) + self.x, -10 * math.sin(self.theta) + self.y, self.z, 0, 0, 1.0)

		self.drawGrid()
	
		self.drawTriangle([[0, 0, 0], [0, 1, 0], [0, 1, 1]], (200, 200, 200))
		if self.obj is not None:
			points, tri_indices = self.obj.getObj()
			for tri in tri_indices:
				vertices = [points[tri[0]], points[tri[1]], points[tri[2]]]
				self.drawTriangle(vertices, (200, 200, 200))

		glutSwapBuffers()

	def initGL(self):
		glClearColor(0.0, 0.0, 0.0, 1.0)
		glClearDepth(1.0)

		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)

		#light_position = [0.0, 0.0, 1000.0]
		#glLightfv(GL_LIGHT0, GL_POSITION, light_position)
		#glEnable(GL_LIGHTING)
		#glEnable(GL_LIGHT0)

	def keydown(self, key, x, y):
	
		if key == b'j':
			self.view_radius -= 5
			self.theta = 3.14159 * self.view_radius / 180.0
		if key == b'l':
			self.view_radius += 5
			self.theta = 3.14159 * self.view_radius / 180.0
		if key == b'i':
			self.z += 5
		if key == b'k':
			self.z -= 5
	
		if key == b'a':
			self.x -= 5
		if key == b'd':
			self.x += 5
		if key == b'w':
			self.y += 5
		if key == b's':
			self.y -= 5
	

if __name__ == "__main__":
	glui = view3D();
