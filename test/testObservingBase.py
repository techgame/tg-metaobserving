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

import unittest

from TG.metaObserving import MetaObservableType

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ObservableBase(object):
    __metaclass__ = MetaObservableType

class ObserverBase(object):
    def __init__(self, testcase, pName, obclass=None, obinstance=None):
        self.pName = pName
        self.testcase = testcase
        self.obclass = obclass
        self.obinstance = obinstance

class ObserverClassInit(ObserverBase):
    def onObservableClassInit(self, pName, obKlass):
        self.testcase.failUnlessEqual(pName, self.pName)
        self.obclass.append(obKlass)

class ObserverInit(ObserverBase):
    def onObservableClassInit(oself, pName, obInstance):
        self.testcase.failUnlessEqual(pName, self.pName)
        self.obinstance.append(obInstance)

class ObserverBothInit(ObserverInit, ObserverClassInit):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestObservingSubclasses(unittest.TestCase):
    def testCreation(self):
        """Passes if the base class can be created"""
        ObservableBase()

    def testObserveClassInit(self):
        obclassA = []

        class A(ObservableBase):
            oname = ObserverClassInit(self, 'oname', obclassA)
            self.failUnlessEqual(obclassA, [])

        self.failUnlessEqual(obclassA, [A])

        inst1 = A()
        inst2 = A()
        self.failUnlessEqual(obclassA, [A])

    def testObserveTwoClassInit(self):
        obclassA = []
        class A(ObservableBase):
            oname = ObserverClassInit(self, 'oname', obclassA)
            self.failUnlessEqual(obclassA, [])
        self.failUnlessEqual(obclassA, [A])

        inst1 = A()
        inst2 = A()
        self.failUnlessEqual(obclassA, [A])

        obclassB = []
        class B(ObservableBase):
            propName = ObserverClassInit(self, 'propName', obclassB)
        self.failUnlessEqual(obclassA, [A])
        self.failUnlessEqual(obclassB, [B])

        inst3 = B()
        inst4 = B()
        self.failUnlessEqual(obclassA, [A])
        self.failUnlessEqual(obclassB, [B])

    def testObserveThreeWithSubclassInit(self):
        obclassA = []
        class A(ObservableBase):
            oname = ObserverClassInit(self, 'oname', obclassA)
            self.failUnlessEqual(obclassA, [])
        self.failUnlessEqual(obclassA, [A])

        obclassB = []
        class B(ObservableBase):
            propName = ObserverClassInit(self, 'propName', obclassB)
            self.failUnlessEqual(obclassB, [])
        self.failUnlessEqual(obclassB, [B])

        obclassC = []
        class C(A):
            attrTest = ObserverClassInit(self, 'attrTest', obclassC)
            self.failUnlessEqual(obclassA, [A])
            self.failUnlessEqual(obclassC, [])

        self.failUnlessEqual(obclassA, [A, C])
        self.failUnlessEqual(obclassB, [B])
        self.failUnlessEqual(obclassC, [C])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

