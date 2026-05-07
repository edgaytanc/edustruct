# EduStruct — Épica 4: Implementación de Estructuras Lineales Base

## 1. Objetivo de la Épica

Implementar estructuras lineales reutilizables para el sistema EduStruct:

- Lista enlazada
- Pila
- Cola

Estas estructuras funcionan como base para recorridos, historial, colas de atención, serialización visual y futuras estructuras complejas.

---

## 2. Alcance Implementado

Durante la Épica 4 se implementó:

- Lista enlazada manual en Python puro.
- Pila manual reutilizando la lista enlazada.
- Cola manual reutilizando la lista enlazada.
- Pruebas unitarias.
- Servicios de aplicación.
- Endpoints REST funcionales.
- Serialización compatible con React Flow.
- Documentación educativa.
- Ejemplos de payloads y respuestas.

No se implementó todavía:

- AVL.
- Árbol B/B+.
- Grafos complejos.
- DFS/BFS reales.
- Balanceos.
- Animaciones frontend.

---

## 3. Arquitectura Final

```text
backend/app/
├── routes/
│   ├── list_structure.py
│   ├── stack.py
│   └── queue.py
├── services/
│   ├── list_service.py
│   ├── stack_service.py
│   └── queue_service.py
├── structures/
│   ├── list_model.py
│   ├── stack.py
│   └── queue.py
└── serializers/
    ├── response_serializer.py
    ├── metrics_serializer.py
    └── react_flow_serializer.py
```

Separación de responsabilidades:

| Capa | Responsabilidad |
|---|---|
| `routes` | Manejo HTTP |
| `services` | Casos de uso |
| `structures` | Estructuras puras |
| `serializers` | Respuestas y visualización |
| `tests` | Validación técnica |

---

## 4. Lista Enlazada

Archivo principal:

```text
backend/app/structures/list_model.py
```

Aplicación educativa:

```text
Lista de estudiantes inscritos
```

Operaciones principales:

- `append`
- `prepend`
- `remove`
- `find`
- `to_list`
- `clear`
- `is_empty`
- `size`

Complejidad:

| Operación | Complejidad |
|---|---:|
| Insertar al inicio | O(1) |
| Insertar al final | O(1) |
| Eliminar | O(n) |
| Buscar | O(n) |
| Recorrer | O(n) |

---

## 5. Pila

Archivo principal:

```text
backend/app/structures/stack.py
```

Aplicación educativa:

```text
Historial de navegación académica
```

Operaciones principales:

- `push`
- `pop`
- `peek`
- `to_list`
- `clear`
- `is_empty`
- `size`

Complejidad:

| Operación | Complejidad |
|---|---:|
| Push | O(1) |
| Pop | O(1) |
| Peek | O(1) |
| Buscar desde servicio | O(n) |
| Recorrer | O(n) |

---

## 6. Cola

Archivo principal:

```text
backend/app/structures/queue.py
```

Aplicación educativa:

```text
Turnos de asesoría académica
```

Operaciones principales:

- `enqueue`
- `dequeue`
- `front`
- `to_list`
- `clear`
- `is_empty`
- `size`

Complejidad:

| Operación | Complejidad |
|---|---:|
| Enqueue | O(1) |
| Dequeue | O(1) |
| Front | O(1) |
| Buscar desde servicio | O(n) |
| Recorrer | O(n) |

---

## 7. Endpoints Implementados

### Lista

```text
GET    /api/list/state
POST   /api/list/insert
DELETE /api/list/delete
GET    /api/list/search?value=...
POST   /api/list/demo/load
GET    /api/list/traverse
POST   /api/list/reset
```

### Pila

```text
GET    /api/stack/state
POST   /api/stack/insert
DELETE /api/stack/delete
GET    /api/stack/search?value=...
GET    /api/stack/peek
POST   /api/stack/demo/load
GET    /api/stack/traverse
POST   /api/stack/reset
```

### Cola

```text
GET    /api/queue/state
POST   /api/queue/insert
DELETE /api/queue/delete
GET    /api/queue/search?value=...
GET    /api/queue/front
POST   /api/queue/demo/load
GET    /api/queue/traverse
POST   /api/queue/reset
```

---

## 8. Serialización React Flow

Las estructuras lineales devuelven:

```json
{
  "nodes": [],
  "edges": []
}
```

Tipos de layout:

| Estructura | Layout |
|---|---|
| Lista | Horizontal |
| Pila | Vertical |
| Cola | Horizontal |

Marcadores visuales:

| Estructura | Marcadores |
|---|---|
| Lista | HEAD, TAIL |
| Pila | TOP |
| Cola | FRONT, REAR |

---

## 9. Casos Demo

### Lista

```text
2024001 - Ana López
2024002 - Carlos Méndez
2024003 - Sofía Ramírez
```

Contexto:

```text
Lista de estudiantes inscritos
```

### Pila

```text
Dashboard
Pensum
Curso MAT101
```

Contexto:

```text
Historial de navegación académica
```

### Cola

```text
Turno 1 - Ana López
Turno 2 - Carlos Méndez
Turno 3 - Sofía Ramírez
```

Contexto:

```text
Cola de turnos de asesoría académica
```

---

## 10. Pruebas

La Épica 4 contempla pruebas para:

- Lista enlazada.
- Pila.
- Cola.
- Servicios.
- Rutas REST.
- Serializadores React Flow.

Comando sugerido:

```bash
cd backend
pytest
```

---

## 11. Decisiones Técnicas

### Python puro

No se usaron librerías mágicas para implementar las estructuras. Esto cumple el objetivo académico del curso.

### Reutilización

Pila y cola reutilizan la lista enlazada como base lógica, evitando duplicación innecesaria.

### Servicios desacoplados

La lógica de aplicación se mantiene fuera de Flask.

### Serialización aislada

React Flow no contamina las estructuras puras. La visualización se resuelve en serializers.

### Estado en memoria

Las estructuras viven en memoria durante la ejecución de Flask. Esto es suficiente para la fase educativa e interactiva del proyecto.

---

## 12. Preparación para Futuras Épicas

La Épica 4 deja listas bases para:

- BFS usando cola.
- DFS usando pila.
- Historial de navegación.
- Animaciones de recorridos.
- Manejo de colisiones en tabla hash mediante listas.
- Serialización visual consistente para React Flow.
- Métricas comunes para dashboard.

---

## 13. Git Workflow

Rama de trabajo:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-4-linear-structures
```

Commits recomendados:

```bash
git commit -m "feat(structures): implement linear data structures"
git commit -m "feat(api): integrate linear structures endpoints"
git commit -m "feat(visualization): add react flow serializers for linear structures"
git commit -m "docs(epic-4): add educational examples and api usage"
```

Cierre de rama:

```bash
git checkout develop
git pull origin develop
git merge feature/epic-4-linear-structures
git push origin develop
git branch -d feature/epic-4-linear-structures
git push origin --delete feature/epic-4-linear-structures
```

---

## 14. Estado Final

La Épica 4 queda lista cuando:

- Las estructuras funcionan en backend.
- Los endpoints responden correctamente.
- React Flow recibe `nodes` y `edges`.
- Las métricas básicas están disponibles.
- Las pruebas pasan.
- La documentación describe el uso educativo.

Resultado:

```text
Base lineal lista para construir estructuras complejas.
```
