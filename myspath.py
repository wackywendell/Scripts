#format PYTHON

"""An extension of spath to include directory walking."""

import spath
import os.path

class path(spath.path):
    """A modification of spath.path to semi-support unicode strings, as well
    as adding a 'getfiles' and 'getdirs' function."""
    def __new__(cls, arg=None):
        # Allow for unicode path names by switching to ascii if possible
        if isinstance(arg, unicode):
            return spath.path.__new__(cls, str(arg))
        else:
            return spath.path.__new__(cls, arg)
    
    def getdirs(self, descend = False):
        """Yields subdirectories in the path.
        
        Args:
        descend (default False): Set to True to descend into subdirectories and also yield subsubdirectories, etc."""
        for (dirpath, dirnames, filenames) in os.walk(str(self)):
            curpath = self.__class__(dirpath)
            if descend:
                yield curpath
                continue
            else:
                for d in dirnames:
                    yield curpath + d
                break
            
    
    def getfiles(self, descend = False):
        """Yields files (NOT directories) in the path.
        
        Args:
        descend (default False): Set to True to descend into subdirs"""
        for (dirpath, dirnames, filenames) in os.walk(str(self)):
            curpath = self.__class__(dirpath)
            for f in filenames:
                yield curpath + f
            if not descend:
                break
    
    def expanduser(self):
        return self.__class__(os.path.expanduser(str(self)))

    def expandvars(self):
        return self.__class__(os.path.expandvars(str(self)))
    
    @property
    def extension(self):
        return ''.join(self[-1].rsplit('.', 1)[1:])

#p1 = spath.path('~/scripts/test/rlab604.mp3')
#p2 = path('~/scripts/test/rlab604.mp3')