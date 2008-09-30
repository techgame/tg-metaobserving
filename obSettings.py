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

from copy import deepcopy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def mapMerge(data, dnew):
    for key, newValue in dnew.iteritems():
        if isinstance(newValue, dict):
            value = data.get(key)
            if isinstance(value, dict):
                newValue = mapMerge(value.copy(), newValue)
        data[key] = newValue
    return data

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBSettings(dict):
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)
        self.branchLists()

    @classmethod
    def fromEntry(klass, entry):
        return klass(entry)
        
    def onObservableClassInit(self, propertyName, obKlass):
        self = self.copy()
        setattr(obKlass, propertyName, self)
    onObservableClassInit.priority = -5

    def onObservableInit(self, propertyName, obInstance):
        self = self.copy()
        setattr(obInstance, propertyName, self)
    onObservableInit.priority = -5

    def copy(self):
        return self.fromEntry(deepcopy(self))

    def branch(self, *args, **kw):
        self = self.copy()
        self.update(*args, **kw)
        return self

    def __getattr__(self, name):
        try:
            return self[name]
        except LookupError, e:
            raise AttributeError(str(e))
    def __setattr__(self, name, value):
        try:
            self[name] = value
        except LookupError, e:
            raise AttributeError(str(e))
    def __delattr__(self, name):
        try:
            del self[name]
        except LookupError, e:
            raise AttributeError(str(e))

    def get(self, key, default=None):
        value = dict.get(self, key, default)
        if value.__class__ is dict:
            value = self.fromEntry(value)
            self[key] = value
        return value

    def __getitem__(self, key):
        value = dict.__getitem__(self, key)
        if value.__class__ is dict:
            value = self.fromEntry(value)
            self[key] = value
        return value
    def __setitem__(self, key, value):
        if value.__class__ is dict:
            value = self.fromEntry(value)
        return dict.__setitem__(self, key, value)

    mapMerge = mapMerge
    def update(self, *args, **kw):
        dnew = dict(*args, **kw)
        self.mapMerge(dnew)
        return self

    def merge(self, obSettings):
        result = self.copy()
        for each in obSettings:
            if each is not None:
                result.update(each)
        return result

    def branchLists(self):
        kw = {}
        for k,v in self.iteritems():
            if v.__class__ is list:
                kw[k] = v[:]
        if kw: self.update(kw)

