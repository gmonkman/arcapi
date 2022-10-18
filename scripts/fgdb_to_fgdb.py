"""
Export a file geodatabase to a another file geodatabase.

Although we can simply copy a file geodatabase, the use case is where we are merging into an already existing destination.
"""
import os  # noqa
import os.path as path  # noqa
from os.path import normpath as np
import argparse

import fuckit

import arcpy
from tqdm import tqdm

import iolib


def main():
    """main"""
    cmdline = argparse.ArgumentParser(description=__doc__)  # use the module __doc__

    cmdline.add_argument('source_gdb', type=np, help='The source file-geodatabase')
    cmdline.add_argument('dest_gdb', type=np, help='The destination file-geodatabase')
    cmdline.add_argument('-recreate', '--recreate', help='Delete and recreate the destination fGDB', action='store_true')
    # cmdline.add_argument('-overwrite', '--overwrite', help='Allow overwriting in the destination fGDB', action='store_true')

    args = cmdline.parse_args()

    arcpy.env.workspace = args.source_gdb


    src_fld, src_fname, src_ext = iolib.get_file_parts2(args.source_gdb)  # noqa Not used at mo - but leave for now
    dest_fld, dest_fname, dest_ext = iolib.get_file_parts2(args.dest_gdb)

    if dest_fname[-4:] != '.gb':
        raise ValueError('dest_gdb did not end with .gdb')

    if args.recreate:
        print 'Deleting the destination GDB...'
        iolib.folder_delete(args.dest_gdb)

    if not iolib.folder_exists(args.dest_gdb):
        print 'Creating a destination fGDB "%s" ...' % args.dest_gdb
        arcpy.CreateFileGDB_management(dest_fld, dest_fname)

    print 'Exporting feature classes....'
    for fc in tqdm(arcpy.ListFeatureClasses()):
        with fuckit:
            arcpy.management.Copy(fc, iolib.fixp(args.dest_gdb, fc))

    print 'Exporting tables....'
    for tbl in tqdm(arcpy.ListTables()):
        with fuckit:
            arcpy.management.Copy(tbl,  iolib.fixp(args.dest_gdb, tbl))

    print 'All done.'
    iolib.folder_open(dest_fld)


if __name__ == '__main__':
    main()
