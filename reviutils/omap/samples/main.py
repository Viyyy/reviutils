from .Base import ObjectTypes
from .Base import DetailBase
from .Base import ObjectBase
from .Base import ItemBase
from ..constants import MarkerTypes
from ..constants import Colors
from ..constants import PolylineTypes
from ..constants import PolygonTypes

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


class PolygonDetail(DetailBase):
    '''
    "ObjectDetail":
    {"Gcj02":0,"OverlayIdx":0,"ShowLevel":1,"ShowLevelMax":0,"OuterRgnIdx":0,"EditMode":1,"ShowFlag":0,"LineClr":65535,"LineWidth":1,"CadLineShowWid":0,"LineAlpha":50,"AreaClr":65535,"AreaAlpha":50,"StartAngle":0.00000000,"EndAngle":360.00000000,"FillType":0,"FillSubType":0,"FillPattern":0,"FillChgClr":0,"FillRotate":0.00000000,"FillScale":0.00000000,"FillOffsetX":0.00000000,"FillOffsetY":0.00000000,"Mtp":2,"Latlng":[23.24304351,109.16585804,23.23694565,109.17243418]
    }
    '''
    Mtp: int = Field(description="Mtp of the polygon")
    Latlng: List[float] = Field(description="List of latitude and longitude of the polygon")
    LineClr: int = Field(default=65535, description="Line color of the polygon")
    LineWidth: int = Field(default=1, description="Line width of the polygon")
    
    AreaClr: int = Field(default=65535, description="Area color of the polygon")
    Gcj02: int = Field(description="Whether the coordinates are in GCJ02")
    
    LineAlpha: int = Field(default=50, description="Line alpha of the polygon")
    
    AreaAlpha: int = Field(default=50, description="Area alpha of the polygon")
    
    # 决定形状的值
    StartAngle: float = Field(description="Start angle of the polygon")
    EndAngle: float = Field(description="End angle of the polygon")
    
    OverlayIdx: int = Field(default=0, description="Overlay index of the polygon")
    OuterRgnIdx: int = Field(default=0, description="Outer region index of the polygon")
    EditMode: int = Field(default=1, description="Edit mode of the polygon")
    ShowFlag: int = Field(default=0, description="Show flag of the polygon")
    CadLineShowWid: int = Field(default=0, description="Cad line show width of the polygon")

    FillType: int = Field(default=0, description="Fill type of the polygon")
    FillSubType: int = Field(default=0, description="Fill sub type of the polygon")
    FillPattern: int = Field(default=0, description="Fill pattern of the polygon")
    FillChgClr: int = Field(default=0, description="Fill change color of the polygon")
    FillRotate: float = Field(default=0.0, description="Fill rotate of the polygon")
    FillScale: float = Field(default=0.0, description="Fill scale of the polygon")
    FillOffsetX: float = Field(default=0.0, description="Fill offset x of the polygon")
    FillOffsetY: float = Field(default=0.0, description="Fill offset y of the polygon")

class PolygonObject(ObjectBase):
    def __init__(self, name, detail:PolygonDetail,comment=""):
        super().__init__(name=name, obj_detail=detail, type_id=ObjectTypes.Polygon.value.id)
        self.Comment = comment
        
class Polygon(ItemBase):
    def __init__(
        self,
        name: str,
        polygon_type: PolygonTypes,
        latlng: List[float],
        is_gcj02: bool,
        line_color: Union[Colors,int] = Colors.Default,
        line_width: int = 1,
        line_alpha: int = 0,
        area_color: Union[Colors,int] = Colors.Default,
        area_alpha: int = 0,
        edit: bool = True,
        parent_id: int = 1,
    ):
        # 检查坐标数量是否符合要求
        if len(latlng) % 2 != 0:
            raise ValueError("Polygon coordinates should be even number")
        assert len(latlng)>=polygon_type.value.length_min*2 and len(latlng)<=polygon_type.value.length_max*2, f"Polygon coordinates should be between {polygon_type.value.length_min*2} and {polygon_type.value.length_max*2}"
        detail = PolygonDetail(
            Mtp=len(latlng)//2,
            Latlng=latlng,
            StartAngle=polygon_type.value.start_angle,
            EndAngle=polygon_type.value.end_angle,
            LineClr=line_color.value.id,
            LineWidth=line_width,
            AreaClr=area_color.value.id,
            Gcj02=is_gcj02,
            LineAlpha=line_alpha,
            AreaAlpha=area_alpha,
            EditMode=int(edit),
        )
        obj = PolygonObject(name=name, detail=detail)
        super().__init__(
            obj=obj,
            parent_id=parent_id,
            type_id=ObjectTypes.Polygon.value.id,
        )


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
        line_color: Union[Colors,int] = Colors.Default,
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
            LineClr=line_color.value.id if isinstance(line_color, Colors) else line_color,
            LineWidth=line_width,
            LineAlpha=line_alpha,
            ShowType=polyline_type.value.ShowType,
        )
        detail = PolylineDetail(
            Gcj02=is_gcj02,
            Mtp = len(latlng)//2 if polyline_type == PolylineTypes.Polyline else polyline_type.value.Mtp,
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
        font_size:int = 16,
        color: Union[Colors,int] = Colors.Default,
        rotation: int = 0,
        parent_id: int = 1,
    ):
        extinfo = ExtInfoObject(
            FontClr=color.value.id if isinstance(color, Colors) else color,
            FontRotateAngle=rotation,
            FontSize=font_size
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
        detail: FolderDetail=None,
        parent_id: int = 1,
    ):
        if detail is None:
            detail = FolderDetail()
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
