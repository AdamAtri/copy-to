#! /usr/bin/python

import os
import time
import shutil

import argparse
parser = argparse.ArgumentParser(description = """
    Copy the contents of the source directory to the destination directory, sorting
    and depositing them into newly created sub-directories based on the field argument.
""")
parser.add_argument('--source', help="the source directory")
parser.add_argument('--dest', help="the destination directory")
parser.add_argument('--field', help="the field used to sort the files ('date' and 'ext' are currently the only accepted fields.)", default='date')
parser.add_argument('--exts', nargs='+', help="(optional) the file extension(s) [.jpg, .png, .pdf, etc] to copy")
parser.add_argument('-r', '--recursive', help="whether to dig into and copy the contents of sub-directories", default=False)
arguments = parser.parse_args()


def start(args):

    # make sure that source and dest are passed. (field will default to "date")
    if not (args.source and args.dest):
        raise Exception("'--source' and '--dest' are required arguments. {}".format(args))

    print "Attempting to copy files from {} to {} ".format(args.source, args.dest)
    if args.exts:
        print "but only if its extension is in '{}' formats.".format("', '".join(exts))

    # make the dest dir if it doesn't exist
    print "Checking for destination path..."
    if os.path.exists(args.dest):
        if not os.path.isdir(args.dest):
            raise Exception('Can\'t use that destination path. Try again.')
        print "Cool, destination directory already exists."
    else:
        os.mkdir(args.dest, 0755)
        print "Made directory {}.".format(args.dest)
    # if there aren't any extensions in the list, remove the list
    if not args.exts or len(args.exts) == 0:
        exts = None
        print "Didn't get any file extensions, so everything's getting copied."
    # copy the files
    copy_files(args)

def copy_files(args):
    print "Starting file copy..."
    # move files from source dir to dest dir
    for filename in os.listdir(args.source):
        # check if we received extensions and if the current file conforms
        if (args.exts) :
            ext = '.{}'.format(filename.split('.')[-1])
            if ext not in args.exts:
                continue
        # get the source file
        source_file = os.path.join(args.source, filename)
        # if the source file is a directory, check if we're performing a recursive sort
        if os.path.isdir(source_file):
            if not args.recursive:
                continue
            new_dest = os.path.join(args.dest, filename)
            new_args = Args(source_file, new_dest, args.field, args.exts, True)
            print '>> Start sub-directory'
            start(new_args)
            continue
        # get the destination folder
        dest_dir = get_destination_dir(source_file, args.field, args.dest)
        # if a folder with that sub-directory doesn't exist in the dest dir, create it
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir, 0755)
        dest_file = os.path.join(dest_dir, filename)
        print ("Copying {0} to {1}".format(source_file, dest_file))
        shutil.copy2(source_file, dest_file)
    print "Finished. Oh yeah."
    return

def get_destination_dir(source_file, field, dest):
    # evaluate the field and return the new destination file
    if field == 'date':
        return get_date_dir(source_file, dest)
    elif field == 'ext':
        return get_ext_dir(source_file, dest)
    else:
        raise Exception('Field not expected: %s' % field)
    return None

def get_date_dir(source_file, dest):
    # get the mod date of the file
    ts = time.strptime(time.ctime(os.path.getmtime(source_file)))
    # get the year month and date of file
    ymd = "{y}_{m}_{d}".format(y=ts.tm_year, m=ts.tm_mon, d=ts.tm_mday)
    return os.path.join(dest, ymd)

def get_ext_dir(source_file, dest):
    # get the ext
    ext = source_file.split('.')[-1]
    ext = ext.upper() + 's'
    return os.path.join(dest, ext)


class Args(object):
    def __init__(self, in_source=None, in_dest=None, in_field=None, in_exts=None, in_recursive=None):
        self.dest = in_dest
        self.source = in_source
        self.field = in_field
        self.exts = in_exts
        self.recursive = in_recursive


print 'Starting...'
start(arguments)
