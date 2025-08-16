from typing import Dict, Any, Optional
from uuid import uuid4

DB: Dict[str, Dict[str, Any]] = {}

def create_item(name: str, category: str, price: float) -> Dict[str, Any]:
    item_id = str(uuid4())
    item = {
        "id": item_id,
        "name": name,
        "category": category,
        "price": float(price)
    }
    DB[item_id] = item
    return item


def list_items(category: Optional[str] = None):
    # Fetch Items from the databse, optionally filtering by category
    items = list(DB.values())
    if category:
        items = [i for i in items if i["category"].lower() == category.lower()]
    return items

def get_items(item_id: str) -> Optional[Dict[str, Any]]:
    return DB.get(item_id)

def update_item(item_id: str, **fields) -> Optional[Dict[str, Any]]:
    item = DB.get(item_id)
    if not item:
        return None
    name = fields.get("name", item["name"])
    category = fields.get("category", item["category"])
    price = fields.get("price", item["price"])
    item.update({"name": name, "category": category, "price": price})
    return item