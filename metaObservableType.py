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
        for varName, varInit in self.getClassVars('onObservableClassInit'):
            varInit(varName, self)

    def getClassVars(self, attr, incPriorities=False, missing=None):
        result = {}
        oidx = 0
        defaultPriority = 0
        for base in reversed(self.__mro__):
            for k, v in vars(base).items():
                av = getattr(v, attr, missing)
                if av is not missing:
                    pri = getattr(av, 'priority', defaultPriority)
                    result[k] = (pri, oidx, k, av)
                    oidx += 1

        result = result.values()
        result.sort()
        if not incPriorities: 
            result = [e[2:] for e in result]
        return result

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
        self._refreshObservables()

    def _refreshObservables(self):
        self._initObservers = self.getClassVars('onObservableInit', True)

    def __call__(self, *args, **kw):
        instance = self.__new__(self, *args, **kw)
        for pass_ in self.iterObserverNotifyInit(instance):
            instance.__init__(*args, **kw)

        return instance

    def observerNotifyInit(self, instance):
        for pass_ in self.iterObserverNotifyInit(instance):
            pass

    def iterObserverNotifyInit(self, instance):
        initObservers = iter(self._initObservers)

        count = len(self._initObservers)
        for pri, oidx, varName, varInit in initObservers:
            if pri < 0: 
                varInit(varName, instance)
                count -= 1
            else: 
                yield
                varInit(varName, instance)
                count -= 1
                break
        else: 
            yield
            return

        for pri, oidx, varName, varInit in initObservers:
            varInit(varName, instance)
            count -= 1
        return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MetaObservalbeObject(object):
    __metaclass__ = MetaObservableType

