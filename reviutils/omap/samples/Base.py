from datetime import datetime
from ..constants import ObjectTypes
from pydantic import BaseModel, Field
import time
import random

def create_obj_id():
    timestamp = int(time.time())  # 获取当前时间戳
    random_num = random.randint(1000, 9999)  # 生成一个四位数的随机整数
    id_value = int(timestamp) + random_num  # 结合时间戳和随机数生成ID
    return id_value

class DetailBase(BaseModel):
    ShowLevel: int = Field(default=1, description="Show level of the point")
    ShowLevelMax: int = Field(default=0, description="Show level max of the point")

class ObjectBase:
    def __init__(self, type_id: int, obj_detail, name: str = ""):
        self.Name = name
        self.Type = type_id
        self.ObjectDetail = obj_detail

class ItemBase:
    def __init__(
        self,
        type_id: ObjectTypes,
        obj: ObjectBase,
        parent_id: int = 1,
    ):
        self.ObjID = create_obj_id()
        self.ParentID = parent_id
        self.Type = type_id
        self.Object = obj
        self.tmModify = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
