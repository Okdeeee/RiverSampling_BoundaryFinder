import arcpy
import os
import numpy as np

river_layer = arcpy.GetParameter(0)
ouptut_layer_path = arcpy.GetParameter(1)
river_code_field = arcpy.GetParameter(2)
split_dist = arcpy.GetParameter(3)
extend_dist = arcpy.GetParameter(4)
sampling_distance = arcpy.GetParameter(5)

arcpy.env.workspace = os.path.dirname(ouptut_layer_path.value)

#	Code = [AA][0000][+/-0000]
def points_along_line(line_lyr, pnt_layer, pnt_dist, extend_dirt):
	"""
	line_lyr (feature layer) - Single part line
	pnt_layer (feature layer) - Path to point feature class
	pnt_dist (integer) - Interval distance in map units to add points
	"""
	if not arcpy.Exists(pnt_layer):
		arcpy.CreateFeatureclass_management(os.path.dirname(pnt_layer.value), os.path.basename(pnt_layer.value), 'POINT', spatial_reference=arcpy.SpatialReference(3826))

	arcpy.AddField_management(pnt_layer, 'Code', 'TEXT', field_scale=20)

	search_cursor = arcpy.da.SearchCursor(line_lyr, field_names= ['SHAPE@', river_code_field.value])
	insert_cursor = arcpy.da.InsertCursor(pnt_layer, field_names= ['SHAPE@', 'Code'])

	for row in search_cursor:
		for n, dist in enumerate(np.arange(0, row[0].length, pnt_dist)):
			point = row[0].positionAlongLine(dist)
			insert_cursor.insertRow([point, f'{row[1]}{n:>04}+0000'])
			# insert_cursor.insertRow([arcpy.Polyline(arcpy.Array([point.pointFromAngleAndDistance(90, extend_dirt, 'PLANAR').firstPoint, point.firstPoint, point.pointFromAngleAndDistance(270, extend_dirt, 'GEODESIC').firstPoint]))])
			for count, sample in enumerate(np.arange(0 ,extend_dist, sampling_distance)) :
				if sample == 0.0 :
					r_point = point.pointFromAngleAndDistance(90, sampling_distance, 'PLANAR')
					l_point = point.pointFromAngleAndDistance(270, sampling_distance, 'PLANAR')
				else :
					r_point = r_point.pointFromAngleAndDistance(90, sampling_distance, 'PLANAR')
					l_point = l_point.pointFromAngleAndDistance(270, sampling_distance, 'PLANAR')			
				insert_cursor.insertRow([r_point, f'{row[1]}{n:>04}+{count+1:>04}'])
				insert_cursor.insertRow([l_point, f'{row[1]}{n:>04}-{count+1:>04}'])		




#   EX: points_along_line(r'E:\work\VDR\VDR.gdb\river', r'E:\work\VDR\VDR.gdb\river_output_point', 0.05)
points_along_line(river_layer, ouptut_layer_path, split_dist, extend_dist)
arcpy.CalculateField_management(ouptut_layer_path, 'ForSheet', "int(f'{!Code![-5]}{int(!Code![-4:])}')", 'PYTHON3', '', 'LONG')