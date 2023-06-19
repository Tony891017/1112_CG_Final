import numpy as np
import math

def lookAt(eye, at, up):
	forward = np.subtract(at, eye)
	forward = forward / np.linalg.norm(forward)

	right = np.cross(forward, up)
	right = right / np.linalg.norm(right)

	UP = np.cross(right, forward)
	
	rotation_matrix = np.array([
		[right[0], right[1], right[2], 0],
		[UP[0], UP[1], UP[2], 0],
		[-forward[0], -forward[1], -forward[2], 0],
		[0, 0, 0, 1]
	])

	translation_matrix = np.array([
		[1, 0, 0, -eye[0]],
		[0, 1, 0, -eye[1]],
		[0, 0, 1, -eye[2]],
		[0, 0, 0, 1]
	])
	
	view_matrix = np.dot(rotation_matrix, translation_matrix)

	return view_matrix

def perspective(fovy, aspect, zNear, zFar):
	f = 1.0 / math.tan(fovy * math.pi / 360.0)
	alpha = (zFar + zNear) / (zNear - zFar)
	beta = 2.0 * zFar * zNear / (zNear - zFar)

	perspective_matrix = np.array([
		[f / aspect, 0, 0, 0],
		[0, f, 0, 0],
		[0, 0, alpha, beta],
		[0, 0, -1.0, 0]
	])

	return perspective_matrix

def rotation(points, x_degree, y_degree, z_degree):
	x_sin = math.sin(x_degree)
	x_cos = math.cos(x_degree)
	rotate_x = np.array([[1, 0, 0], [0, x_cos, -x_sin], [0, x_sin, x_cos]])

	y_sin = math.sin(y_degree)
	y_cos = math.cos(y_degree)
	rotate_y = np.array([[y_cos, 0, y_sin], [0, 1, 0], [-y_sin, 0, y_cos]])
	
	z_sin = math.sin(z_degree)
	z_cos = math.cos(z_degree)
	rotate_z = np.array([[z_cos, -z_sin, 0], [z_sin, z_cos, 0], [0, 0, 1]])

	rotation = rotate_x @ rotate_y @ rotate_z
	
	rotated_points = (rotation @ points.T).T
	return rotated_points
