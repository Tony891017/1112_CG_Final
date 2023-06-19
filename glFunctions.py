import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np

def normalize(n):
	return n / np.linalg.norm(n)


class view3D:
	def __init__(self, name="View 3D", obj=None):
		self.view_radius = -90.0
		self.theta = 3.14159 * self.view_radius / 180.0
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		self.look_at = [10 * math.cos(self.theta) + self.x, -10 * math.sin(self.theta) + self.y, self.z]
		
		# Light

		self.obj = obj

		glutInit()
		glutInitWindowSize(500, 500)
		glutCreateWindow(name)
		self.initGL()

		glutKeyboardFunc(self.keydown)
		glutDisplayFunc(self.display)
		glutIdleFunc(self.display)
		glutMainLoop()

	def drawTriangle(self, vertices, obj_color):
		v0, v1, v2 = vertices
		direct1 = np.subtract(v1, v0)
		direct2 = np.subtract(v2, v0)

		n = np.cross(direct1, direct2)
		n = normalize(n)
		if np.dot(n, v0) < 0: n *= -1

		glBegin(GL_TRIANGLES)
		for v in vertices:
			color = self.shading(v, n, obj_color)
			glColor3f(color[0], color[1], color[2])
			glVertex3f(v[0], v[1], v[2])
		glEnd()

	def drawGrid(self, size=50):
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
		glColor3f(0.8, 0, 0)
		glVertex3f(0, 0, 0)
		glVertex3f(-size, 0, 0)

		glColor3f(0, 1, 0)
		glVertex3f(0, 0, 0)
		glVertex3f(0, size, 0)
		glColor3f(0, 0.8, 0)
		glVertex3f(0, 0, 0)
		glVertex3f(0, -size, 0)

		glColor3f(0, 0, 1)
		glVertex3f(0, 0, 0)
		glVertex3f(0, 0, size)
		glEnd()
	
	def shading(self, p, n, color):
		light_position = [100.0, 100.0, 150.0]
		light_direction = np.subtract(light_position, [0.0, 0.0, 0.0])
		camera_position = [self.x, self.y, self.z]
		view_vector = np.subtract(camera_position, p)#[0.0, 0.0, 0.0])

		r = np.dot(light_direction, n) * 2 * n - light_direction
		r = normalize(r)
		l = normalize(light_direction)

		K_d, K_s, K_a = [0.6, 0.6, 0.6], [0.4, 0.4, 0.4], color
		I_d, I_s, I_a = [0.8, 0.8, 0.8], [0.01, 0.01, 0.01], [0.5, 0.5, 0.5]

		diffuse = np.multiply(K_d, I_d) * max(0, np.dot(l, n))
		specular = np.multiply(K_s, I_s) * math.pow(np.dot(view_vector, r), 2)
		ambient = np.multiply(K_a, I_a)
	
		color = diffuse + specular + ambient
		return color


	def display(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	   
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(60, 1, 0.1, 50)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		gluLookAt(self.x, self.y, 10.0, self.look_at[0], self.look_at[1], self.look_at[2], 0, 0, 1.0)

		self.drawGrid()
	
		color = [0.5, 0.5, 1.0]
		if self.obj is not None:
			points, tri_indices = self.obj.getObj()
			for tri in tri_indices:
				vertices = [points[tri[0]], points[tri[1]], points[tri[2]]]
				self.drawTriangle(vertices, color)

		glutSwapBuffers()

	def initGL(self):
		glClearColor(0.0, 0.0, 0.0, 1.0)
		glClearDepth(1.0)

		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)


	def keydown(self, key, x, y):
	
		if key == b'j':
			self.view_radius -= 5
			self.theta = 3.14159 * self.view_radius / 180.0
		if key == b'l':
			self.view_radius += 5
			self.theta = 3.14159 * self.view_radius / 180.0
		if key == b'i':
			self.z += 1
		if key == b'k':
			self.z -= 1
	
		if key == b'a':
			self.x -= 5
		if key == b'd':
			self.x += 5
		if key == b'w':
			self.y += 5
		if key == b's':
			self.y -= 5
		self.look_at = [10 * math.cos(self.theta) + self.x, -10 * math.sin(self.theta) + self.y, self.z]
	

if __name__ == "__main__":
	glui = view3D()
