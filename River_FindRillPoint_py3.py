import arcpy
import os
import numpy

group_layer = arcpy.GetParameter(0)

output_point_name = arcpy.GetParameterAsText(1)
threshold = arcpy.GetParameter(2)

arcpy.env.workspace = os.path.dirname(output_point_name)
arcpy.env.overwriteOutput = True

def FindRillPoint(avg_list, group_list) :
	if len(avg_list) < 4 :
		return [group_list[0][-1], group_list[-1][0]]
	returnList = []

	FirstPoint, SecondPoint, ThirdPoint, FourthPoint = -1, 0, -1, 0
	for count, avg in enumerate(avg_list) :

		if FirstPoint == -1 :
			if len(avg_list) - count < 3 :
				# returnList.append(group_list[-1][0])
				break

			FirstPoint = avg
			continue
		if not SecondPoint :
			if FirstPoint > avg :
				SecondPoint = avg
				returnList.append(group_list[count][-1])
				continue
			else :
				FirstPoint = avg
		else :
			if ThirdPoint == -1 :
				ThirdPoint = avg
				continue
			if not FourthPoint :
				if ThirdPoint < avg :
					FourthPoint = avg
					returnList.append(group_list[count][0])
					FirstPoint, SecondPoint, ThirdPoint, FourthPoint = -1, 0, -1, 0
					continue
				else :
					ThirdPoint = avg
	if SecondPoint :
		returnList.append(group_list[-1][0])
	if len(returnList) == 0 :
		returnList = [group_list[0][-1], group_list[-1][0]]
	return returnList

arcpy.CreateFeatureclass_management(os.path.dirname(output_point_name), os.path.basename(output_point_name), 'POINT', has_m= 'DISABLED', has_z= 'DISABLED', spatial_reference= arcpy.SpatialReference(3826))
arcpy.AddFields_management(output_point_name, [
	['Code', 'TEXT', 'Code'],
	['ForSheet', 'LONG', 'ForSheet'],
	['RASTERVALU', 'DOUBLE', 'RASTERVALU']
])

cursor = arcpy.da.InsertCursor(output_point_name, ['Code', 'ForSheet', 'RASTERVALU', 'Shape@'])
code_list = list(set([row[0][:-5] for row in arcpy.da.SearchCursor(group_layer, ['Code'])]))
code_list.sort()
for code in code_list :
	# arcpy.MakeFeatureLayer_management(group_layer, 'Group_temp_layer', f"Code LIKE '{code}%'")
	rows = arcpy.da.SearchCursor(group_layer, ['Code', 'ForSheet', 'RASTERVALU', 'Shape@'], where_clause= f"Code LIKE '{code}%'", sql_clause= (None, "ORDER BY ForSheet"))
	groups = []
	temp_list = []

	for count, row in enumerate(rows) :
		if count != 0 :
			if abs(row[2]-base) > threshold :
				groups.append(temp_list)
				temp_list = []
				base = row[2]
			temp_list.append(row)
		else :
			base = row[2]    
			temp_list.append(row)
	groups.append(temp_list)     

	avg_list= [numpy.mean([j[2] for j in i]) for i in groups]
	
	rill_point = FindRillPoint(avg_list, groups)
	for p in rill_point :
		cursor.insertRow(p)
		# print(row[0], row[1], row[2])
	# arcpy.Delete_management('Group_temp_layer')
	# print(code)
del cursor