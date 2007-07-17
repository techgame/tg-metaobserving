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
from .obProperty import obproperty

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBCallN(object):
    def call_ak(self, *args, **kw):
        for obs in self.inCallOrder():
            obs(*args, **kw)
    __call__ = call_ak

    def call_a(self, *args):
        for obs in self.inCallOrder():
            obs(*args)

    def call_n1(self, a1):
        for obs in self.inCallOrder():
            obs(a1)

    def call_n2(self, a1, a2):
        for obs in self.inCallOrder():
            obs(a1, a2)

    def call_n3(self, a1, a2, a3):
        for obs in self.inCallOrder():
            obs(a1, a2, a3)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBList(list, OBCallN):
    def __repr__(self):
        return '[' + ', '.join(sorted([k.__name__ for k in self])) + ']'

    def copy(self):
        return self.__class__(self[:])

    def inCallOrder(self):
        return list(self)

    def on(self, fn):
        self.add(fn)
        return fn

    def add(self, observer):
        self.append(observer)
    def discard(self, observer):
        try:
            while 1: self.remove(observer)
        except ValueError: 
            pass

    def change(self, bAdd, observer):
        if bAdd: self.add(observer)
        else: self.discard(observer)

OBList.property = classmethod(obproperty)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBDict(set, OBCallN):
    def __repr__(self):
        return '{' + ', '.join(sorted(['%s: %s' % (n, k.__name__) for n, k in self.items()])) + '}'

    def on(self, fn):
        self[fn] = fn
        return fn

    def inCallOrder(self):
        return self.values()

OBDict.property = classmethod(obproperty)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBSet(set, OBCallN):
    def __repr__(self):
        return '{' + ', '.join(sorted([k.__name__ for k in self])) + '}'

    def inCallOrder(self):
        return list(self)

    def on(self, fn):
        self.add(fn)
        return fn

    def change(self, bAdd, observer):
        if bAdd: self.add(observer)
        else: self.discard(observer)
OBSet.property = classmethod(obproperty)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBKeyedCollection(defaultdict):
    OBCollection = None
    _purgeEmpty = True

    def __init__(self, OBCollection=None):
        if OBCollection is None:
            OBCollection = self.OBCollection
        defaultdict.__init__(self, OBCollection)

    def __repr__(self):
        klass = self.__class__
        keys = ', '.join(self.keys())
        return '<%s.%s keys: %s>' % (klass.__module__, klass.__name__, keys)

    @classmethod
    def new(klass):
        return klass()

    def __repr__(self):
        r = sorted([(k, repr(o)) for k,o in self.items()])
        if r:
            r = ('  %s: %s,' % e for e in r)
            return '{\n' + '\n'.join(r) + '\n}'
        else: return '{}'
    def copy(self):
        result = self.new()
        result.update((k, v.copy()) for k,v in self.iteritems())
        return result

    def change(self, bAdd, key, observer):
        if bAdd: self.add(key, observer)
        else: self.discard(key, observer)
    def add(self, key, observer):
        obsSet = self[key]
        obsSet.add(observer)
        return observer
    def remove(self, key, observer):
        obsSet = self[key]
        obsSet.remove(observer)
        if not obsSet and self._purgeEmpty:
            del self[key]
    def discard(self, key, observer):
        obsSet = self[key]
        obsSet.discard(observer)
        if not obsSet and self._purgeEmpty:
            del self[key]
    def clear(self, key=None):
        if self._purgeEmpty:
            if key is None:
                defaultdict.clear(self)
            else: self.pop(key, None)
        elif key is None:
            for v in self.itervalues():
                v.clear()
        else:
            self[key].clear()

    def on(self, key, fn=None):
        if fn is not None:
            self.add(key, fn)
            return

        def addKey(fn):
            self.add(key, fn)
            return fn
        return addKey

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _call_enabled = False
    def __call__(self, key, *args, **kw):
        if not self._call_enabled:
            raise NotImplementedError('%s is not currently callable' % (self.__class__.__name__,))
        obsSet = self.get(key, None)
        if obsSet is not None:
            return obsSet.call_ak(*args, **kw)

    def call_a(self, key, *args):
        obsSet = self.get(key, None)
        if obsSet is not None:
            return obsSet.call_a(*args)

    def call_ak(self, key, *args, **kw):
        obsSet = self.get(key, None)
        if obsSet is not None:
            return obsSet.call_ak(*args, **kw)

    def call_n1(self, key, a1):
        obsSet = self.get(key, None)
        if obsSet is not None:
            return obsSet.call_n1(a1)

    def call_n2(self, key, a1, a2):
        obsSet = self.get(key, None)
        if obsSet is not None:
            return obsSet.call_n2(a1, a2)

    def call_n3(self, key, a1, a2, a3):
        obsSet = self.get(key, None)
        if obsSet is not None:
            return obsSet.call_n3(a1, a2, a3)

OBKeyedCollection.property = classmethod(obproperty)

class OBKeyedList(OBKeyedCollection):
    OBCollection = OBList

class OBChannelList(OBKeyedList):
    _purgeEmpty = False

class OBKeyedSet(OBKeyedCollection):
    OBCollection = OBSet

class OBChannelSet(OBKeyedSet):
    _purgeEmpty = False

