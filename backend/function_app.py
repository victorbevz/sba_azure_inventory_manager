import azure.functions as func
import json

from Inventory import Inventory
from Product import Product
from Utils import apply_global_discount

app = func.FunctionApp()

inventory = Inventory()
inventory.add_product(Product("Laptop", 4000, 2))
inventory.add_product(Product("Mouse", 50, 10))
inventory.add_product(Product("Keyboard", 120, 5))


def cors_response(body: dict, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(body),
        status_code=status_code,
        mimetype="application/json",
        headers={"Access-Control-Allow-Origin": "*"}
    )


@app.route(route="products", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET", "OPTIONS"])
def get_products(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type"})

    products = [
        {"name": p.name, "price": round(p.price, 2), "quantity": p.quantity}
        for p in inventory.products
    ]
    return cors_response(products)


@app.route(route="total", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET", "OPTIONS"])
def total(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, OPTIONS", "Access-Control-Allow-Headers": "Content-Type"})

    return cors_response({"total": round(inventory.total_inventory_value(), 2)})


@app.route(route="discount", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST", "OPTIONS"])
def discount(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type"})

    try:
        body = req.get_json()
    except ValueError:
        return cors_response({"error": "Invalid JSON body"}, 400)

    percent = body.get("percent")

    if percent is None:
        return cors_response({"error": "Missing field: percent"}, 400)

    try:
        percent = float(percent)
    except (TypeError, ValueError):
        return cors_response({"error": "percent must be a number"}, 400)

    if not (0 < percent <= 100):
        return cors_response({"error": "percent must be between 1 and 100"}, 400)

    apply_global_discount(inventory.products, percent)
    return cors_response({"message": f"Discount of {percent}% applied successfully"})


@app.route(route="reset", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST", "OPTIONS"])
def reset(req: func.HttpRequest) -> func.HttpResponse:
    """Reset inventory to original prices (useful since state is in-memory)."""
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type"})

    inventory.products.clear()
    inventory.add_product(Product("Laptop", 4000, 2))
    inventory.add_product(Product("Mouse", 50, 10))
    inventory.add_product(Product("Keyboard", 120, 5))
    return cors_response({"message": "Inventory reset to defaults"})
