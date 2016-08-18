import arcpy

def select_pour_point(pour_points, name_field, name):
    where_clause = "\"%s\" = %s" % (name_field, name)
    cur_point = "in_memory/pp_%s" % (name)
    if os.path.exists(cur_point):
        arcpy.Delete_management(cur_point)
    arcpy.Select_analysis(pour_points, cur_point, where_clause)
    return cur_point

def make_watershed_raster(flow_dir, pour_point, name, out_dir):
    shed_raster = "%s_shed.tif" % (name)
    shed_raster_path = os.path.join(out_dir, shsed_raster)
    if not os.path.exits(shed_raster_path):
        shed_raster = Watersehd(flow_dir, pour_point)
        shed_raster.save(shed_raster_path)
    elif VERBOSE:
        print "watershed raster %s already exists, skipping creation" % (name)
    return shed_raster_path

def make_watershed_polygon(shed_raster, name):
    shed_polygon = "%s_shed.shp" % (name)
    out_shed = os.path.join(out_dir, shed_polygon)

for point in arcpy.da.SearchCursor(POUR_POINTS, NAME_FIELD):
    name = str(point)
    print "Working on pour point %s" % (name)
    cur_point = select_pour_point(POUR_POINTS, NAME_FIELD, name)
    shed_raster = make_watershed_raster(FLOW_DIRECTION, cur_point, name, SCRATCH)


