import requests
from functools import cache
from .enums import CoordSys

class AmapAPI:
    def __init__(self, key, secret:str=None):
        self.key = key
        self.secret = secret
    
    @cache
    def get_lng_lat(self, address):
        '''地理编码,获取经纬度
        参数：
        - address：地址
        返回值：
        - 经度和纬度，格式为元组
        '''
        url = f'https://restapi.amap.com/v3/geocode/geo?address={address}&key={self.key}'
        
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            location = result.get('geocodes')
            
            if location:
                location = location[0].get('location')
                return tuple(map(float, location.split(',')))
            else:
                return None
    
    @cache
    def get_address(self, lng, lat):
        '''逆地理编码,获取地址信息
        参数：
        - lng：经度
        - lat：纬度
        返回值：
        - 地址信息，格式为字典
        '''
        url = f'https://restapi.amap.com/v3/geocode/regeo?output=json&location={lng},{lat}&key={self.key}'
        
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            address = result.get('regeocode')
            
            if address:
                return address.get('formatted_address')
            else:
                return None
            
    @cache
    def convert_lng_lat(self, lng, lat, coord_sys:CoordSys=CoordSys.GPS):
        '''坐标转换,将坐标从一种坐标系转换为另一种坐标系
        参数：
        - lng：经度
        - lat：纬度
        - type_：转换类型，可选值有CoordSys.GPS、CoordSys.Baidu、CoordSys.Mapbar
        返回值：
        - 转换后的经度和纬度，格式为元组
        '''
        url = f'https://restapi.amap.com/v3/assistant/coordinate/convert?locations={lng},{lat}&coordsys={coord_sys.value}&key={self.key}'
        
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            location = result.get('locations')
            
            if location:
                return tuple(map(float, location.split(',')))
            else:
                return None
            

        
        