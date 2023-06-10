#OBJ file output
def objFileWriter(points, triangle_indices, file_name):
	output_file = open(file_name, "w")
	for v in points:
		output_str = "v"
		for x in v:
			output_str += " " + str(x)
		output_str += "\n"
		output_file.write(output_str)

	"""
	mirror_points = points
	mirror_points[:, 2] *= -1
	for v in mirror_points:
		output_str = "v"
		for x in v:
			output_str += " " + str(x)
		output_str += "\n"
		output_file.write(output_str)
	"""
	for i in triangle_indices:
		output_str = "f"
		for j in i:
			output_str += " " + str(j + 1)
		output_str += "\n"
		output_file.write(output_str)
	"""
	offset = len(points)
	for i in triangle_indices:
		output_str = "f"
		for j in i:
			output_str += " " + str(j + 1 + offset)
		output_str += "\n"
		output_file.write(output_str)
	"""
	output_file.close()
