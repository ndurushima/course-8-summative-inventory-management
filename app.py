from flask import Flask, request, jsonify
from models import list_items, create_item
from utils import ok, json_required, bad_request

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
    except ValueError:
        return bad_request("data validation error")


@app.get("/items")
def list_items_route():
    category = request.args.get("category")
    items = list_items(category)
    return ok({"count": len(items), "items":items})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5555)