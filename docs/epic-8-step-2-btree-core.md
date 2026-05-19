# Épica 8 — Step 2: Backend core BTree

## Objetivo

Implementar la estructura base `BTree` en Python puro, sin dependencias externas, manteniendo separación estricta entre lógica de estructura de datos y capas HTTP, servicios, serializadores o frontend.

## Archivos agregados

```text
backend/app/structures/btree.py
backend/tests/structures/test_btree.py
docs/epic-8-step-2-btree-core.md
```

También se incluye el documento validado del Step 1 para mantener continuidad en la rama:

```text
docs/epic-8-step-1-btree-decision.md
```

## Decisiones técnicas

- Se implementa `BTree` y `BTreeNode` manualmente en Python puro.
- El `order` representa el máximo número de hijos por nodo.
- Cada nodo puede almacenar como máximo `order - 1` claves.
- El orden mínimo permitido es `3`.
- La inserción se realiza de forma recursiva y divide nodos cuando exceden el máximo de claves.
- Los duplicados se rechazan con `DUPLICATE_KEY` para evitar identificadores visuales ambiguos.
- Los eventos de split se registran en `split_events` para ser reutilizados por servicio, API y React Flow en steps posteriores.
- La estructura no importa Flask, servicios, rutas ni serializadores.

## Contrato base de nodo

```python
class BTreeNode:
    keys
    children
    leaf
```

Cada nodo serializa a:

```python
{
    "keys": [10, 20, 30],
    "leaf": False,
    "children": [...]
}
```

## Operaciones implementadas

- `insert(key)`
- `search(key)`
- `contains(key)`
- `inorder()`
- `levelorder()`
- `levelorder_nodes()`
- `height()`
- `levels_count()`
- `node_count()`
- `leaf_count()`
- `edges_count()`
- `to_dict()`
- `validate_invariants()`
- `clear()`

## Split events

Cada split registra metadata pensada para visualización:

```python
{
    "type": "SPLIT",
    "level": 1,
    "promotedKey": 30,
    "beforeKeys": [10, 20, 30, 40],
    "leftKeys": [10, 20],
    "rightKeys": [40],
    "leaf": True,
    "createdNewRoot": False,
    "parentKeysAfter": [...]
}
```

## Pruebas agregadas

```text
backend/tests/structures/test_btree.py
```

Cobertura incluida:

- Árbol vacío.
- Validación de orden.
- Inserción raíz.
- Rechazo de duplicados.
- Rechazo de claves vacías.
- Rechazo de claves incomparables.
- Split de raíz.
- Inserciones múltiples.
- Búsqueda exitosa y fallida.
- Metadata de recorrido por niveles.
- Métricas.
- Limpieza del árbol.
- Serialización `to_dict`.
- Validación de invariantes.
- Orden configurable con `order=5`.

## Comandos de validación sugeridos

Desde la raíz del proyecto:

```bash
cd backend
pytest tests/structures/test_btree.py
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
git checkout -b feature/epic-8-btree

git add backend/app/structures/btree.py \
        backend/tests/structures/test_btree.py \
        docs/epic-8-step-1-btree-decision.md \
        docs/epic-8-step-2-btree-core.md

git commit -m "feat(btree): implement btree core structure"
```

## Siguiente step

Step 3 debe integrar `BTree` con la capa de servicio y extender el serializador React Flow con soporte para nodos multi-clave.
