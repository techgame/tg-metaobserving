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

from functools import partial

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBClassRegistry(dict):
    def onObservableClassInit(self, pubName, obKlass):
        setattr(obKlass, pubName, self.copy())
    onObservableClassInit.priority = -5

    def __missing__(self, key):
        return self.get(None, None)

    def copy(self):
        return self.__class__(self)

    def on(self, key, fn=None):
        return self.set(key, fn)

    def set(self, key, fn=None):
        if fn is None:
            return partial(self.set, key)

        self[key] = fn
        return fn
    
    def discard(self, key):
        r = self.pop(key, None)
        return r is not None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBRegistry(OBClassRegistry):
    def onObservableInit(self, pubName, obInst):
        setattr(obInst, pubName, self.copy())
    onObservableInit.priority = -5


