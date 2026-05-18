# EduStruct — Épica 6 — STEP 1 Backend Core Binary Tree

## Objetivo

Implementar la base del Árbol Binario como Binary Search Tree (BST) en Python puro, manteniendo la arquitectura por capas del proyecto.

## Archivos agregados

```text
backend/app/structures/binary_tree.py
backend/app/services/binary_tree_service.py
backend/tests/structures/test_binary_tree.py
backend/tests/services/test_binary_tree_service.py
```

## Alcance implementado

### Estructura pura

`backend/app/structures/binary_tree.py`

Incluye:

- `BinaryTreeNode`
- `BinaryTree`
- inserción BST
- eliminación BST
- búsqueda
- recorridos:
  - preorder
  - inorder
  - postorder
  - levelorder
- métricas:
  - size
  - height
  - levels
  - leafCount
  - edgesCount
  - balanceFactor raíz

El recorrido levelorder reutiliza la `Queue` manual existente del proyecto.

### Servicio de aplicación

`backend/app/services/binary_tree_service.py`

Incluye:

- `state()`
- `insert(value)`
- `delete(value)`
- `search(value)`
- `traverse(type)`
- `metrics()`
- `load_demo()`
- `reset()`

El servicio traduce errores internos a excepciones del dominio existente:

- `ValidationError`
- `DuplicateKeyError`
- `NotFoundError`
- `StructureEmptyError`

## Decisiones técnicas

### BST como base

Se implementa como Binary Search Tree porque permite:

- búsqueda ordenada
- recorrido inorder ordenado
- transición natural hacia AVL en una épica posterior
- visualización clara izquierda/derecha

### Valores únicos

No se permiten duplicados para mantener nodos visuales únicos y evitar ambigüedad en React Flow.

### Eliminación

La eliminación cubre:

- nodo hoja
- nodo con un hijo
- nodo con dos hijos
- raíz

Para nodos con dos hijos se usa el sucesor inorder.

## Validación local

Comando sugerido:

```bash
cd backend
PYTHONPATH=. pytest tests/structures/test_binary_tree.py tests/services/test_binary_tree_service.py -q
```

Resultado esperado:

```text
37 passed
```

## Git workflow

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-6-binary-tree
```

Aplicar archivos del ZIP y ejecutar pruebas.

Commit sugerido:

```bash
git add backend/app/structures/binary_tree.py \
        backend/app/services/binary_tree_service.py \
        backend/tests/structures/test_binary_tree.py \
        backend/tests/services/test_binary_tree_service.py \
        docs/epic-6-step-1-backend-binary-tree.md

git commit -m "feat(binary-tree): implement bst core structure"
```

## Siguiente paso

STEP 2 debe conectar el servicio con las rutas Flask en:

```text
backend/app/routes/binary_tree.py
```

También debe agregar pruebas de rutas para validar el contrato REST.
