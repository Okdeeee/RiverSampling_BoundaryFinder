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

river_layer = arcpy.GetParameter(0)
ouptut_layer_path = arcpy.GetParameter(1)
in_raster = arcpy.GetParameter(2)
river_code_field = arcpy.GetParameter(3)
split_dist = arcpy.GetParameter(4)
extend_dist = arcpy.GetParameter(5)
sampling_distance = arcpy.GetParameter(6)

arcpy.env.workspace = os.path.dirname(ouptut_layer_path.value)
arcpy.env.overwriteOutput = True

root_path = os.path.dirname(ouptut_layer_path.value)
#	Code = [AA][0000][+/-0000]
#	製作河流取樣點圖層
def points_along_line(line_lyr, pnt_layer, pnt_dist, extend_dist):
	"""
	line_lyr (feature layer) - Single part line
	pnt_layer (feature layer) - Path to point feature class
	pnt_dist (integer) - Interval distance in map units to add points
	"""
	if not arcpy.Exists(pnt_layer):
		arcpy.CreateFeatureclass_management(os.path.dirname(pnt_layer.value), 'River_temp_layer', 'POINT', spatial_reference=arcpy.SpatialReference(3826))

	arcpy.AddField_management('River_temp_layer', 'Code', 'TEXT', field_scale=20)

	search_cursor = arcpy.da.SearchCursor(line_lyr, field_names= ['SHAPE@', river_code_field.value])
	insert_cursor = arcpy.da.InsertCursor('River_temp_layer', field_names= ['SHAPE@', 'Code'])

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

def groupSamplingPoint(point_layer, output_layer) :
	arcpy.CreateFeatureclass_management(os.path.dirname(output_layer), )
	code_list = list(set([row[0][-5:] for row in arcpy.da.SearchCursor(point_layer, ['Code'])]))
	for key in code_list :
		arcpy.MakeFeatureLayer_management(point_layer, 'code_temp_layer', f"Code = '{key}'")
		rows = arcpy.da.SearchCursor('code_temp_layer', ['Code', 'ForSheet'])


#	製作河流取樣點圖層
points_along_line(river_layer, ouptut_layer_path, split_dist, extend_dist)
#	製作圖表用索引欄位
arcpy.CalculateField_management('River_temp_layer', 'ForSheet', "int(f'{!Code![-5]}{int(!Code![-4:])}')", 'PYTHON3', '', 'LONG')
# #	將raster數值丟進點圖層
# arcpy.sa.ExtractValuesToPoints('River_temp_layer', in_raster, 'Raster_value_river_layer', 'NONE', 'VALUE_ONLY')
