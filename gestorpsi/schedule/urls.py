# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.schedule.views',
    (r'^$', 'index'), # list objects
    (r'^save/$', 'save'), # save new object
	(r'^(?P<date_start>[0-9]{14})/(?P<date_end>[0-9]{14})$', 'schedules_in_range'), # schedules by range
	(r'^(?P<date_start>[0-9]{8})$', 'schedules_daily'), # schedules daily

#    (r'^add/$', 'form'), # new object form
#    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'form'), # edit object form
#    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', 'save'), # update object
#    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/delete/$', 'delete'), # delete object
)