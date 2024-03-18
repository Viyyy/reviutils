# -*- coding: utf-8 -*-
# Author: Vi
# Created on: 2024-03-18 10:11:34
# Description: 提供声功能区相关信息 ——声环境质量标准(GB 3096-2008)

from enum import Enum
from pydantic import BaseModel, Field
from functools import singledispatch

class FuncAreaInfo(BaseModel):
    """声功能区信息"""
    name: str = Field(description="声功能区名称")
    id: int = Field(description="声功能区ID")
    lmtd: float = Field(description="声功能区昼间限值")
    lmtn: float = Field(description="声功能区昼间限值")
    desc: str = Field(description="声功能区描述")

class FuncArea(Enum):
    # """声功能区"""
    F0 = FuncAreaInfo(name="0类", id=30, lmtd=50, lmtn=40, desc="指康复疗养区等特别需要安静的区域。")
    F1 = FuncAreaInfo(name="1类", id=31, lmtd=55, lmtn=45, desc="指以居民住宅、医疗卫生、文化教育、科研设计、行政办公为主要功能，需要保持安静的区域。")
    F2 = FuncAreaInfo(name="2类", id=32, lmtd=60, lmtn=50, desc="指以商业金融、集市贸易为主要功能，或者居住、商业、工业混杂，需要维护住宅安静的区域。")
    F3 = FuncAreaInfo(name="3类", id=33, lmtd=65, lmtn=55, desc="指以工业生产、仓储物流为主要功能，需要防止工业噪声对周围环境产生严重影响的区域。")
    F4a = FuncAreaInfo(name="4a类", id=34, lmtd=70, lmtn=55, desc="指交通干线两侧一定距离之内，需要防止交通噪声对周围环境产生严重影响的区域，包括4a类和 4b类两种类型。4a类为高速公路、一级公路、二级公路、城市快速路、城市主干路、城市次干路、城市轨道交通(地面段)、内河航道两侧区域。")
    F4b = FuncAreaInfo(name="4b类", id=35, lmtd=70, lmtn=60, desc="指交通干线两侧一定距离之内，需要防止交通噪声对周围环境产生严重影响的区域，包括4a类和 4b类两种类型。4b 类为铁路干线两侧区域。")
    
@singledispatch
def get_func_area_info(name_or_id_or_enum):
    '''
    根据名称（str），id（int）或FuncArea对象，返回对应的FuncAreaInfo对象
    参数:
        - name_or_id_or_enum: str or int or FuncArea, 声功能区名称或ID或Enum对象
    返回值:
        - FuncAreaInfo, 声功能区信息
    示例:
        ```python
        >>> get_func_area_info("F0")
        FuncAreaInfo(name='0类', id=30, lmtd=50.0, lmtn=40.0, desc='指康复疗养区等特别需要安静的区域。')
        >>> get_func_area_info("0类")
        FuncAreaInfo(name='0类', id=30, lmtd=50.0, lmtn=40.0, desc='指康复疗养区等特别需要安静的区域。')
        >>> get_func_area_info(31)
        FuncAreaInfo(name='1类', id=31, lmtd=55.0, lmtn=45.0, desc='指以居民住宅、医疗卫生、文化教育、科研设计、行政办公为主要功能，需要保持安静的区域。')
        >>> get_func_area_info(FuncArea.F2)
        FuncAreaInfo(name='2类', id=32, lmtd=60.0, lmtn=50.0, desc='指以商业金融、集市贸易为主要功能，或者居住、商业、工业混杂，需要维护住宅安静的区域。')
        ```
    '''
    raise NotImplementedError("Unsupported type")

@get_func_area_info.register(str)
def _(name_or_id_or_enum: str):
    for func_area in FuncArea:
        if func_area.value.name == name_or_id_or_enum or func_area.name == name_or_id_or_enum:
            return func_area.value
    raise ValueError(f"Unsupported name: {name_or_id_or_enum}")

@get_func_area_info.register(int)
def _(name_or_id_or_enum: int):
    for func_area in FuncArea:
        if func_area.value.id == name_or_id_or_enum:
            return func_area.value
    raise ValueError(f"Unsupported id: {name_or_id_or_enum}")


@get_func_area_info.register(FuncArea)
def _(name_or_id_or_enum: FuncArea):
    return name_or_id_or_enum.value