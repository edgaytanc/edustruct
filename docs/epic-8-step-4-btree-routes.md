# Épica 8 — Step 4: REST routes del Árbol B

## Objetivo

Exponer el core y el servicio del Árbol B mediante endpoints REST coherentes con los patrones ya usados en BST y AVL.

## Archivos actualizados

- `backend/app/routes/btree.py`
- `backend/tests/routes/test_btree_routes.py`
- `docs/epic-8-step-4-btree-routes.md`

## Endpoints implementados

Base path:

```txt
/api/btree
```

Rutas:

```txt
GET  /state
POST /configure
POST /insert
POST /bulk-insert
GET  /search
POST /demo/load
GET  /traverse
GET  /metrics
POST /reset
```

## Contrato principal

Todas las respuestas mantienen el contrato estándar:

```json
{
  "success": true,
  "message": "...",
  "data": {
    "structure": "btree",
    "operation": "...",
    "nodes": [],
    "edges": [],
    "metrics": {},
    "traversal": {},
    "result": {}
  },
  "error": null
}
```

## Operaciones soportadas

### Estado

```http
GET /api/btree/state
```

Devuelve el árbol actual, nodos React Flow, aristas, métricas e invariantes.

### Configurar orden

```http
POST /api/btree/configure
Content-Type: application/json

{
  "order": 5
}
```

Reinicia el árbol con un nuevo orden. El orden mínimo válido es `3`.

### Insertar clave

```http
POST /api/btree/insert
Content-Type: application/json

{
  "key": 2024008
}
```

Inserta una clave individual. Si ocurre split, la respuesta incluye:

```json
{
  "splitOccurred": true,
  "lastSplit": {
    "type": "SPLIT",
    "promotedKey": 30,
    "beforeKeys": [10, 20, 30, 40],
    "leftKeys": [10, 20],
    "rightKeys": [40]
  }
}
```

### Inserción múltiple

```http
POST /api/btree/bulk-insert
Content-Type: application/json

{
  "keys": [40, 20, 60, 10, 30, 50, 70]
}
```

También se soporta `POST /api/btree/insert` con `keys` para facilitar consumo desde frontend.

### Buscar

```http
GET /api/btree/search?key=2024048
```

Devuelve:

- `found`
- `node`
- `level`
- `path`
- snapshot visual completo

### Cargar demo

```http
POST /api/btree/demo/load
```

Carga claves de expedientes académicos y produce splits visibles.

### Recorridos

```http
GET /api/btree/traverse?type=levelorder
GET /api/btree/traverse?type=inorder
```

El recorrido por niveles permite visualizar nodos multi-clave por nivel. El inorder permite verificar orden lógico de las claves.

### Métricas

```http
GET /api/btree/metrics
```

Incluye:

- `count`
- `height`
- `levels`
- `order`
- `maxKeys`
- `minKeys`
- `nodeCount`
- `leafCount`
- `edgesCount`
- `splitCount`
- `isValid`

### Reset

```http
POST /api/btree/reset
```

Limpia el árbol conservando el orden configurado.

## Validaciones HTTP

- `400 VALIDATION_ERROR`: falta `key`, `keys` no es lista, orden inválido o recorrido inválido.
- `409 DUPLICATE_KEY`: clave duplicada.

## Validación ejecutada

```bash
cd backend
PYTHONPATH=. pytest tests/routes/test_btree_routes.py
PYTHONPATH=. pytest tests/routes tests/services/test_btree_service.py tests/serializers/test_react_flow_btree_serializer.py tests/structures/test_btree.py
```

## Commit sugerido

```bash
git add backend/app/routes/btree.py \
        backend/tests/routes/test_btree_routes.py \
        docs/epic-8-step-4-btree-routes.md

git commit -m "feat(btree): expose btree rest endpoints"
```
