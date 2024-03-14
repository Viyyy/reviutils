from typing import List, Union, Tuple
import pandas as pd
import numpy as np
from decimal import Decimal
from ..common import round_half_even
from .hourhelper import is_daytime

spl_list_type = Union[pd.Series,np.ndarray,List[float],Tuple[float]]

#region 声级数据计算
def calc_Leq(spl_series:spl_list_type, precision:int=1) -> float:
    '''
    计算一组声级数据的等效声压级（Leq）
    
    参数:
        - spl_series: Union[pd.Series,np.ndarray,List[float],Tuple[float]]，声级数据
        - precision: int，计算精度，默认为1
    返回值:
        float: 计算得到的等效声压级（Leq）
    示例:
        >>> import pandas as pd
        >>> from reviutils.noisepollution.splhelper import calc_Leq
        >>> data = [100, 80, 60, 40, 20]
        >>> df = pd.DataFrame({'SPL':data})
        >>> Leq = calc_Leq(df['SPL'])
        >>> print(Leq)
        93.1
    '''
    if len(spl_series)==0:
        return None
    spl_arr = np.array(spl_series).astype(Decimal)
    # 计算Leq
    Leq = 10 * np.log10( 
                        np.mean(
                            np.power(10, 0.1 * spl_arr))) 
    Leq = round_half_even(Leq, precision) # 保留precision位小数
    return Leq

def calc_Ldn(hour_data:List[int],leq_data:spl_list_type, precision:int=0):
    '''
    计算小时数据的Ld，Ln，Ldn
    
    参数:
        - HourData:小时数据列表
        - LData:声级数据列表
        - precision: int，计算精度，默认为0
    返回值:
        dict: 包含Ld，Ln，Ldn的字典，以及小时数据和声级数据
    示例:
        >>> from reviutils.noisepollution.splhelper import calc_Ldn
        >>> hour_data = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        >>> leq_data = [60,70,67,76,75,70,72,78,75,70,72,78,75,70,72,78,75,70,72,78,75,70,72,75]
        >>> result = calc_Ldn(hour_data, leq_data)
        >>> print(result)
        {'result': {'Ld': 75.0, 'Ln': 73.0, 'Ldn': 79.0}, 'data': {'Day': {'Hour': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], 'Leq': [72, 78, 75, 70, 72, 78, 75, 70, 72, 78, 75, 70, 72, 78, 75, 70]}, 'Night': {'Hour': [0, 1, 2, 3, 4, 5, 22, 23], 'Leq': [60, 70, 67, 76, 75, 70, 72, 75]}}}
        
    '''
    if any(hour < 0 or hour > 23 for hour in hour_data):
        invalid_hours = [hour for hour in hour_data if hour < 0 or hour > 23]
        raise ValueError(f'小时数据中包含范围外的值: {invalid_hours}')
    
    if len(hour_data) != len(leq_data):
        raise ValueError(f'小时数据(length={len(hour_data)})和声级数据(length={len(leq_data)})的长度不一致')
    
    data = {'Hour':hour_data,"Leq":leq_data}
    data = pd.DataFrame(data)
    data['IsDay'] = data['Hour'].map(is_daytime)
    day_data = data[data['IsDay']]
    Ld = calc_Leq(day_data['Leq'], precision=precision)
    night_data = data[data['IsDay']==False]
    Ln = calc_Leq(night_data['Leq'], precision=precision)
    Ldn = calc_Leq(pd.concat([day_data['Leq'],night_data['Leq']+10]), precision=precision)
    return {
        'result':{
            'Ld':Ld,
            'Ln':Ln,
            'Ldn':Ldn,
        },
        'data':{
            'Day':{
                'Hour':day_data['Hour'].values.tolist(),
                'Leq':day_data['Leq'].values.tolist(),
            },
            'Night':{
                'Hour':night_data['Hour'].values.tolist(),
                'Leq':night_data['Leq'].values.tolist(),
            }
        }
    }

def calc_Lt(spl_series:spl_list_type, precision:int=1) -> float:
    '''
    计算一组声级数据的叠加声压级（Lt）
    
    参数:
        - spl_series: pd.Series，声级数据
        - precision: int，计算精度，默认为1
    返回值:
        float: 计算叠加后的声压级（Lt）
    示例:
        >>> import pandas as pd
        >>> from reviutils.noisepollution.splhelper import calc_Lt
        >>> data = [50.1, 52.3, 54.5, 56.7, 58.9, 61.1, 63.3, 65.5, 67.7, 69.9]
        >>> df = pd.DataFrame({'SPL':data})
        >>> Lt = calc_Lt(df['SPL'])
        >>> print(Lt)
        73.9
    '''
    if len(spl_series)==0:
        return "-"
    spl_arr = np.array(spl_series).astype(Decimal)
    Lt = 10 * np.log10(
                        np.sum(
                            np.power(10, 0.1 * spl_arr)))
    Lt = round_half_even(Lt, precision)
    return Lt

def calc_PSL(spl_series:spl_list_type, percent_arr: list=[10, 50, 90], precision: int=1) -> dict:
    '''
    计算一组数据的累积百分声级（percentile sound level, PSL）
    
    参数:
        - spl_series: pd.Series，声级数据
        - percent_arr: list，需要计算的百分位数列表，默认为 [10, 50, 90]
    返回值:
        result: dict，各百分位数所对应的累积百分声级（PSL）
    示例:
        >>> import pandas as pd
        >>> from reviutils.noisepollution.splhelper import calc_PSL
        >>> data = [50.1, 52.3, 54.5, 56.7, 58.9, 61.1, 63.3, 65.5, 67.7, 69.9]
        >>> df = pd.DataFrame({'SPL':data})
        >>> result = calc_PSL(df['SPL'])
        >>> print(result)
        {'L10': 67.9, 'L50': 60.0, 'L90': 52.1}
    '''
    if len(spl_series):
        result = {}
        spl_series = pd.Series(spl_series)
        for idx, percent in enumerate(percent_arr):
            assert percent > 0 and percent < 100, f"百分位数需要在0到100之间: percent_arr[{idx}]={percent}"
            result[f'L{percent}'] = round_half_even(spl_series.quantile(1 - percent / 100), precision)
        return result
    else:
        print("spl_series长度为0")

def calc_LA(spl_series: spl_list_type, precision: int = 1) -> dict:
    '''
    功能:
        计算监测声强时所需的各类声级数据，包括:L10、L50、L90、Leq、Lmax、Lmin、标准差(std)
    参数:
        spl_series: pd.Series，声级数据
    返回值:
        dict: 记录了计算出的各类声级数据，{"L10": float, "L50": float, "L90": float,
                                                            "Leq": float, "Lmax": float, "Lmin": float, "std": float}
    示例:
        >>> import pandas as pd
        >>> from reviutils.noisepollution.splhelper import calc_LA
        >>> data = [50.1, 52.3, 54.5, 56.7, 58.9, 61.1, 63.3, 65.5, 67.7, 69.9]
        >>> df = pd.DataFrame({'SPL':data})
        >>> result = calc_LA(df['SPL'])
        >>> print(result)
        {'L10': 67.9, 'L50': 60.0, 'L90': 52.1, 'Leq': 63.9, 'Lmax': 69.9, 'Lmin': 50.1, 'std': 6.7}
    '''
    if len(spl_series):
        # 调用函数 calc_PSL() 计算 L10、L50、L90
        result = calc_PSL(spl_series, precision=precision)
        # 调用函数 calc_Leq() 计算等效声压级（Leq）
        result['Leq'] = calc_Leq(spl_series, precision=precision)
        # 计算最大值、最小值、标准差
        result['Lmax'] = spl_series.max()
        result['Lmin'] = spl_series.min()
        result['std'] = round_half_even(spl_series.std(), precision)
        return result
#endregion