# EduStruct — Resumen de Épica 5

## Épica 5: Implementación del Árbol General

### Objetivo

Representar el pensum académico jerárquico mediante un árbol general con múltiples hijos, expuesto desde una API REST Flask y visualizado en React Flow.

### Alcance implementado

Durante esta épica se implementó el módulo de Árbol General para el caso educativo principal:

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

### Backend

Archivos principales:

```text
backend/app/structures/general_tree.py
backend/app/services/tree_service.py
backend/app/routes/tree.py
backend/app/serializers/react_flow_serializer.py
```

Se implementó una estructura manual en Python puro, sin librerías externas para árboles.

#### Responsabilidades por capa

| Capa | Responsabilidad |
|---|---|
| `structures/general_tree.py` | Nodo general, árbol, inserción, eliminación, búsqueda y recorridos. |
| `services/tree_service.py` | Casos de uso académicos, validaciones, dataset demo y métricas. |
| `routes/tree.py` | Endpoints REST para interactuar con el árbol. |
| `serializers/react_flow_serializer.py` | Conversión de nodos/aristas para React Flow. |

### Nodo general

Cada nodo académico contiene:

```text
node_id
label
category
metadata
children[]
```

Categorías usadas:

```text
faculty
career
cycle
course
academic
```

### Operaciones soportadas

| Operación | Descripción |
|---|---|
| Insertar | Agrega raíz o hijo mediante `parentId`. |
| Eliminar | Elimina un nodo y todo su subárbol. |
| Buscar | Busca nodo por `id` y devuelve nivel. |
| Recorrer | Soporta `preorder`, `postorder` y `levelorder`. |
| Métricas | Devuelve cantidad de nodos, altura, niveles, hojas, aristas y máximo de hijos. |
| Demo | Carga el pensum académico base. |
| Reset | Limpia la estructura actual. |

### Recorridos

#### Preorder

Visita primero el padre y luego sus hijos.

Uso principal:

```text
lectura jerárquica y serialización lógica
```

#### Postorder

Visita primero los hijos y luego el padre.

Uso principal:

```text
eliminación conceptual de subárboles
```

#### Levelorder

Visita por niveles usando la cola manual del proyecto.

Uso principal:

```text
layout visual, métricas por nivel y demostración de reutilización de Queue
```

### Métricas

La API devuelve:

```text
count
height
levels
edgesCount
leafCount
maxChildren
balanceFactor
collisions
```

Para Árbol General:

```text
balanceFactor = null
collisions = null
```

Estos campos se mantienen por compatibilidad con el contrato visual general del proyecto.

### API REST

Ruta base:

```text
/api/tree
```

Endpoints:

```text
GET    /api/tree/state
POST   /api/tree/insert
DELETE /api/tree/delete
GET    /api/tree/search?id=<node_id>
POST   /api/tree/demo/load
GET    /api/tree/traverse?type=levelorder|preorder|postorder
GET    /api/tree/metrics
POST   /api/tree/reset
```

### Frontend

Archivos principales:

```text
frontend/src/api/tree.js
frontend/src/pages/GeneralTreePage.jsx
frontend/src/router/AppRouter.jsx
frontend/src/pages/HomePage.jsx
```

Se integró una vista interactiva con React Flow para visualizar el árbol académico.

Funcionalidades de UI:

```text
- cargar dataset demo
- insertar nodos
- eliminar nodos
- buscar nodos
- ver recorridos
- visualizar métricas
- refrescar el grafo después de cada operación
```

### Serialización React Flow

El backend entrega:

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
metadata
```

Cada arista representa relación padre-hijo.

### Testing

Archivos reforzados:

```text
backend/tests/structures/test_general_tree.py
backend/tests/services/test_tree_service.py
backend/tests/routes/test_tree_routes.py
```

Cobertura agregada:

```text
- inserción de raíz
- inserción por padre
- duplicados
- padre inexistente
- eliminación de subárbol
- eliminación de raíz
- búsqueda existente e inexistente
- recorridos preorder, postorder y levelorder
- métricas del árbol
- rutas REST exitosas
- rutas REST con errores controlados
```

### Decisiones técnicas

1. El árbol vive en memoria durante la ejecución del backend.
2. No se implementó persistencia en base de datos porque no pertenece al alcance de la épica.
3. La estructura no depende de Flask ni de React Flow.
4. La capa de servicio traduce errores internos a excepciones del dominio HTTP.
5. `levelorder` reutiliza la implementación manual de `Queue` ya creada en Épica 4.
6. El frontend consume únicamente la API REST; no replica lógica de árbol.

### Complejidades

| Operación | Complejidad |
|---|---|
| Insertar por padre | O(n) |
| Buscar | O(n) |
| Eliminar | O(n + k), donde `k` es el tamaño del subárbol eliminado |
| Preorder | O(n) |
| Postorder | O(n) |
| Levelorder | O(n) |
| Métricas | O(n) |

### Restricciones respetadas

No se implementó:

```text
- AVL
- Árbol B/B+
- balanceos
- grafos complejos
- persistencia en base de datos
```

### Estado final

La Épica 5 queda funcional para demostrar:

```text
- Árbol General manual
- jerarquía académica
- operaciones CRUD básicas sobre nodos
- recorridos
- métricas
- visualización con React Flow
- integración frontend/backend
- pruebas unitarias y de rutas
```

## Git workflow de cierre

Commit recomendado para este paso:

```bash
git add .
git commit -m "test(tree): strengthen general tree test coverage"
git commit -m "docs(epic-5): document general tree completion"
```

Merge al finalizar validación:

```bash
git checkout develop
git pull origin develop
git merge feature/epic-5-general-tree
git push origin develop
git branch -d feature/epic-5-general-tree
git push origin --delete feature/epic-5-general-tree
```
