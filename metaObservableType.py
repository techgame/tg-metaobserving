##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
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

class TypeObserverClassInit(object):
    def onObservableClassInit(self, pName, obKlass):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    onObservableClassInit.priority = 0

class TypeObserverInit(object):
    def onObservableInit(self, pName, obInstance):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    onObservableInit.priority = 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MetaObservableClassType(type):
    """Metaclass enabling subclassing and instantiation as cooperative events.
    
     - Subclass notification:
        Add an instance implementing onObservableClassInit to the class's
        namespace.  See TypeObserverClassInit

     - Instantiaton notification:
        Not supported.  Use MetaObservableType instead.
    """
    def __init__(self, name, bases, kvars):
        self.observerNotifyClassInit()

    def observerNotifyClassInit(self):
        for varName, varInit in self._getClassVars('onObservableClassInit'):
            varInit(varName, self)

    def _getClassVars(self, attr, missing=object()):
        r = {}
        i = 0
        for base in reversed(self.__mro__):
            for k, v in vars(base).items():
                a = getattr(v, attr, missing)
                if a is not missing:
                    r[k] = ((a, i), (k, a))
                    i += 1

        r = r.values()
        r.sort(key=self._listSortByPriority)
        return [e[1] for e in r]

    @staticmethod
    def _listSortByPriority(entry):
        a, i = entry[0]
        aw = getattr(a, 'priority', 0)
        return (aw, i)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MetaObservableType(MetaObservableClassType):
    """Metaclass enabling subclassing and instantiation as cooperative events.

    Extends MetaObservableClassType to make instantion observable, too.  The two
    options are provided primarily to address performance issues.  This
    subclass performs more processing at instantiation time.
    
     - Subclass notification:
        Add an instance implementing onObservableClassInit to the class's
        namespace.  See TypeObserverClassInit

     - Instantiaton notification:
        Add an instance implementing onObservableInit to the class's
        namespace.  See TypeObserverInit
    """
    def __init__(self, name, bases, kvars):
        self.observerNotifyClassInit()
        self.refreshObservables()

    def refreshObservables(self):
        self._initObservers = self._getClassVars('onObservableInit')

    def __call__(self, *args, **kw):
        instance = type.__call__(self, *args, **kw)
        self.observerNotifyInit(instance)
        return instance

    def observerNotifyInit(self, instance):
        initObservers = self._initObservers
        if initObservers:
            for varName, varInit in initObservers:
                varInit(varName, instance)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MetaObservalbeObject(object):
    __metaclass__ = MetaObservableType

