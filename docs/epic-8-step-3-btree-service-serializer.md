# EduStruct — Épica 8 — Step 3

## Service + serializer React Flow para Árbol B

### Objetivo

Agregar la capa de servicio y serialización visual del Árbol B sin acoplar la estructura pura a Flask ni al frontend.

Este step se apoya en el core implementado en:

- `backend/app/structures/btree.py`

Y extiende los patrones ya usados por BST y AVL:

- servicio de aplicación en `backend/app/services/`
- serialización visual en `backend/app/serializers/react_flow_serializer.py`
- pruebas aisladas por capa

---

## Archivos creados

### `backend/app/services/btree_service.py`

Servicio de aplicación para coordinar operaciones educativas del Árbol B:

- `state()`
- `configure(order)`
- `insert(key)`
- `bulk_insert(keys)`
- `search(key)`
- `traverse(type)`
- `metrics()`
- `load_demo()`
- `reset()`

El servicio mantiene separación estricta de responsabilidades:

- No usa Flask.
- No conoce rutas HTTP.
- No conoce React.
- Traduce errores internos de estructura a errores de dominio del backend.
- Entrega payloads listos para API REST.

---

## Archivos actualizados

### `backend/app/serializers/react_flow_serializer.py`

Se agregó:

```python
def serialize_btree(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
```

La función serializa nodos multi-clave para React Flow usando el contrato:

```json
{
  "keys": [10, 20, 30],
  "leaf": false,
  "level": 2
}
```

Cada nodo React Flow incluye metadata para:

- claves del nodo
- cantidad de claves
- nivel
- si es hoja
- índice de hijo
- claves del padre
- máximo de claves permitido
- categoría visual: `root`, `internal`, `leaf`

---

## Archivos de prueba creados

### `backend/tests/services/test_btree_service.py`

Valida:

- estado inicial
- configuración de orden
- inserción individual
- inserción con split
- inserción masiva
- búsqueda encontrada/no encontrada
- recorridos `levelorder` e `inorder`
- carga demo
- métricas
- reset
- errores de validación
- duplicados
- claves incomparables

### `backend/tests/serializers/test_react_flow_btree_serializer.py`

Valida:

- serialización vacía
- nodos multi-clave
- metadata visual
- categorías `root`, `internal`, `leaf`
- aristas padre-hijo
- distribución horizontal por nivel

---

## Contrato visual del serializer

Ejemplo de nodo:

```json
{
  "id": "btree-20-40",
  "type": "btreeNode",
  "position": {
    "x": 0,
    "y": 0
  },
  "data": {
    "label": "20 | 40",
    "category": "root",
    "metadata": {
      "structure": "btree",
      "keys": [20, 40],
      "leaf": false,
      "level": 0,
      "keyCount": 2,
      "maxKeys": 3
    }
  }
}
```

Ejemplo de arista:

```json
{
  "id": "btree-edge-btree-30-btree-10-20",
  "source": "btree-30",
  "target": "btree-10-20",
  "type": "smoothstep",
  "label": "0",
  "data": {
    "relationship": "parent-child"
  }
}
```

---

## Decisiones técnicas

### 1. Se mantiene Árbol B, no B+

La decisión formal sigue cerrada en:

- `docs/epic-8-step-1-btree-decision.md`

### 2. `serialize_btree()` no depende de `BTree`

Recibe una lista de diccionarios generada por `BTree.levelorder()`.

Ventaja:

- permite probar serializer de forma aislada
- evita dependencia circular estructura → serializer
- mantiene compatibilidad con los serializers existentes

### 3. El servicio reporta splits incrementales

En `insert()` y `bulk_insert()` se capturan únicamente los splits generados por esa operación mediante diferencia de contador antes/después.

Campos relevantes:

```json
{
  "splitOccurred": true,
  "splitEvents": [],
  "lastSplit": {}
}
```

### 4. Demo académica determinística

`load_demo()` usa carnés simulados:

```python
[2024008, 2024016, 2024024, 2024032, 2024040, 2024048, 2024056, 2024064, 2024072, 2024080, 2024088]
```

Esto provoca splits visibles y mantiene el caso de uso de índice académico.

---

## Validación ejecutada

Desde `backend/`:

```bash
PYTHONPATH=. pytest tests/structures/test_btree.py tests/services/test_btree_service.py tests/serializers/test_react_flow_btree_serializer.py -q
```

Resultado:

```text
40 passed
```

Validación completa de backend:

```bash
PYTHONPATH=. pytest tests -q
```

Resultado:

```text
277 passed
```

---

## Workflow Git sugerido

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-8-btree
```

Si la rama ya existe:

```bash
git checkout feature/epic-8-btree
```

Agregar cambios del Step 3:

```bash
git add backend/app/services/btree_service.py \
        backend/app/serializers/react_flow_serializer.py \
        backend/tests/services/test_btree_service.py \
        backend/tests/serializers/test_react_flow_btree_serializer.py \
        docs/epic-8-step-3-btree-service-serializer.md
```

Commit semántico:

```bash
git commit -m "feat(btree): add btree service and serializer"
```

---

## Estado del step

Step 3 queda cerrado técnicamente.

No se implementaron rutas REST ni frontend en este step. Eso corresponde al Step 4 y Step 5 respectivamente.
