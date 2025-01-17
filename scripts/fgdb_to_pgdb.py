"""
Export a file geodatabase to a personal geodatabase.

Does not currently recreate/export relationships

Notes:
    See fgdb_to_pgdb2, this copies related tables and their relationships.
"""
import os  # noqa
import os.path as path  # noqa
from os.path import normpath as np

import argparse

import arcpy
from tqdm import tqdm

import iolib


def main():
    """main"""
    cmdline = argparse.ArgumentParser(description=__doc__)  # use the module __doc__

    cmdline.add_argument('fGDB', type=np, help='The source file geodatabase')
    cmdline.add_argument('pGDB', type=np, help='The destination personal geodatabase')
    cmdline.add_argument('-recreate', '--recreate', help='Delete and recreate the personal GDB', action='store_true')
    # cmdline.add_argument('-overwrite', '--overwrite', help='Allow overwriting in the personal GDB', action='store_true')

    args = cmdline.parse_args()

    arcpy.env.workspace = args.fGDB

    src_fld, src_fname, src_ext = iolib.get_file_parts2(args.fGDB)  # noqa Not used at mo - but leave for now
    dest_fld, dest_fname, dest_ext = iolib.get_file_parts2(args.pGDB)


    if args.recreate:
        print 'Deleting the existing personal GDB...'
        iolib.file_delete(args.pGDB)
        print 'Creating a new personal GDB...'
        arcpy.CreatePersonalGDB_management(dest_fld, dest_fname)

    print('Exporting feature classes....')
    for fc in tqdm(arcpy.ListFeatureClasses()):
        arcpy.CopyFeatures_management(fc, iolib.fixp(args.pGDB, fc))

    print('Exporting tables....')
    for tbl in tqdm(arcpy.ListTables()):
        arcpy.management.CopyRows(tbl, iolib.fixp(args.pGDB, tbl))

    print('All done.')
    iolib.folder_open(dest_fld)


if __name__ == '__main__':
    main()
