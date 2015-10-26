import imp
import os
import sys

def module_from_path(path):
    modulename = os.path.splitext(os.path.basename(path))[0]

    try:
        return sys.modules[modulename]
    except KeyError:
        pass

    try:
        fileobj = open(path, mode='U')
        return imp.load_module(modulename, fileobj, path, ('py', 'U', imp.PY_SOURCE))
    finally:
        if fileobj: fileobj.close()