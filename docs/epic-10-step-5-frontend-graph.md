# Épica 10 — Step 5: Frontend de visualización de grafos

## Objetivo del step

Integrar en React la visualización interactiva del grafo de prerrequisitos universitarios, consumiendo los endpoints REST implementados en el Step 4 y manteniendo el patrón visual usado por las épicas anteriores.

Este step no modifica la lógica core del backend. La responsabilidad principal queda en el frontend:

- cliente API `graph.js`;
- página `GraphPage.jsx`;
- registro de ruta `/graph`;
- acceso desde `HomePage.jsx`.

## Archivos entregados

```text
frontend/src/api/graph.js
frontend/src/pages/GraphPage.jsx
frontend/src/router/AppRouter.jsx
frontend/src/pages/HomePage.jsx
docs/epic-10-step-5-frontend-graph.md
```

## Cliente API

Se creó `frontend/src/api/graph.js` con funciones desacopladas para consumir el blueprint `/api/graph`:

- `getGraphState()`
- `addGraphNode({ id, value })`
- `addGraphEdge({ source, target })`
- `searchGraphCourse(courseId)`
- `loadGraphDemo()`
- `traverseGraph({ algorithm, startNodeId })`
- `runGraphDfs(startNodeId)`
- `runGraphBfs(startNodeId)`
- `getGraphMetrics()`
- `resetGraph()`

El archivo mantiene la misma convención usada por APIs previas: Axios, `VITE_API_URL || "/api"` y extracción centralizada de `response.data`.

## Página GraphPage

`frontend/src/pages/GraphPage.jsx` implementa una interfaz con React Flow para representar el mapa de prerrequisitos.

Funcionalidades incluidas:

1. Carga automática del estado del grafo.
2. Carga del dataset demo cuando el grafo está vacío.
3. Botón para cargar demo manualmente.
4. Botón para reiniciar solo la visualización.
5. Botón para vaciar el grafo en backend.
6. Selección de nodo inicial.
7. Ejecución de DFS.
8. Ejecución de BFS.
9. Visualización del orden de visita.
10. Controles de paso anterior/siguiente para animar recorridos.
11. Búsqueda de curso por código.
12. Alta manual de nodos.
13. Alta manual de aristas `prerrequisito -> curso habilitado`.
14. Métricas principales:
    - vértices;
    - aristas;
    - componentes conectados;
    - grado máximo de salida;
    - densidad.

## Visualización React Flow

La página reutiliza el contrato generado por `serialize_graph()`:

- `nodes`: nodos React Flow con metadata académica;
- `edges`: aristas dirigidas con relación `prerequisite`;
- `metrics`: métricas calculadas por backend;
- `traversal`: orden y pasos de DFS/BFS.

En frontend se normalizan los nodos para mostrar:

- código del curso;
- nombre del curso;
- grado de entrada;
- grado de salida;
- número de visita durante recorridos;
- estado activo del paso actual;
- resultado de búsqueda.

Las aristas se resaltan progresivamente según los pasos de recorrido devueltos por backend.

## Integración de rutas

Se actualizó `frontend/src/router/AppRouter.jsx` para registrar:

```text
/graph
```

apuntando a `GraphPage`.

## Integración con Home

Se extendió `frontend/src/pages/HomePage.jsx` agregando la tarjeta:

```text
Épica 10 — Grafos DFS/BFS
```

con enlace directo a `/graph`.

No se eliminó contenido previo. La documentación y la UI se extendieron de forma incremental.

## Validación realizada

Desde `frontend`:

```bash
npm run build
```

Resultado esperado:

```text
✓ built
```

Desde `backend`:

```bash
PYTHONPATH=. pytest
```

Resultado esperado del acumulado hasta Step 5:

```text
417 passed
```

## Workflow Git del step

Comandos recomendados para este step:

```bash
git checkout feature/epic-10-graphs

git add frontend/src/api/graph.js \
        frontend/src/pages/GraphPage.jsx \
        frontend/src/router/AppRouter.jsx \
        frontend/src/pages/HomePage.jsx \
        docs/epic-10-step-5-frontend-graph.md

git commit -m "feat(graph): add graph visualization page"
```

## Estado del step

Step 5 queda listo para validación del usuario.

No se avanza al Step 6 hasta recibir validación explícita.
