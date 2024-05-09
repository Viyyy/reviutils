from .samples import *
import json

class ItemManager:
    def __init__(self, items:list[ItemBase]=None):
        if items is None:
            self.items:list[ItemBase] = []
        else:
            self.items = items
        
    def add_item(self, item:ItemBase):
        self.items.append(item)
        
    def __len__(self):
        return len(self.items)
    
    def save_ovjsn(self, save_path):
        """
        保存OMAP对象到json文件
        - obj_items: OMAP对象列表
        - save_path: 保存路径
        """
        items = [obj_to_json(item) for item in self.items]
        with open(save_path, "w", encoding="utf-8") as f:
            result = {"Version": "V9.9.3", "Type": 1, "ObjItems": items}
            json.dump(result, f, ensure_ascii=False, indent=4)
            print(save_path, "保存成功")
        