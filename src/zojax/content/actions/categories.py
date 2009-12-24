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
from zope import interface

import interfaces
from interfaces import _, IActionCategory


class ActionCategory(object):
    interface.implements(IActionCategory)

    def __init__(self, title, weight, schema):
        self.title = title
        self.weight = weight
        self.schema = schema


AddContent = ActionCategory(
    _(u'Add content'), 10, interfaces.IAddContentCategory)


ManageContent = ActionCategory(
    _(u'Manage content'), 20, interfaces.IManageContentCategory)


BrowseContent = ActionCategory(
    _(u'Browse content'), 30, interfaces.IBrowseContentCategory)


Notification = ActionCategory(
    _(u'Notifications'), 40, interfaces.INotificationCategory)
