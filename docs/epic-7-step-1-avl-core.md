# Épica 7 — Step 1: Backend core AVL

## Objetivo

Implementar la estructura base `AVLTree` en Python puro, sin dependencias externas, manteniendo separación estricta entre lógica de estructura de datos y capas HTTP/servicio/frontend.

## Archivos agregados

```text
backend/app/structures/avl_tree.py
backend/tests/structures/test_avl_tree.py
docs/epic-7-step-1-avl-core.md
```

## Decisiones técnicas

- `AVLNode` mantiene `value`, `left`, `right` y `height`.
- La altura interna del nodo es one-based, estándar en AVL.
- La métrica pública `height()` conserva el contrato visual existente del proyecto: altura cero para árbol vacío o raíz única.
- Los valores duplicados se rechazan con `DUPLICATE_VALUE` para evitar IDs visuales repetidos en React Flow.
- La estructura no importa Flask, servicios, serializers ni rutas.
- Las rotaciones se registran con snapshots `before` y `after` para que los siguientes steps puedan visualizarlas.

## Operaciones implementadas

- Inserción balanceada.
- Eliminación balanceada.
- Búsqueda.
- Recorridos preorder, inorder, postorder y levelorder.
- Métricas base: tamaño, altura, niveles, hojas, aristas, factor de balance y estado balanceado.
- Serialización estructural con metadata AVL.

## Rotaciones cubiertas

```text
LL -> rotación derecha
RR -> rotación izquierda
LR -> izquierda + derecha
RL -> derecha + izquierda
```

Cada evento de rotación sigue este contrato:

```python
{
    "type": "LL | RR | LR | RL",
    "pivot": 30,
    "before": {...},
    "after": {...}
}
```

## Pruebas agregadas

```text
backend/tests/structures/test_avl_tree.py
```

Cobertura incluida:

- Árbol vacío.
- Inserción raíz.
- Orden BST preservado.
- Rechazo de duplicados.
- Rechazo de valores vacíos.
- Rechazo de valores incomparables.
- Rotaciones LL, RR, LR y RL.
- Búsqueda y `contains`.
- Nivel por nodo.
- Recorridos.
- Metadata AVL en levelorder.
- Métricas.
- Eliminación de hoja.
- Eliminación de nodo con un hijo.
- Eliminación de nodo con dos hijos.
- Eliminación de valor inexistente.
- Serialización `to_dict`.
- Limpieza de árbol y eventos.

## Comandos de validación sugeridos

Desde la raíz del proyecto:

```bash
cd backend
pytest tests/structures/test_avl_tree.py
```

Validación completa recomendada antes de continuar:

```bash
cd backend
pytest
```

## Workflow Git del step

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-7-avl-tree

git add backend/app/structures/avl_tree.py \
        backend/tests/structures/test_avl_tree.py \
        docs/epic-7-step-1-avl-core.md

git commit -m "feat(avl): implement avl core structure"
```

## Siguiente step

Step 2 debe integrar la estructura AVL con la capa de servicio, serialización inicial y contrato para operaciones API, sin tocar todavía la interfaz visual completa.
