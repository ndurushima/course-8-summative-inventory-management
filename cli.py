#!/usr/bin/env python3
import os
import argparse
import json
import requests
from typing import Optional

API = os.environ.get("INVENTORY_API", "http://localhost:5555")

def _print_json(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))

def cmd_list(args):
    params = {}
    if args.category:
        params["category"] = args.category
    r = requests.get(f"{API}/items", params=params)
    _print_json(_response_json(r))

def cmd_add(args):
    payload = {"name": args.name, "category": args.category, "price": args.price}
    r = requests.post(f"{API}/items", json=payload)
    _print_json(_response_json(r))

def cmd_get(args):
    r = requests.get(f"{API}/items/{args.item_id}")
    _print_json(_response_json(r))

def cmd_update(args):
    body = {}
    if args.name is not None: body["name"] = args.name
    if args.category is not None: body["category"] = args.category
    if args.price is not None: body["price"] = args.price
    if not body:
        print("Nothing to update. Pass at least one of --name/--category/--price")
        return
    r = requests.patch(f"{API}/items/{args.item_id}", json=body)
    _print_json(_response_json(r))

def cmd_delete(args):
    r = requests.delete(f"{API}/items/{args.item_id}")
    _print_json(_response_json(r))

def cmd_lookup_barcode(args):
    r = requests.get(f"{API}/lookup/{args.barcode}")
    _print_json(_response_json(r))

def cmd_lookup_name(args):
    params = {"name": args.name}
    if args.limit is not None:
        params["limit"] = args.limit
    r = requests.get(f"{API}/lookup", params=params)
    _print_json(_response_json(r))


def _response_json(r: requests.Response):
    try:
        data = r.json()
    except ValueError:
        data = {"error": f"Non-JSON response", "status_code": r.status_code, "text": r.text[:200]}
    # Attach HTTP status in output for clarity
    return {"status_code": r.status_code, "data": data}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventory Management CLI (talks to the Flask API)"
    )
    parser.add_argument(
        "--api", default=API,
        help=f"Base API URL (default: {API}). Can also set INVENTORY_API env var."
    )

    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("list", help="List items (optionally filter by category)")
    p.add_argument("--category", help="Filter by category")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("add", help="Add a new item")
    p.add_argument("name")
    p.add_argument("category")
    p.add_argument("price", type=float)
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("get", help="Get an item by ID")
    p.add_argument("item_id")
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("update", help="Update an item (partial)")
    p.add_argument("item_id")
    p.add_argument("--name")
    p.add_argument("--category")
    p.add_argument("--price", type=float)
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("delete", help="Delete an item by ID")
    p.add_argument("item_id")
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("lookup-barcode", help="Lookup product by barcode (OpenFoodFacts)")
    p.add_argument("barcode")
    p.set_defaults(func=cmd_lookup_barcode)

    p = sub.add_parser("lookup-name", help="Search products by name (OpenFoodFacts)")
    p.add_argument("name")
    p.add_argument("--limit", type=int, default=5)
    p.set_defaults(func=cmd_lookup_name)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    # Allow overriding API base per call
    global API
    API = args.api

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
