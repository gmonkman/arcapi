"""
Export a file geodatabase to a personal geodatabase.

This does recreate/export relationships, unlike fgdb_to_pgdb.py

TODO: Error handling and logging
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

    args = cmdline.parse_args()

    arcpy.env.workspace = args.fGDB

    src_fld, src_fname, src_ext = iolib.get_file_parts2(args.fGDB)  # noqa Not used at mo - but leave for now
    dest_fld, dest_fname, dest_ext = iolib.get_file_parts2(args.pGDB)

    failed_tbls = []
    failed_fcs = []

    if args.recreate:
        print 'Deleting the existing personal GDB...'
        iolib.file_delete(args.pGDB)

    if not iolib.file_exists(args.pGDB):
        print 'Creating personal GDB "%s" ...' % args.pGDB
        arcpy.CreatePersonalGDB_management(dest_fld, dest_fname)

    print('Exporting feature classes....')
    for fc in tqdm(arcpy.ListFeatureClasses()):
        try:
            arcpy.management.Copy(fc, iolib.fixp(args.pGDB, fc))
        except Exception as e:
            # Already exists error. shared names cannot exist in the source, so this
            # is not an error in the destination. This is caused by arcpy.management.Copy
            # transferring related tables/feature classes
            if 'ERROR 000725' not in str(e):
                print 'Import of feature class %s failed. The error was:\n%s' % (fc, str(e))
                failed_fcs += [fc]

    print('Exporting tables....')
    for tbl in tqdm(arcpy.ListTables()):
        try:
            arcpy.management.Copy(tbl,  iolib.fixp(args.pGDB, tbl))
        except Exception as e:
            # Already exists error. shared names cannot exist in the source, so this
            # is not an error in the destination. This is caused by arcpy.management.Copy
            # transferring related tables/feature classes
            if 'ERROR 000725' not in str(e):
                print 'Import of table %s failed. The error was:\n%s' % (tbl, str(e))
                failed_tbls += [tbl]

    if not failed_tbls and not failed_fcs:
        print('All tables and feature classes migrated successfully')
    else:
        if failed_fcs:
            print('*** Feature classes "%s" NOT imported ***' % ';'.join(failed_fcs))
        if failed_tbls:
            print('*** Tables "%s" NOT imported ***' % ';'.join(failed_tbls))

    iolib.folder_open(dest_fld)


if __name__ == '__main__':
    main()
