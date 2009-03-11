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

    def onObservableRestore(self, pName, obInstance):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    onObservableRestore.priority = 0

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

    def getClassVars(self, attr, incPriorities=False, missing=object()):
        result = {}
        defaultPriority = 0

        if incPriorities:
            entry = lambda *args: args
        else: entry = lambda p,n,a: (n,a)

        obkeys = set(k for b in self.__mro__ for k,v in vars(b).iteritems() if hasattr(v, attr))
        for obname in obkeys:
            obvar = getattr(self, obname)
            obattr = getattr(obvar, attr, missing)
            if obattr is not missing:
                pri = getattr(obattr, 'priority', defaultPriority)
                result[obname] = entry(pri, obname, obattr)

        result = result.values()
        result.sort()
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
        self._restoreObservers = self.getClassVars('onObservableRestore')

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
        for pri, varName, varInit in initObservers:
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

        for pri, varName, varInit in initObservers:
            varInit(varName, instance)
            count -= 1
        return

    def observerNotifyRestore(self, instance):
        for varName, varRestore in self._restoreObservers:
            varRestore(varName, instance)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MetaObservalbeObject(object):
    __metaclass__ = MetaObservableType

    def __setstate__(self, state):
        type(self).observerNotifyRestore(self)

