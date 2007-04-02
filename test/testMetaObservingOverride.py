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

import unittest
from TG.metaObserving import MetaObservalbeObject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MOO = MetaObservalbeObject

class TestTEMPLATE(unittest.TestCase):
    def test(self):
        class TypeObserver(object):
            def __repr__(self):
                return '<%s:%08x %d,%d>' % (self.name, id(self), self.nClassInit, self.nInit)
            nClassInit = 0
            def onObservableClassInit(self, pName, obKlass):
                self.name = pName
                self.nClassInit += 1

            nInit = 0
            def onObservableInit(self, pName, obInstance):
                self.nInit += 1

            @property
            def value(self):
                return self.nClassInit, self.nInit

        class T0(MOO):
            ob_0 = TypeObserver()
            ob_1 = TypeObserver()
            ob_2 = TypeObserver()

            @classmethod
            def kvv(klass):
                return (klass.ob_0.value, klass.ob_1.value, klass.ob_2.value)
            def vv(self):
                return (self.ob_0.value, self.ob_1.value, self.ob_2.value)

        self.assertEqual(T0.kvv(), ((1,0), (1,0), (1,0)))

        class T1(T0):
            ob_1 = TypeObserver()
            ob_2 = TypeObserver()

        self.assertEqual(T0.kvv(), ((2,0), (1,0), (1,0)))
        self.assertEqual(T1.kvv(), ((2,0), (1,0), (1,0)))

        class T2(T1):
            ob_2 = TypeObserver()

        self.assertEqual(T0.kvv(), ((3,0), (1,0), (1,0)))
        self.assertEqual(T1.kvv(), ((3,0), (2,0), (1,0)))
        self.assertEqual(T2.kvv(), ((3,0), (2,0), (1,0)))

        class T3(T2):
            pass

        self.assertEqual(T0.kvv(), ((4,0), (1,0), (1,0)))
        self.assertEqual(T1.kvv(), ((4,0), (3,0), (1,0)))
        self.assertEqual(T2.kvv(), ((4,0), (3,0), (2,0)))
        self.assertEqual(T3.kvv(), ((4,0), (3,0), (2,0)))

        i3 = T3()
        self.assertEqual(i3.vv(),  ((4,1), (3,1), (2,1)))
        self.assertEqual(T0.kvv(), ((4,1), (1,0), (1,0)))
        self.assertEqual(T1.kvv(), ((4,1), (3,1), (1,0)))
        self.assertEqual(T2.kvv(), ((4,1), (3,1), (2,1)))
        self.assertEqual(T3.kvv(), ((4,1), (3,1), (2,1)))

        i1 = T1()
        self.assertEqual(i1.vv(),  ((4,2), (3,2), (1,1)))
        self.assertEqual(T0.kvv(), ((4,2), (1,0), (1,0)))
        self.assertEqual(T1.kvv(), ((4,2), (3,2), (1,1)))
        self.assertEqual(T2.kvv(), ((4,2), (3,2), (2,1)))
        self.assertEqual(T3.kvv(), ((4,2), (3,2), (2,1)))

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

