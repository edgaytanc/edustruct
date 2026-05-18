# Épica 6 — STEP 2: Rutas Flask para Árbol Binario

## Objetivo

Conectar el `BinaryTreeService` con la API REST de Flask mediante el blueprint existente `binary_tree_bp`.

## Archivos involucrados

```text
backend/app/routes/binary_tree.py
backend/tests/routes/test_binary_tree_routes.py
docs/epic-6-step-2-binary-tree-routes.md
```

## Endpoints implementados

Base path:

```text
/api/binary-tree
```

### GET `/state`

Retorna el estado actual del árbol binario.

### POST `/insert`

Inserta un valor en el BST.

Payload:

```json
{
  "value": 50
}
```

### DELETE `/delete`

Elimina un valor del BST.

Acepta JSON:

```json
{
  "value": 50
}
```

O query param:

```text
/api/binary-tree/delete?value=50
```

### GET `/search`

Busca un valor.

```text
/api/binary-tree/search?value=40
```

### POST `/demo/load`

Carga el árbol demo:

```text
50, 25, 75, 10, 40, 60, 90
```

### GET `/traverse`

Recorridos disponibles:

```text
preorder
inorder
postorder
levelorder
```

Ejemplo:

```text
/api/binary-tree/traverse?type=inorder
```

### GET `/metrics`

Retorna métricas del árbol.

### POST `/reset`

Limpia el árbol.

## Contrato de respuesta

Todas las rutas usan `success_response`, manteniendo el contrato estándar:

```json
{
  "success": true,
  "message": "...",
  "data": {
    "structure": "binary-tree",
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

## Manejo de errores

Los errores siguen el flujo global de handlers:

- `ValidationError` → HTTP 400
- `DuplicateKeyError` → HTTP 409
- `NotFoundError` → HTTP 404
- `StructureEmptyError` → HTTP 422

## Validación esperada

```bash
cd backend
pytest tests/routes/test_binary_tree_routes.py
```

Resultado esperado:

```text
16 passed
```

## Git workflow

```bash
git checkout develop
git pull origin develop
git checkout feature/epic-6-binary-tree
```

Commit sugerido:

```bash
git add backend/app/routes/binary_tree.py backend/tests/routes/test_binary_tree_routes.py docs/epic-6-step-2-binary-tree-routes.md
git commit -m "feat(binary-tree): expose bst rest endpoints"
```
