#############################################################################
# This script was created by Joe Martin
# and modified by Amanda Schmidt for GEOL235 use
#############################################################################
# This script creates watersheds from a file with multiple pour points.
# if you run the watershed tool with mutliple overlapping pour points,
# you don't get the full watersheds.  This script outputs polygons and rasters.
# It also can copy over information from fields in the pour point shapefile
# and fix holes due to errors in the DEM causing regions to be internally
# drained.

# SETTINGS
# Most of what you edit will be in this folder

# Directories
# Remember to switch '\' to '/' when copying directory names from windows explorer
# and to end all directories with a '/'

# SCRATCH - where all the intermediate data is stored, points, rasters, etc
SCRATCH = "" #Fill in your folder location here. This is where your output rasters are stored.
# OUT_FOLDER - where the final polygons are stored
OUT_FOLDER = "" #Fill in your folder location here. This is for your output polygons.
# IN_FOLDER - where the inputs, (pour points and flow direction) are stored
IN_FOLDER = "" #Fill in your folder location here. This is where your flow direction and pour points are

# Inputs

# POUR_POINTS - the file with all the pour points.  This needs to have some
# sort of ID column, numbered from 0.   
POUR_POINTS = IN_FOLDER + "" #Fill in just the name of your pour_points file here
# pour point settings
# ID COLUMN - a column numbered from 0, incrementing by one
ID_COLUMN = "FID" #If your pour points have an ID you want to use beside "FID", change it here.

# FlOW_DIRECTION - the flow direction raster for calculating watersheds
FLOW_DIRECTION = IN_FOLDER + "" #Fill in just the name of your flow direction grid here

# Settings

# JOIN_FIELDS - any fields from the pour points you want copied to your
# watershed polygons.  This actually creates new fields in the output watersheds
# and copies over the information, and is not a table join.  Table joins are
# wierd and scary.
JOIN_FIELDS = ["Id"] #If you have other info to copy, here is the place to specify names
# FILL_HOLES - this fills any holes in the output watershed polygons.  Sometimes
# your DEM has errors, and the flow direction ends up creating areas that are
# internally drained even though they shouldn't be, leading to holes in your
# watershed.  When FILL_HOLES is true, the final polygon will have those holes
# filled.  You should enable this only if you know that no areas in your
# watershed should be internally drained, but that your DEM has errors that
# would cause regions to be internally drained
FILL_HOLES = False
# VERBOSE - this prints out what step it is on, for debugging and your own
# peace of mind
VERBOSE = True 

NAME_FIELD = "FID" #Change this if you want to have your basins named something different.

# THE SCRIPT

# the imports you need
import arcpy
from arcpy.sa import *
import os

arcpy.CheckOutExtension("Spatial")

for row in arcpy.da.SearchCursor(POUR_POINTS, [NAME_FIELD, ID_COLUMN]): #range (0, SIZE):
#############################################################################
# This script was created by Joe Martin
# and modified by Amanda Schmidt for GEOL235 use
#############################################################################
# This script creates watersheds from a file with multiple pour points.
# if you run the watershed tool with mutliple overlapping pour points,
# you don't get the full watersheds.  This script outputs polygons and rasters.
# It also can copy over information from fields in the pour point shapefile
# and fix holes due to errors in the DEM causing regions to be internally
# drained.

# SETTINGS
# Most of what you edit will be in this folder

# Directories
# Remember to switch '\' to '/' when copying directory names from windows explorer
# and to end all directories with a '/'

# SCRATCH - where all the intermediate data is stored, points, rasters, etc
SCRATCH = "" #Fill in your folder location here. This is where your output rasters are stored.
# OUT_FOLDER - where the final polygons are stored
OUT_FOLDER = "" #Fill in your folder location here. This is for your output polygons.
# IN_FOLDER - where the inputs, (pour points and flow direction) are stored
IN_FOLDER = "" #Fill in your folder location here. This is where your flow direction and pour points are

# Inputs

# POUR_POINTS - the file with all the pour points.  This needs to have some
# sort of ID column, numbered from 0.   
POUR_POINTS = IN_FOLDER + "" #Fill in just the name of your pour_points file here
# pour point settings
# ID COLUMN - a column numbered from 0, incrementing by one
ID_COLUMN = "FID" #If your pour points have an ID you want to use beside "FID", change it here.

# FlOW_DIRECTION - the flow direction raster for calculating watersheds
FLOW_DIRECTION = IN_FOLDER + "" #Fill in just the name of your flow direction grid here

# Settings

# JOIN_FIELDS - any fields from the pour points you want copied to your
# watershed polygons.  This actually creates new fields in the output watersheds
# and copies over the information, and is not a table join.  Table joins are
# wierd and scary.
JOIN_FIELDS = ["Id"] #If you have other info to copy, here is the place to specify names
# FILL_HOLES - this fills any holes in the output watershed polygons.  Sometimes
# your DEM has errors, and the flow direction ends up creating areas that are
# internally drained even though they shouldn't be, leading to holes in your
# watershed.  When FILL_HOLES is true, the final polygon will have those holes
# filled.  You should enable this only if you know that no areas in your
# watershed should be internally drained, but that your DEM has errors that
# would cause regions to be internally drained
FILL_HOLES = False
# VERBOSE - this prints out what step it is on, for debugging and your own
# peace of mind
VERBOSE = True 

NAME_FIELD = "FID" #Change this if you want to have your basins named something different.

# THE SCRIPT

# the imports you need
import arcpy
from arcpy.sa import *
import os

arcpy.CheckOutExtension("Spatial")

for point in arcpy.da.SearchCursor(POUR_POINTS, NAME_FIELD: #range (0, SIZE):
    name = str(point)
    print "Working on pour point %s" % (name)
    cur_point = select_pour_point(pour_points, NAME_FIELD, name)
    # make watershed
    if VERBOSE:
        print "\t calculating watershed"
    shed_raster = "%s_shed.tif" % (name)
    shed_raster_path = os.path.join(scratch, shed_raster)
    if not os.path.exists(shed_raster_path):
        shed_raster = Watershed(FLOW_DIRECTION, cur_point)
        shed_raster.save(shed_raster_path)
    elif VERBOSE:
        print "watershed raster %s already exists, skiping creation" % () 
    # convert to polygon
    shed_polygon = "%s_shed.shp" % (name)
    out_shed = SCRATCH + "shed" + name + ".shp"

    if VERBOSE:
        print "\t converting to polygon"
    if not os.path.exists(out_shed):
        arcpy.RasterToPolygon_conversion(shed_raster, out_shed)
    elif VERBOSE:
        print "watershed polygon %s already exists, skipping creation" % out_shed
    # get list of fields from pour point
    pp_fields = arcpy.ListFields(cur_point)
    # add fields
    if VERBOSE:
        print "\t creating new fields"
    for field in JOIN_FIELDS:
        # get type of field to join
        field_type = [x for x in pp_fields if x.aliasName == field][0].type
        # make new field of the type of the join field
        if VERBOSE:
            print "\t\t adding " + field_type + " field \"" + field + "\""
        if field_type == 'OID':
            field = 'old_' + field
            if VERBOSE:
                print "\t\t\tID field found, renaming as " + field
            field_type = 'LONG'
        arcpy.AddField_management(out_shed, field, field_type)
    # fill holes
    if VERBOSE:
        print "\t filling holes"
    if FILL_HOLES:
        holeless_shed = SCRATCH + "shed" + name + "no_hole.shp"
        temp = SCRATCH + "temp" + name + ".shp"
        arcpy.Union_analysis(out_shed, temp, "ALL", gaps="NO_GAPS")
        arcpy.Dissolve_management(temp, holeless_shed, JOIN_FIELDS)
        out_shed = holeless_shed
    output = OUT_FOLDER + "shed" + name + ".shp"
    if not os.path.exists(output):
        out_shed = arcpy.Copy_management(out_shed, output)
    # join fields
    # loop through fields to join
    if VERBOSE:
        print "\t copying over field data"
    for field in JOIN_FIELDS:
        field_type = [x for x in pp_fields if x.aliasName == field][0].type
        if field_type == 'OID':
            field = 'old_' + field
            if VERBOSE:
                print "\t\t\tID field found, renaming as " + field
            field_type = 'LONG'
        # get a cursor for the pour point, and the new watershed
        pp_cursor = arcpy.SearchCursor(cur_point)
        shed_cursor = arcpy.UpdateCursor(out_shed)
        # get the row of each feature (since there should be one feature
        # per file, we can just assume that the first row is what we need
        pp_row = pp_cursor.next()
        shed_row = shed_cursor.next()
        # now set the value of the new field in the watershed to the matching
        # value in the pour point
        if VERBOSE:
            print "\t\t copying " + str(pp_row.getValue(field)) + " to " + field
        shed_row.setValue(field, pp_row.getValue(field))
        shed_cursor.updateRow(shed_row)      
    # clean up cursors
    pp_cursor.reset()
    shed_cursor.reset()
    name = str(row[0])
    point_id = str(row[1])
    print "Working on pour point " + name
    # select the pour point
    where_clause = '"' + ID_COLUMN + '" = ' + point_id
    cur_point = SCRATCH + "pp" + name + ".shp"
    if os.path.exists(cur_point):
        arcpy.Delete_management(cur_point)
    arcpy.Select_analysis(POUR_POINTS, cur_point, where_clause)
    # make watershed
    if VERBOSE:
        print "\t calculating watershed"
    outWatershed_name = OUT_FOLDER + name + ".tif"
    if not os.path.exists(outWatershed_name):
        shed_raster = Watershed(FLOW_DIRECTION, cur_point)
        shed_raster.save(outWatershed_name)
    elif VERBOSE:
        print "watershed raster %s already exists, skiping creation" % outWatershed_name
    # convert to polygon
    out_shed = SCRATCH + "shed" + name + ".shp"
    if VERBOSE:
        print "\t converting to polygon"
    if not os.path.exists(out_shed):
        arcpy.RasterToPolygon_conversion(shed_raster, out_shed)
    elif VERBOSE:
        print "watershed polygon %s already exists, skipping creation" % out_shed
    # get list of fields from pour point
    pp_fields = arcpy.ListFields(cur_point)
    # add fields
    if VERBOSE:
        print "\t creating new fields"
    for field in JOIN_FIELDS:
        # get type of field to join
        field_type = [x for x in pp_fields if x.aliasName == field][0].type
        # make new field of the type of the join field
        if VERBOSE:
            print "\t\t adding " + field_type + " field \"" + field + "\""
        if field_type == 'OID':
            field = 'old_' + field
            if VERBOSE:
                print "\t\t\tID field found, renaming as " + field
            field_type = 'LONG'
        arcpy.AddField_management(out_shed, field, field_type)
    # fill holes
    if VERBOSE:
        print "\t filling holes"
    if FILL_HOLES:
        holeless_shed = SCRATCH + "shed" + name + "no_hole.shp"
        temp = SCRATCH + "temp" + name + ".shp"
        arcpy.Union_analysis(out_shed, temp, "ALL", gaps="NO_GAPS")
        arcpy.Dissolve_management(temp, holeless_shed, JOIN_FIELDS)
        out_shed = holeless_shed
    output = OUT_FOLDER + "shed" + name + ".shp"
    if not os.path.exists(output):
        out_shed = arcpy.Copy_management(out_shed, output)
    # join fields
    # loop through fields to join
    if VERBOSE:
        print "\t copying over field data"
    for field in JOIN_FIELDS:
        field_type = [x for x in pp_fields if x.aliasName == field][0].type
        if field_type == 'OID':
            field = 'old_' + field
            if VERBOSE:
                print "\t\t\tID field found, renaming as " + field
            field_type = 'LONG'
        # get a cursor for the pour point, and the new watershed
        pp_cursor = arcpy.SearchCursor(cur_point)
        shed_cursor = arcpy.UpdateCursor(out_shed)
        # get the row of each feature (since there should be one feature
        # per file, we can just assume that the first row is what we need
        pp_row = pp_cursor.next()
        shed_row = shed_cursor.next()
        # now set the value of the new field in the watershed to the matching
        # value in the pour point
        if VERBOSE:
            print "\t\t copying " + str(pp_row.getValue(field)) + " to " + field
        shed_row.setValue(field, pp_row.getValue(field))
        shed_cursor.updateRow(shed_row)      
    # clean up cursors
    pp_cursor.reset()
    shed_cursor.reset()
