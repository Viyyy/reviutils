from enum import Enum
from pydantic import BaseModel, Field
from typing import Union

# region Base classes
class ConstantsBase(BaseModel):
    """
    Marker type class
    - name: Marker type name
    - id: Marker type id
    """

    name: str = Field(..., description="constant name")
    id: Union[int, None] = Field(..., description="constant id")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{type(self)}(name='{self.name}', id={self.id})"


class EnumBase(Enum):
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)
# endregion


# region 标签类型
class MarkerType(ConstantsBase):
    """
    Marker type class
    - name: Marker type name
    - id: Marker type id, corresponds to the SignPic value
    """

    pass


class MarkerTypes(EnumBase):
    """Marker types enum class"""

    PushPinYellow = MarkerType(name="图钉-黄色", id=4)
    PushPinBlue = MarkerType(name="图钉-蓝色", id=5)
    PushPinGreen = MarkerType(name="图钉-绿色", id=6)
    PushPinCyan = MarkerType(name="图钉-青色", id=7)
    PushPinRed = MarkerType(name="图钉-红色", id=10)
    PushPinWhite = MarkerType(name="图钉-白色", id=11)
    OvalNailRed = MarkerType(name="椭圆钉-红色", id=123)
    OvalNailWhite = MarkerType(name="椭圆钉-白色", id=52)
    OvalNailGreen = MarkerType(name="椭圆钉-绿色", id=53)
    OvalNailCyan = MarkerType(name="椭圆钉-青色", id=54)
    OvalNailBlue = MarkerType(name="椭圆钉-蓝色", id=56)
    WireNailRed = MarkerType(name="线钉-红色", id=1)
    WireNailGreen = MarkerType(name="线钉-绿色", id=2)
    WireNailBlue = MarkerType(name="线钉-蓝色", id=3)


# endregion


# region 字体颜色
class Color(ConstantsBase):
    """
    Font color type class
    - name: Font color name
    - id: Font color id
    """

    pass


class Colors(EnumBase):
    """ color enum class """
    Default = Color(name="默认", id=65535)
    Black = Color(name="黑色", id=4194304000)
    White = Color(name="白色", id=4211081215)
    Pink = Color(name="粉色", id=4202692863)
    Green = Color(name="绿色", id=4194369280)
    Blue = Color(name="蓝色", id=4211015680)
    Red = Color(name="红色", id=4194304255)
    Yellow = Color(name="黄色", id=4194369535)
    Cyan = Color(name="青色", id=4211080960)
    Purple = Color(name="紫色", id=4211015808)
    Orange = Color(name="橙色", id=4194304511)
# endregion


# region 对象类型
class ObjectType(ConstantsBase):
    """
    Object type class
    - name: Object type name
    - id: Object type id
    """

    pass


class ObjectTypes(EnumBase):
    """Object type enum class"""
    Point = ObjectType(name="点", id=7)
    Polyline = ObjectType(name="线", id=8)
    Polygon = ObjectType(name="多边形", id=13)
    Folder = ObjectType(name="文件夹", id=30)
    

class PolylineType(ConstantsBase):
    Mtp:int = Field(description="MTP, 指最多的点的数量")
    ShowType:int = Field(description="显示类型")
    length_min: int = Field(description="至少需要的坐标数")
    length_max: int = Field(description="最多允许的坐标数")
    
class PolylineTypes(EnumBase):
    Polyline = PolylineType(name="折线", id=8, Mtp=2, ShowType=5, length_min=2, length_max=9999)
    Arc = PolylineType(name="圆弧", id=8, Mtp=3, ShowType=7, length_min=3, length_max=3)
    Ellipse = PolylineType(name="椭圆", id=8, Mtp=3, ShowType=9, length_min=3, length_max=3)
    Circle = PolylineType(name="圆", id=8, Mtp=2, ShowType=7, length_min=2, length_max=2)
    
class PolygonType(ConstantsBase):
    start_angle: int = Field(description="起始角度")
    end_angle: int = Field(description="终止角度")
    
    length_min: int = Field(description="至少需要的坐标数")
    length_max: int = Field(description="最多允许的坐标数")
    
class PolygonTypes(EnumBase):
    Polygon = PolygonType(name="多边形", id=13, start_angle=180, end_angle=180, length_min=3, length_max=9999)
    Rectangle = PolygonType(name="矩形", id=13, start_angle=180, end_angle=180, length_min=2, length_max=2)
    Ellipse = PolygonType(name="椭圆", id=13, start_angle=0, end_angle=360, length_min=2, length_max=2)
# endregion
