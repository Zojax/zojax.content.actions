##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope.component import getAdapters
from zojax.content.type.interfaces import IDraftedContent
from zojax.content.actions.interfaces import IContextAction


class ContextActions(object):

    def update(self):
        super(ContextActions, self).update()

        context = self.context
        request = self.request

        actions = []
        for name, action in getAdapters((context, request), IContextAction):
            if action.isAvailable():
                actions.append((action.weight, action.title, action))

        actions.sort()
        self.actions = [action for _w, _t, action in actions]

    def isAvailable(self):
        if IDraftedContent.providedBy(self.context):
            return False

        return bool(self.actions)
