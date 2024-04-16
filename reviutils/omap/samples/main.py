from .Base import ObjectTypes
from .Base import DetailBase
from .Base import ObjectBase
from .Base import ItemBase
from ..constants import MarkerTypes
from ..constants import Colors
from ..constants import PolylineTypes

from pydantic import Field, BaseModel
from typing import List, Union
import datetime


def obj_to_json(obj):
    result = {}
    for k, v in obj.__dict__.items():
        if isinstance(v, (DetailBase, ObjectBase, ItemBase, BaseModel)):
            result[k] = obj_to_json(v)
        elif isinstance(v, list):
            result[k] = []
            for item in v:
                if isinstance(item, (DetailBase, ObjectBase, ItemBase, BaseModel)):
                    result[k].append(obj_to_json(item))
                else:
                    result[k].append(item)
        else:
            result[k] = v
    return result


class PolygonDetail(BaseModel):
    pass


class Polygon(ItemBase):
    pass


class TrackDrawObject(BaseModel):
    ShowType: int = Field(description="Show type of the track draw object")
    LineClr: int = Field(description="Line color of the track draw object")
    LineWidth: int = Field(description="Line width of the track draw object", gt=0)
    LineAlpha: int = Field(
        description="Line alpha of the track draw object", ge=0, le=100
    )
    CadLineShowWid: int = Field(
        default=0, description="Cad line show width of the track draw object"
    )

    LineType: int = Field(default=0, description="Line type of the track draw object")
    CircleClr: int = Field(
        default=32768, description="Circle color of the track draw object"
    )
    CircleWidth: int = Field(
        default=5, description="Circle width of the track draw object"
    )
    SplineDegree: int = Field(
        default=0, description="Spline degree of the track draw object"
    )
    LineTypeCustom: int = Field(
        default=0, description="Line type custom of the track draw object"
    )
    LineTypeScale: float = Field(
        default=0.00000000, description="Line type scale of the track draw object"
    )
    NeedDrawDetail: int = Field(
        default=0, description="Need draw detail of the track draw object"
    )
    Close: int = Field(default=0, description="Close of the track draw object")


class PolylineDetail(DetailBase):
    Mtp: int = Field(description="Mtp of the polyline")
    Latlng: List[float] = Field(description="List of latitude and longitude of the polyline")
    TrackDraw: TrackDrawObject = Field(description="Track draw object of the polyline")
    Gcj02: int = Field( description="Whether the coordinates are in GCJ02")
    
    ShowName: int = Field(default=0, description="Show name of the polyline")
    Edit: int = Field(default=1, description="Edit status of the polyline")
    
    OverlayIdx: int = Field(default=0, description="Overlay index of the polyline")
    TrackType: int = Field(default=0, description="Track type of the polyline")
    AltitudeColor: int = Field(default=0, description="Altitude color of the polyline")
    
class PolylineObject(ObjectBase):
    def __init__(self, name, detail:PolylineDetail,comment=""):
        super().__init__(name=name, obj_detail=detail, type_id=ObjectTypes.Polyline.value.id)
        self.Comment = comment

class Polyline(ItemBase):
    def __init__(
        self,
        name: str,
        polyline_type: PolylineTypes,
        latlng: List[float],
        is_gcj02: bool,
        line_color: Colors = Colors.Default,
        line_width: int = 1,
        line_alpha: int = 100,
        show_name: bool = False,
        edit: bool = False,
        parent_id: int = 1,
    ):
        # 检查坐标数量是否符合要求
        if len(latlng) % 2 != 0:
            raise ValueError("Polyline coordinates should be even number")
        assert len(latlng)>=polyline_type.value.length_min*2 and len(latlng)<=polyline_type.value.length_max*2, f"Polyline coordinates should be between {polyline_type.value.length_min*2} and {polyline_type.value.length_max*2}"
        tdo = TrackDrawObject(
            LineClr=line_color.value.id,
            LineWidth=line_width,
            LineAlpha=line_alpha,
            ShowType=polyline_type.value.ShowType,
        )
        detail = PolylineDetail(
            Gcj02=is_gcj02,
            Mtp = polyline_type.value.Mtp,
            Latlng=latlng,
            TrackDraw=tdo,
            ShowName=show_name,
            Edit=edit
        )
        obj = PolylineObject(name=name, detail=detail)
        super().__init__(
            obj=obj,
            parent_id=parent_id,
            type_id=ObjectTypes.Polyline.value.id,
        )
        


# region Point
class SignPicObject(BaseModel):
    SignPic: int = Field(description="Sign picture id")
    AlignFlag: int = Field(default=0, description="Alignment flag of the sign picture")
    SignClr: int = Field(default=0, description="Sign color of the sign picture")
    PicScale: int = Field(default=0, description="Scale of the sign picture")
    SignPicNum: int = Field(default=0, description="Sign picture number")
    SignPicNumOffx: int = Field(default=0, description="Sign picture number offset x")
    SignPicNumOffy: int = Field(default=0, description="Sign picture number offset y")
    SignPicNumClr: int = Field(default=0, description="Sign picture number color")
    SignPicNumSize: int = Field(default=0, description="Sign picture number size")

class ExtInfoObject(BaseModel):
    FontClr: int = Field(default=65535, description="Font color of the object")
    FontRotateAngle: int = Field(default=0, description="Font rotate angle of the object")
    FontName: str = Field(default="", description="Font name of the object")
    FontZoomWithMap: int = Field(default=0, description="Font zoom with map status of the object")
    FontWithBox: int = Field(default=0, description="Font with box status of the object")
    FontAlpha: int = Field(default=0, description="Font alpha of the object")
    FontEffect: int = Field(default=0, description="Font effect of the object")
    FontBkStyle: int = Field(default=0, description="Font background style of the object")
    FontBkClr: int = Field(default=0, description="Font background color of the object")
    FontMinLevel: int = Field(default=0, description="Font min level of the object")
    FontMaxLevel: int = Field(default=0, description="Font max level of the object")
    FontBindLevel: int = Field(default=0, description="Font bind level of the object")
    FontSize: int = Field(default=16, description="Font size of the object")
    NoHotFontEvent: int = Field(default=0, description="No hot font event of the object")
    NoHotMapEvent: int = Field(default=0, description="No hot map event of the object")
    ShowComment: int = Field(default=0, description="Show comment of the object")
    CommentAlign: int = Field(default=0, description="Comment align of the object")
    
class PointDetailBase(DetailBase):
    Lng: float = Field(description="Longitude of the point")
    Lat: float = Field(description="Latitude of the point")
    Gcj02: int = Field(
        default=False, description="Whether the coordinates are in GCJ02"
    )
    Altitude: int = Field(default=0, description="Altitude of the point")
    EditMode: int = Field(default=0, description="Edit mode of the point")
    OverlayIdx: int = Field(default=0, description="Overlay index of the point")
    TimeUncertain: int = Field(default=0, description="Time uncertain of the point")
    SignEvent: dict = Field(default={"Radius": 0, "ShowClr": 0})
    Time: str = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    TxtShowSta: int = Field(default=0, description="Text show status of the point")
    TxtShowStaSet: int = Field(
        default=0, description="Text show status set of the point"
    )
    
class TextDetail(PointDetailBase):
    ExtInfo: ExtInfoObject = Field(description="Ext info object of the point")
    TxtType: int = Field(default=3, description="Text type of the point")

class Text(ItemBase):
    def __init__(
        self,
        name: str,
        lng: float,
        lat: float,
        is_gcj02: bool,
        color: Colors = Colors.Default,
        rotation: int = 0,
        parent_id: int = 1,
    ):
        extinfo = ExtInfoObject(
            FontClr=color.value.id,
            FontRotateAngle=rotation
        )
        detail = TextDetail(Lng=lng, Lat=lat, Gcj02=is_gcj02, ExtInfo=extinfo)
        obj = ObjectBase(
            name=name, obj_detail=detail, type_id=ObjectTypes.Point.value.id
        )
        super().__init__(
            obj=obj,
            parent_id=parent_id,
            type_id=ObjectTypes.Point.value.id,
        )
    
class PointDetail(PointDetailBase):
    SignPic: SignPicObject = Field(description="Sign picture object of the point")
    TxtType: int = Field(default=1, description="Text type of the point")

class Point(ItemBase):
    def __init__(
        self,
        name: str,
        lng: float,
        lat: float,
        is_gcj02: bool,
        marker_type: MarkerTypes = MarkerTypes.OvalNailRed,
        parent_id: int = 1,
    ):
        sign_pic = SignPicObject(SignPic=marker_type.value.id)
        detail = PointDetail(Lng=lng, Lat=lat, Gcj02=is_gcj02, SignPic=sign_pic)
        obj = ObjectBase(
            name=name, obj_detail=detail, type_id=ObjectTypes.Point.value.id
        )
        super().__init__(
            obj=obj,
            parent_id=parent_id,
            type_id=ObjectTypes.Point.value.id,
        )


# endregion


# region Folder
class FolderDetail(DetailBase):
    ObjChildren: list = Field(default=[], description="List of child objects")
    LoadOk: int = Field(default=1, description="Load status of the object")
    SaveMerge: int = Field(default=0, description="Save merge status of the object")
    Group: int = Field(default=0, description="Group status of the object")
    AutoLoad: int = Field(default=1, description="Auto load status of the object")
    Share: int = Field(default=0, description="Share status of the object")
    ReadOnly: int = Field(default=0, description="Read only status of the object")
    NotHotId: int = Field(default=0, description="Not hot id of the object")
    Bind: int = Field(default=0, description="Bind status of the object")
    BindCheck: int = Field(default=0, description="Bind check status of the object")
    Link: int = Field(default=0, description="Link status of the object")
    LinkAutoCheck: int = Field(
        default=0, description="Link auto check status of the object"
    )
    ChildiOverlay: int = Field(
        default=0, description="Child overlay status of the object"
    )
    LineClr: int = Field(default=0, description="Line color of the object")
    LineAlpha: int = Field(default=0, description="Line alpha of the object")
    LineType: int = Field(default=0, description="Line type of the object")
    LineWid: int = Field(default=0, description="Line width of the object")
    LineUrl: str = Field(default="", description="Line url of the object")
    Relate: int = Field(default=0, description="Relate status of the object")

    @property
    def Child(self):
        return len(self.ObjChildren)

    def add_child(self, child: Union[ItemBase, List[ItemBase]]):
        if isinstance(child, list):
            for c in child:
                self.add_child(c)
        elif isinstance(child, ItemBase):
            self.ObjChildren.append(child)
        else:
            raise NotImplementedError(f"Unsupported child type: {type(child)}")


class Folder(ItemBase):
    def __init__(
        self,
        name: str,
        detail: FolderDetail,
        parent_id: int = 1,
    ):
        obj = ObjectBase(
            name=name, obj_detail=detail, type_id=ObjectTypes.Folder.value.id
        )
        super().__init__(
            obj=obj,
            parent_id=parent_id,
            type_id=ObjectTypes.Folder.value.id,
        )

    def add_child(self, child: Union[ItemBase, List[ItemBase]]):
        if isinstance(child, list):
            for c in child:
                c.ParentID = self.ObjID
        else:
            child.ParentID = self.ObjID
        self.Object.ObjectDetail.add_child(child)
        return self


# endregion
