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

from datetime import datetime, date, time, timedelta
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext as _
from swingtime.forms import MultipleOccurrenceForm, SingleOccurrenceForm
from swingtime import utils
from gestorpsi.schedule.models import ScheduleOccurrence, OccurrenceConfirmation
from gestorpsi.place.models import Room
from gestorpsi.device.models import DeviceDetails
from gestorpsi.schedule import settings as swingtime_settings
from gestorpsi.util.widgets import SplitSelectDateTimeWidget
from gestorpsi.schedule.models import OCCURRENCE_CONFIRMATION_PRESENCE 

def timeslot_offset_options(
    interval=swingtime_settings.TIMESLOT_INTERVAL,
    start_time=swingtime_settings.TIMESLOT_START_TIME,
    end_delta=swingtime_settings.TIMESLOT_END_TIME_DURATION,
    fmt=swingtime_settings.TIMESLOT_TIME_FORMAT
):
    '''
    Create a list of time slot options for use in swingtime forms.
    
    The list is comprised of 2-tuples containing the number of seconds since the
    start of the day and a 12-hour temporal representation of that offset.
    
    '''
    dt = datetime.combine(date.today(), time(0))
    dtstart = datetime.combine(dt.date(), start_time)
    dtend = dtstart + end_delta
    options = []

    delta = utils.time_delta_total_seconds(dtstart - dt)
    seconds = utils.time_delta_total_seconds(interval)
    while dtstart <= dtend:
        options.append((delta, dtstart.strftime('%H:%M')))
        dtstart += interval
        delta += seconds
    
    return options

default_timeslot_options = timeslot_offset_options()
default_timeslot_offset_options = timeslot_offset_options()

class SplitDateTimeWidget(forms.MultiWidget):
    '''
    A Widget that splits datetime input into a SelectDateWidget for dates and
    Select widget for times.
    
    '''
    #---------------------------------------------------------------------------
    def __init__(self, attrs=None):
        widgets = (
            SelectDateWidget(attrs=attrs), 
            forms.Select(choices=default_timeslot_options, attrs=attrs)
        )
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

    #---------------------------------------------------------------------------
    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        
        return [None, None]

class ScheduleSingleOccurrenceForm(SingleOccurrenceForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), widget=forms.Select(attrs={'class':'extramedium asm', }))
    device = forms.ModelMultipleChoiceField(required = False, queryset=DeviceDetails.objects.all(), widget=forms.SelectMultiple(attrs={'class':'multiselectable', }))
    annotation = forms.CharField(required = False, widget=forms.Textarea(attrs={'class':'giant'}))
    
    class Meta:
        model = ScheduleOccurrence

class ScheduleOccurrenceForm(MultipleOccurrenceForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), widget=forms.Select(attrs={'class':'extramedium asm', }))
    device = forms.ModelMultipleChoiceField(required = False, queryset=DeviceDetails.objects.all(), widget=forms.SelectMultiple(attrs={'class':'multiselectable', }))
    annotation = forms.CharField(required = False, widget=forms.Textarea())
    start_time_delta = forms.IntegerField(
        label='Start time',
        widget=forms.Select(choices=default_timeslot_offset_options)
    )
    
    end_time_delta = forms.IntegerField(
        label='End time',
        widget=forms.Select(choices=default_timeslot_offset_options)
    )
    
    class Meta:
        model = ScheduleOccurrence

    def save(self, event):
        if self.cleaned_data['repeats'] == 'no':
            params = {}
        else:
            params = self._build_rrule_params()

        event.errors = event.add_occurrences(
            self.cleaned_data['start_time'], 
            self.cleaned_data['end_time'],
            self.cleaned_data['room'].id,
            self.cleaned_data['device'],
            self.cleaned_data['annotation'],
            **params
        )

        return event

class OccurrenceConfirmationForm(forms.ModelForm):
    presence = forms.CharField(label=_('Presence'), required=True, widget=forms.RadioSelect(choices=OCCURRENCE_CONFIRMATION_PRESENCE))
    date_started = forms.DateTimeField(label=_('Time Started'), required=False, widget=SplitSelectDateTimeWidget(minute_step=5))
    date_finished = forms.DateTimeField(label=_('Time Finished'), required=False, widget=SplitSelectDateTimeWidget(minute_step=5))
    device = forms.ModelMultipleChoiceField(label=_('Devices utilized in this session'), required = False, queryset=DeviceDetails.objects.all(), widget=forms.SelectMultiple(attrs={'class':'multiselectable', }))
    reason = forms.CharField(label=_('Unmark or Reschedule Reason (if exists)'), required = False, widget=forms.Textarea(attrs={'class':'giant'}))
    anotation = forms.CharField(label=_('Anotation'), required = False, widget=forms.Textarea(attrs={'class':'giant'}))

    def __init__(self, *args, **kwargs):
        super(OccurrenceConfirmationForm, self).__init__(*args, **kwargs)
        self.initial.setdefault('date_started', self.initial.get('start_time'))
        self.initial.setdefault('date_finished', self.initial.get('end_time'))
        self.initial.setdefault('occurrence', self.initial.get('occurrence'))
        self.fields['presence'].required = True

    class Meta:
        model = OccurrenceConfirmation
        fields = ('date_started', 'date_finished', 'presence', 'reason', 'device')
    
    
