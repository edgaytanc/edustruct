# Épica 7 — Step 2: Servicio AVL y serialización React Flow

## Objetivo

Integrar el núcleo `AVLTree` con una capa de servicio desacoplada y una serialización compatible con React Flow, sin exponer todavía endpoints REST ni frontend.

## Archivos agregados

```text
backend/app/services/avl_service.py
backend/tests/services/test_avl_service.py
backend/tests/serializers/test_react_flow_avl_serializer.py
docs/epic-7-step-2-avl-service-serializer.md
```

## Archivos actualizados

```text
backend/app/serializers/react_flow_serializer.py
```

## Funcionalidad implementada

### Servicio AVL

`AVLService` coordina operaciones de aplicación sobre `AVLTree`:

- `state()`
- `insert(value)`
- `delete(value)`
- `search(value)`
- `traverse(type)`
- `metrics()`
- `load_demo()`
- `reset()`

El servicio mantiene separación estricta entre estructura pura y API HTTP. No depende de Flask.

### Visualización antes/después

Las operaciones mutables devuelven:

```json
{
  "before": { "nodes": [], "edges": [] },
  "after": { "nodes": [], "edges": [] }
}
```

Esto prepara el contrato para que el frontend pueda mostrar el árbol antes y después de una inserción o eliminación.

### Rotaciones visibles

El servicio expone:

```json
{
  "rotationEvents": [],
  "lastRotation": null
}
```

Cada evento conserva el contrato definido en Step 1:

```json
{
  "type": "LL | RR | LR | RL",
  "pivot": 30,
  "before": {},
  "after": {}
}
```

### Serialización AVL

Se agregó `serialize_avl_tree()` en:

```text
backend/app/serializers/react_flow_serializer.py
```

Cada nodo serializado incluye metadata AVL:

```json
{
  "height": 3,
  "visualHeight": 2,
  "balanceFactor": -1,
  "isUnbalanced": false,
  "structure": "avl-tree"
}
```

## Dataset demo temporal del servicio

Para Step 2 se agregó una demo determinística desde el servicio:

```python
[10, 20, 50, 25, 27, 40, 30]
```

Esta secuencia fuerza rotaciones visibles y deja el árbol balanceado. El dataset JSON formal se agregará en un step posterior cuando se conecte con endpoints y UI.

## Validaciones cubiertas

Pruebas agregadas para validar:

- Estado inicial serializable.
- Inserción AVL.
- Rotaciones LL, RR, LR, RL desde servicio.
- Demo balanceada con eventos de rotación.
- Búsqueda.
- Eliminación con rebalanceo.
- Recorridos.
- Métricas.
- Reset.
- Metadata React Flow AVL.
- Categoría visual para nodo desbalanceado cuando el serializer la recibe.

## Workflow Git sugerido

```bash
git status
git add backend/app/services/avl_service.py \
        backend/app/serializers/react_flow_serializer.py \
        backend/tests/services/test_avl_service.py \
        backend/tests/serializers/test_react_flow_avl_serializer.py \
        docs/epic-7-step-2-avl-service-serializer.md
git commit -m "feat(avl): add avl service and serializer"
```

## Próximo step recomendado

`Step 3`: exponer endpoints REST en `backend/app/routes/avl.py`, registrar blueprint si aplica y crear pruebas de rutas.
