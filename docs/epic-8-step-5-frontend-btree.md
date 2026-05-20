# Épica 8 — Step 5: Frontend visualization BTree

## Objetivo

Integrar la visualización del Árbol B en React, manteniendo el patrón existente de las páginas de Árbol Binario y AVL.

## Archivos agregados

- `frontend/src/api/btree.js`
- `frontend/src/pages/BTreePage.jsx`

## Archivos actualizados

- `frontend/src/router/AppRouter.jsx`
- `frontend/src/pages/HomePage.jsx`

## Funcionalidades implementadas

- Configuración de orden del Árbol B.
- Inserción individual de claves.
- Inserción por lote.
- Carga de dataset demo de expedientes académicos.
- Búsqueda con resaltado de ruta y nodo encontrado.
- Visualización React Flow de nodos multi-clave.
- Visualización de niveles, hojas, nodos internos y raíz.
- Panel de métricas: claves, altura, orden, nodos y splits.
- Panel de último split con mediana promovida y nodos resultantes.
- Recorridos `levelorder` e `inorder`.
- Reset y refresco del estado.

## Decisión visual

Cada nodo del Árbol B se renderiza como un bloque que contiene varias claves ordenadas. Esto evita representar una clave como nodo independiente y respeta el comportamiento real del Árbol B como índice multi-clave.

## Validación ejecutada

```bash
npm run build
```

Resultado:

```text
✓ built successfully
```

## Workflow Git sugerido

```bash
git add frontend/src/api/btree.js \
        frontend/src/pages/BTreePage.jsx \
        frontend/src/router/AppRouter.jsx \
        frontend/src/pages/HomePage.jsx \
        docs/epic-8-step-5-frontend-btree.md

git commit -m "feat(btree): add btree visualization page"
```
