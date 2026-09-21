# API de productos con Django

API REST mínima creada solo con Django: no usa Django REST Framework.

## Preparación

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe runserver
```

La API queda disponible en `http://127.0.0.1:8000/api/`.

## Endpoints

| Método | URL | Función |
| --- | --- | --- |
| `GET` | `/api/products/` | Lista productos. Admite `?search=texto` y `?active=true`/`false`. |
| `POST` | `/api/products/` | Crea un producto. |
| `GET` | `/api/products/<id>/` | Obtiene un producto. |
| `PUT` / `PATCH` | `/api/products/<id>/` | Actualiza un producto (`PUT` exige nombre y precio; `PATCH`, solo los campos que cambien). |
| `DELETE` | `/api/products/<id>/` | Elimina un producto. |

Ejemplo para crear un producto:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/products/ `
  -ContentType 'application/json' `
  -Body '{"name":"Teclado mecánico","description":"Switches rojos","price":"59.90","stock":12,"active":true}'
```

Los campos obligatorios son `name` y `price`. `stock` inicia en `0` y `active` en `true` si se omiten.
