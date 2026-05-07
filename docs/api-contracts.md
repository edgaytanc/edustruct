# EduStruct — Contratos de API

## 1. Objetivo

Documentar el contrato oficial de comunicación entre el frontend React y el backend Flask REST API para el proyecto EduStruct.

Este documento define:

- Convenciones REST.
- Endpoints iniciales.
- Payloads estándar.
- Respuestas estándar.
- Serialización compatible con React Flow.
- Métricas comunes.
- Manejo de errores HTTP.

> Este documento pertenece a la Épica 3: Diseño de arquitectura técnica y contratos de API.
> En esta épica no se implementa lógica pesada de estructuras de datos.

---

## 2. Arquitectura de comunicación

La arquitectura general del sistema será:

```text
Frontend React + Vite
        ↓ Axios
Backend Flask REST API
        ↓ Servicios de aplicación
Lógica de estructuras en Python puro
        ↓
Serialización JSON compatible con React Flow
```

Responsabilidades principales:

- React consume datos y renderiza visualmente.
- Flask expone endpoints REST.
- Python puro implementa las estructuras de datos.
- Los serializadores convierten las estructuras internas a JSON visualizable.
- React Flow recibe `nodes` y `edges`.

---

## 3. Base URL

Todos los endpoints de estructuras de datos deben usar el prefijo:

```text
/api
```

Ejemplo:

```text
/api/tree/state
/api/avl/insert
/api/graph/traverse
```

---

## 4. Estructuras soportadas inicialmente

Las rutas base serán:

```text
/api/tree
/api/binary-tree
/api/avl
/api/btree
/api/hash
/api/graph
/api/list
/api/stack
/api/queue
```

Uso esperado:

| Ruta base | Estructura |
|---|---|
| `/api/tree` | Árbol general |
| `/api/binary-tree` | Árbol binario |
| `/api/avl` | Árbol AVL |
| `/api/btree` | Árbol B / B+ |
| `/api/hash` | Tabla hash |
| `/api/graph` | Grafo |
| `/api/list` | Lista |
| `/api/stack` | Pila |
| `/api/queue` | Cola |

---

## 5. Endpoints comunes

Todas las estructuras deben seguir una convención uniforme.

| Operación | Método HTTP | Endpoint |
|---|---:|---|
| Obtener estado actual | GET | `/api/{structure}/state` |
| Insertar elemento | POST | `/api/{structure}/insert` |
| Eliminar elemento | DELETE | `/api/{structure}/delete` |
| Buscar elemento | GET | `/api/{structure}/search?key={value}` |
| Cargar dataset demo | POST | `/api/{structure}/demo/load` |
| Recorrer estructura | GET | `/api/{structure}/traverse?type={type}` |
| Reiniciar estructura | POST | `/api/{structure}/reset` |

Ejemplos:

```text
GET /api/tree/state
POST /api/avl/insert
DELETE /api/hash/delete
GET /api/graph/search?key=course-001
POST /api/graph/demo/load
GET /api/graph/traverse?type=bfs&start=course-001
POST /api/tree/reset
```

---

## 6. Payload estándar para insertar

Endpoint:

```text
POST /api/{structure}/insert
```

Payload:

```json
{
  "key": "course-001",
  "value": {
    "name": "Programación III",
    "cycle": 5,
    "credits": 5
  },
  "metadata": {
    "source": "manual"
  }
}
```

Campos:

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---:|---|
| `key` | string | Sí | Identificador único del elemento |
| `value` | object | Sí | Datos asociados al elemento |
| `metadata` | object | No | Información adicional de contexto |

---

## 7. Payload estándar para eliminar

Endpoint:

```text
DELETE /api/{structure}/delete
```

Payload:

```json
{
  "key": "course-001"
}
```

Campos:

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---:|---|
| `key` | string | Sí | Identificador del elemento a eliminar |

---

## 8. Payload estándar para buscar

Endpoint:

```text
GET /api/{structure}/search?key={value}
```

Ejemplo:

```text
GET /api/avl/search?key=2024001
```

La búsqueda debe devolver:

- Resultado encontrado o no encontrado.
- Estado actualizado de la estructura.
- Camino recorrido, cuando aplique.

---

## 9. Payload estándar para cargar demo

Endpoint:

```text
POST /api/{structure}/demo/load
```

Payload:

```json
{
  "dataset": "courses",
  "mode": "replace"
}
```

Campos:

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---:|---|
| `dataset` | string | Sí | Nombre del dataset demo |
| `mode` | string | No | Modo de carga: `replace` o `append` |

Modos permitidos:

| Modo | Descripción |
|---|---|
| `replace` | Limpia la estructura actual y carga datos demo |
| `append` | Agrega datos demo a la estructura actual |

---

## 10. Payload estándar para recorridos

Endpoint:

```text
GET /api/{structure}/traverse?type={type}
```

Ejemplos:

```text
GET /api/tree/traverse?type=preorder
GET /api/tree/traverse?type=inorder
GET /api/tree/traverse?type=postorder
GET /api/graph/traverse?type=bfs&start=course-001
GET /api/graph/traverse?type=dfs&start=course-001
```

Tipos de recorrido sugeridos:

| Estructura | Tipos |
|---|---|
| Árbol general | `preorder`, `postorder`, `levelorder` |
| Árbol binario | `preorder`, `inorder`, `postorder`, `levelorder` |
| AVL | `preorder`, `inorder`, `postorder`, `levelorder` |
| Árbol B/B+ | `inorder`, `levelorder` |
| Grafo | `bfs`, `dfs` |
| Lista | `forward` |
| Pila | `top-to-bottom` |
| Cola | `front-to-back` |

---

## 11. Respuesta estándar exitosa

Todas las respuestas exitosas deben seguir esta forma:

```json
{
  "success": true,
  "message": "Operación realizada correctamente.",
  "data": {
    "structure": "avl",
    "operation": "insert",
    "nodes": [],
    "edges": [],
    "metrics": {
      "count": 0,
      "height": null,
      "balanceFactor": null,
      "collisions": null,
      "levels": null,
      "edgesCount": 0
    },
    "traversal": {
      "type": null,
      "start": null,
      "order": [],
      "steps": []
    },
    "result": {}
  },
  "error": null
}
```

Campos principales:

| Campo | Tipo | Descripción |
|---|---|---|
| `success` | boolean | Indica si la operación fue exitosa |
| `message` | string | Mensaje legible para el usuario |
| `data` | object | Resultado funcional y visual |
| `error` | null | Sin error en respuestas exitosas |

---

## 12. Respuesta estándar con error

Todas las respuestas con error deben seguir esta forma:

```json
{
  "success": false,
  "message": "No se pudo completar la operación.",
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "httpStatus": 400,
    "details": [
      {
        "field": "key",
        "message": "El campo key es obligatorio."
      }
    ]
  }
}
```

Campos del error:

| Campo | Tipo | Descripción |
|---|---|---|
| `code` | string | Código interno de error |
| `httpStatus` | number | Código HTTP asociado |
| `details` | array | Detalles específicos del error |

---

## 13. Códigos HTTP estándar

| HTTP | Uso |
|---:|---|
| 200 | Operación exitosa |
| 201 | Inserción exitosa |
| 400 | Payload inválido |
| 404 | Recurso no encontrado |
| 409 | Duplicado o conflicto |
| 422 | Operación válida, pero no aplicable |
| 500 | Error inesperado |

---

## 14. Catálogo de errores internos

| Código interno | HTTP | Cuándo usarlo |
|---|---:|---|
| `VALIDATION_ERROR` | 400 | Faltan campos o existen tipos inválidos |
| `NOT_FOUND` | 404 | Nodo, curso, estudiante o registro no existe |
| `DUPLICATE_KEY` | 409 | Carnet, curso o clave ya existe |
| `INVALID_OPERATION` | 422 | Recorrido u operación no soportada |
| `STRUCTURE_EMPTY` | 422 | Se intenta recorrer o buscar en una estructura vacía |
| `DATASET_ERROR` | 422 | Dataset demo inválido o no compatible |
| `INTERNAL_ERROR` | 500 | Error no controlado |

---

## 15. Serialización compatible con React Flow

El backend debe devolver estructuras listas para ser renderizadas con React Flow.

### Nodo estándar

```json
{
  "id": "course-001",
  "type": "default",
  "position": {
    "x": 100,
    "y": 200
  },
  "data": {
    "label": "Programación III",
    "category": "course",
    "metadata": {
      "cycle": 5,
      "credits": 5
    }
  }
}
```

Campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | string | Identificador único del nodo |
| `type` | string | Tipo de nodo para React Flow |
| `position` | object | Coordenadas iniciales |
| `data.label` | string | Texto visible del nodo |
| `data.category` | string | Categoría funcional del nodo |
| `data.metadata` | object | Datos adicionales |

### Arista estándar

```json
{
  "id": "edge-course-001-course-002",
  "source": "course-001",
  "target": "course-002",
  "type": "smoothstep",
  "label": "prerrequisito",
  "animated": false,
  "data": {
    "relationship": "requires"
  }
}
```

Campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | string | Identificador único de la arista |
| `source` | string | Nodo origen |
| `target` | string | Nodo destino |
| `type` | string | Tipo visual de arista |
| `label` | string | Texto visible de relación |
| `animated` | boolean | Indica si la arista está animada |
| `data.relationship` | string | Relación lógica |

---

## 16. Métricas estándar

Las métricas deben mantener una forma estable entre estructuras.

```json
{
  "count": 0,
  "height": null,
  "balanceFactor": null,
  "collisions": null,
  "levels": null,
  "edgesCount": 0
}
```

Uso recomendado:

| Métrica | Aplica principalmente a |
|---|---|
| `count` | Todas |
| `height` | Árboles |
| `balanceFactor` | AVL |
| `collisions` | Tabla hash |
| `levels` | Árboles y grafos por capas |
| `edgesCount` | Árboles y grafos |

Cuando una métrica no aplique, debe devolverse como `null`.

---

## 17. Recorridos y animación

Formato estándar:

```json
{
  "type": "bfs",
  "start": "course-001",
  "order": [
    "course-001",
    "course-002",
    "course-003"
  ],
  "steps": [
    {
      "step": 1,
      "nodeId": "course-001",
      "action": "visit"
    },
    {
      "step": 2,
      "nodeId": "course-002",
      "action": "visit"
    }
  ]
}
```

Campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `type` | string/null | Tipo de recorrido |
| `start` | string/null | Nodo inicial |
| `order` | array | Orden final de visita |
| `steps` | array | Pasos para animación frontend |

Acciones sugeridas:

```text
visit
enqueue
dequeue
push
pop
compare
found
skip
```

---

## 18. Tipos visuales recomendados

Tipos base de React Flow:

```text
default
input
output
group
```

Tipos personalizados sugeridos para EduStruct:

```text
faculty-node
career-node
cycle-node
course-node
student-node
record-node
hash-bucket-node
queue-node
stack-node
```

Estos tipos podrán implementarse en el frontend durante épicas posteriores.

---

## 19. Estrategia de posicionamiento visual

El backend debe entregar posiciones iniciales para facilitar la visualización.

Reglas recomendadas:

| Estructura | Posicionamiento inicial |
|---|---|
| Árboles | `x` según orden horizontal, `y` según nivel |
| Grafos | Distribución por nivel académico o dependencia |
| Hash | Buckets en columna, elementos en fila |
| Lista | Nodos horizontales |
| Pila | Nodos verticales |
| Cola | Nodos horizontales con dirección |

El frontend podrá permitir reajuste visual, pero no debe depender de calcular la estructura desde cero.

---

## 20. Regla de consumo frontend

El frontend debe consumir principalmente:

```text
data.nodes
data.edges
data.metrics
data.traversal
data.result
```

Regla de error frontend:

```text
Mostrar message al usuario.
Usar error.code para decisiones internas.
```

Ejemplo:

- `VALIDATION_ERROR`: resaltar campos.
- `NOT_FOUND`: mostrar estado vacío.
- `DUPLICATE_KEY`: bloquear inserción repetida.
- `STRUCTURE_EMPTY`: mostrar mensaje de estructura vacía.
- `INVALID_OPERATION`: deshabilitar recorrido no permitido.

---

## 21. Restricción de la Épica 3

Durante esta épica no se debe implementar lógica pesada de:

- Árboles.
- AVL.
- Grafos.
- Árbol B/B+.
- Tabla hash.
- Recorridos reales.
- Balanceos.
- Animaciones complejas.

La prioridad es dejar definidos:

- Arquitectura.
- Contratos.
- Convenciones.
- Serialización.
- Organización modular.

---

## 22. Git workflow recomendado

Crear rama de trabajo:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-3-api-architecture
```

Durante el desarrollo:

```bash
git status
git add docs/api-contracts.md
git commit -m "docs: define initial api contracts for data structures"
```

Al finalizar la épica:

```bash
git checkout develop
git pull origin develop
git merge feature/epic-3-api-architecture
git push origin develop
git branch -d feature/epic-3-api-architecture
git push origin --delete feature/epic-3-api-architecture
```

---

## 23. Criterios de aceptación relacionados

Este contrato cumple con:

- Existe contrato claro frontend/backend.
- Todas las estructuras siguen convención común.
- El frontend sabe qué esperar.
- La serialización es consistente.
- La arquitectura queda lista para implementación en Épica 4.

---

# Anexo Épica 4 — Contratos Reales para Estructuras Lineales

Este anexo complementa los contratos generales definidos en la Épica 3 con los endpoints reales implementados para lista, pila y cola durante la Épica 4.

La convención general del contrato se mantiene. La diferencia principal es que estas estructuras lineales usan el campo `value` como dato principal, porque no requieren clave única obligatoria en esta etapa.

---

## 24. Consideración sobre `key` y `value` en estructuras lineales

El contrato general define `key` como identificador estándar para estructuras futuras como AVL, árbol B/B+, hash y grafos.

Para las estructuras lineales de Épica 4, el backend trabaja principalmente con:

```json
{
  "value": "dato educativo"
}
```

Motivo:

- Lista, pila y cola son estructuras secuenciales.
- No requieren clave única obligatoria.
- El orden de inserción es parte del comportamiento.
- El frontend puede representar cada elemento como nodo visual usando índices internos.

Cuando se implementen estructuras indexadas, se retomará el uso fuerte de `key`.

---

## 25. Endpoints reales — Lista

### Obtener estado

```http
GET /api/list/state
```

Respuesta exitosa:

```json
{
  "success": true,
  "message": "Estado de la lista obtenido correctamente.",
  "data": {
    "structure": "list",
    "operation": "state",
    "nodes": [],
    "edges": [],
    "metrics": {
      "count": 0,
      "height": null,
      "balanceFactor": null,
      "collisions": null,
      "levels": null,
      "edgesCount": 0
    },
    "traversal": {
      "type": null,
      "start": null,
      "order": [],
      "steps": []
    },
    "result": {
      "items": [],
      "size": 0,
      "head": null,
      "tail": null,
      "isEmpty": true,
      "nodes": [],
      "edges": []
    }
  },
  "error": null
}
```

### Insertar elemento

```http
POST /api/list/insert
```

Payload:

```json
{
  "value": "2024001 - Ana López",
  "position": "tail"
}
```

Campos:

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---:|---|
| `value` | any | Sí | Valor que se insertará en la lista |
| `position` | string | No | `head` o `tail`. Por defecto: `tail` |

Respuesta parcial esperada:

```json
{
  "success": true,
  "message": "Elemento insertado correctamente en la lista.",
  "data": {
    "structure": "list",
    "operation": "insert",
    "nodes": [
      {
        "id": "list-node-0",
        "type": "default",
        "position": {
          "x": 0,
          "y": 0
        },
        "data": {
          "label": "2024001 - Ana López",
          "category": "head tail item",
          "metadata": {
            "index": 0,
            "role": "HEAD/TAIL"
          }
        }
      }
    ],
    "edges": [],
    "metrics": {
      "count": 1,
      "height": null,
      "balanceFactor": null,
      "collisions": null,
      "levels": null,
      "edgesCount": 0
    },
    "result": {
      "items": ["2024001 - Ana López"],
      "size": 1,
      "head": "2024001 - Ana López",
      "tail": "2024001 - Ana López",
      "isEmpty": false,
      "inserted": "2024001 - Ana López",
      "position": "tail"
    }
  },
  "error": null
}
```

### Eliminar elemento

```http
DELETE /api/list/delete
```

Payload:

```json
{
  "value": "2024001 - Ana López"
}
```

### Buscar elemento

```http
GET /api/list/search?value=2024001%20-%20Ana%20López
```

### Recorrer lista

```http
GET /api/list/traverse
```

Tipo de recorrido devuelto:

```text
linear
```

### Cargar demo

```http
POST /api/list/demo/load
```

Contexto demo:

```text
Lista de estudiantes inscritos
```

---

## 26. Endpoints reales — Pila

### Obtener estado

```http
GET /api/stack/state
```

### Apilar elemento

```http
POST /api/stack/insert
```

Payload:

```json
{
  "value": "Curso MAT101"
}
```

Respuesta parcial esperada:

```json
{
  "success": true,
  "message": "Elemento apilado correctamente.",
  "data": {
    "structure": "stack",
    "operation": "push",
    "nodes": [
      {
        "id": "stack-node-0",
        "type": "default",
        "position": {
          "x": 0,
          "y": 0
        },
        "data": {
          "label": "Curso MAT101",
          "category": "top item",
          "metadata": {
            "indexFromTop": 0,
            "role": "TOP"
          }
        }
      }
    ],
    "edges": [],
    "metrics": {
      "count": 1,
      "height": null,
      "balanceFactor": null,
      "collisions": null,
      "levels": null,
      "edgesCount": 0
    },
    "result": {
      "items": ["Curso MAT101"],
      "size": 1,
      "top": "Curso MAT101",
      "isEmpty": false,
      "pushed": "Curso MAT101"
    }
  },
  "error": null
}
```

### Desapilar elemento

```http
DELETE /api/stack/delete
```

No requiere payload. Retira el elemento ubicado en el tope.

### Consultar tope

```http
GET /api/stack/peek
```

### Buscar elemento

```http
GET /api/stack/search?value=Curso%20MAT101
```

### Recorrer pila

```http
GET /api/stack/traverse
```

Tipo de recorrido devuelto:

```text
stack-top-to-bottom
```

### Cargar demo

```http
POST /api/stack/demo/load
```

Contexto demo:

```text
Historial de navegación académica
```

---

## 27. Endpoints reales — Cola

### Obtener estado

```http
GET /api/queue/state
```

### Encolar elemento

```http
POST /api/queue/insert
```

Payload:

```json
{
  "value": "Turno 1 - Ana López"
}
```

Respuesta parcial esperada:

```json
{
  "success": true,
  "message": "Elemento encolado correctamente.",
  "data": {
    "structure": "queue",
    "operation": "enqueue",
    "nodes": [
      {
        "id": "queue-node-0",
        "type": "default",
        "position": {
          "x": 0,
          "y": 0
        },
        "data": {
          "label": "Turno 1 - Ana López",
          "category": "front rear item",
          "metadata": {
            "indexFromFront": 0,
            "role": "FRONT/REAR"
          }
        }
      }
    ],
    "edges": [],
    "metrics": {
      "count": 1,
      "height": null,
      "balanceFactor": null,
      "collisions": null,
      "levels": null,
      "edgesCount": 0
    },
    "result": {
      "items": ["Turno 1 - Ana López"],
      "size": 1,
      "front": "Turno 1 - Ana López",
      "rear": "Turno 1 - Ana López",
      "isEmpty": false,
      "enqueued": "Turno 1 - Ana López"
    }
  },
  "error": null
}
```

### Desencolar elemento

```http
DELETE /api/queue/delete
```

No requiere payload. Retira el elemento ubicado en el frente.

### Consultar frente

```http
GET /api/queue/front
```

### Buscar elemento

```http
GET /api/queue/search?value=Turno%201%20-%20Ana%20López
```

### Recorrer cola

```http
GET /api/queue/traverse
```

Tipo de recorrido devuelto:

```text
queue-front-to-rear
```

### Cargar demo

```http
POST /api/queue/demo/load
```

Contexto demo:

```text
Cola de turnos de asesoría académica
```

---

## 28. Serialización React Flow para estructuras lineales

Las estructuras lineales ya devuelven `nodes` y `edges` listos para React Flow.

### Lista

Layout horizontal:

```text
HEAD → item → item → TAIL
```

Relación de aristas:

```text
next
```

### Pila

Layout vertical:

```text
TOP
 ↓
item
 ↓
item
```

Relación de aristas:

```text
below
```

### Cola

Layout horizontal:

```text
FRONT → item → item → REAR
```

Relación de aristas:

```text
next
```

---

## 29. Consumo frontend recomendado para estructuras lineales

El frontend debe leer:

```text
data.nodes
data.edges
data.metrics
data.traversal
data.result
```

Uso sugerido:

| Campo | Uso |
|---|---|
| `data.nodes` | Renderizar nodos en React Flow |
| `data.edges` | Renderizar conexiones |
| `data.metrics.count` | Mostrar cantidad de elementos |
| `data.metrics.edgesCount` | Mostrar cantidad de conexiones |
| `data.traversal.steps` | Animar recorridos |
| `data.result.items` | Mostrar panel textual educativo |

---

## 30. Git workflow para cierre de Épica 4

Rama de trabajo:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-4-linear-structures
```

Commit recomendado para documentación:

```bash
git add docs/data-structures-mapping.md docs/api-contracts.md docs/epic-4-summary.md
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
