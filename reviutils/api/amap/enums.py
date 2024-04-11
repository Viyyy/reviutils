from enum import Enum

class CoordSys(Enum):
    WGS84 = 'gps'
    MapBar = 'mapbar'
    Baidu = 'baidu'
    AutoNavi = 'autonavi' # 高德坐标