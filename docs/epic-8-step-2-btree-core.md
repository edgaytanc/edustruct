# Épica 8 — Step 2: Core del Árbol B

## Objetivo

Implementar el núcleo puro del Árbol B para EduStruct, manteniendo separación estricta entre estructura de datos, servicios, rutas y frontend.

## Decisión aplicada

Se implementa un **Árbol B** de orden configurable. Por defecto se usa `order = 4`, lo que significa:

- máximo 4 hijos por nodo;
- máximo 3 claves por nodo;
- al llenarse un nodo, se divide;
- la clave mediana se promueve al padre.

Esta decisión permite mostrar visualmente nodos multi-clave y splits sin agregar la complejidad adicional de enlaces entre hojas propia de un B+.

## Archivo agregado

`backend/app/structures/btree.py`

## Clases implementadas

### `BTreeNode`

Responsabilidades:

- almacenar múltiples claves ordenadas;
- almacenar hijos;
- indicar si el nodo es hoja;
- serializarse a diccionario plano.

Atributos:

```python
keys: list[Any]
children: list[BTreeNode]
leaf: bool
```

### `BTree`

Responsabilidades:

- validar orden del árbol;
- insertar claves únicas;
- dividir nodos llenos;
- promover clave mediana;
- buscar claves;
- recorrer por niveles;
- calcular métricas base;
- registrar metadata de splits.

## Operaciones implementadas

- `insert(key)`
- `search(key)`
- `contains(key)`
- `levelorder()`
- `height()`
- `levels_count()`
- `node_count()`
- `leaf_count()`
- `edges_count()`
- `to_dict()`
- `clear()`

## Metadata de splits

Cada split registra:

```json
{
  "type": "split",
  "promotedKey": 20,
  "parentKeys": [20],
  "childIndex": 0,
  "before": {
    "keys": [10, 20, 30],
    "leaf": true,
    "children": []
  },
  "after": {
    "parent": {},
    "left": {},
    "right": {}
  }
}
```

Esta metadata queda lista para el Step 3, donde el servicio y serializer podrán exponerla al frontend.

## Validaciones

Se rechaza:

- orden menor que 3;
- claves vacías;
- claves duplicadas;
- claves incomparables.

## Pruebas agregadas

`backend/tests/structures/test_btree.py`

Cobertura:

- árbol vacío;
- validación de orden;
- inserción en raíz multi-clave;
- split de raíz;
- split de hijo interno;
- búsqueda exitosa;
- búsqueda fallida;
- duplicados;
- claves requeridas;
- claves incomparables;
- recorrido por niveles;
- métricas;
- serialización;
- limpieza del árbol.

## Validación ejecutada

Comando recomendado:

```bash
cd backend
python -m pytest tests/structures/test_btree.py
```

## Workflow Git sugerido

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-8-btree

git add backend/app/structures/btree.py backend/tests/structures/test_btree.py docs/epic-8-step-2-btree-core.md
git commit -m "feat(btree): implement core btree structure"
```

## Siguiente step

Step 3 debe crear la capa de servicio y serialización React Flow:

- `backend/app/services/btree_service.py`
- extensión de `backend/app/serializers/react_flow_serializer.py` con `serialize_btree()`
- `backend/tests/services/test_btree_service.py`
- `backend/tests/serializers/test_react_flow_btree_serializer.py`
