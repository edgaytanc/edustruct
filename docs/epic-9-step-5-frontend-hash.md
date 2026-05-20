# Épica 9 — Step 5: Frontend de Tabla Hash

## Objetivo

Integrar la Tabla Hash al frontend de EduStruct para permitir interacción visual con buckets, cadenas de colisión, búsqueda por carnet, eliminación, carga demo y métricas.

## Archivos creados o modificados

```text
frontend/src/api/hashTable.js
frontend/src/pages/HashPage.jsx
frontend/src/router/AppRouter.jsx
frontend/src/pages/HomePage.jsx
docs/epic-9-step-5-frontend-hash.md
```

## API frontend

Se creó `frontend/src/api/hashTable.js` siguiendo el patrón usado por `btree.js`, `avl.js` y `binaryTree.js`.

Endpoints consumidos:

```text
GET    /api/hash/state
POST   /api/hash/configure
POST   /api/hash/insert
POST   /api/hash/bulk-insert
GET    /api/hash/search
DELETE /api/hash/delete
POST   /api/hash/demo/load
GET    /api/hash/traverse
GET    /api/hash/metrics
POST   /api/hash/reset
```

## Página visual

`frontend/src/pages/HashPage.jsx` implementa:

- configuración de capacidad inicial;
- inserción por carnet;
- valor asociado del estudiante;
- búsqueda por carnet;
- eliminación por carnet;
- carga demo;
- reset;
- recorrido por buckets;
- visualización con React Flow;
- resaltado de colisiones;
- métricas de tabla hash.

## Visualización

La representación usa el contrato JSON generado por `serialize_hash_table()`:

- cada bucket aparece como nodo inicial de fila;
- cada entrada se dibuja hacia la derecha del bucket;
- las colisiones aparecen como nodos encadenados;
- las aristas indican `head` y `next`;
- los buckets con más de un elemento se resaltan;
- el último elemento buscado, insertado o eliminado queda marcado mediante metadata.

## Métricas visibles

La interfaz muestra:

- elementos almacenados;
- cantidad de buckets;
- colisiones acumuladas;
- factor de carga;
- longitud máxima de cadena;
- buckets con colisión.

## Integración de navegación

Se actualizó `frontend/src/router/AppRouter.jsx` agregando la ruta:

```text
/hash
```

Se extendió `frontend/src/pages/HomePage.jsx` con una tarjeta de acceso para la Épica 9.

## Validación recomendada

```bash
cd backend
PYTHONPATH=. pytest

cd ../frontend
npm run build
```

## Commit semántico sugerido

```bash
git add frontend/src/api/hashTable.js frontend/src/pages/HashPage.jsx frontend/src/router/AppRouter.jsx frontend/src/pages/HomePage.jsx docs/epic-9-step-5-frontend-hash.md
git commit -m "feat(hash): add hash visualization page"
```

## Estado

Step 5 completado. La implementación queda detenida hasta validación explícita antes de iniciar el Step 6.
