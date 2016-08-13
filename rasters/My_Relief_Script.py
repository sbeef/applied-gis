import arcpy

def meanLocalRelief(in_raster, neighborhood, out_raster):
    max_elev = arcpy.FocalStatistics(in_raster, neighborhood, "MAXIMUM")
    min_elev = arcpy.FocalStatistics(in_raster, neighborhood, "MINIMUM")
    output = max_elev - min_elev
    output.save(out_raster)
