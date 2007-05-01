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
#~ OB Property Implementation 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBProperty(object):
    """Uses MetaObservableType mechanism to implement a property with a factory.
    
    Implements TypeObserverInit and TypeObserverClassInit.
    Can only be used on a object using MetaObservableType-based metaclass.
    """
    missing = object()
    public = None
    private = None
    _private_fmt = '__ob_%s'

    def __init__(self, factory=NotImplemented, isValue=None, publish=None):
        self._setPublishName(publish)
        if isValue is None:
            # autodetect parameter
            if factory is NotImplemented:
                factory = None
            elif factory is None or isinstance(factory, (basestring, int, long, float)):
                factory = self.factoryFromValue(factory)
        elif isValue:
            # turn the value into a factory for convinence
            factory = self.factoryFromValue(factory)
        self.factory = factory

    def factoryFromValue(self, value):
        return (lambda value=value: value)

    def _setPublishName(self, publish):
        if publish is None or isinstance(self.public, str):
            return

        self.public = publish
        self.private = self._private_fmt % (publish,)

    def onObservableClassInit(self, propertyName, obKlass):
        self._setPublishName(propertyName)

    def __get__(self, obInst, obKlass):
        if obInst is None:
            return self
        missing = self.missing
        result = getattr(obInst, self.private, missing)
        if result is missing:
            factoryResult = self.setWithFactory(obInst)
            if not factoryResult:
                raise AttributeError("'%s' object attribute '%s' has not been initialized" % (obInst, self.public))
            else: result = factoryResult[-1]
        return result

    def setWithFactory(self, obInst):
        factory = self.factory
        if factory is not None:
            result = factory()
            self.__set__(obInst, result)
            return (True, result)
    def __set__(self, obInst, value):
        setattr(obInst, self.private, value)
        self._modified_(obInst)
    def __delete__(self, obInst):
        if not self.setWithFactory(obInst):
            delattr(obInst, self.private)
            self._modified_(obInst)

    def _modified_(self, obInst):
        pass

def obproperty(obObjectFactory, *args, **kw):
    if args or kw:
        instFactory = lambda: obObjectFactory(*args, **kw)
    else: instFactory = obObjectFactory
    return OBProperty(instFactory)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ OBProperty that passes the instance back to the factory
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBInstProperty(OBProperty):
    def factoryFromValue(self, value):
        return (lambda obInst, value=value: value)
    def setWithFactory(self, obInst):
        factory = self.factory
        if factory is not None:
            result = factory(obInst)
            self.__set__(obInst, result)
            return (True, result)

def obInstProperty(obObjectFactory, *args, **kw):
    if args or kw:
        instFactory = lambda obInst: obObjectFactory(obInst, *args, **kw)
    else: instFactory = obObjectFactory
    return OBInstProperty(instFactory)

