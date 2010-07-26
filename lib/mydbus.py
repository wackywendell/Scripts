import collections

import dbus

class Bus(collections.Mapping):
    def __init__(self, bus):
        self._bus = bus
    def __len__(self):
        return len(self.keys())
    def __iter__(self):
        return iter(self.keys())
    def __contains__(self, obj):
        return obj in self.keys()
    def keys(self):
        return [unicode(u) for u in self._bus.list_names()]
    def __getitem__(self):
        return 

system = dbus.SystemBus()
session = dbus.SessionBus()