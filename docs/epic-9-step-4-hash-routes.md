# Épica 9 — Step 4: Rutas REST para Tabla Hash

## Objetivo

Exponer la tabla hash manual mediante endpoints REST compatibles con el contrato existente de EduStruct:

React → API REST Flask → servicio → estructura en Python puro.

## Archivos nuevos o modificados

```text
backend/app/routes/hash_table.py
backend/tests/routes/test_hash_table_routes.py
docs/epic-9-step-4-hash-routes.md
```

> Nota técnica: el proyecto ya tenía registrado `backend/app/routes/hash_table.py` en `backend/app/routes/__init__.py`. Por coherencia arquitectónica y para no tocar wiring funcional innecesario, se reemplazó el placeholder existente por la implementación real de rutas. No se creó `hash_routes.py` para evitar duplicar blueprints o romper compatibilidad.

## Endpoints implementados

Base URL:

```text
/api/hash
```

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/state` | Obtiene estado actual, buckets, nodos, aristas y métricas. |
| POST | `/configure` | Configura capacidad inicial y reinicia la tabla. |
| POST | `/insert` | Inserta una entrada `{ key, value }`. También acepta alias `entries` para inserción múltiple. |
| POST | `/bulk-insert` | Inserta múltiples entradas. |
| GET | `/search?key=...` | Busca por carnet/clave. |
| DELETE | `/delete` | Elimina por clave usando body JSON o query param. |
| POST | `/demo/load` | Carga demo estudiantil con colisiones visibles. |
| GET | `/metrics` | Obtiene métricas actuales. |
| GET | `/traverse` | Recorre buckets y cadenas como inspección didáctica. |
| POST | `/reset` | Limpia la tabla y reinicia contador de colisiones. |

## Contrato de respuesta

Se reutiliza `success_response()` para conservar el formato estándar:

```json
{
  "success": true,
  "message": "...",
  "data": {
    "structure": "hash",
    "operation": "insert",
    "nodes": [],
    "edges": [],
    "metrics": {},
    "traversal": {},
    "result": {}
  },
  "error": null
}
```

## Manejo de errores

Las rutas delegan validaciones al servicio y a los handlers globales:

- `ValidationError` → HTTP 400
- `DuplicateKeyError` → HTTP 409
- `StructureEmptyError` → HTTP 422
- `NotFoundError` → HTTP 404

Esto mantiene separación estricta de responsabilidades: la ruta traduce HTTP, el servicio coordina el caso de uso y la estructura conserva la lógica pura.

## Pruebas agregadas

Archivo:

```text
backend/tests/routes/test_hash_table_routes.py
```

Cobertura incluida:

- Estado inicial.
- Configuración por JSON y query param.
- Validación de capacidad inválida.
- Inserción individual.
- Inserción múltiple.
- Alias `entries` desde `/insert`.
- Detección de colisiones.
- Búsqueda encontrada y no encontrada.
- Validación de clave faltante.
- Eliminación por body y query param.
- Errores de tabla vacía y clave inexistente.
- Carga demo con colisiones.
- Métricas.
- Recorrido por buckets.
- Reset.

## Validación ejecutada

```bash
cd backend
PYTHONPATH=. pytest
```

Resultado:

```text
368 passed
```

## Workflow Git

Comandos recomendados para este step:

```bash
git status
git add backend/app/routes/hash_table.py backend/tests/routes/test_hash_table_routes.py docs/epic-9-step-4-hash-routes.md
git commit -m "feat(hash): expose hash table endpoints"
```

## Estado del step

Step 4 completado y detenido para validación explícita antes de avanzar al Step 5.
