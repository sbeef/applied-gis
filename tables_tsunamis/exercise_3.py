import selection_script as select

POPULATION_FEATURE = # the census block shapefile
POPULATION_FIELD   = # the name of the field in the census block file which
                     # contains population information
ELEVATION_RASTER   = # the DEM for your reigion
OVERLAP_TYPES      = # a list of 'overlap types' used by the select by layer tool
                     # e.g. ["WITHIN", "HAVE_THEIR_CENTER_IN", "INTERSECT"]
SEALEVEL_RISE      = 10# the ammount of sealevel rise you want to model.  Units
                     # are whatever vertical units your DEM uses 

# labeling the name of the sealevel polygon to be created
sealevel_feature = "in_memory/sealevel"
# making the new sealevel polygon
select.create_elevation_polygon(SEALEVEL_RISE, ELEVATION_RASTER, sealevel_feature)
# creating layers for the selection tools
arcpy.MakeFeatureLayer_management(sealevel_feature, "sealevel")
arcpy.MakeFeatureLayer_management(POPULATION_FEATURE, "population")
# selecting the polygons representing the area below the new sealevel
elevation_query = '"GRIDCODE" = 1'
arcpy.SelectLayerByAttribute_management("sealevel", "NEW_SELECTION", elevation_query)
# a loop to calculate how many people are affected by sealevel rise
for ???? in ????:
    arcpy.SelectLayerByLocation_management("population",
                                           overlap_type= ????,
                                           select_features= "sealevel",
                                           selection_type="NEW_SELECTION")
    total = select.sum_field("population", POPULATION_FIELD)
    print "For overlap_type=%s, %s people affected" % (????, total)
