from enum import Enum
import math
from typing import Union

class CRS(Enum):
    WGS84 = 'EPSG:4326'
    GCJ02 = 'EPSG:3395'
    BD09 = 'EPSG:3857'
    MapBar = 'EPSG:54030'

# region 5个基础的坐标转换
''' MapBar-->WGS84<-->GCJ02<-->BD09
    # 5个基础的坐标转换
    1. MapBar-->WGS84
    2. WGS84-->GCJ02
    3. GCJ02-->WGS84
    4. GCJ02-->BD09
    5. BD09-->GCJ02
'''
PI = math.pi
PIX = PI * 3000.0 / 180.0 # 弧度
EE = 0.00669342162296594323 # 偏心率平方
A = 6378245.0 # 长半轴

def transform_lat(lng, lat):
    """GCJ02 latitude transformation"""
    ret = -100 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * PI) + 40.0 * math.sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * PI) + 320.0 * math.sin(lat * PI / 30.0)) * 2.0 / 3.0
    return ret

def transform_lng(lng, lat):
    """GCJ02 longtitude transformation"""
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * PI) + 40.0 * math.sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * PI) + 300.0 * math.sin(lng / 30.0 * PI)) * 2.0 / 3.0
    return ret

def out_of_china(lng, lat):
    """No offset when coordinate out of China."""
    if lng < 72.004 or lng > 137.8437:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False

# 1. MapBar-->WGS84
def _mapbar_to_wgs84(lng:float, lat:float) -> tuple:
    lng = lng * 100000.0 % 36000000
    lat = lat * 100000.0 % 36000000
    lng1 = int(lng - math.cos(lat / 100000.0) * lng / 18000.0 - math.sin(lng / 100000.0) * lat / 9000.0) 
    lat1 = int(lat - math.sin(lat / 100000.0) * lng / 18000.0 - math.cos(lng / 100000.0) * lat / 9000.0)
    lng2 = int(lng - math.cos(lat1 / 100000.0) * lng1 / 18000.0 - math.sin(lng1 / 100000.0) * lat1 / 9000.0 + (1 if lng > 0 else -1))
    lat2 = int(lat - math.sin(lat1 / 100000.0) * lng1 / 18000.0 - math.cos(lng1 / 100000.0) * lat1 / 9000.0 + (1 if lat > 0 else -1)) 
    lng, lat = lng2 / 100000.0, lat2 / 100000.0
    return lng, lat

# 2. WGS84-->GCJ02
def _wgs84_to_gcj02(lng:float, lat:float) -> tuple:
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((A * (1 - EE)) / (magic * sqrtmagic) * PI)
    dlng = (dlng * 180.0) / (A / sqrtmagic * math.cos(radlat) * PI)
    lng, lat = lng + dlng, lat + dlat
    return lng, lat

# 3. GCJ02-->WGS84
def _gcj02_to_wgs84(lng:float, lat:float) -> tuple:
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((A * (1 - EE)) / (magic * sqrtmagic) * PI)
    dlng = (dlng * 180.0) / (A / sqrtmagic * math.cos(radlat) * PI)
    lng, lat = lng - dlng, lat - dlat
    return lng, lat

# 4. GCJ02-->BD09
def _gcj02_to_bd09(lng:float, lat:float) -> tuple:
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * PIX)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * PIX)
    lng, lat = z * math.cos(theta) + 0.0065, z * math.sin(theta) + 0.006
    return lng, lat

# 5. BD09-->GCJ02
def _bd09_to_gcj02(lng:float, lat:float) -> tuple:
    x, y =  lng - 0.0065, lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * PIX)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * PIX)
    lng, lat = z * math.cos(theta), z * math.sin(theta)
    return lng, lat
# endregion

class _Convertor:
    graph:dict[CRS, dict[CRS, list[callable]]]={} # 转换图, 经纬度坐标系是多对多的关系，因此使用图表示

    def add_transform(self, from_crs:CRS, to_crs:CRS, func:Union[list[callable],callable]):
        if from_crs not in self.graph:
            self.graph[from_crs] = {}
        self.graph[from_crs][to_crs] = func if isinstance(func, list) else [func]

    def transform(self, lng:float, lat:float, from_crs:CRS, to_crs:CRS) -> tuple:
        if from_crs == to_crs:
            return lng, lat
        if from_crs not in self.graph or to_crs not in self.graph[from_crs]:
            raise ValueError(f"No transform from {from_crs} to {to_crs}")
        for func in self.graph[from_crs][to_crs]:
            lng, lat = func(lng, lat)
        return lng, lat
    
    def transform_batch(self, lngs:list[float], lats:list[float], from_crs:CRS, to_crs:CRS) -> list[tuple]:
        if from_crs == to_crs:
            return list(zip(lngs, lats))
        if from_crs not in self.graph or to_crs not in self.graph[from_crs]:
            raise ValueError(f"No transform from {from_crs} to {to_crs}")
        for func in self.graph[from_crs][to_crs]:
            lngs, lats = list(zip(*[func(lng, lat) for lng, lat in zip(lngs, lats)]))
        return list(zip(lngs, lats))
    
    def show_graph(self):
        for from_crs in self.graph:
            for to_crs in self.graph[from_crs]:
                print(f"{from_crs} To {to_crs}: {'->'.join([func.__name__ for func in self.graph[from_crs][to_crs]])}")
# 实例化转换器
Convertor = _Convertor()

# 注册转换函数
Convertor.add_transform(CRS.MapBar, CRS.WGS84, _mapbar_to_wgs84) # MapBar-->WGS84
Convertor.add_transform(CRS.WGS84, CRS.GCJ02, _wgs84_to_gcj02) # WGS84-->GCJ02
Convertor.add_transform(CRS.GCJ02, CRS.WGS84, _gcj02_to_wgs84) # GCJ02-->WGS84
Convertor.add_transform(CRS.GCJ02, CRS.BD09, _gcj02_to_bd09) # GCJ02-->BD09
Convertor.add_transform(CRS.BD09, CRS.GCJ02, _bd09_to_gcj02) # BD09-->GCJ02

# 注册多步转换函数
Convertor.add_transform(CRS.MapBar, CRS.GCJ02, [_mapbar_to_wgs84, _wgs84_to_gcj02]) # MapBar-->WGS84-->GCJ02
Convertor.add_transform(CRS.MapBar, CRS.BD09, [_mapbar_to_wgs84, _wgs84_to_gcj02, _gcj02_to_bd09]) # MapBar-->WGS84-->GCJ02-->BD09
Convertor.add_transform(CRS.WGS84, CRS.BD09, [_wgs84_to_gcj02, _gcj02_to_bd09]) # WGS84-->GCJ02-->BD09
Convertor.add_transform(CRS.BD09, CRS.WGS84, [_bd09_to_gcj02, _gcj02_to_wgs84]) # BD09-->GCJ02-->WGS84