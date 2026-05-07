# EduStruct — Mapeo Formal de Estructuras de Datos

## Objetivo del Documento

Este documento define cómo se aplicará cada estructura de datos dentro del dominio educativo de EduStruct.

La finalidad es evitar implementaciones forzadas y asegurar que cada estructura tenga una función clara, justificable y útil dentro del sistema.

---

# Resumen General del Mapeo

| Estructura de Datos | Aplicación en EduStruct | Propósito Principal |
|---|---|---|
| Árbol General | Pensum académico | Representar jerarquía académica |
| Árbol Binario | Decisiones académicas | Simular evaluación de condiciones |
| Árbol AVL | Índice por ID | Búsqueda eficiente y balanceada |
| Árbol B/B+ | Expedientes académicos | Simular índice de base de datos |
| Tabla Hash | Búsqueda por carnet | Acceso rápido a estudiantes |
| Grafo | Prerrequisitos | Representar dependencias entre cursos |
| Lista | Estudiantes inscritos | Mantener colecciones ordenadas |
| Pila | Historial académico | Registrar acciones recientes |
| Cola | Turnos de asesoría | Gestionar atención FIFO |

---

# 1. Árbol General — Pensum Académico

## Aplicación

El árbol general representará la jerarquía académica completa:

Facultad → Carrera → Ciclo → Curso

## Justificación

Un pensum académico tiene una estructura naturalmente jerárquica. Una facultad puede contener varias carreras, cada carrera puede contener varios ciclos y cada ciclo puede contener varios cursos.

## Nodos del Árbol

- Facultad
- Carrera
- Ciclo
- Curso

## Operaciones previstas

- Insertar nodo académico
- Buscar curso dentro del pensum
- Recorrer jerarquía completa
- Visualizar niveles del pensum
- Eliminar o actualizar nodos académicos

## Ejemplo

Facultad de Ingeniería
└── Ingeniería en Sistemas
    ├── Primer Ciclo
    │   ├── Introducción a la Programación
    │   └── Matemática I
    └── Segundo Ciclo
        ├── Programación I
        └── Matemática II

---

# 2. Árbol Binario — Decisiones Académicas

## Aplicación

El árbol binario representará decisiones académicas simples.

## Caso de uso

Determinar si un estudiante puede asignarse un curso.

## Justificación

Un árbol binario permite modelar decisiones con dos posibles caminos:

- Sí
- No

Esto encaja con reglas académicas condicionales.

## Ejemplo de decisión

¿El estudiante aprobó Programación II?

- Sí → Puede evaluar asignación de Programación III
- No → No puede asignarse Programación III

## Operaciones previstas

- Insertar decisión
- Evaluar condición
- Recorrer árbol de decisión
- Mostrar camino tomado
- Reiniciar evaluación

---

# 3. Árbol AVL — Índice Balanceado por ID

## Aplicación

El árbol AVL se utilizará como índice balanceado para búsquedas por identificadores.

## Posibles índices

- ID de curso
- ID de estudiante
- ID de expediente

## Justificación

Un AVL mantiene el árbol balanceado automáticamente, permitiendo búsquedas eficientes incluso después de múltiples inserciones y eliminaciones.

## Operaciones previstas

- Insertar registro por ID
- Buscar registro por ID
- Eliminar registro
- Mostrar rotaciones
- Mostrar factor de balance
- Calcular altura

## Métricas visibles

- Altura del árbol
- Factor de balance
- Rotaciones simples
- Rotaciones dobles

---

# 4. Árbol B/B+ — Expedientes Académicos

## Aplicación

El árbol B o B+ se utilizará para simular un índice de expedientes académicos.

## Justificación

Los expedientes funcionan como registros persistentes que normalmente se consultarían desde una base de datos. El árbol B/B+ permite representar cómo se organizan índices para búsquedas eficientes en grandes volúmenes de datos.

## Clave de búsqueda

- ID de expediente

## Operaciones previstas

- Insertar expediente
- Buscar expediente por ID
- Eliminar expediente
- Dividir nodos
- Mostrar niveles del índice
- Visualizar claves ordenadas

## Ejemplo

Expedientes:

- EXP-1001
- EXP-1002
- EXP-1003
- EXP-1004

El árbol agrupará claves por nodos, simulando almacenamiento indexado.

---

# 5. Tabla Hash — Búsqueda por Carnet

## Aplicación

La tabla hash se utilizará para buscar estudiantes mediante su carnet.

## Justificación

El carnet del estudiante es único y funciona muy bien como clave para una tabla hash.

## Clave

- Carnet del estudiante

## Valor

- Información básica del estudiante

## Operaciones previstas

- Insertar estudiante
- Buscar estudiante por carnet
- Eliminar estudiante
- Manejar colisiones
- Mostrar índice calculado
- Mostrar cantidad de colisiones

## Estrategia de colisiones

Se podrá utilizar encadenamiento mediante listas.

## Ejemplo

Carnet: 2024001  
Hash: índice 3  
Valor: estudiante asociado

---

# 6. Grafo — Prerrequisitos de Cursos

## Aplicación

El grafo representará las dependencias académicas entre cursos.

## Justificación

Los prerrequisitos no forman necesariamente una jerarquía simple. Un curso puede depender de varios cursos y un curso puede habilitar varios cursos posteriores. Esto corresponde naturalmente a un grafo dirigido.

## Tipo de grafo

Grafo dirigido.

## Nodos

Cursos.

## Aristas

Relaciones de prerrequisito.

## Ejemplo

Programación I → Programación II → Programación III

## Operaciones previstas

- Agregar curso
- Agregar prerrequisito
- Eliminar relación
- Ejecutar BFS
- Ejecutar DFS
- Verificar si un curso es alcanzable
- Detectar rutas académicas

## Métricas visibles

- Orden DFS
- Orden BFS
- Cantidad de nodos
- Cantidad de aristas

---

# 7. Lista — Estudiantes Inscritos

## Aplicación

La lista representará estudiantes inscritos en un curso.

## Justificación

Una inscripción es una colección de estudiantes asociada a un curso. La lista permite insertar, eliminar y recorrer estudiantes inscritos de forma simple.

## Operaciones previstas

- Agregar estudiante inscrito
- Eliminar estudiante inscrito
- Buscar estudiante dentro del curso
- Listar inscritos
- Contar inscritos

## Ejemplo

Curso: Programación III

Lista de inscritos:

1. Ana López
2. Carlos Pérez
3. María García

---

# 8. Pila — Historial Académico

## Aplicación

La pila representará el historial de acciones recientes dentro del sistema.

## Justificación

Una pila sigue el principio LIFO. Esto permite modelar acciones recientes como deshacer operaciones o consultar el último cambio realizado.

## Ejemplos de acciones

- Estudiante inscrito en curso
- Curso eliminado
- Expediente consultado
- Prerrequisito agregado

## Operaciones previstas

- Push: registrar acción
- Pop: deshacer última acción
- Peek: ver acción reciente
- Limpiar historial

## Caso de uso

Deshacer la última inscripción realizada.

---

# 9. Cola — Turnos de Asesoría

## Aplicación

La cola representará los turnos de asesoría académica.

## Justificación

Los turnos deben atenderse en orden de llegada. Esto corresponde directamente al principio FIFO.

## Operaciones previstas

- Enqueue: agregar turno
- Dequeue: atender siguiente turno
- Peek: ver próximo estudiante
- Mostrar cola completa
- Contar turnos pendientes

## Ejemplo

Turnos pendientes:

1. Estudiante A
2. Estudiante B
3. Estudiante C

El primero en entrar será el primero en ser atendido.

---

# Criterios de Coherencia

Cada estructura cumple una función específica dentro del sistema:

- No se usan estructuras solo por obligación académica
- Cada estructura representa un problema real del dominio educativo
- Las operaciones permiten interacción desde frontend
- Las métricas permiten demostrar comportamiento algorítmico
- El diseño permite crecimiento modular del backend y frontend

---

# Relación con el Frontend

Cada estructura deberá poder visualizarse gráficamente.

## Visualización esperada

| Estructura | Visualización |
|---|---|
| Árbol General | Jerarquía expandible |
| Árbol Binario | Diagrama de decisiones |
| AVL | Árbol balanceado con rotaciones |
| Árbol B/B+ | Nodos con múltiples claves |
| Hash | Tabla con buckets |
| Grafo | Nodos y aristas |
| Lista | Secuencia lineal |
| Pila | Bloques apilados |
| Cola | Fila horizontal |

---

# Relación con el Backend

Cada estructura deberá exponerse mediante endpoints REST.

## Operaciones mínimas comunes

- Crear elemento
- Buscar elemento
- Eliminar elemento
- Consultar estado actual
- Consultar métricas
- Consultar representación visual en JSON

---

# Conclusión

El mapeo formal de estructuras de datos para EduStruct establece una base sólida para la implementación técnica.

Cada estructura tiene una aplicación natural dentro del contexto educativo y permite demostrar conceptos fundamentales de Programación III mediante una aplicación visual, interactiva y justificable.

---

# Anexo Épica 4 — Implementación Real de Estructuras Lineales

Este anexo complementa el mapeo formal original con la implementación concreta realizada durante la Épica 4.

La finalidad es documentar cómo las estructuras lineales base se aplican actualmente en EduStruct, cómo se visualizan y cómo quedan preparadas para futuras épicas.

---

## A. Lista Enlazada — Implementación Real

### Aplicación concreta

La lista representa estudiantes inscritos en un curso universitario.

Caso educativo:

```text
Curso: Programación III
HEAD → 2024001 - Ana López → 2024002 - Carlos Méndez → 2024003 - Sofía Ramírez → TAIL
```

### Implementación técnica

La estructura se implementa manualmente en Python puro mediante una lista enlazada simplemente.

Archivo principal:

```text
backend/app/structures/list_model.py
```

### Responsabilidad

- Mantener una colección ordenada de elementos.
- Insertar al inicio o al final.
- Eliminar por valor.
- Buscar por valor.
- Recorrer de `head` a `tail`.
- Servir como base reutilizable para pila y cola.

### Operaciones implementadas

| Operación | Descripción | Complejidad |
|---|---|---:|
| `prepend` | Inserta al inicio | O(1) |
| `append` | Inserta al final | O(1) |
| `remove` | Elimina el primer valor coincidente | O(n) |
| `find` | Busca un valor | O(n) |
| `to_list` | Convierte a lista serializable | O(n) |
| `clear` | Limpia la estructura | O(1) |
| `size` | Devuelve cantidad de elementos | O(1) |

### Endpoints disponibles

```text
GET    /api/list/state
POST   /api/list/insert
DELETE /api/list/delete
GET    /api/list/search?value=...
POST   /api/list/demo/load
GET    /api/list/traverse
POST   /api/list/reset
```

### Payload de inserción

```json
{
  "value": "2024001 - Ana López",
  "position": "tail"
}
```

### Visualización React Flow

La lista se serializa horizontalmente:

```text
HEAD → Nodo 1 → Nodo 2 → Nodo 3 → TAIL
```

Cada nodo se entrega dentro de `data.nodes` y las relaciones `next` dentro de `data.edges`.

---

## B. Pila — Implementación Real

### Aplicación concreta

La pila representa historial académico o historial de navegación dentro del sistema.

Caso educativo:

```text
TOP
 ↓
Curso MAT101
 ↓
Pensum
 ↓
Dashboard
```

### Implementación técnica

La pila se implementa manualmente en Python puro reutilizando la lista enlazada.

Archivo principal:

```text
backend/app/structures/stack.py
```

### Responsabilidad

- Registrar acciones recientes.
- Consultar el último elemento agregado.
- Deshacer o retirar la acción más reciente.
- Servir como base futura para recorridos tipo DFS y manejo de historial.

### Operaciones implementadas

| Operación | Descripción | Complejidad |
|---|---|---:|
| `push` | Agrega al tope | O(1) |
| `pop` | Retira el tope | O(1) |
| `peek` | Consulta el tope sin retirarlo | O(1) |
| `to_list` | Devuelve elementos de top a bottom | O(n) |
| `clear` | Limpia la pila | O(1) |
| `size` | Devuelve cantidad de elementos | O(1) |

### Endpoints disponibles

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

### Payload de inserción

```json
{
  "value": "Curso MAT101"
}
```

### Visualización React Flow

La pila se serializa verticalmente:

```text
TOP
 ↓
Nodo 1
 ↓
Nodo 2
 ↓
Nodo 3
```

El primer nodo representa el tope.

---

## C. Cola — Implementación Real

### Aplicación concreta

La cola representa turnos de asesoría académica.

Caso educativo:

```text
FRONT → Turno 1 - Ana López → Turno 2 - Carlos Méndez → Turno 3 - Sofía Ramírez → REAR
```

### Implementación técnica

La cola se implementa manualmente en Python puro reutilizando la lista enlazada.

Archivo principal:

```text
backend/app/structures/queue.py
```

### Responsabilidad

- Registrar turnos en orden de llegada.
- Atender el primer turno pendiente.
- Consultar el frente de la cola.
- Servir como base futura para recorridos BFS.

### Operaciones implementadas

| Operación | Descripción | Complejidad |
|---|---|---:|
| `enqueue` | Agrega al final | O(1) |
| `dequeue` | Retira del frente | O(1) |
| `front` | Consulta el frente sin retirarlo | O(1) |
| `to_list` | Devuelve elementos de front a rear | O(n) |
| `clear` | Limpia la cola | O(1) |
| `size` | Devuelve cantidad de elementos | O(1) |

### Endpoints disponibles

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

### Payload de inserción

```json
{
  "value": "Turno 1 - Ana López"
}
```

### Visualización React Flow

La cola se serializa horizontalmente:

```text
FRONT → Nodo 1 → Nodo 2 → Nodo 3 → REAR
```

El primer nodo representa el frente y el último representa el final de la cola.

---

## D. Relación de Estructuras Lineales con Futuras Épicas

Las estructuras lineales implementadas en esta épica preparan el backend para:

| Futuro uso | Estructura base |
|---|---|
| DFS | Pila |
| BFS | Cola |
| Historial de navegación | Pila |
| Turnos académicos | Cola |
| Colisiones en hash por encadenamiento | Lista |
| Recorridos animados | Lista, pila y cola |
| Serialización React Flow | Todas |

---

## E. Criterios de Aceptación Cubiertos

| Criterio | Estado |
|---|---|
| Lista implementada manualmente | Cumplido |
| Pila implementada manualmente | Cumplido |
| Cola implementada manualmente | Cumplido |
| Sin librerías mágicas | Cumplido |
| Pruebas unitarias básicas | Cumplido |
| Reutilización desde otros módulos | Cumplido |
| Código desacoplado | Cumplido |
| Preparado para estructuras complejas | Cumplido |

