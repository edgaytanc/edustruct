# Épica 5 — Diseño e implementación base del Árbol General

## Objetivo

Representar el pensum académico jerárquico mediante un árbol general con múltiples hijos, usando Python puro y manteniendo la arquitectura cliente-servidor del proyecto EduStruct.

## Alcance del Paso 2

Este paso implementa la base backend del árbol general:

- Nodo general con hijos múltiples.
- Inserción por padre.
- Eliminación de nodo con todo su subárbol.
- Búsqueda por identificador.
- Cálculo de nivel, altura/profundidad, cantidad de nodos, hojas y máximo número de hijos.
- Recorridos preorder, postorder y levelorder.
- Levelorder usando la estructura `Queue` existente.
- Serialización visual para React Flow.
- Rutas REST funcionales para árbol general.
- Dataset demo académico en memoria.
- Pruebas unitarias y de rutas.

## Arquitectura aplicada

```text
backend/app/structures/general_tree.py
backend/app/services/tree_service.py
backend/app/routes/tree.py
backend/app/serializers/react_flow_serializer.py
```

### Capa de estructura

`GeneralTree` y `GeneralTreeNode` viven en `backend/app/structures/general_tree.py`.

Responsabilidades:

- Administrar nodos académicos.
- Mantener raíz única.
- Insertar hijos múltiples.
- Buscar nodos.
- Eliminar subárboles.
- Calcular métricas estructurales.
- Ejecutar recorridos sin depender de Flask.

### Capa de servicio

`TreeService` vive en `backend/app/services/tree_service.py`.

Responsabilidades:

- Validar datos de entrada.
- Convertir errores internos en excepciones del dominio de la API.
- Construir resultados serializables.
- Cargar el dataset demo del pensum académico.

### Capa REST

`tree.py` expone endpoints bajo:

```text
/api/tree
```

Endpoints incluidos:

```text
GET    /api/tree/state
POST   /api/tree/insert
DELETE /api/tree/delete
GET    /api/tree/search?id=<id>
POST   /api/tree/demo/load
GET    /api/tree/traverse?type=preorder|postorder|levelorder
GET    /api/tree/metrics
POST   /api/tree/reset
```

## Dataset demo

```text
Facultad de Ingeniería
└── Ingeniería en Sistemas
    ├── Ciclo 1
    │   ├── Matemática I
    │   └── Introducción a la Programación
    └── Ciclo 2
        ├── Programación I
        └── Matemática II
```

## Recorridos

### Preorder

Visita primero el padre y luego sus hijos.

Uso principal:

- Lectura jerárquica.
- Exportación ordenada por dependencia padre-hijo.

### Postorder

Visita hijos antes que el padre.

Uso principal:

- Eliminación lógica de subárboles.
- Procesamiento descendente seguro.

### Levelorder

Visita por niveles usando `Queue`.

Uso principal:

- Visualización en React Flow.
- Cálculo de niveles.
- Layout horizontal por nivel.

## Serialización React Flow

El serializer recibe la salida levelorder y genera:

```json
{
  "nodes": [],
  "edges": []
}
```

Cada nodo incluye:

```text
id
position
label
category
metadata.level
metadata.parentId
metadata.childrenCount
```

Cada arista representa una relación:

```text
parent-child
```

## Métricas

El backend devuelve:

```text
count
height
levels
edgesCount
leafCount
maxChildren
```

Campos reservados para otras estructuras:

```text
balanceFactor = null
collisions = null
```

## Complejidades

| Operación | Complejidad |
|---|---:|
| Insertar con búsqueda de padre | O(n) |
| Buscar nodo | O(n) |
| Eliminar nodo | O(n) |
| Preorder | O(n) |
| Postorder | O(n) |
| Levelorder | O(n) |
| Calcular altura | O(n) |

## Workflow Git

Inicio de épica:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-5-general-tree
```

Commits sugeridos para este paso:

```bash
git add backend/app/structures/general_tree.py
git commit -m "feat(tree): implement general tree structure"

git add backend/app/services/tree_service.py backend/app/routes/tree.py backend/app/serializers/react_flow_serializer.py
git commit -m "feat(tree): expose general tree api and visualization"

git add backend/tests/structures/test_general_tree.py backend/tests/services/test_tree_service.py backend/tests/routes/test_tree_routes.py
git commit -m "test(tree): add general tree backend tests"

git add docs/epic-5-general-tree-design.md
git commit -m "docs(epic-5): document general tree backend design"
```

## Validación recomendada

Desde `backend`:

```bash
pytest
```

Endpoints manuales sugeridos:

```bash
curl -X POST http://localhost:5000/api/tree/demo/load
curl http://localhost:5000/api/tree/state
curl http://localhost:5000/api/tree/traverse?type=levelorder
curl http://localhost:5000/api/tree/metrics
```
