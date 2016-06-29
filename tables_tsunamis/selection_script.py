import arcpy
arcpy.CheckOutExtension('Spatial')
arcpy.env.overwriteOutput=True

#reclassify
def create_remap_table(break_value, raster_file):
		raster = arcpy.Raster(raster_file)
		below = [raster.minimum, break_value, 0]
		above = [break_value, raster.maximum, 1]
		return arcpy.sa.RemapRange([below, above])

def new_sealevel_raster(break_value, raster_file, reclass_field="VALUE"):
	remap_table = create_remap_table(break_value, raster_file)
	return arcpy.sa.Reclassify(raster_file, reclass_field, remap_table)

def create_sealevel_polygon(break_value, raster_file, output_polygon, reclass_field="VALUE"):
	new_raster = new_sealevel_raster(break_value, raster_file, reclass_field)
	arcpy.RasterToPolygon_conversion(new_raster, output_polygon)
	return output_polygon

#raster to polygon
def get_affected_blocks(block_polygons, sea_polygons, selection_type):
	block_layer = "in_memory/block_layer"
	sea_layer = "in_memory/sea_layer"
	print "sea polygons:%s" % sea_polygons
	print arcpy.Exists(sea_polygons)
	#arcpy.MakeFeatureLayer_management(block_polygons, block_layer)
	#arcpy.MakeFeatureLayer_management(sea_polygons, sea_layer)
	sea_layer = sea_polygons
	block_layer = block_polygons
	print arcpy.Exists(block_layer)
	print arcpy.Exists(sea_layer)
	print "in features:%s\nselect features:%s\noverlap type:%s" % (block_layer, sea_layer, selection_type)
	arcpy.SelectLayerByLocation_management(block_layer, overlap_type=selection_type, select_features=sea_layer)
	#arcpy.CopyFeatures_management(block_layer)
	return block_layer
#select

#sum
def sum_field(feature, field):
	cursor = arcpy.da.SearchCursor(feature, [field])
	val = 0 
	for row in cursor:
		val = val + row[0]
	return val

def add_field(row, field, val):
	val += row[field]
	return val

def make_field_adder(field):
	adder = lambda row, val: add_field(row, field, val) #look up lambda notation
	return adder

def sum_feature(feature, field):
	adder = make_field_adder(field)
	sum = apply_to_feature(feature, adder)
	return sum

def sum_below_sealevel(population_feature, elevation_raster, sealevel, selection_type, population_field):
	sealevel_polygon = "in_memory/sealevel" #"Y:/Documents/oberlin gis/tables tsunami/sealevel_test.shp" #"in_memory/sealevel"
	sealevel_polygon = create_sealevel_polygon(sealevel, elevation_raster, sealevel_polygon)
	arcpy.MakeFeatureLayer_management(sealevel_polygon, "sealevel")
	arcpy.MakeFeatureLayer_management(population_feature, "blocks")
	#select sewalevel stuff
	arcpy.SelectLayerByAttribute_management("sealevel", "NEW_SELECTION", " \"GRIDCODE\" = 0")
#	arcpy.SaveToLayerFile_management("sealevel", "sealevel_polygon", "RELATIVE")
	selected_blocklayer = get_affected_blocks("blocks", "sealevel", selection_type)
	#selected_blocklayer = get_affected_blocks(population_feature, sealevel_polygon, selection_type)
	sum = sum_field(selected_blocklayer, population_field)
	return sum
