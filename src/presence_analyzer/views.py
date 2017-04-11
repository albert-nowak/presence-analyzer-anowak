# -*- coding: utf-8 -*-
"""
Defines views.
"""
import calendar
from flask import redirect, abort
from time import gmtime, strftime

from main import app
from utils import jsonify, get_data, mean, \
    group_by_weekday

import logging
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@app.route('/')
def mainpage():
    """
    Redirects to front page.
    """
    return redirect('/static/presence_weekday.html')


@app.route('/api/v1/users', methods=['GET'])
@jsonify
def users_view():
    """
    Users listing for dropdown.
    """
    data = get_data()
    return [
        {'user_id': i, 'name': 'User {0}'.format(str(i))}
        for i in data.keys()
    ]


@app.route('/api/v1/mean_time_weekday/<int:user_id>', methods=['GET'])
@jsonify
def mean_time_weekday_view(user_id):
    """
    Returns mean presence time of given user grouped by weekday.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = group_by_weekday(data[user_id])
    result = [
        (calendar.day_abbr[weekday], mean(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]

    return result


@app.route('/api/v1/presence_weekday/<int:user_id>', methods=['GET'])
@jsonify
def presence_weekday_view(user_id):
    """
    Returns total presence time of given user grouped by weekday.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = group_by_weekday(data[user_id])
    result = [
        (calendar.day_abbr[weekday], sum(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]

    result.insert(0, ('Weekday', 'Presence (s)'))
    return result


@app.route('/api/v1/presence_start_end/<int:user_id>', methods=['GET'])
@jsonify
def presence_start_end_view(user_id):
    """
    Returns daily timespan working hours of given user.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    start_times = group_by_weekday(data[user_id], seconds=True, start=True)
    end_times = group_by_weekday(data[user_id], seconds=True, end=True)

    result = []
    for i in xrange(7):  # 7 days a week
        avg_start = round(mean(start_times[i]))
        avg_end = round(mean(end_times[i]))
        hour_start = strftime('%H:%M:%S', gmtime(avg_start))
        hour_end = strftime('%H:%M:%S', gmtime(avg_end))
        result.append(
            [
                calendar.day_abbr[i],
                'January 1, ' + hour_start,
                'January 1, ' + hour_end
            ]
        )
    return result
