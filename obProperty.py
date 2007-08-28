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

class OBNamedAttribute(object):
    """Uses MetaObservableType mechanism to implement a property with a factory.
    
    Implements TypeObserverInit and TypeObserverClassInit.
    Can only be used on a object using MetaObservableType-based metaclass.
    """

    public = None
    private = None
    _private_fmt = '__ob_%s'

    def __init__(self, publish=None):
        if publish:
            self._setPublishName(publish)

    def __repr__(self):
        klass = self.__class__
        return '<%s.%s name:%s|%s>' % (
                    klass.__module__, klass.__name__,
                    self.public, self.private)

    def onObservableClassInit(self, propertyName, obKlass):
        self._setPublishName(propertyName)
    onObservableClassInit.priority = -15

    def propertyNameTuple(self):
        return (self.public, self.private)

    def _setPublishName(self, publish):
        if publish is None:
            return
        elif isinstance(self.public, str):
            return 
        else:
            self.public = publish
            self.private = self._private_fmt % (publish,)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBProperty(OBNamedAttribute):
    missing = object()

    def __init__(self, factory=NotImplemented, isValue=None, publish=None):
        OBNamedAttribute.__init__(self, publish)
        self.setFactoryFrom(factory, isValue)

    def setFactoryFrom(self, factory=NotImplemented, isValue=None):
        if isValue is None:
            # autodetect parameter
            if factory is self.missing:
                factory = None
            elif factory is None or isinstance(factory, (basestring, int, long, float)):
                factory = self.factoryFromValue(factory)
        elif isValue:
            # turn the value into a factory for convinence
            factory = self.factoryFromValue(factory)
        self.factory = factory

    def factoryFromValue(self, value):
        return (lambda value=value: value)

    def __get__(self, obInst, obKlass):
        if obInst is None:
            return self
        missing = self.missing
        result = getattr(obInst, self.private, missing)
        if result is missing:
            factoryResult = self.setWithFactory(obInst)
            if not factoryResult:
                raise AttributeError("%r instance attribute '%s' has not been initialized" % (obInst.__class__, self.public))
            else: result = factoryResult[-1]
        return result

    def setWithFactory(self, obInst):
        factory = self.factory
        if factory is not None:
            result = factory()
            self.__set_factory__(obInst, result)
            return (True, result)
    def set(self, obInst, value):
        setattr(obInst, self.private, value)
        self._modified_(obInst)

    __set__ = set
    __set_factory__ = __set__

    def __delete__(self, obInst):
        if not self.setWithFactory(obInst):
            delattr(obInst, self.private)
            self._modified_(obInst)

    def _modified_(self, obInst):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def factoryMethod(klass):
        def boundProperty(obObjectFactory, *args, **kw):
            if args or kw:
                factory = lambda: obObjectFactory(*args, **kw)
            else: factory = obObjectFactory

            self = klass(factory, False)
            return self
        return boundProperty

obproperty = OBProperty.factoryMethod()

