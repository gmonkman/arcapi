"""
#-------------------------------------------------------------------------------
# Name:        arcapi
# Purpose:     Convenient API for arcpy
#
# Authors:     Filip Kral, Caleb Mackey
#
# Created:     01/02/2014
# Licence:     LGPL v3
#-------------------------------------------------------------------------------
# Wrapper functions, helper functions, and aliases that make ArcGIS Python
# scripting easier.
#
# Arcapi is a Python package of functions that simplify common tasks, are easy
# on the programmer, and make prototyping faster. However, Arcapi is intended
# for skilled Python coders with solid experience with ArcPy and ArcGIS.
#
# While the code should work with all types of workspaces, ESRI File Geodatabase
# was adopted as primary format. Most functions were designed for and tested
# with plain tables and feature classes with basic field types like SHORT, LONG,
# TEXT, DOUBLE, FLOAT. If you work with feature datasets, topologies,
# relationship classes, annotation feature classes, TINs, BLOBs, and other
# complex objects, you will likely need to use core arcpy functions.
#
# Exception handling
# ------------------
# Because arcapi functions are generally wrappers around arcpy functions, input
# checking and exception handling is used sporadically. This allows invalid
# input to reach core (arcpy etc.) functions and raised errors propagate back
# the calling functions.
# In rare cases, to distinguish Exceptions raised in arcapi, an Exception
# of type arcapi.ArcapiError is raised.
#
# Package structure
# -----------------
# Arcapi is a Python package which allows for modular structure. The core
# module is called aracpi and all its content is imported when you import
# the arcapi package.
#
# ArcGIS Extensions modules
# -------------------------
# Some functions use extensions modules (e.g. Spatial Analyst's arcpy.sa).
# Bodies of these functions are wrapped in try-except(ImportError) statements.
# The extension-dependent functions will return string if the extensions is not
# installed, but rest of arcapi will still work normally.
#
#-------------------------------------------------------------------------------
"""
from arcapi import *
