from pydantic import BaseModel, Field
# from typing import Self # python3.10才有的
from .convertor import Convertor, CRS

class Location(BaseModel):
    lng: float = Field(..., description="Longitude of the location")
    lat: float = Field(..., description="Latitude of the location")
    crs: CRS = Field(..., description="Coordinate Reference System of the location")

    def convert_to(self, crs: CRS)->'Location':
        lng, lat = Convertor.transform(self.lng, self.lat, self.crs, crs)
        return Location(lng=lng, lat=lat, crs=crs)