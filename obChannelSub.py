# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab:
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2011  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from collections import defaultdict

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBChannelSub(object):
    def __init__(self, chan, extend=None):
        self._chanName = chan
        self._initSubs(extend)

    def copy(self):
        return self.__class__(self._chanName, self.subs)

    def onObservableClassInit(self, pubName, obInstance):
        self = self.copy()
        setattr(obInstance, pubName, self)
    onObservableClassInit.priority = -8

    def onObservableInit(self, pubName, obInstance):
        self._replay(obInstance)
    onObservableInit.priority = -8
    def onObservableRestore(self, pubName, obInstance):
        self._replay(obInstance)
    onObservableRestore.priority = -8

    def _initSubs(self, extend):
        self.subs = []
        if extend: self.subs.extend(extend)

    def _replay(self, host):
        chan = self._chanName
        if not isinstance(chan, basestring):
            chan = chan.public
        chan = getattr(host, chan)
        return self.replayOn(host, chan)

    def replayOn(self, host, chan):
        for fn in self.subs:
            chan.on(self._resolveFn(host, fn))

    def on(self, key=None, fn=None):
        if fn is not None:
            return self.bind(fn, key)
        return lambda fn: self.bind(fn, key)

    def bind(self, fn, key):
        if key is None:
            key = fn.__name__.rsplit('_')[-1]
        self.subs.append(fn)
        return fn

    def _resolveFn(self, host, fn):
        # use getattr to allow overriding by standard python conventions
        return getattr(host, fn.__name__, fn)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBKeyedChannelSub(OBChannelSub):
    def _initSubs(self, extend):
        self.subs = {}
        if extend: self.subs.update(extend)

    def replayOn(self, host, chan):
        for key, fn in self.subs.iteritems():
            chan.on(key, self._resolveFn(host, fn))

    def bind(self, fn, key):
        if key is None:
            key = fn.__name__.rsplit('_')[-1]
        self.subs[key] = fn
        return fn

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OBMultiKeyedChannelSub(OBChannelSub):
    def _initSubs(self, extend):
        self.subs = defaultdict(list)
        if extend: 
            for k, v in extend.iteritems():
                self.subs[k].extend(v)

    def replayOn(self, host, chan):
        for key, fns in self.subs.iteritems():
            for fn in fns:
                chan.on(key, self._resolveFn(host, fn))

    def bind(self, fn, key):
        if key is None:
            key = fn.__name__.rsplit('_')[-1]
        self.subs[key].append(fn)
        return fn

