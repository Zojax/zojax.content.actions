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
from zope import interface, component
from zope.i18n import translate
from zope.component import queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.app.component.interfaces import ISite
from zojax.content.type.interfaces import IContent, IContentType
from zojax.content.type.interfaces import IUnremoveableContent,IRenameNotAllowed

import interfaces
from interfaces import _
from action import Action


class ContentAction(Action):
    component.adapts(IContent, interface.Interface)

    action = u''
    actionTitle = u''

    def __init__(self, context, request, view=None):
        super(ContentAction, self).__init__(context, request, view)

        self.contenttype = IContentType(self.context, None)

    @property
    def title(self):
        return u'%s %s'%(translate(self.actionTitle),
                         translate(self.contenttype.title))

    @property
    def description(self):
        return self.contenttype.description

    @property
    def url(self):
        return '%s/%s'%(absoluteURL(self.context, self.request), self.action)

    def isAvailable(self):
        if self.contenttype is None:
            return False

        return super(ContentAction, self).isAvailable()


@interface.implementer(interface.Interface)
def ContentTypeIcon(action, request):
    return queryMultiAdapter((action.contenttype, request), name='zmi_icon')


@interface.implementer(interface.Interface)
def ContentActionIcon(action, request):
    return queryMultiAdapter((action.context, request), name='zmi_icon')


class EditContentAction(ContentAction):
    interface.implements(interfaces.IEditContentAction,
                         interfaces.IManageContentCategory)

    weight = 10
    action = 'context.html'
    actionTitle = _('Edit')
    permission = 'zojax.ModifyContent'


class EditContentContextAction(Action):
    component.adapts(IContent, interface.Interface)
    interface.implements(interfaces.IEditContentContextAction,
                         interfaces.IManageContentCategory)

    weight = 0
    title = _('Edit')

    @property
    def url(self):
        return '%s/context.html'%absoluteURL(self.context, self.request)


class DeleteContentAction(ContentAction):
    interface.implements(interfaces.IDeleteContentAction,
                         interfaces.IManageContentCategory)

    weight = 50
    action = 'delete.html'
    actionTitle = _('Delete')
    permission = 'zojax.DeleteContent'

    def isAvailable(self):
        context = self.context
        if ISite.providedBy(context) or \
                IUnremoveableContent.providedBy(context) or \
                IRenameNotAllowed.providedBy(context):
            return False

        return super(DeleteContentAction, self).isAvailable()


class BrowseContentAction(ContentAction):
    interface.implements(interfaces.IBrowseContentAction,
                         interfaces.IBrowseContentCategory)

    weight = 50
    action = 'browse.html'
    actionTitle = _('Browse')
    permission = 'zope.View'


class AddContent(object):
    interface.implements(interfaces.IAddContentAction,
                         interfaces.IAddContentCategory)

    def __init__(self, context, request, contenttype, weight):
        self.context = context
        self.request = request
        self.contenttype = contenttype
        self.weight = weight

    @property
    def title(self):
        return u'%s %s'%(translate(_('Add')),
                         translate(self.contenttype.title))

    @property
    def description(self):
        return self.contenttype.description

    @property
    def url(self):
        return u'%s/+/%s/'%(
            absoluteURL(self.context, self.request), self.contenttype.name)

    def isAvailable(self):
        return True


class AddContentActions(ContentAction):
    component.adapts(IContent, interface.Interface)
    interface.implements(interfaces.IAddContentActions)

    def __iter__(self):
        if self.contenttype is None:
            raise StopIteration

        context = self.context
        request = self.request

        weight = 999

        for ct in self.contenttype.listContainedTypes():
            weight = weight + 1
            yield AddContent(context, request, ct, weight)
