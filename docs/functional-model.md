# EduStruct — Modelo Funcional

## Objetivo

Definir el comportamiento funcional esperado de EduStruct antes de iniciar implementación técnica en backend o frontend.

Este documento establece qué hará cada módulo del sistema, qué operaciones estarán disponibles, qué entradas recibirá, qué salidas devolverá y qué métricas deberán visualizarse.

---

# Alcance del Modelo Funcional

El modelo funcional cubre:

- Módulos principales del sistema
- Operaciones por estructura de datos
- Entradas esperadas
- Salidas esperadas
- Métricas funcionales
- Respuestas JSON conceptuales
- Responsabilidades del backend
- Responsabilidades del frontend

---

# Módulos Funcionales del Sistema

EduStruct estará organizado en los siguientes módulos:

1. Dashboard general
2. Pensum académico
3. Decisiones académicas
4. Índices AVL
5. Expedientes académicos
6. Búsqueda por carnet
7. Prerrequisitos
8. Inscripciones
9. Historial académico
10. Turnos de asesoría

---

# 1. Dashboard General

## Objetivo

Mostrar una vista general del sistema y permitir acceso rápido a cada estructura de datos.

## Funcionalidades

- Mostrar resumen de estructuras disponibles
- Mostrar cantidad de entidades cargadas
- Mostrar estado del dataset demo
- Navegar hacia cada módulo visual

## Entrada esperada

No requiere entrada inicial.

## Salida esperada

Resumen general del sistema.

## Respuesta JSON conceptual

```json
{
  "system": "EduStruct",
  "dataset": "demo",
  "modules": [
    "general_tree",
    "binary_tree",
    "avl_tree",
    "b_tree",
    "hash_table",
    "graph",
    "list",
    "stack",
    "queue"
  ],
  "status": "ready"
}
```

---

# 2. Pensum Académico — Árbol General

## Objetivo

Visualizar la jerarquía académica:

Facultad → Carrera → Ciclo → Curso

## Operaciones

- Cargar pensum
- Insertar nodo académico
- Buscar curso
- Eliminar nodo
- Recorrer jerarquía
- Consultar nivel de un nodo

## Entradas esperadas

```json
{
  "id": "CUR-013",
  "name": "Programación III",
  "type": "course",
  "parent_id": "CIC-003"
}
```

## Salidas esperadas

```json
{
  "message": "Nodo académico agregado correctamente",
  "tree": {},
  "metrics": {
    "height": 4,
    "total_nodes": 21
  }
}
```

## Métricas

- Altura del árbol
- Total de nodos
- Nivel de cada nodo
- Cantidad de hijos por nodo

## Frontend esperado

- Visualizar árbol jerárquico
- Expandir y contraer nodos
- Resaltar búsquedas
- Mostrar niveles

---

# 3. Decisiones Académicas — Árbol Binario

## Objetivo

Evaluar decisiones académicas mediante caminos binarios.

## Caso de uso principal

Determinar si un estudiante puede asignarse un curso.

## Operaciones

- Cargar árbol de decisión
- Evaluar estudiante y curso
- Mostrar camino tomado
- Reiniciar evaluación
- Consultar resultado final

## Entrada esperada

```json
{
  "student_id": "2024001",
  "course_id": "CUR-013"
}
```

## Salida esperada

```json
{
  "student_id": "2024001",
  "course_id": "CUR-013",
  "can_enroll": true,
  "path": [
    "¿Tiene expediente activo?",
    "¿Aprobó prerrequisitos?",
    "¿Tiene cupo disponible?"
  ],
  "result": "Puede asignarse el curso"
}
```

## Métricas

- Cantidad de decisiones evaluadas
- Profundidad del camino
- Resultado final

## Frontend esperado

- Mostrar árbol binario
- Resaltar el camino recorrido
- Mostrar resultado de decisión

---

# 4. Índices AVL

## Objetivo

Permitir búsquedas eficientes y balanceadas por identificador.

## Aplicaciones

- Índice de cursos por ID
- Índice de estudiantes por ID
- Índice de expedientes por ID

## Operaciones

- Insertar nodo
- Buscar nodo
- Eliminar nodo
- Calcular altura
- Calcular factor de balance
- Mostrar rotaciones

## Entrada esperada

```json
{
  "id": "CUR-013",
  "name": "Programación III"
}
```

## Salida esperada

```json
{
  "message": "Nodo insertado en AVL",
  "root": "CUR-009",
  "metrics": {
    "height": 3,
    "balance_factor": 0,
    "last_rotation": "left-right"
  }
}
```

## Métricas

- Altura
- Factor de balance
- Rotaciones simples
- Rotaciones dobles
- Nodo raíz actual

## Frontend esperado

- Visualizar árbol AVL
- Mostrar rotaciones paso a paso
- Mostrar factor de balance por nodo
- Resaltar búsqueda

---

# 5. Expedientes Académicos — Árbol B/B+

## Objetivo

Simular un índice de base de datos para expedientes académicos.

## Operaciones

- Insertar expediente
- Buscar expediente por ID
- Eliminar expediente
- Dividir nodos
- Consultar claves ordenadas
- Mostrar niveles del índice

## Entrada esperada

```json
{
  "record_id": "EXP-1001",
  "student_carnet": "2024001",
  "status": "Activo"
}
```

## Salida esperada

```json
{
  "message": "Expediente insertado",
  "record_id": "EXP-1001",
  "index": {},
  "metrics": {
    "order": 3,
    "height": 2,
    "splits": 1
  }
}
```

## Métricas

- Orden del árbol
- Altura
- Cantidad de divisiones
- Cantidad de claves
- Niveles del índice

## Frontend esperado

- Mostrar nodos con múltiples claves
- Mostrar divisiones de nodo
- Visualizar búsqueda por expediente

---

# 6. Búsqueda por Carnet — Tabla Hash

## Objetivo

Buscar estudiantes rápidamente utilizando su carnet como clave única.

## Operaciones

- Insertar estudiante
- Buscar por carnet
- Eliminar estudiante
- Mostrar índice hash
- Mostrar colisiones
- Listar buckets

## Entrada esperada

```json
{
  "carnet": "2024001",
  "name": "Ana López"
}
```

## Salida esperada

```json
{
  "message": "Estudiante insertado",
  "hash_index": 3,
  "collisions": 0,
  "table": []
}
```

## Métricas

- Tamaño de tabla
- Índice generado
- Colisiones
- Factor de carga
- Buckets ocupados

## Frontend esperado

- Mostrar tabla con buckets
- Mostrar colisiones visualmente
- Resaltar resultado de búsqueda

---

# 7. Prerrequisitos — Grafo Dirigido

## Objetivo

Representar dependencias entre cursos.

## Operaciones

- Agregar curso
- Agregar prerrequisito
- Eliminar arista
- Ejecutar DFS
- Ejecutar BFS
- Buscar ruta académica
- Validar si un curso puede ser alcanzado

## Entrada esperada

```json
{
  "from": "CUR-009",
  "to": "CUR-013",
  "relation": "prerequisite"
}
```

## Salida esperada

```json
{
  "message": "Prerrequisito agregado",
  "graph": {},
  "metrics": {
    "nodes": 16,
    "edges": 8
  }
}
```

## Métricas

- Cantidad de nodos
- Cantidad de aristas
- Orden DFS
- Orden BFS
- Rutas encontradas

## Frontend esperado

- Visualizar nodos y aristas
- Animar DFS y BFS
- Resaltar ruta entre cursos
- Mostrar prerrequisitos directos e indirectos

---

# 8. Inscripciones — Lista

## Objetivo

Administrar estudiantes inscritos en un curso.

## Operaciones

- Agregar estudiante
- Eliminar estudiante
- Buscar estudiante
- Listar inscritos
- Contar inscritos

## Entrada esperada

```json
{
  "course_id": "CUR-013",
  "student_carnet": "2024001"
}
```

## Salida esperada

```json
{
  "message": "Estudiante inscrito",
  "course_id": "CUR-013",
  "students": [
    "2024001",
    "2024002"
  ],
  "count": 2
}
```

## Métricas

- Total de inscritos
- Posición del estudiante
- Curso asociado

## Frontend esperado

- Mostrar lista lineal
- Permitir insertar y eliminar estudiantes
- Mostrar cantidad de inscritos

---

# 9. Historial Académico — Pila

## Objetivo

Registrar acciones recientes del sistema para permitir revisión o deshacer operaciones.

## Operaciones

- Registrar acción
- Ver última acción
- Deshacer última acción
- Limpiar historial
- Listar historial actual

## Entrada esperada

```json
{
  "action": "student_enrolled",
  "description": "Ana López fue inscrita en Programación III"
}
```

## Salida esperada

```json
{
  "message": "Acción registrada",
  "top": "student_enrolled",
  "size": 4
}
```

## Métricas

- Tamaño de la pila
- Última acción
- Acciones disponibles para deshacer

## Frontend esperado

- Mostrar pila vertical
- Resaltar última acción
- Permitir operación deshacer

---

# 10. Turnos de Asesoría — Cola

## Objetivo

Gestionar solicitudes académicas en orden de llegada.

## Operaciones

- Agregar turno
- Atender turno
- Ver próximo turno
- Listar turnos pendientes
- Contar turnos

## Entrada esperada

```json
{
  "student_carnet": "2024001",
  "reason": "Validación de prerrequisitos"
}
```

## Salida esperada

```json
{
  "message": "Turno agregado",
  "next": {
    "student_carnet": "2024001",
    "reason": "Validación de prerrequisitos"
  },
  "pending": 4
}
```

## Métricas

- Total de turnos pendientes
- Próximo estudiante
- Turnos atendidos

## Frontend esperado

- Mostrar cola horizontal
- Resaltar próximo turno
- Permitir atender siguiente

---

# Responsabilidades del Backend

El backend será responsable de:

- Implementar estructuras de datos desde cero
- Mantener estado temporal de cada estructura
- Procesar operaciones
- Calcular métricas
- Serializar estructuras a JSON
- Validar reglas de negocio
- Exponer endpoints REST

---

# Responsabilidades del Frontend

El frontend será responsable de:

- Consumir la API REST
- Renderizar estructuras visualmente
- Permitir interacción del usuario
- Mostrar métricas
- Animar recorridos
- Resaltar operaciones realizadas
- Presentar errores de forma clara

---

# Contrato Conceptual de Respuesta

Todas las respuestas funcionales deberán mantener una estructura similar:

```json
{
  "success": true,
  "message": "Operación ejecutada correctamente",
  "data": {},
  "metrics": {},
  "errors": []
}
```

En caso de error:

```json
{
  "success": false,
  "message": "No se pudo ejecutar la operación",
  "data": null,
  "metrics": {},
  "errors": [
    "El estudiante no cumple los prerrequisitos"
  ]
}
```

---

# Validaciones Funcionales Generales

## Validación 1
No se debe insertar un estudiante con carnet duplicado.

## Validación 2
No se debe crear un prerrequisito hacia un curso inexistente.

## Validación 3
No se debe consultar un expediente inexistente sin devolver un error claro.

## Validación 4
No se debe atender una cola vacía.

## Validación 5
No se debe hacer pop de una pila vacía.

## Validación 6
No se debe eliminar un nodo inexistente sin informar el problema.

---

# Criterios de Aceptación Funcional

La Épica 2 será funcionalmente válida si:

- Cada módulo tiene propósito claro
- Cada estructura tiene operaciones definidas
- Cada estructura tiene métricas asociadas
- Backend y frontend tienen responsabilidades separadas
- Las respuestas JSON son consistentes
- Las reglas de negocio están alineadas al dominio educativo
- El diseño permite implementar las siguientes épicas sin rehacer la base

---

# Conclusión

El modelo funcional de EduStruct define cómo debe comportarse el sistema desde una perspectiva de usuario, API y visualización.

Este documento servirá como puente entre el dominio educativo y la implementación técnica posterior.
