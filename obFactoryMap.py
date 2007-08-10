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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBFactoryMap(object):
    def __init__(self, *args, **kw):
        if args or kw:
            self._update_(*args, **kw)

    def onObservableClassInit(self, propertyName, obKlass):
        self = self._copy_()
        setattr(obKlass, propertyName, self)
    onObservableClassInit.priority = -10

    @classmethod
    def _new_(klass):
        return klass()
    new = _new_

    def _copy_(self):
        r = self._new_()
        r._update_(self.__dict__)
        return r
    copy = _copy_

    def _branch_(self, *args, **kw):
        self = self.copy()
        self.update(*args, **kw)
        return self
    branch = _branch_

    def _update_(self, *args, **kw):
        self.__dict__.update(*args, **kw)
    update = _update_

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _keys_(self):
        self.__dict__.keys()
    keys = _keys_

    def _values_(self, *args, **kw):
        self.__dict__.values(*args, **kw)
    values = _values_

    def _items_(self, *args, **kw):
        self.__dict__.items(*args, **kw)
    items = _items_

