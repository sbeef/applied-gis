import arcpy

def select_pour_point(pour_points, name_field, name):
    """
    Selects a point from a shapefile and returns a temporary shapefile
    containing only that point

    Args:
        pour_points: A shapefile
        name_field: the field that contains the value you wish to select by
        name: the value to select by

    Returns:
        A shapefile in the "in_memory" workspace containing only the point
        selected.
    """
    where_clause = "\"%s\" = %s" % (name_field, name)
    cur_point = "in_memory/pp_%s" % (name)
    if os.path.exists(cur_point):
        arcpy.Delete_management(cur_point)
    arcpy.Select_analysis(pour_points, cur_point, where_clause)
    return cur_point

def make_watershed_raster(flow_dir, pour_point, name, out_dir):
    """
    Makes a watershed raster (if it does not already exist) from a pour point)

    Args:
        flow_dir: A flow direction raster for your region
        pour_point: The shapefile containing the pour_point to make your
                    watershed from
        name: Something to name your output watershed raster
        out_dir: a directory for your output watershed to be saved

    Returns:
        A watershed raster
    """
    shed_raster = "%s_shed.tif" % (name)
    shed_raster_path = os.path.join(out_dir, shsed_raster)
    if not os.path.exits(shed_raster_path):
        shed_raster = Watersehd(flow_dir, pour_point)
        shed_raster.save(shed_raster_path)
    elif VERBOSE:
        print "watershed raster %s already exists, skipping creation" % (name)
    return shed_raster_path

def make_watershed_polygon(shed_raster, name, out_dir):
    """
    Creates a polygon from a watershed raster

    Args:
        shed_raster: The watershed raster
        name: A name for the watershed
        out_dir:  directory for the output shapefile

    Returns:
        A shapefile of the watershed polygon
    """
    shed_polygon = "%s_shed.shp" % (name)
    shed_poly_path = os.path.join(out_dir, shed_polygon)
    if not os.path.exists(shed_poly_path):
        arcpy.RasterToPolygon_conversion(shed_raster, shed_poly_path)
    elif VERBOSE:
        print "watershed polygon %s already exists, skipping creation" % (name) 
    return shed_poly_path

def fill_holes(shed_polygon, name, out_dir)
    """
    Removes all internally drained areas from a watershed

    Args:
        shed_polygin: A watershed polygon
        name: A name for the watershed
        out_dir: A directory for the output shapefile to be saved in.

    Returns:
        A shapefile contained a watershed with no internally drained regions
    """
    unioned_shed = "in_memory/union_%s.shp" % (name)
    arcpy.Union_analysis(out_shed, unioned_shed, "ALL", gaps="NO_GAPS")
    holeless_shed = "%s_no_hole.shp" % (name)
    holeless_path = os.path.join(out_dir, holeless_shed)
    arcpy.Dissolve_management(unioned_shed, holeless_path)
    return holeless_path

def join_fields(pour_point, shed_polygon, join_fields):
    """
    Joins table data from the pour point to a watershed

    Args:
        pour_point: a shapefiel containing a pour point used to make a watershed.
        shed_polygon: a watershed polygon
        join_fields: a list of field names in the pour_point data file.
    Returns:
        This function returns nothing as no new files are created.  The watershed
        polygon file supplied is simply updated.
    """
    pp_fields = {field.aliasName: field for field in arcpy.ListFields(pour_point)}
    for field in join_fields:
        field_type = ppfields[field].type
        arcpy.AddField_management(out_shed, field, field_type)
    pp_cursor = arcpy.da.SearchCursor(pour_point, join_fields)
    shed_cursor = arcpy.da.UpdateCursor(shed_polygon, join_fields)
    for row in shed_cursor:
        pour_point = pp_cursor.next()
        for field in join_fields:
            row.setValue(field, pour_point.getValue(field))
        shed_cursor.updateRow(row)


for point in arcpy.da.SearchCursor(POUR_POINTS, NAME_FIELD):
    name = str(point)
    print "Working on pour point %s" % (name)
    cur_point = select_pour_point(POUR_POINTS, NAME_FIELD, name)
    shed_raster = make_watershed_raster(FLOW_DIRECTION, cur_point, name, SCRATCH)
    shed_polygon - make_watershed_polygon(shed_raster, name)
    
