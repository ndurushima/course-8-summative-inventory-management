from flask import Flask, request, jsonify
from models import list_items, create_item, update_item, get_items, delete_item
from utils import ok, json_required, bad_request, not_found
import requests

app = Flask(__name__)

@app.post("/items")
def create_item_route():
    data, err, code = json_required("name", "category", "price")
    if err:
        return err, code
    try:
        item = create_item( 
            name=data["name"],
            category=data["category"],
            price=data["price"]
        )
        return ok(item, 201)
    except ValueError as e:
        return bad_request(str(e))

@app.get("/items")
def list_items_route():
    category = request.args.get("category")
    items = list_items(category)
    return ok({"count": len(items), "items":items})

@app.get("/items/<item_id>")
def get_item_route(item_id):
    item = get_items(item_id)
    if not item:
        return not_found("Item not found")
    return ok(item)

@app.patch("/items/<item_id>")
def update_item_route(item_id):
    if not get_items(item_id):
        return not_found("Item not found")
    data = request.get_json(silent=True) or {}
    try:
        updated = update_item(item_id, **data)
        return ok(updated)
    except ValueError as e:
        return bad_request(str(e))

@app.delete("/items/<item_id>")
def delete_item_route(item_id):
    if delete_item(item_id):
        return ok({"deleted": item_id})
    return not_found("Item not found")

@app.get("/lookup/<barcode>")
def lookup_product(barcode):
    try:
        url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}.json"
        resp = requests.get(url, auth=("off", "off"), timeout=5)

        if resp.status_code != 200:
            return bad_request("Failed to fetch product details")

        data = resp.json()

        if data.get("status") != 1:
            return not_found("Product not found")

        product = data["product"]

        simplified = {
            "barcode": barcode,
            "name": product.get("product_name"),
            "brands": product.get("brands"),
            "categories": product.get("categories"),
            "nutriscore": product.get("nutriscore_grade"),
        }

        return ok(simplified)

    except requests.RequestException:
        return bad_request("Error connecting to external API")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5555)