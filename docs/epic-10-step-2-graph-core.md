# Épica 10 — Step 2: Core backend Graph

## Objetivo del step

Implementar el núcleo manual del grafo para representar relaciones de prerrequisitos entre cursos universitarios, dejando lista la base para servicios, serialización React Flow, endpoints REST y visualización frontend en steps posteriores.

Este step no modifica rutas, servicios, serializers ni frontend. Su alcance se limita a:

- `backend/app/structures/graph.py`
- `backend/tests/structures/test_graph.py`
- `docs/epic-10-step-2-graph-core.md`

## Decisión técnica aplicada

Se implementó un grafo con **lista de adyacencia dirigida**.

La dirección recomendada para el dominio EduStruct es:

```text
prerequisite_course_id -> dependent_course_id
```

Ejemplo:

```text
CS-201 Programación II -> CS-301 Estructuras de Datos
```

Esta dirección permite explicar qué cursos se desbloquean al aprobar un prerrequisito y hace más clara la diferencia entre DFS y BFS durante la visualización.

## Archivo implementado

Ruta completa:

```text
backend/app/structures/graph.py
```

## Clases agregadas

### `GraphNode`

Representa un vértice del grafo.

Atributos:

- `id`: identificador estable del curso.
- `value`: payload asociado al curso.
- `neighbors`: lista de ids vecinos salientes.

Métodos principales:

- `degree()`
- `to_dict()`

### `GraphSearchResult`

Resultado de búsqueda de curso por id.

Incluye:

- `found`
- `node_id`
- `node`
- `comparisons`

### `GraphTraversalStep`

Paso individual para futuras animaciones DFS/BFS.

Incluye:

- número de paso
- acción (`VISIT` o `DISCOVER`)
- nodo actual
- orden visitado acumulado
- frontera actual
- arista descubierta

### `GraphTraversalResult`

Resultado completo de DFS o BFS.

Incluye:

- algoritmo
- nodo inicial
- orden final
- pasos de animación

### `Graph`

Grafo manual con lista de adyacencia.

Atributos principales:

- `adjacency_list`
- `vertices_count`
- `edges_count`
- `directed`
- `last_operation`

Métodos principales:

- `add_node(node_id, value=None)`
- `add_edge(source_id, target_id)`
- `search(node_id)`
- `contains(node_id)`
- `dfs(start_node_id)`
- `bfs(start_node_id)`
- `degree(node_id)`
- `in_degree(node_id)`
- `connected_components_count()`
- `nodes()`
- `edges()`
- `to_dict()`

## Validaciones implementadas

El core rechaza:

- ids vacíos o nulos
- nodos duplicados
- aristas duplicadas
- self-loops
- aristas con nodo origen inexistente
- aristas con nodo destino inexistente
- nodo inicial inexistente para DFS/BFS
- configuración `directed` no booleana

## DFS

Se implementó DFS iterativo usando la estructura `Stack` existente del proyecto.

Características:

- recorrido determinístico según orden de inserción de vecinos
- pasos `VISIT` y `DISCOVER`
- frontera serializable para animación futura
- actualización de `last_operation`

## BFS

Se implementó BFS usando la estructura `Queue` existente del proyecto.

Características:

- recorrido por niveles
- pasos `VISIT` y `DISCOVER`
- frontera serializable para animación futura
- actualización de `last_operation`

## Métricas base del grafo

Se incluyeron métricas necesarias para steps posteriores:

- cantidad de vértices
- cantidad de aristas
- grado saliente del nodo
- grado entrante del nodo
- componentes conectados débiles para grafos dirigidos

La conectividad se calcula como conectividad débil porque el grafo de prerrequisitos es dirigido, pero para una métrica visual básica interesa saber si existen grupos aislados aunque la dirección académica se mantenga para DFS/BFS.

## Pruebas agregadas

Ruta completa:

```text
backend/tests/structures/test_graph.py
```

Casos cubiertos:

- grafo vacío
- validación del flag `directed`
- inserción de nodos
- validación de ids
- rechazo de nodos duplicados
- inserción de aristas
- rechazo de self-loops
- rechazo de aristas duplicadas
- validación de nodos inexistentes en aristas
- grafo no dirigido
- búsqueda de curso existente e inexistente
- DFS
- BFS
- diferencia visible entre DFS y BFS
- validación de nodo inicial inexistente
- grado saliente
- grado entrante
- conectividad básica
- serialización JSON-friendly del core

## Validación ejecutada

Comando ejecutado desde `backend`:

```bash
PYTHONPATH=. pytest tests/structures/test_graph.py
```

Resultado:

```text
16 passed
```

Validación completa de backend ejecutada desde `backend`:

```bash
PYTHONPATH=. pytest
```

Resultado:

```text
384 passed
```

## Archivos creados en este step

```text
backend/app/structures/graph.py
backend/tests/structures/test_graph.py
docs/epic-10-step-2-graph-core.md
```

## Workflow Git del step

Comandos recomendados:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-10-graphs

git add backend/app/structures/graph.py
git add backend/tests/structures/test_graph.py
git add docs/epic-10-step-2-graph-core.md

git commit -m "feat(graph): implement graph core"
```

Si la rama `feature/epic-10-graphs` ya existe desde el Step 1:

```bash
git checkout feature/epic-10-graphs
git pull origin feature/epic-10-graphs

git add backend/app/structures/graph.py
git add backend/tests/structures/test_graph.py
git add docs/epic-10-step-2-graph-core.md

git commit -m "feat(graph): implement graph core"
```

## Estado

Step 2 completado y detenido para validación explícita antes de avanzar al Step 3.
