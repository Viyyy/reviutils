# -*- coding: utf-8 -*-
# Author: Vi
# Created on: 2024-03-15 09:38:39
# Description: 用于处理小时数据，区分昼夜间

from functools import singledispatch
from datetime import datetime

_day_hours = range(6,22)
_hour_range = range(24)
_out_of_range_hour = ValueError('小时需在0-23之间')

@singledispatch
def is_daytime(time):
    raise NotImplementedError("Unsupported type: {}".format(type(time)))

@is_daytime.register(int)
def _(time):
    assert time in _hour_range, _out_of_range_hour
    return time in _day_hours

@is_daytime.register(str)
def _(time):
    try:
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        return is_daytime(time)
    except Exception:
        raise ValueError('无法解析时间字符串: {}'.format(time))

@is_daytime.register(float)
def _(time):
    hour = int(time)
    return is_daytime(hour)

@is_daytime.register(datetime)
def _(time):
    return time.hour in _day_hours

@is_daytime.register(bool)
def _(time):
    return time
