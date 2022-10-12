"""
Input/Output related helpers
"""
import os as _os
import os.path as _path
import shutil as _shutil
import subprocess as _subprocess


import fuckit as _fuckit

def fixp(*args):
    """(str|list)->str
    basically path.normpath
    """
    s = ''
    for u in args:
        s = _path.join(s, u)
    return _path.normpath(s)


def file_exists(file_name):
    """(str) -> bool
    Returns true if file exists
    """
    file_name = _path.normpath(file_name)
    if isinstance(file_name, str):
        return _path.isfile(fixp(file_name))

    return False


def folder_delete(fld):
    """
    Delete a folder. Calls shutil.rmtree. Suppresses all errors.

    Args:
        fld (str): the folder

    Returns:
        None
    """
    fld = _path.normpath(fld)
    with _fuckit:
        _shutil.rmtree(fld, ignore_errors=True)


def folder_open(folder='.'):
    """(_string) -> void
    opens a windows folder at path folder"""
    if _os.name == 'nt':
        folder = folder.replace('/', '\\')

    try:
        _subprocess.check_call(['explorer', folder])
    except:
        pass


def get_file_parts(filepath):
    """
    Given path to a file, split it into path,
    file part and extension.

    Args:
        filepath (str): full path to a file.

    Returns:
        list: [folder, filename sans extension, extension]

    Examples:
        >>> get_file_parts('c:/temp/myfile.txt')
        'c:/temp', 'myfile', '.txt'
    """
    filepath = _path.normpath(filepath)
    folder, fname = _path.split(filepath)
    fname, ext = _path.splitext(fname)
    return [folder, fname, ext]


def get_file_parts2(filepath):
    """
    Split a full file path into path, file name with extension and dotted extension.

    Args:
        filepath (str): full path to a file.

    Returns:
        list: [folder, file name with extension, dotted extension]

    Examples:
        >>> get_file_parts2('c:/temp/myfile.txt')
        'c:/temp', 'myfile.txt', '.txt'
    """
    folder, fname = _path.split(filepath)
    ext = _path.splitext(fname)[1]
    return [folder, fname, ext]


def file_delete(fname):
    """Delete a single file

    Is normpathed first

    Args:
        fname (str): file to be deleted

    Returns:
        None
    """
    files_delete2(fname)


def files_delete2(filenames):
    """(list|str) -> void
    Delete file(s) without raising an error

    Args:
        filenames (str, iter): A string or iterable of file names

    Returns:
        None

    Examples:
        >>> files_delete2('C:/myfile.tmp')
        >>> files_delete2(['C:/myfile.tmp', 'C:/otherfile.log'])
    """
    if isinstance(filenames, str):
        filenames = [filenames]

    for fname in filenames:
        fname = _path.normpath(fname)
        if file_exists(fname):
            _os.remove(fname)


if __name__ == '__main__':
    pass
