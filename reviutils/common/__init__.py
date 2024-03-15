# -*- coding: utf-8 -*-
# Author: Vi
# Created on: 2024-03-15 09:40:23
# Description: 常用方法集合

from bisect import bisect_left
from typing import List, Union
from enum import Enum
import random
import time
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_EVEN

def grade(score, breakpoints: List[Union[int, float]], grades: List[str]) -> str:
    """
    根据分数和分数段来确定等级。

    参数:
        - score (int 或 float): 要评级的分数。
        - breakpoints (List[int 或 float]): 分数段的断点列表，必须有序排列。
        - grades (List[str]): 对应的等级列表。

    返回值:
        str: 分数对应的等级。

    示例:
        >>> breakpoints = [60, 70, 80, 90]
        >>> grades = 'EDCBA'
        >>> grade(75, breakpoints, grades)
        'C'
    """
    i = bisect_left(breakpoints, score)
    return grades[i]

def get_passrate(pass_num:int, total:int, rep:str='-', check_pass:bool=False):
    '''
    计算达标率/采样率，返回百分比字符串
    参数:
        - pass_num:  达标数（分子）
        - total: 总数（分母）
        - rep: 空值，分母为0时的替代值，默认为 “-”
        - check_pass: 如果为True，当pass_num==0, 返回rep
    返回值:
        - str: 达标率百分比字符串， 或替代值
    示例:
        >>> get_passrate(10, 20)
        '50.00%'
        >>> get_passrate(0, 20)
        '0.00%'
        >>> get_passrate(0, 20, check_pass=True)
        '-'
    '''
    if check_pass:
        return rep if pass_num==0 or total==0 else '{:.2f}%'.format(pass_num/total * 100)
    else:
        return rep if total==0 else '{:.2f}%'.format(pass_num/total * 100)
    
def get_random_str(random_str:str = "reviutils"):
    '''
    获取随机字符串
    参数:
        - random_str: 随机字符串，默认为 "reviutils"
    返回值:
        - str: 随机字符串
    示例:
        >>> get_random_str()
    '''
    random_str = list(random_str)
    random.shuffle(random_str)
    random_str = list(f"{time.time_ns()}_{''.join(random_str)}")
    random.shuffle(random_str)
    return ''.join(random_str)

class TimeStr(Enum):
    '''常用的时间格式'''
    Ymd = "%Y-%m-%d"
    Ymd_CN = "%Y年%m月%d日"
    md_ = "%m-%d"
    md_CN = "%m月%d日"
    YmdHMS = "%Y-%m-%d %H:%M:%S"
    YmdHMS_CN = "%Y年%m月%d日 %H时%M分%S秒"
    
def get_time_str(time_:Union[datetime, date], type_:TimeStr):
   '''
   获取指定时间的字符串格式
   参数:
       - time_: 时间对象
       - type_: 时间格式枚举
   返回值:
       - str: 时间字符串
   示例:
       >>> get_time_str(datetime.now(), TimeStr.Ymd)
   '''
   return time_.strftime(type_.value)

def round_half_even(value:float, precision:int=1)->float:
    """
    对给定的浮点数进行四舍五入操作，并遵循四舍五入六成双的规则。

    参数:
        - value (float): 待四舍五入的浮点数。
        - precision: 保留的小数位数，默认值为1，即保留1位小数。

    返回值:
        float: 四舍五入后的结果。
    示例:
        >>> round_half_even(3.141592653589793,2)
        3.14
    """
    try:
        return float(Decimal(value).quantize(Decimal(f'{10**(-precision)}'), rounding=ROUND_HALF_EVEN))
    except:
        return '-'