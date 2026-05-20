# Épica 10 — Resumen técnico

## Objetivo

Implementar grafos DFS/BFS en EduStruct para modelar prerrequisitos de cursos universitarios.

## Decisión técnica principal

Se eligió lista de adyacencia sobre matriz de adyacencia porque:

- El mapa de prerrequisitos es naturalmente disperso.
- DFS y BFS se implementan de forma directa.
- La estructura es más clara para fines pedagógicos.
- Facilita serializar nodos y aristas para React Flow.

## Backend implementado

Archivos principales:

```text
backend/app/structures/graph.py
backend/app/services/graph_service.py
backend/app/routes/graph.py
backend/app/serializers/react_flow_serializer.py
```

Capacidades:

- Grafo manual en Python puro.
- Nodos de curso.
- Aristas dirigidas de prerrequisito a curso.
- DFS.
- BFS.
- Búsqueda.
- Métricas.
- Serialización visual.
- Carga demo desde datasets.

## Frontend implementado

Archivos principales:

```text
frontend/src/api/graph.js
frontend/src/pages/GraphPage.jsx
frontend/src/router/AppRouter.jsx
frontend/src/pages/HomePage.jsx
```

Capacidades:

- Cargar grafo demo.
- Seleccionar nodo inicial.
- Ejecutar DFS.
- Ejecutar BFS.
- Visualizar nodos y aristas en React Flow.
- Mostrar orden de visita.
- Resaltar recorrido.
- Reset visual.
- Mostrar métricas del grafo.

## Testing implementado

Archivos principales:

```text
backend/tests/structures/test_graph.py
backend/tests/services/test_graph_service.py
backend/tests/routes/test_graph_routes.py
backend/tests/serializers/test_react_flow_graph_serializer.py
```

Validación final:

```bash
417 passed
```

## Resultado

La Épica 10 completa el módulo de grafos requerido por el proyecto final, alineado al contexto educativo y a la arquitectura React → Flask REST → estructuras Python puro.

