# -*- coding: utf-8 -*-
import os

# Use the scandir version of walk if possible,
# otherwise use the os module version
try:
    # https://github.com/benhoyt/scandir
    # Accepted into Python 3.5 stdlib
    # Increases speed 2-20 times (depending on the platform and file system)
    from scandir import walk
except ImportError:
    # The old way with OS.
    from os import walk

__VERSION__ = "0.7.1"


def get_dirs(
        directory=os.path.curdir,
        depth=None,
        absolute=True):
    """Yield a list of directories

    Args:
        directory (Optional[str]): Starting directory.
                Default: ```os.path.curdir```
        depth (Optional[int]): Depth to recurse to.
                Default: None (Infinite depth)
        absolute (Optional[bool]): Return absolue path
                Default: True

    Yields:
        str: Next directory.

    Raises:
        FileNotFoundError: If ```directory``` does not exist
    """
    curdepth = 0

    # Make sure that the directory exists.
    if not os.path.exists(directory):
        raise FileNotFoundError

    # If absolute is specified change directory into
    # an absolpte directory paths
    if absolute:
        directory = os.path.abspath(directory)

    # Walk through the directory from the top.
    for root, dirs, files in walk(directory, topdown=True):
        # Increment current depth.
        curdepth += 1
        for dir_ in dirs:
            # Ignore hidden directories.
            if dir_ == "." or dir_ == "..":
                continue
            # Yield the current path
            yield os.path.join(root, dir_)
        # If depth none (infinite depth)
        if depth is None:
            # Just continue
            continue
        # If the current depth is greater than requested depth:
        if curdepth >= depth:
            # Break
            break


def get_files(
        directory=os.path.curdir,
        extensions=None,
        depth=None,
        absolute=True):
    """
    Args:
        directory (Optional[str]): Starting directory.
                Default: ```os.path.curdir```
        extensions (Optional[str]): List of extensions to yield
                Case insensitive. ('.JPG' and '.jpg' are equivalent)
                Default: None (All files).
        depth (Optional[int]): Depth to recurse to.
                Default: None (Infinite depth)
        absolute (Optional[bool]): Return absolue path
                Default: True

    Yields:
        str: List of all files found in ``directory``

    Raises:
        FileNotFoundError: If ```directory``` does not exist
    """
    curdepth = 0

    # If the given of extensions is just a string.
    # Turn it into a set so that 'in' can be used.
    if isinstance(extensions, str):
        extensions = {extensions}

    # Convert all extensions to lowercase.
    if extensions is not None:
        extensions = [extension.lower() for extension in extensions]

    # If absolute is specified change directory into
    # an absolpte directory path
    if absolute:
        directory = os.path.abspath(directory)

    # Make sure that the directory exists.
    if not os.path.exists(directory):
        raise FileNotFoundError

    # Walk the directory, starting at the top.
    for root, dirs, files in walk(directory, topdown=True):
        # Increment the current depth.
        curdepth += 1
        # Loop through each of the files.
        for name in files:
            # Join the root and the name.
            file = os.path.join(root, name)
            # If extensions is not none.
            if extensions is not None:
                # Get the extension and convert it to lower case.
                ext = os.path.splitext(file)[1].lower()
                # If the file extension is in the extensions list
                # yield the file
                if ext in extensions:
                    yield file
            else:
                # If extensions is None, just yield the file.
                yield file
        # If depth none (infinite depth)
        if depth is None:
            # Just continue
            continue
        # If the current depth is greater than requested depth:
        if curdepth >= depth:
            # Break
            break
