import arcpy
import os
import numpy as np

river_layer = arcpy.GetParameter(0)
ouptut_layer_path = arcpy.GetParameter(1)
split_dist = arcpy.GetParameter(2)
extend_dirt = arcpy.GetParameter(3)

arcpy.env.workspace = os.path.dirname(ouptut_layer_path.value)


def points_along_line(line_lyr, pnt_layer, pnt_dist, extend_dirt):
    """
    line_lyr (feature layer) - Single part line
    pnt_layer (feature layer) - Path to point feature class
    pnt_dist (integer) - Interval distance in map units to add points
    """
    if not arcpy.Exists(pnt_layer):
        arcpy.CreateFeatureclass_management(os.path.dirname(pnt_layer.value), os.path.basename(pnt_layer.value), 'POLYLINE', spatial_reference=arcpy.SpatialReference(3826))

    search_cursor = arcpy.da.SearchCursor(line_lyr, field_names= ['SHAPE@'])
    insert_cursor = arcpy.da.InsertCursor(pnt_layer, field_names= ['SHAPE@'])

    for row in search_cursor:
        for dist in np.arange(0, row[0].length, pnt_dist):
            point = row[0].positionAlongLine(dist)
            insert_cursor.insertRow([arcpy.Polyline(arcpy.Array([point.pointFromAngleAndDistance(90, extend_dirt, 'PLANAR').firstPoint, point.firstPoint, point.pointFromAngleAndDistance(270, extend_dirt, 'GEODESIC').firstPoint]))])




#   EX: points_along_line(r'E:\work\VDR\VDR.gdb\river', r'E:\work\VDR\VDR.gdb\river_output_point', 0.05)
points_along_line(river_layer, ouptut_layer_path, split_dist, extend_dirt)