# Épica 6 — STEP 4: Frontend para Árbol Binario

## Objetivo

Integrar la interfaz visual del Árbol Binario BST en React, conectada a los endpoints Flask implementados en los pasos anteriores.

## Archivos incluidos

- `frontend/src/api/binaryTree.js`
- `frontend/src/pages/BinaryTreePage.jsx`
- `frontend/src/router/AppRouter.jsx`
- `frontend/src/pages/HomePage.jsx`

## Funcionalidad agregada

### Cliente API

Se creó `frontend/src/api/binaryTree.js` con funciones para consumir:

- `GET /api/binary-tree/state`
- `POST /api/binary-tree/demo/load`
- `POST /api/binary-tree/reset`
- `POST /api/binary-tree/insert`
- `DELETE /api/binary-tree/delete`
- `GET /api/binary-tree/search`
- `GET /api/binary-tree/traverse`
- `GET /api/binary-tree/metrics`

### Página visual

Se creó `frontend/src/pages/BinaryTreePage.jsx` con:

- carga automática del demo si el árbol está vacío;
- inserción de valores;
- eliminación de valores;
- búsqueda con resaltado visual;
- recorridos `preorder`, `inorder`, `postorder` y `levelorder`;
- visualización de nodos y aristas en React Flow;
- métricas del árbol;
- panel JSON del estado estructural.

### Navegación

Se actualizó `frontend/src/router/AppRouter.jsx` para registrar:

```jsx
<Route path="/binary-tree" element={<BinaryTreePage />} />
```

Se actualizó `frontend/src/pages/HomePage.jsx` para agregar una tarjeta de acceso a la Épica 6.

## Validación manual sugerida

1. Levantar backend y frontend.
2. Entrar a `/binary-tree`.
3. Validar carga automática del demo `[50, 25, 75, 10, 40, 60, 90]`.
4. Insertar `55`.
5. Buscar `55` y verificar resaltado.
6. Ejecutar `inorder` y validar orden ascendente.
7. Eliminar `25` y validar que la estructura mantiene la propiedad BST.
8. Reiniciar el árbol.

## Workflow Git

```bash
git status
git add frontend/src/api/binaryTree.js \
  frontend/src/pages/BinaryTreePage.jsx \
  frontend/src/router/AppRouter.jsx \
  frontend/src/pages/HomePage.jsx \
  docs/epic-6-step-4-frontend-binary-tree.md
git commit -m "feat(binary-tree): add frontend visualization page"
```

## Nota técnica

Este paso no modifica backend. Consume el contrato ya expuesto en `/api/binary-tree` y mantiene la separación estricta entre cliente API, página visual y rutas React.
