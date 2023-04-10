import os
import shutil
import logging
import uuid

logging.basicConfig(filename='example.log', level=logging.DEBUG)


def trycopy(source, dest, verbose=False):
    """
    Copy a file or directory from source to dest.

    Parameters
    ----------
    source: str
        source file or directory path
    dest: str
        destination file or directory path
    verbose: bool, optional
        If True, print debug information. Default is False.

    Returns
    -------
    None
    """
    try:
        shutil.copy2(source, dest)
        if verbose:
            print("done copying {} to {}".format(source, dest))
    except Exception as e:
        logging.exception(e)


def trymkdir(path, verbose=False):
    """
    Creates dir at destination

    Parameters
    ----------
    path: str
        path with folder already in
    verbose: bool, optional
        If True, print debug information. Default is False.

    Returns
    -------
    None
    """
    try:
        os.mkdir(path)
        if verbose:
            print("created dir at", path)
    except Exception as e:
        logging.exception(e)


def trymkfile(path, content, verbose=False):
    """
    Creates file

    Parameters
    ----------
    path: str
        path to create file with filename included
    content: str
        file content
    verbose: bool, optional
        If True, print debug information. Default is False.

    Returns
    -------
    None
    """
    try:
        with open(path, "x") as f:
            f.write(content)
        if verbose:
            print("file created at {}".format(path))
            print("with content:")
            print(content)
    except Exception as e:
        logging.exception(e)


def absdiroffile(filepath):
    """
    Gives absolute directory of file, normally expects __file__ as
    param

    Parameters
    ----------
    filepath: str
        path of file

    Returns
    -------
    str
        Absolute dir path of file
    """
    return os.path.dirname(os.path.abspath(filepath))


def get_folders(path):
    """
    Get a list of directories in the given path.

    Parameters
    ----------
    path: str
        Path to search for directories.

    Returns
    -------
    list
        List of directories in the given path.
    """
    dirs = [d for d in os.listdir(
        path) if os.path.isdir(os.path.join(path, d))]
    return dirs


def unique_filename(fname):
    """
    Generate a unique filename by prepending a UUID to the given filename.

    Parameters
    ----------
    fname: str
        Original filename.

    Returns
    -------
    str
        Unique filename with prepended UUID.
    """
    prepended = str(uuid.uuid4()).replace("-", "_")[:10]
    return "{}_{}".format(prepended, fname)


def delete_file(path):
    """
    Delete the file at the given path.

    Parameters
    ----------
    path: str
        Path of the file to delete.

    Returns
    -------
    None
    """
    try:
        os.remove(path)
        logging.info("File deleted: {}".format(path))
    except Exception as e:
        logging.exception(e)


# def unique_sec_filename(filename):
#     return unique_filename(secure_filename(filename))
