import arcpy
import os

group_layer = r'D:\River\River.gdb\Raster_value_river_layer'

code_list = list(set([row[0][:-5] for row in arcpy.da.SearchCursor(group_layer, ['Code'])]))
for code in code_list :
    # arcpy.MakeFeatureLayer_management(group_layer, 'Group_temp_layer', f"Code LIKE '{code}%'")
    rows = arcpy.da.SearchCursor(group_layer, ['Code', 'ForSheet', 'RASTERVALU'], where_clause=f"Code LIKE '{code}%'", sql_clause= (None, "ORDER BY ForSheet"))
    for row in rows :
        print(row[0], row[1], row[2])
    # arcpy.Delete_management('Group_temp_layer')
    # print(code)