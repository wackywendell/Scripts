"""Provides Leasyid3 class."""

from mutagen.easyid3 import EasyID3
import mutagen
import os as _os

class Leasyid3(EasyID3):
    """An EasyID3 derivative that also allows for other fields.
    
    Both human-readable names (in Leasyid3.valid_keys) as well as the actual
    field names (e.g. 'TIT1', 'TOPE') are accepted.
    
    Fields can be accessed and set using an Leasyid3 instance as a dict, and
    str objects as values, although the save() method must be called to save."""
    
    def __init__(self, filename=None, usedefault=False):
        #"""Create an Leasyid3 object from a file.
        #
        #The 'usedefault' setting treats valid but non-existent fields as blank, and 
        #returns '' when __getitem__ is called on a non-existent field, and gives
        #no error when a non-existent (but valid) field is deleted.
        #
        #otherwise the same as EasyID3.__init__."""
        
        mysave = self.save
        EasyID3.__init__(self, filename=filename)
        self.oldfname = filename
        self.usedefault = usedefault
        self.__id3 = self._EasyID3__id3
        self._save = self.save
        self.save = mysave
    
    __mungers = EasyID3._EasyID3__mungers
    __default = EasyID3._EasyID3__default
        
    valid_keys = {
        "album": "TALB",
        "composer": "TCOM",
        "genre": "TCON",
        "date": "TDRC",
        "lyricist": "TEXT",
        "title": "TIT2",
        "version": "TIT3",
        "artist": "TPE1",
        "tracknum": "TRCK",
        "origperformer":"TOPE",
        "year":"TYER",
    }
    """Valid names for tracks; extended from EasyID3"""
    
    otherkeys = [
        "TALB", "TBPM", "TCOM", "TCON", "TCOP", "TDEN", "TDLY", 
        "TDOR", "TDRC", "TDRL", "TDTG", "TENC", "TEXT", "TFLT", 
        "TIPL", "TIT1", "TIT2", "TIT3", "TKEY", "TLAN", "TLEN", 
        "TMCL", "TMED", "TMOO", "TOAL", "TOFN", "TOLY", "TOPE", 
        "TOWN", "TPE1", "TPE2", "TPE3", "TPE4", "TPOS", "TPRO", 
        "TPUB", "TRCK", "TRSN", "TRSO", "TSOA", "TSOP", "TSOT", 
        "TSRC", "TSSE", "TSST", "TXXX"
    ]
    """Long list of accepted track names"""
    
    def __getitem__(self, key):
        frame = key.upper()
        if frame in self.otherkeys:
            getter = self.__mungers.get(frame, self.__default)[0]
            try:
                returned = getter(self, self.__id3[frame])
            except KeyError:
                if self.usedefault:
                    returned = ['']
                else: raise
        else:
            returned = EasyID3.__getitem__(self, key)
            
        if isinstance(returned, list):
            return returned[0]
        else:
            return returned
    
    def __setitem__(self, key, value):
        frame = key.upper()
        if frame in self.otherkeys:
            setter = self.__mungers.get(frame, self.__default)[1]
            if frame not in self.__id3:
                frame = mutagen.id3.Frames[frame](encoding=3, text=value)
                self.__id3.loaded_frame(frame)
            else:
                setter(self, self.__id3[frame], value)
        else:
            return EasyID3.__setitem__(self, key, value)
    
    def __delitem__(self, key):
        frame = key.upper()
        if frame in self.otherkeys:
            try:
                del(self.__id3[frame])
            except KeyError:
                if self.usedefault:
                    return
                else: raise
        else:
            try:
                EasyID3.__delitem__(self, key)
            except KeyError:
                if self.usedefault:
                    return
                else: raise
    
    
    def keys(self):
        ks = list(EasyID3.keys(self))
        for k in self.otherkeys:
            if k in self.__id3 and k not in self.valid_keys.values():
                ks.append(k)
        return ks
    
    def pprint(self):
        """Print tag key=value pairs."""
        strings = []
        for key in self.keys():
            value = self[key]
            strings.append("{0:15}={1}".format(key, value))
        return "\n".join(strings)
    
    def save(self, *args, **kwargs):
        newfname = self.filename
        self._save(newfname, *args, **kwargs)
        #print "SAVING!"
        if self.oldfname != newfname:
            _os.rename(self.oldfname, newfname)
        #print "RENAMED!"