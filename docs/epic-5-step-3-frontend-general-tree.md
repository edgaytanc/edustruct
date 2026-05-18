# Épica 5 — Paso 3: Integración frontend del Árbol General

## Objetivo

Integrar la visualización del árbol general académico en React usando React Flow y consumiendo los endpoints Flask creados en el Paso 2.

## Archivos agregados

```text
frontend/src/api/tree.js
frontend/src/pages/GeneralTreePage.jsx
```

## Archivos actualizados

```text
frontend/src/router/AppRouter.jsx
frontend/src/pages/HomePage.jsx
```

## Ruta frontend

```text
/general-tree
```

## Endpoints consumidos

```text
GET    /api/tree/state
POST   /api/tree/demo/load
POST   /api/tree/reset
POST   /api/tree/insert
DELETE /api/tree/delete
GET    /api/tree/search?id=<node_id>
GET    /api/tree/traverse?type=<levelorder|preorder|postorder>
```

## Operaciones disponibles en UI

- Cargar dataset demo.
- Reiniciar árbol.
- Insertar nodo por `parentId`.
- Eliminar nodo por `id`.
- Buscar nodo por `id`.
- Consultar recorridos `levelorder`, `preorder` y `postorder`.
- Visualizar métricas: nodos, altura, niveles, hojas, máximo de hijos y aristas.

## Decisiones técnicas

- La página no implementa lógica de árbol; solo consume API REST.
- React Flow recibe `nodes` y `edges` generados por backend.
- El resaltado de búsqueda se maneja en frontend mediante estilos del nodo encontrado.
- Se mantiene separación estricta entre API client, página y layout.
- No se agrega persistencia ni estructuras fuera del alcance de la épica.

## Git workflow

```bash
git status
git add frontend/src/api/tree.js frontend/src/pages/GeneralTreePage.jsx frontend/src/router/AppRouter.jsx frontend/src/pages/HomePage.jsx docs/epic-5-step-3-frontend-general-tree.md
git commit -m "feat(frontend): add general tree visualization page"
```

## Validación sugerida

```bash
cd frontend
npm install
npm run build
npm run lint
```

También validar manualmente:

1. Abrir `/general-tree`.
2. Confirmar que carga el demo.
3. Insertar un curso bajo un ciclo existente.
4. Buscar el nodo insertado.
5. Eliminar el nodo.
6. Revisar métricas y recorridos.
