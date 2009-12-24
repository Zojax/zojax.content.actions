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
from zope.security import checkPermission


class Action(object):

    url = u''
    title = u''
    description = u''
    weight = 999
    permission = None
    contextInterface = None

    def __init__(self, context, request, view=None):
        contextInterface = self.contextInterface
        if contextInterface is not None:
            newcontext = context
            while not contextInterface.providedBy(newcontext) and \
                    newcontext is not None:
                newcontext = getattr(newcontext, '__parent__', None)

            if newcontext is not None:
                context = newcontext

        self.context = context
        self.request = request
        self.view = None

    def isAvailable(self):
        if self.permission is not None and \
                not checkPermission(self.permission, self.context):
            return False

        return True
