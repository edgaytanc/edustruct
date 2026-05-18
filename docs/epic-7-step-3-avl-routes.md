# Épica 7 — Step 3: Endpoints REST para Árbol AVL

## Objetivo

Exponer el árbol AVL mediante API REST siguiendo el contrato ya usado por las estructuras previas del proyecto EduStruct.

## Archivos incluidos

```text
backend/app/routes/avl.py
backend/tests/routes/test_avl_routes.py
docs/epic-7-step-3-avl-routes.md
```

## Endpoints implementados

```text
GET     /api/avl/state
POST    /api/avl/insert
DELETE  /api/avl/delete
GET     /api/avl/search
POST    /api/avl/demo/load
GET     /api/avl/traverse
GET     /api/avl/metrics
POST    /api/avl/reset
```

## Contrato de respuesta

Todos los endpoints devuelven el formato estándar del proyecto:

```json
{
  "success": true,
  "message": "...",
  "data": {
    "structure": "avl",
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

## Detalles técnicos

- Se conecta `backend/app/routes/avl.py` con `AVLService`.
- Se mantiene una instancia de servicio por blueprint, igual al patrón usado en `binary_tree.py`.
- Se agregan helpers internos para extraer `nodes`, `edges`, `metrics` y `traversal` desde el resultado del servicio.
- Se agrega normalización de valores de entrada para convertir strings numéricos recibidos por query params a enteros.
- Las operaciones `insert` y `delete` devuelven snapshots `before` y `after` cuando aplica.
- Las rotaciones visibles se exponen en `result.rotationEvents` y `result.lastRotation`.
- El endpoint `/metrics` expone métricas AVL: altura, cantidad de nodos, niveles, balance de raíz, cantidad de hojas, estado balanceado y cantidad de rotaciones.

## Pruebas agregadas

Se creó:

```text
backend/tests/routes/test_avl_routes.py
```

Cobertura validada:

- Estado vacío del árbol.
- Inserciones con rotaciones LL, RR, LR y RL.
- Validación de valor requerido.
- Rechazo de duplicados.
- Carga de dataset demo.
- Búsqueda encontrada y no encontrada.
- Eliminación por JSON body y query param.
- Eliminación en árbol vacío.
- Eliminación de valor inexistente.
- Recorridos `inorder` y `levelorder`.
- Rechazo de recorrido inválido.
- Métricas.
- Reset.

## Validación sugerida

```bash
PYTHONPATH=backend pytest backend/tests/routes/test_avl_routes.py -q
PYTHONPATH=backend pytest backend/tests/structures/test_avl_tree.py backend/tests/services/test_avl_service.py backend/tests/serializers/test_react_flow_avl_serializer.py backend/tests/routes/test_avl_routes.py -q
PYTHONPATH=backend pytest backend/tests -q
```

## Workflow Git

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-7-avl-tree
```

Commit semántico sugerido para este step:

```bash
git add backend/app/routes/avl.py backend/tests/routes/test_avl_routes.py docs/epic-7-step-3-avl-routes.md
git commit -m "feat(avl): expose avl rest endpoints"
```

## Estado

Step 3 deja lista la capa REST del AVL para que el frontend pueda consumir operaciones, métricas, snapshots antes/después y eventos de rotación.
