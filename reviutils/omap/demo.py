from .samples import Point, Polyline, Text, MarkerTypes, PolylineTypes, Colors, Polygon, PolygonTypes

def create_point_obj(name: str, lng: float, lat: float, is_gcj02: bool):
    style = {"marker_type": MarkerTypes.OvalNailRed}
    return Point(
        name=name,
        lng=lng,
        lat=lat,
        is_gcj02=is_gcj02,
        **style,
    )

def create_circle_obj(name: str, latlng:list[float], is_gcj02: bool):
    assert len(latlng) == 4
    style = {
        "polyline_type": PolylineTypes.Circle,
        "line_width": 300,
        "line_alpha": 40,
        "line_color": Colors.Yellow,
    }
    return Polyline(
        name=name,
        latlng=latlng,
        is_gcj02=is_gcj02,
        **style,
    )

def create_radius_obj(name: str, latlng:list[float], is_gcj02: bool):
    assert len(latlng) == 4
    radius_style = {
        "is_gcj02": is_gcj02,
        "polyline_type": PolylineTypes.Polyline,
        "line_width": 200,
        "line_alpha": 100,
        "line_color": Colors.White,
    }
    return Polyline(
        name=name,
        latlng=latlng,
        **radius_style,
    )
    
def create_radius_text_obj(name: str, lng: float, lat: float, is_gcj02: bool):
    style = {
        "color": Colors.Blue,
        "font_size": 15,
        "rotation": 0,
    }
    return Text(
        name=name,
        lng=lng,
        lat=lat,
        is_gcj02=is_gcj02,
        **style
    )

def create_buildings_obj(name: float, lng: float, lat: float, is_gcj02: bool, building_type: int, font_size: int = 17, rotation: int = 0):
    styles_dict = {
        1: {"color": Colors.White},
        2: {"color": Colors.Orange},
    }
    text = Text(
        name=name,
        is_gcj02=is_gcj02,
        lng=lng,
        lat=lat,
        font_size=font_size,
        rotation=rotation,
        **styles_dict[building_type],
    )
    return text

def create_rectange_obj(name: str, latlng:list[float], is_gcj02: bool):
    assert len(latlng) == 4
    style = {
        "polygon_type": PolygonTypes.Rectangle,
        "line_width": 3,
        "line_alpha": 40,
        "line_color": Colors.Yellow,
        "area_color":Colors.Green,
        "area_alpha": 10,
    }
    
    return Polygon(
        name=name,
        latlng=latlng,
        is_gcj02=is_gcj02,
        **style,
    )
    
def create_polygon_obj(name: str, latlng:list[float], is_gcj02: bool):
    assert len(latlng) >= 6
    style = {
        "polygon_type": PolygonTypes.Polygon,
        "line_width": 3,
        "line_alpha": 40,
        "line_color": Colors.Yellow,
        "area_color":Colors.Pink,
        "area_alpha": 10,
    }
    
    return Polygon(
        name=name,
        latlng=latlng,
        is_gcj02=is_gcj02,
        **style,
    )
    
def create_ellipse_obj(name: str, latlng:list[float], is_gcj02: bool):
    assert len(latlng) == 4
    style = {
        "polygon_type": PolygonTypes.Ellipse,
        "line_width": 3,
        "line_alpha": 40,
        "line_color": Colors.Yellow,
        "area_color":Colors.Green,
        "area_alpha": 10,
    }
    
    return Polygon(
        name=name,
        latlng=latlng,
        is_gcj02=is_gcj02,
        **style,
    )