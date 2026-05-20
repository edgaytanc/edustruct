# Épica 10 — Step 3: Service + Serializer de Grafo

## Objetivo

Integrar el core manual del grafo con la capa de aplicación y la serialización visual para React Flow, sin introducir dependencias externas de grafos y sin tocar rutas REST ni frontend todavía.

## Archivos incluidos

```text
backend/app/services/graph_service.py
backend/app/serializers/react_flow_serializer.py
backend/tests/services/test_graph_service.py
backend/tests/serializers/test_react_flow_graph_serializer.py
docs/epic-10-step-3-graph-service-serializer.md
```

## Decisión técnica

El servicio `GraphService` encapsula los casos de uso del mapa de prerrequisitos y mantiene la estructura `Graph` libre de Flask, HTTP y serialización visual.

La serialización se agregó como función incremental en:

```text
backend/app/serializers/react_flow_serializer.py
```

Función nueva:

```python
serialize_graph(graph, traversal=None, search=None)
```

No se eliminó ni sobrescribió serialización previa. Se extendió el serializer existente con un contrato específico para grafos.

## Contrato del grafo

El grafo se modela como dirigido:

```text
prerequisite_id -> course_id
```

Ejemplo:

```text
CUR-001 -> CUR-005
Introducción a la Programación habilita Programación I
```

Esta dirección permite que DFS/BFS representen cómo un curso base desbloquea cursos posteriores.

## Responsabilidades de `GraphService`

```text
state()
add_node(node_id, value)
add_edge(source_id, target_id)
search(node_id)
traverse(algorithm, start_node_id)
dfs(start_node_id)
bfs(start_node_id)
metrics()
load_demo()
reset()
```

## Dataset usado por `load_demo()`

El servicio carga los archivos existentes:

```text
datasets/courses.json
datasets/prerequisites.json
```

No se creó todavía `datasets/course_graph.json` porque el Step 3 trabaja service + serializer. El dataset demo dedicado queda alineado para el Step 4 o Step 5 según integración REST/frontend.

## Manejo de errores

Se reutilizan excepciones existentes del proyecto:

```text
ValidationError
DuplicateKeyError
NotFoundError
DatasetError
```

Casos cubiertos:

- nodo inválido
- algoritmo inválido
- nodo duplicado
- arista duplicada
- nodo origen/destino inexistente
- inicio de recorrido inexistente
- dataset inválido
- referencias a cursos inexistentes

## Serialización React Flow

Cada nodo visual incluye:

```json
{
  "id": "CUR-001",
  "type": "graphNode",
  "data": {
    "label": "SIS-101\nIntroducción a la Programación",
    "category": "source-course",
    "metadata": {
      "neighbors": ["CUR-005"],
      "degree": 1,
      "outDegree": 1,
      "inDegree": 0,
      "visited": false,
      "visitOrder": null,
      "searchMatch": false
    }
  }
}
```

Cada arista visual representa una relación académica:

```json
{
  "source": "CUR-001",
  "target": "CUR-005",
  "label": "habilita",
  "data": {
    "relationship": "prerequisite",
    "isTraversalEdge": false
  }
}
```

## Animación preparada

El serializer acepta `traversal.steps` generados por DFS/BFS y marca:

- nodos visitados
- orden de visita
- aristas de recorrido
- aristas animadas para el frontend

Esto deja lista la base para `GraphPage.jsx` en Step 5.

## Métricas disponibles

```text
verticesCount
edgesCount
connectedComponents
isolatedVertices
maxOutDegree
maxInDegree
density
```

## Validación ejecutada

```bash
cd backend
PYTHONPATH=. pytest tests/services/test_graph_service.py tests/serializers/test_react_flow_graph_serializer.py tests/structures/test_graph.py
```

Resultado:

```text
33 passed
```

Validación completa de regresión:

```bash
cd backend
PYTHONPATH=. pytest
```

Resultado:

```text
401 passed
```

## Workflow Git recomendado

```bash
git status
git add backend/app/services/graph_service.py \
        backend/app/serializers/react_flow_serializer.py \
        backend/tests/services/test_graph_service.py \
        backend/tests/serializers/test_react_flow_graph_serializer.py \
        docs/epic-10-step-3-graph-service-serializer.md

git commit -m "feat(graph): add graph service and serializer"
```

## Estado del Step 3

Step 3 completado y detenido para validación explícita antes de avanzar a Step 4.
