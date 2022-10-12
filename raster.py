"""raster manipulation"""
import os

import arcpy as _arcpy

import arcapi as _arcapi


def int_to_float(raster, out_raster, decimals):
    """Convert an Integer Raster to a Float Raster
    *** Requires spatial analyst extension ***

    E.g., for a cell with a value of 45750, using this tool with 3
    decimal places will give this cell a value of 45.750

    Required:
    raster -- input integer raster
    out_raster -- new float raster
    decimals -- number of places to to move decimal for each cell

    Examples:
        >>> int_to_float('C:/Temp/ndvi_int', 'C:/Temp/ndvi_float', 4)
    """

    _arcpy.CheckOutExtension('Spatial')
    fl_rast = _arcpy.sa.Float(_arcpy.Raster(raster) / float(10 ** int(decimals)))
    try:
        fl_rast.save(out_raster)
    except:
        # having random issues with Esri GRID format, change to tiff
        #   if grid file is created
        if not _arcpy.Exists(out_raster):
            out_raster = out_raster.split('.')[0] + '.tif'
            fl_rast.save(out_raster)
    try:
        _arcpy.CalculateStatistics_management(out_raster)
        _arcpy.BuildPyramids_management(out_raster)
    except:
        pass

    _arcapi.msg('Created: %s' % out_raster)
    _arcpy.CheckInExtension('Spatial')
    return out_raster



def fill_no_data(in_raster, out_raster, w=5, h=5):
    """Fill "NoData" cells with mean values from focal statistics.

    Use a larger neighborhood for raster with large areas of no data cells.

    *** Requires spatial analyst extension ***

    Args:
        in_raster -- input raster
        out_raster -- output raster
        w -- search radius width for focal stats (rectangle)
        h -- search radius height for focal stats (rectangle)

    Examples:
        >>> fill_no_data('C:/Temp/ndvi', r'C:/Temp/ndvi_filled', 10, 10)
    """

    # Make Copy of Raster
    _dir, name = os.path.split(_arcpy.Describe(in_raster).catalogPath)
    temp = os.path.join(_dir, 'rast_copyxxx')
    if _arcpy.Exists(temp):
        _arcpy.Delete_management(temp)
    _arcpy.CopyRaster_management(in_raster, temp)

    # Fill NoData
    _arcpy.CheckOutExtension('Spatial')
    filled = _arcpy.sa.Con(_arcpy.sa.IsNull(temp), _arcpy.sa.FocalStatistics(temp, _arcpy.sa.NbrRectangle(w, h), 'MEAN'), temp)
    filled.save(out_raster)
    _arcpy.BuildPyramids_management(out_raster)
    _arcpy.CheckInExtension('Spatial')

    # Delete original and replace
    if _arcpy.Exists(temp):
        _arcpy.Delete_management(temp)
    _arcapi.msg('Filled NoData Cells in: %s' % out_raster)
    return out_raster

