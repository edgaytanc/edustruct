# Épica 10 — Step 4: REST routes para Grafos DFS/BFS

## Objetivo del step

Exponer la estructura `Graph` y el `GraphService` mediante endpoints REST de Flask, manteniendo el contrato estándar de EduStruct:

```text
React → API REST Flask → Service → Estructura manual Python
```

Este step no modifica frontend. La integración visual queda reservada para el Step 5.

## Archivos creados o actualizados

```text
backend/app/routes/graph.py
backend/tests/routes/test_graph_routes.py
docs/epic-10-step-4-graph-routes.md
```

## Diseño REST aplicado

El blueprint existente `graph_bp` se conserva con el prefijo:

```text
/api/graph
```

La implementación reemplaza los endpoints placeholder por rutas conectadas al `GraphService`.

## Endpoints implementados

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/graph/state` | Devuelve estado completo del grafo y contrato React Flow |
| POST | `/api/graph/nodes` | Agrega un nodo de curso |
| POST | `/api/graph/add-node` | Alias explícito para agregar nodo |
| POST | `/api/graph/edges` | Agrega una arista dirigida `prerrequisito -> curso` |
| POST | `/api/graph/add-edge` | Alias explícito para agregar arista |
| POST | `/api/graph/insert` | Endpoint compatible para insertar nodo o arista según payload |
| GET | `/api/graph/search` | Busca curso por `id`, `nodeId` o `courseId` |
| POST | `/api/graph/demo/load` | Carga demo desde `courses.json` y `prerequisites.json` |
| GET | `/api/graph/traverse` | Ejecuta DFS/BFS usando `algorithm` y `start` |
| GET | `/api/graph/dfs` | Atajo para DFS |
| GET | `/api/graph/bfs` | Atajo para BFS |
| GET | `/api/graph/metrics` | Devuelve métricas de conectividad y grados |
| POST | `/api/graph/reset` | Limpia el grafo actual |

## Contrato de respuesta

Todas las respuestas exitosas usan `success_response()`:

```json
{
  "success": true,
  "message": "...",
  "data": {
    "structure": "graph",
    "operation": "...",
    "nodes": [],
    "edges": [],
    "metrics": {},
    "traversal": {},
    "result": {}
  },
  "error": null
}
```

## Payloads aceptados

### Crear nodo

```json
{
  "id": "CUR-001",
  "value": {
    "code": "SIS-101",
    "name": "Introducción a Sistemas"
  }
}
```

Alias soportados para id:

```text
id, nodeId, courseId
```

### Crear arista

```json
{
  "source": "CUR-001",
  "target": "CUR-005"
}
```

Alias soportados:

```text
source, sourceId, prerequisiteId, prerequisite_id
target, targetId, courseId, course_id
```

La semántica oficial es:

```text
source/prerequisiteId -> target/courseId
```

Es decir:

```text
prerrequisito -> curso habilitado
```

## Recorridos

### DFS

```text
GET /api/graph/traverse?algorithm=DFS&start=CUR-001
GET /api/graph/dfs?start=CUR-001
```

### BFS

```text
GET /api/graph/traverse?algorithm=BFS&start=CUR-001
GET /api/graph/bfs?start=CUR-001
```

El resultado incluye:

- `order`
- `steps`
- `visitedOrder`
- nodos/aristas listos para React Flow
- métricas actualizadas

## Errores controlados

Los errores se delegan al sistema global de handlers ya existente:

| Caso | HTTP | Código |
|---|---:|---|
| Nodo requerido vacío | 400 | `VALIDATION_ERROR` |
| Algoritmo inválido | 400 | `VALIDATION_ERROR` |
| Nodo no encontrado | 404 | `NOT_FOUND` |
| Nodo/arista duplicada | 409 | `DUPLICATE_KEY` |
| Dataset inválido | 422 | `DATASET_ERROR` |

## Pruebas agregadas

Archivo:

```text
backend/tests/routes/test_graph_routes.py
```

Cobertura:

- estado vacío del grafo
- creación de nodos
- alias `/insert` para nodo
- duplicados
- validación de id requerido
- creación de aristas dirigidas
- alias `/insert` para aristas
- búsqueda encontrada/no encontrada
- validación de búsqueda sin id
- DFS y BFS con órdenes diferentes
- rutas shortcut `/dfs` y `/bfs`
- validación de algoritmo inválido
- validación de nodo inicial inexistente
- carga del dataset demo
- métricas
- reset

## Validación sugerida

Desde `backend`:

```bash
PYTHONPATH=. pytest tests/routes/test_graph_routes.py
PYTHONPATH=. pytest
```

## Workflow Git del step

```bash
git checkout develop
git pull origin develop
git checkout feature/epic-10-graphs

git add backend/app/routes/graph.py \
        backend/tests/routes/test_graph_routes.py \
        docs/epic-10-step-4-graph-routes.md

git commit -m "feat(graph): expose graph routes"
```

## Estado del step

Step 4 completado. La API REST del grafo queda lista para ser consumida por el frontend en el Step 5.
