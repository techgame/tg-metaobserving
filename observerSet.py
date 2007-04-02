##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from collections import defaultdict

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ObserverSet(set):
    def call_ak(self, *args, **kw):
        for obs in self.copy():
            obs(*args, **kw)

    def call_n1(self, a1):
        for obs in self.copy():
            obs(a1)

    def call_n2(self, a1, a2):
        for obs in self.copy():
            obs(a1, a2)

    def call_n3(self, a1, a2, a3):
        for obs in self.copy():
            obs(a1, a2, a3)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class KeyedObserverSet(defaultdict):
    ObserverSet = ObserverSet
    def __init__(self):
        defaultdict.__init__(self, self.ObserverSet)

    def __repr__(self):
        klass = self.__class__
        keys = ', '.join(self.keys())
        return '<%s.%s keys: %s>' % (klass.__module__, klass.__name__, keys)

    @classmethod
    def new(klass):
        return klass()

    def copy(self):
        result = self.new()
        result.update((k, v.copy()) for k,v in self.iteritems())
        return result

    def add(self, key, observer):
        obsSet = self[key]
        obsSet.add(observer)
        return observer
    def remove(self, key, observer):
        obsSet = self[key]
        obsSet.remove(observer)
        if not obsSet:
            del self[key]
    def discard(self, key, observer):
        obsSet = self[key]
        obsSet.discard(observer)
        if not obsSet:
            del self[key]
    def clear(self, key=None):
        if key is None:
            defaultdict.clear(self)
        else:
            del self[key]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def call_ak(self, key, *args, **kw):
        obsSet = self[key]
        return obsSet.call(*args, **kw)

    def call_n1(self, key, a1):
        obsSet = self[key]
        return obsSet.call_n1(a1)

    def call_n2(self, key, a1, a2):
        obsSet = self[key]
        return obsSet.call_n2(a1, a2)

    def call_n3(self, key, a1, a2, a3):
        obsSet = self[key]
        return obsSet.call_n3(a1, a2, a3)

