class T(tuple):
    def __getslice__(self, i,j):
        return self.__getitem__(slice(i,j))
    def __getitem__(self, key):
        """A base implementation of __getitem__ that determines 
        whether the slice includes the last element, and calls 
        the appropriate sub-method"""
        tupslice = tuple.__getitem__(self, key)
        if not isinstance(key, slice):
            # in the case a single inner item is requested,
            # return it (as a string, not as a path)
            return tupslice
        start, stop, step = key.indices(len(self))
        stop -= (stop+step-1-start) % step
        print start, stop, step
        if stop >= len(self):
            return self._getatend(tupslice)
        else:
            return self._getnotend(tupslice)
    def _getatend(self,tslice):
        return ('End',tslice)
    def _getnotend(self,tslice):
        return ('Not End',tslice)
    def __str__(self):
        return str(tuple(self))
    def __repr__(self):
        return 'T(' + str(tuple(self)) + ')'

t = T(range(1,13))
s = T(range(11))