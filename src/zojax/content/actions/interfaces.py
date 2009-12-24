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
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.content.actions')


class IActionView(interface.Interface):
    """ action view pagelet type """


class IActionsPortlet(interface.Interface):
    """ actions portlet """


class IDoNotCacheActionsPortlet(interface.Interface):
    """ do not cache """


class IBaseAction(interface.Interface):
    """ base action """

    url = interface.Attribute('Action url')
    title = interface.Attribute('Action title')
    description = interface.Attribute('Action description')
    weight = interface.Attribute('Weight')
    permission = interface.Attribute('Permission')

    def isAvailable():
        """ is action available """


class IAction(IBaseAction):
    """ action """


class IContextAction(IBaseAction):
    """ context action """


class IActions(interface.Interface):
    """ sequence of IAction objects """

    def __iter__():
        """ actions iterator """


class IActionCategory(interface.Interface):
    """ action category """

    title = interface.Attribute('Category title')

    weight = interface.Attribute('Weight')

    schema = interface.Attribute('Catagory schema')


class IActionsContext(interface.Interface):
    """ actions context """


# content actions
class IContentAction(IAction):
    """ content action """


class IContentContextAction(IContextAction):
    """ content context action """


class IEditContentAction(IContentAction):
    """ edit content action """


class IEditContentContextAction(IContentContextAction):
    """ edit content context action """


class IDeleteContentAction(IContentAction):
    """ delete content action """


class IBrowseContentAction(IAction):
    """ browse content action """


class IAddContentAction(IAction):
    """ add content action """


class IAddContentActions(IActions):
    """ add content actions """


# action categories
class IManageContentCategory(interface.Interface):
    """ manage content category """


class IBrowseContentCategory(interface.Interface):
    """ browse content category """


class IAddContentCategory(interface.Interface):
    """ add content category """


class INotificationCategory(interface.Interface):
    """ notification category """
