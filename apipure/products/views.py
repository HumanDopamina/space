import json
from decimal import Decimal, InvalidOperation

from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Product


def product_to_dict(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "stock": product.stock,
        "active": product.active,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat(),
    }


def parse_json(request):
    try:
        return json.loads(request.body or "{}"), None
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, JsonResponse(
            {"error": "El cuerpo de la solicitud debe ser JSON válido."}, status=400
        )


def validate_product(data, *, partial=False):
    """Devuelve los valores normalizados y los errores de validación."""
    values, errors = {}, {}
    required_fields = ("name", "price")

    for field in required_fields:
        if not partial and field not in data:
            errors[field] = "Este campo es obligatorio."

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            errors["name"] = "Debe ser un texto no vacío."
        elif len(data["name"].strip()) > 150:
            errors["name"] = "No puede superar los 150 caracteres."
        else:
            values["name"] = data["name"].strip()

    if "description" in data:
        if not isinstance(data["description"], str):
            errors["description"] = "Debe ser texto."
        else:
            values["description"] = data["description"].strip()

    if "price" in data:
        try:
            price = Decimal(str(data["price"]))
            if (
                not price.is_finite()
                or price < 0
                or price > Decimal("99999999.99")
                or price.as_tuple().exponent < -2
            ):
                raise InvalidOperation
            values["price"] = price.quantize(Decimal("0.01"))
        except (InvalidOperation, TypeError, ValueError):
            errors["price"] = (
                "Debe ser un número entre 0 y 99999999.99 con hasta dos decimales."
            )

    if "stock" in data:
        stock = data["stock"]
        if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
            errors["stock"] = "Debe ser un entero igual o mayor que cero."
        else:
            values["stock"] = stock

    if "active" in data:
        if not isinstance(data["active"], bool):
            errors["active"] = "Debe ser verdadero o falso."
        else:
            values["active"] = data["active"]

    return values, errors


@csrf_exempt
def product_list(request):
    if request.method == "GET":
        products = Product.objects.all()
        search = request.GET.get("search")
        if search:
            products = products.filter(name__icontains=search.strip())
        if request.GET.get("active") in ("true", "false"):
            products = products.filter(active=request.GET["active"] == "true")
        return JsonResponse({"count": products.count(), "results": [product_to_dict(p) for p in products]})

    if request.method == "POST":
        data, error_response = parse_json(request)
        if error_response:
            return error_response
        if not isinstance(data, dict):
            return JsonResponse({"error": "El JSON debe ser un objeto."}, status=400)
        values, errors = validate_product(data)
        if errors:
            return JsonResponse({"errors": errors}, status=400)
        product = Product.objects.create(**values)
        return JsonResponse(product_to_dict(product), status=201)

    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "GET":
        return JsonResponse(product_to_dict(product))

    if request.method in ("PUT", "PATCH"):
        data, error_response = parse_json(request)
        if error_response:
            return error_response
        if not isinstance(data, dict):
            return JsonResponse({"error": "El JSON debe ser un objeto."}, status=400)
        values, errors = validate_product(data, partial=request.method == "PATCH")
        if errors:
            return JsonResponse({"errors": errors}, status=400)
        for field, value in values.items():
            setattr(product, field, value)
        product.save()
        return JsonResponse(product_to_dict(product))

    if request.method == "DELETE":
        product.delete()
        return JsonResponse({}, status=204)

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])
