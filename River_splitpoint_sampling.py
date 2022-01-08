# coding=utf-8
import arcpy
import os
import numpy as np

# river_layer = arcpy.GetParameter(0)
# ouptut_layer_path = arcpy.GetParameter(1)
# in_raster = arcpy.GetParameter(2)
# river_code_field = arcpy.GetParameter(3)
# split_dist = arcpy.GetParameter(4)
# extend_dist = arcpy.GetParameter(5)
# sampling_distance = arcpy.GetParameter(6)

river_layer = arcpy.GetParameterAsText(0)
ouptut_layer_path = arcpy.GetParameterAsText(1)
# in_raster = arcpy.GetParameter(2)
river_code_field = arcpy.GetParameter(2)
split_dist = arcpy.GetParameter(3)
extend_dist = arcpy.GetParameter(4)
sampling_distance = arcpy.GetParameter(5)
sampleType = arcpy.GetParameterAsText(6)

arcpy.env.workspace = os.path.dirname(ouptut_layer_path)
arcpy.env.overwriteOutput = True

root_path = os.path.dirname(ouptut_layer_path)
#	Code = [AA][0000][+/-0000]
def points_along_line(line_lyr, pnt_layer, pnt_dist, extend_dist) :
	"""
	line_lyr (feature layer) - Single part line
	pnt_layer (feature layer) - Path to point feature class
	pnt_dist (integer) - Interval distance in map units to add points
	"""
	arcpy.AddMessage(arcpy.Describe(line_lyr).spatialReference)

	if not arcpy.Exists(pnt_layer):
		arcpy.CreateFeatureclass_management(os.path.dirname(pnt_layer), os.path.basename(pnt_layer), 'POINT', has_m= 'DISABLED', has_z= 'DISABLED', spatial_reference=arcpy.Describe(line_lyr).spatialReference)

	arcpy.AddField_management(pnt_layer, 'Code', 'TEXT', field_scale=20)

	search_cursor = arcpy.da.SearchCursor(line_lyr, field_names= ['SHAPE@', river_code_field.value])
	insert_cursor = arcpy.da.InsertCursor(pnt_layer, field_names= ['SHAPE@', 'Code'])
	if sampleType == 'Horizontal' :
		r = 90
		l = 270
	elif sampleType == 'Vertical' :
		r = 0
		l = 180

	for row in search_cursor:
		for n, dist in enumerate(np.arange(0, row[0].length, pnt_dist)):
			point = row[0].positionAlongLine(dist)
			insert_cursor.insertRow([point, '{}{:>04}+0000'.format(row[1], n)])
			# insert_cursor.insertRow([arcpy.Polyline(arcpy.Array([point.pointFromAngleAndDistance(90, extend_dirt, 'PLANAR').firstPoint, point.firstPoint, point.pointFromAngleAndDistance(270, extend_dirt, 'GEODESIC').firstPoint]))])
			for count, sample in enumerate(np.arange(0 ,extend_dist, sampling_distance)) :
				if sample == 0.0 :
					r_point = point.pointFromAngleAndDistance(r, sampling_distance, 'PLANAR')
					l_point = point.pointFromAngleAndDistance(l, sampling_distance, 'PLANAR')
				else :
					r_point = r_point.pointFromAngleAndDistance(r, sampling_distance, 'PLANAR')
					l_point = l_point.pointFromAngleAndDistance(l, sampling_distance, 'PLANAR')
				insert_cursor.insertRow([r_point, '{}{:>04}+{:>04}'.format(row[1], n, count+1)])
				insert_cursor.insertRow([l_point, '{}{:>04}-{:>04}'.format(row[1], n, count+1)])


points_along_line(river_layer, ouptut_layer_path, split_dist, extend_dist)

arcpy.AddField_management(ouptut_layer_path, 'ForSheet', 'LONG')
arcpy.CalculateField_management(ouptut_layer_path, 'ForSheet', "int('{}{}'.format(!Code![-5], int(!Code![-4:])))", 'PYTHON', '' )

# arcpy.sa.ExtractValuesToPoints('River_temp_layer', in_raster, 'Raster_value_river_layer', 'NONE', 'VALUE_ONLY')
