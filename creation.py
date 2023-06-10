import numpy as np
import math
from cv2 import moments 

def centerOfGravity(vertices):
	m = moments(np.append(vertices, vertices[0:1], axis=0))
	mx = int(m['m10'] / m['m00'])
	my = int(m['m01'] / m['m00'])
	return mx, my

def incenter(v1, v2, v3):
	x1, y1 = v1
	x2, y2 = v2
	x3, y3 = v3
	# 計算三邊長
	a = math.sqrt((x2 - x3)**2 + (y2 - y3)**2)
	b = math.sqrt((x1 - x3)**2 + (y1 - y3)**2)
	c = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

	# 計算半周長
	s = (a + b + c) / 2

	# 計算面積
	area = math.sqrt(s * (s - a) * (s - b) * (s - c))

	# 計算內心座標
	x = (a * x1 + b * x2 + c * x3) / (a + b + c)
	y = (a * y1 + b * y2 + c * y3) / (a + b + c)

	return np.array([x, y])


#def sortToConvex(vertices):
#	centroid = np.mean(vertices, axis=0)
#	angles = np.arctan2(vertices[:, 1] - centroid[1], vertices[:, 0] - centroid[0])
#	sorted = vertices[np.argsort(angles)]
#	return sorted

def scaling(center, vertices, scaler):
	scaled = np.empty((0, 2))
	for v in vertices:
		scaled_v = (v - center) * scaler + center
		scaled = np.append(scaled, [scaled_v], axis=0)
	scaled = np.array(scaled, dtype=np.int64)
	return scaled


# 等高線
def elevation(vertices, segments=10, r=1, offset=0): #b決定高度(float)
	gx, gy = centerOfGravity(vertices)
	center = np.array([gx, gy])

	max_x = math.sqrt(r * r - offset * offset)
	fx = lambda x: math.sqrt((r + x) * (r - x)) - offset

	height = np.array([fx(max_x)])
	contours = np.array([vertices])

	for i in range(1, segments):
		height = np.append(height, [fx(max_x * (segments - i) / segments)], axis=0)
		scaled_points = scaling(center, vertices, 1 - i/segments)
		contours = np.append(contours, [scaled_points], axis=0)

	height = np.repeat(height, vertices.shape[0], axis=0)
	height = np.reshape(height, (segments, vertices.shape[0], 1))
	elevated_vertices = np.append(contours, height, axis=2)
	
	return elevated_vertices
 

 
