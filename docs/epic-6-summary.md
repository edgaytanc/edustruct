# EduStruct — Épica 6: Árbol Binario y Recorridos

## Estado

Épica 6 completada.

## Objetivo

Implementar un Árbol Binario de Búsqueda aplicado al contexto educativo de EduStruct, permitiendo insertar, eliminar, buscar, visualizar y recorrer nodos mediante una interfaz web interactiva conectada a una API REST Flask.

## Alcance implementado

### Backend

- Implementación manual de `BinaryTreeNode`.
- Implementación manual de `BinaryTree` como BST.
- Inserción ordenada por regla BST.
- Búsqueda de nodos.
- Eliminación de nodos considerando:
  - nodo hoja,
  - nodo con un hijo,
  - nodo con dos hijos mediante sucesor inorder.
- Recorridos:
  - preorder,
  - inorder,
  - postorder,
  - levelorder.
- Recorrido levelorder reutilizando la cola manual existente del proyecto.
- Métricas:
  - cantidad de nodos,
  - altura,
  - niveles,
  - cantidad de hojas,
  - cantidad de aristas.
- Servicio de aplicación `BinaryTreeService`.
- Endpoints REST para `/api/binary-tree`.
- Serialización compatible con React Flow.

### Frontend

- Cliente API `binaryTree.js`.
- Página `BinaryTreePage.jsx`.
- Visualización gráfica con React Flow.
- Controles para:
  - cargar demo,
  - insertar,
  - eliminar,
  - buscar,
  - reiniciar,
  - ejecutar recorridos.
- Animación visual de recorridos.
- Control de velocidad de animación.
- Panel de métricas y estado.
- Integración con router y HomePage.

### Documentación

Se agregaron documentos incrementales para cada paso de la épica:

- `docs/epic-6-step-1-backend-binary-tree.md`
- `docs/epic-6-step-2-binary-tree-routes.md`
- `docs/epic-6-step-3-binary-tree-react-flow-serializer.md`
- `docs/epic-6-step-4-frontend-binary-tree.md`
- `docs/epic-6-step-5-traversal-animation.md`
- `docs/demo-checklist-epic-6.md`
- `docs/epic-6-summary.md`

## Archivos principales creados o actualizados

### Backend

- `backend/app/structures/binary_tree.py`
- `backend/app/services/binary_tree_service.py`
- `backend/app/routes/binary_tree.py`
- `backend/app/serializers/react_flow_serializer.py`

### Frontend

- `frontend/src/api/binaryTree.js`
- `frontend/src/pages/BinaryTreePage.jsx`
- `frontend/src/router/AppRouter.jsx`
- `frontend/src/pages/HomePage.jsx`

### Tests

- `backend/tests/structures/test_binary_tree.py`
- `backend/tests/services/test_binary_tree_service.py`
- `backend/tests/routes/test_binary_tree_routes.py`
- `backend/tests/serializers/test_react_flow_binary_tree_serializer.py`

## Contrato funcional del BST

El árbol binario implementado sigue la regla:

- valores menores al nodo actual se insertan en el subárbol izquierdo;
- valores mayores al nodo actual se insertan en el subárbol derecho;
- valores duplicados no son permitidos.

Esta decisión permite que el recorrido inorder devuelva los valores en orden ascendente y deja el proyecto preparado para la Épica 7 de Árbol AVL.

## Recorridos disponibles

| Recorrido | Descripción |
|---|---|
| preorder | Visita raíz, subárbol izquierdo y subárbol derecho. |
| inorder | Visita subárbol izquierdo, raíz y subárbol derecho. |
| postorder | Visita subárbol izquierdo, subárbol derecho y raíz. |
| levelorder | Visita por niveles usando cola manual. |

## Valor educativo

La Épica 6 permite demostrar:

- funcionamiento de un BST,
- diferencia entre recorridos clásicos,
- impacto de la estructura del árbol en la búsqueda,
- relación entre backend de estructuras puras y frontend visual,
- serialización de estructuras de datos hacia React Flow.

## Resultado

El módulo de Árbol Binario queda listo para demostración oral y para integrarse como base conceptual de la siguiente épica: Árbol AVL.
