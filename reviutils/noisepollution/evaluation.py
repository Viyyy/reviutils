# -*- coding: utf-8 -*-
# Author: Vi
# Created on: 2024-03-14 15:49:43
# Description: '城市区域环境噪声总体水平等级划分'/'道路交通噪声强度等级划分'评价 ——环境噪声监测技术规范城市声环境常规监测HJ640-2012

from ..common import grade
from enum import Enum
from typing import Union
from datetime import datetime
from .hourhelper import is_daytime

class EvaluationResultType(Enum):
    LEVEL = ['一级', '二级', '三级', '四级', '五级']
    DESCRIPTION = ['好','较好','一般','较差','差']
    
class EvaluationType(Enum):
    REGION = {
        True: [50, 55, 60, 65], # 白天
        False: [40, 45, 50, 55] # 夜晚
    }
    TRAFFIC = {
        True: [68, 70, 72, 74], # 白天
        False: [58, 60, 62, 64] # 夜晚
    }

def get_evaluation(value, time:Union[str,int,float,datetime,bool], etype:EvaluationType, rtype:EvaluationResultType=EvaluationResultType.LEVEL):
    '''
    根据环境噪声分贝值和时间，评价噪声污染程度，返回评价结果。
    参数:
        - value: 噪声分贝值，单位dB
        - time: 时间，可以是datetime对象，也可以是字符串或数字(小时值)，如果是字符串，则格式为'YYYY-MM-DD HH:MM:SS'或小时值(0-23)，如果是bool，则表示白天-True，夜晚-False
        - etype: 评价类型，可以是EvaluationType.REGION或EvaluationType.TRAFFIC
        - rtype: 评价结果类型，可以是EvaluationResultType.LEVEL或EvaluationResultType.DESCRIPTION
    返回值:
        - str: 评价结果，如'一级', '好'
    示例:
        >>> get_evaluation(70, '2022-01-01 12:00:00', EvaluationType.TRAFFIC, EvaluationResultType.LEVEL)
        '二级'
        >>> get_evaluation(70, '2022-01-01 12:00:00', EvaluationType.REGION, EvaluationResultType.DESCRIPTION)
        '差'
    '''
    is_day = is_daytime(time)
    return grade(value, breakpoints=etype.value[is_day], grades=rtype.value)