from .main import Location, Convertor, CRS

__all__ = [
    'Location',
    'Convertor',
    'CRS'
]

import numpy as np
import pyproj

alpha = 216.6 /200 # 距离修正系数
alpha = 50 /(49.775+49.917)*2 * alpha # 距离修正系数

def calculate_new_coordinate(lng, lat, distance_in_meters,angle=0, alpha=alpha):
    '''
    计算距离lng，lat点distance_in_meters米的新坐标
    - param lng: 原坐标经度, wgs84坐标系
    - param lat: 原坐标纬度, wgs84坐标系
    - param distance_in_meters: 距离（米）
    - param alpha: 距离修正系数
    - param angle: 角度（度）
    '''
    assert angle>=0 and angle<360
    # 定义墨卡托投影的CRS
    crs = pyproj.CRS.from_string("+proj=merc +lon_0=105 +lat_ts=0 +x_0=0 +y_0=0 +a=6378137 +b=6378137 +units=m +no_defs")

    # 创建转换器
    transformer = pyproj.Transformer.from_crs("EPSG:4326", crs, always_xy=True)

    # 将经纬度坐标转换为墨卡托坐标
    x, y = transformer.transform(lng, lat)

    # 计算目标距离
    target_distance = distance_in_meters * alpha

    # 计算新的坐标
    new_x = x + target_distance * np.cos(np.deg2rad(angle))
    new_y = y + target_distance * np.sin(np.deg2rad(angle))

    # 将新的x坐标转换回经纬度坐标
    new_lng, new_lat = transformer.transform(new_x, new_y, direction="INVERSE")

    # 返回新的经度和纬度坐标
    return round(new_lng,8), round(new_lat,8)