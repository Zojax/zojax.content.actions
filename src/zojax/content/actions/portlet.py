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
from zope.component import getAdapters, getUtility, getUtilitiesFor
from zope.traversing.api import getPath
from zope.security.proxy import removeSecurityProxy
from zojax.layout.interfaces import ILayout
from zojax.content.type.interfaces import IContent, IDraftedContent

from zojax.cache.view import cache
from zojax.cache.keys import ContextModified
from zojax.cache.timekey import TagTimeKey, each20minutes
from zojax.cache.interfaces import DoNotCache

from cache import ActionsTag
from interfaces import IAction, IActions, IActionsContext, IActionCategory
from interfaces import IActionsPortlet, IDoNotCacheActionsPortlet


def ActionsPortletCache(object, instance, *args, **kw):
    if IDoNotCacheActionsPortlet.providedBy(instance.context):
        raise DoNotCache()

    return {'principal': instance.request.principal.id}


class ActionsPortlet(object):
    interface.implements(IActionsPortlet)

    def __init__(self, context, request, manager, view):
        if ILayout.providedBy(view):
            context = view.maincontext
            view = view.mainview

        context = IActionsContext(context, context)

        super(ActionsPortlet, self).__init__(context, request, manager, view)

    def update(self):
        view = self.view
        request = self.request
        context = removeSecurityProxy(self.context)

        actions = []
        for name, action in getAdapters((context, request), IAction):
            if action.isAvailable():
                actions.append(action)

        for name, action in getAdapters((context, request, view), IAction):
            if action.isAvailable():
                actions.append(action)

        for name, acts in getAdapters((context, request), IActions):
            for action in acts:
                actions.append(action)

        categories = []
        for name, category in getUtilitiesFor(IActionCategory):
            data = []
            for action in list(actions):
                if category.schema.providedBy(action):
                    actions.remove(action)
                    data.append((action.weight, action.title, action))

            data.sort()
            categories.append(
                (category.weight, category.title, category,
                 [a for w, t, a in data]))

        categories.sort()
        self.categories = [{'category': category.title, 'actions': acts}
                           for _w, _t, category, acts in categories if acts]

        if actions:
            actions = [(action.weight, action.title, action)
                       for action in actions]
            actions.sort()
            self.categories.append(
                {'category': u'', 'actions': [a for w,t,a in actions]})

        super(ActionsPortlet, self).update()

    def isAvailable(self):
        if IDraftedContent.providedBy(self.context):
            return False

        return bool(self.categories)

    @cache('portlet.actions',
           ActionsPortletCache, ContextModified,
           TagTimeKey(ActionsTag, each20minutes))
    def updateAndRender(self):
        return super(ActionsPortlet, self).updateAndRender()
