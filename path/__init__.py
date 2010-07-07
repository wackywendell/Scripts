import os
import os.path

class Root(object):
    curroots=dict()
    
    @classmethod
    def parse(cls, s):
        """Should return 'None' if the path does not begin with a root (is relative), or (rootobj, rest_of_s) if the path does begin with a root"""
        raise NotImplementedError, "parse not implemented"
    
    def __str__(self):
        raise NotImplementedError, "__str__ not implemented"
    
    def __repr__(self):
        return str(self.__class__.__name__) + '("' + str(self) + '")'

class PosixRoot(Root):
    @classmethod 
    def _getroot(cls):
        """Only one root on a posix system."""
        if '/' not in cls.curroots:
            cls.curroots['/'] = cls()
        
        return cls.curroots['/']
    
    @classmethod
    def parse(cls, s):
        if len(s) > 0 and s[0] == '/':
            return cls._getroot(), s[1:]
        
        return None
    
    def __str__(self):
        return '/'

class BasePath(tuple):
    """A basic path implementation.
    
    Required for subclasses:
    _rootcls: the associated root class
    
    Optional to override:
    _parserel: a parser for relative classes
            by default, uses str.split(os.path.sep)
    _buildstr: builds a string from the class
            by default, uses os.path.sep.join(self)
    
    Other functions (such as 'new', '__str__', etc.) should not need any modifications.
    """
    def __new__(cls, obj=None):
        print '__new__ ::', obj
        if isinstance(obj, tuple):
            return tuple.__new__(cls, obj)
        elif obj is None:
            return tuple.__new__(cls, tuple())
        elif isinstance(obj, basestring):
            return cls._parsestr(obj)
        elif isinstance(obj, cls._rootcls):
            return tuple.__new__(cls, (obj,))
        
        raise TypeError, ("Path objects can only be constructed from other Path objects, tuples, or strings", 
            obj, type(obj))
    
    def __init__(self, obj):
        self._cachedstr = None
    
    _rootcls = Root
    
    @classmethod
    def _parsestr(cls, s):
        rootparsed = cls._rootcls.parse(s)
        if rootparsed:
            rt, rest = rootparsed
            if not rest:
                return cls(rt)
            relpath = cls._parserel(rest)
            return cls(rt + relpath)
        else:
            relpath = cls._parserel(rest)
            return relpath
    
    @classmethod
    def _parserel(cls, s):
        #return cls(tuple(s.split(os.path.sep)))
        print 'parserel :: ',s, tuple(s.split(os.path.sep))
        return cls(tuple(s.split(os.path.sep)))
    def __unicode__(self):
        """A basic implementation, using a cached copy of self._buildstr()"""
        if self._cachedstr is not None:
            return unicode(self._cachedstr)
        self._cachedstr = self._buildstr()
        return unicode(self._cachedstr)
        
    def __str__(self):
        return str(self.__unicode__())
    
    def __repr__(self):
        return str(self.__class__.__name__) + '("' + str(self) + '")'

    
    def _buildstr(self):
        """A basic implementation, using os.path.sep.join()"""
        return os.path.sep.join(unicode(itm) for itm in self)
    
    @property
    def isabs(self):
        return (len(self) > 0 and
            isinstance(self[0], self._rootcls))
    
    def __add__(self, other):
        other = self.__class__(other)
        if other.isabs:
            raise ValueError, "Right hand value not a relative path"
        return self.__class__(tuple(self) + tuple(other))
    
    def __radd__(self, other):
        other = self.__class__(other)
        return other.__add__(self)

class PosixPath(BasePath):
    _rootcls = PosixRoot
    
    
    def _buildstr(self):
        """A basic implementation, using os.path.sep.join()"""
        if len(self) == 0:
            return '.'
        
        if isinstance(self[0], self._rootcls):
            rest = os.path.sep.join(unicode(itm) 
                                        for itm in self[1:])
            rootstr = str(self[0])
            return rootstr + rest
        
        return os.path.sep.join(unicode(itm) for itm in self)