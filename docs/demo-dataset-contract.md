# EduStruct — Contrato de Datos del Dataset Demo

## Objetivo

Definir la estructura formal de los archivos de datos que serán utilizados por EduStruct para alimentar las estructuras de datos del sistema.

Este documento funciona como contrato previo a la creación de archivos reales dentro de `/datasets`.

---

# Alcance

El contrato define:

- Archivos sugeridos para el dataset
- Estructura JSON por entidad
- Convenciones de identificadores
- Reglas de integridad
- Relaciones entre archivos
- Validaciones mínimas esperadas

---

# Ubicación Propuesta

Los archivos reales del dataset deberán ubicarse en:

```text
/datasets
```

---

# Archivos Propuestos

| Archivo | Propósito |
|---|---|
| faculties.json | Facultades disponibles |
| careers.json | Carreras académicas |
| cycles.json | Ciclos académicos |
| courses.json | Cursos del pensum |
| students.json | Estudiantes registrados |
| records.json | Expedientes académicos |
| prerequisites.json | Relaciones entre cursos |
| enrollments.json | Estudiantes inscritos por curso |
| advisory_turns.json | Cola inicial de turnos de asesoría |
| academic_history.json | Historial inicial de acciones |

---

# Convenciones Generales

## Formato

Todos los archivos deberán estar en formato JSON.

## Codificación

UTF-8.

## Identificadores

Los identificadores deberán seguir prefijos consistentes:

| Entidad | Prefijo | Ejemplo |
|---|---|---|
| Facultad | FAC | FAC-001 |
| Carrera | CAR | CAR-001 |
| Ciclo | CIC | CIC-001 |
| Curso | CUR | CUR-001 |
| Expediente | EXP | EXP-1001 |
| Turno | TURN | TURN-001 |
| Acción histórica | ACT | ACT-001 |

## Carnet

El carnet del estudiante será numérico como cadena de texto para evitar problemas de formato.

Ejemplo:

```json
"carnet": "2024001"
```

---

# 1. faculties.json

## Propósito

Representar las facultades disponibles en el dataset.

## Estructura

```json
[
  {
    "id": "FAC-001",
    "name": "Facultad de Ingeniería",
    "description": "Unidad académica enfocada en ingeniería y tecnología"
  }
]
```

## Campos

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| id | string | Sí | Identificador único |
| name | string | Sí | Nombre de la facultad |
| description | string | No | Descripción breve |

---

# 2. careers.json

## Propósito

Representar carreras asociadas a facultades.

## Estructura

```json
[
  {
    "id": "CAR-001",
    "faculty_id": "FAC-001",
    "name": "Ingeniería en Sistemas",
    "description": "Carrera enfocada en software, sistemas y tecnología"
  }
]
```

## Campos

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| id | string | Sí | Identificador único |
| faculty_id | string | Sí | Facultad asociada |
| name | string | Sí | Nombre de la carrera |
| description | string | No | Descripción breve |

---

# 3. cycles.json

## Propósito

Representar ciclos académicos asociados a una carrera.

## Estructura

```json
[
  {
    "id": "CIC-001",
    "career_id": "CAR-001",
    "name": "Primer Ciclo",
    "order": 1
  }
]
```

## Campos

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| id | string | Sí | Identificador único |
| career_id | string | Sí | Carrera asociada |
| name | string | Sí | Nombre del ciclo |
| order | number | Sí | Orden académico del ciclo |

---

# 4. courses.json

## Propósito

Representar los cursos del pensum académico.

## Estructura

```json
[
  {
    "id": "CUR-001",
    "cycle_id": "CIC-001",
    "code": "SIS-101",
    "name": "Introducción a la Programación",
    "credits": 5,
    "description": "Curso introductorio de programación"
  }
]
```

## Campos

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| id | string | Sí | Identificador único |
| cycle_id | string | Sí | Ciclo asociado |
| code | string | Sí | Código académico del curso |
| name | string | Sí | Nombre del curso |
| credits | number | Sí | Créditos académicos |
| description | string | No | Descripción breve |

---

# 5. students.json

## Propósito

Representar estudiantes registrados.

## Estructura

```json
[
  {
    "carnet": "2024001",
    "name": "Ana López",
    "career_id": "CAR-001",
    "email": "ana.lopez@edustruct.edu",
    "status": "active"
  }
]
```

## Campos

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| carnet | string | Sí | Identificador único del estudiante |
| name | string | Sí | Nombre completo |
| career_id | string | Sí | Carrera asociada |
| email | string | No | Correo académico |
| status | string | Sí | Estado del estudiante |

## Estados permitidos

- active
- suspended
- graduated
- inactive

---

# 6. records.json

## Propósito

Representar expedientes académicos.

## Estructura

```json
[
  {
    "id": "EXP-1001",
    "student_carnet": "2024001",
    "status": "active",
    "average": 86.5,
    "approved_courses": ["CUR-001", "CUR-005", "CUR-009"],
    "failed_courses": []
  }
]
```

## Campos

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| id | string | Sí | Identificador único del expediente |
| student_carnet | string | Sí | Carnet del estudiante |
| status | string | Sí | Estado del expediente |
| average | number | Sí | Promedio académico |
| approved_courses | array | Sí | Cursos aprobados |
| failed_courses | array | Sí | Cursos reprobados |

---

# 7. prerequisites.json

## Propósito

Representar relaciones de prerrequisito entre cursos.

## Estructura

```json
[
  {
    "course_id": "CUR-013",
    "prerequisite_id": "CUR-009"
  }
]
```

## Campos

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| course_id | string | Sí | Curso que requiere prerrequisito |
| prerequisite_id | string | Sí | Curso requerido previamente |

---

# 8. enrollments.json

## Propósito

Representar estudiantes inscritos en cursos.

## Estructura

```json
[
  {
    "course_id": "CUR-013",
    "students": ["2024001", "2024002", "2024003"]
  }
]
```

## Campos

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| course_id | string | Sí | Curso asociado |
| students | array | Sí | Carnets de estudiantes inscritos |

---

# 9. advisory_turns.json

## Propósito

Representar la cola inicial de turnos de asesoría.

## Estructura

```json
[
  {
    "id": "TURN-001",
    "student_carnet": "2024001",
    "reason": "Validación de prerrequisitos",
    "status": "pending",
    "created_at": "2026-05-05T09:00:00"
  }
]
```

## Campos

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| id | string | Sí | Identificador único del turno |
| student_carnet | string | Sí | Estudiante asociado |
| reason | string | Sí | Motivo del turno |
| status | string | Sí | Estado del turno |
| created_at | string | Sí | Fecha y hora de creación |

## Estados permitidos

- pending
- attended
- cancelled

---

# 10. academic_history.json

## Propósito

Representar acciones iniciales para la pila de historial académico.

## Estructura

```json
[
  {
    "id": "ACT-001",
    "type": "enrollment_created",
    "description": "Ana López fue inscrita en Programación III",
    "student_carnet": "2024001",
    "course_id": "CUR-013",
    "created_at": "2026-05-05T09:30:00"
  }
]
```

## Campos

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| id | string | Sí | Identificador único |
| type | string | Sí | Tipo de acción |
| description | string | Sí | Descripción legible |
| student_carnet | string | No | Estudiante relacionado |
| course_id | string | No | Curso relacionado |
| created_at | string | Sí | Fecha y hora de la acción |

---

# Reglas de Integridad

## Regla 1

Todo `faculty_id` en `careers.json` debe existir en `faculties.json`.

## Regla 2

Todo `career_id` en `cycles.json` debe existir en `careers.json`.

## Regla 3

Todo `cycle_id` en `courses.json` debe existir en `cycles.json`.

## Regla 4

Todo `career_id` en `students.json` debe existir en `careers.json`.

## Regla 5

Todo `student_carnet` en `records.json` debe existir en `students.json`.

## Regla 6

Todo curso listado en `approved_courses` y `failed_courses` debe existir en `courses.json`.

## Regla 7

Todo `course_id` y `prerequisite_id` en `prerequisites.json` debe existir en `courses.json`.

## Regla 8

Todo estudiante inscrito en `enrollments.json` debe existir en `students.json`.

## Regla 9

Todo turno en `advisory_turns.json` debe apuntar a un estudiante existente.

## Regla 10

Todo `course_id` y `student_carnet` en `academic_history.json`, cuando existan, deben apuntar a registros válidos.

---

# Relación del Dataset con Estructuras

| Archivo | Estructura Relacionada |
|---|---|
| faculties.json | Árbol general |
| careers.json | Árbol general |
| cycles.json | Árbol general |
| courses.json | Árbol general, AVL, grafo |
| students.json | Hash, AVL, listas |
| records.json | Árbol B/B+ |
| prerequisites.json | Grafo dirigido |
| enrollments.json | Lista |
| academic_history.json | Pila |
| advisory_turns.json | Cola |

---

# Contrato de Carga Inicial

El backend deberá poder cargar los archivos en este orden:

1. faculties.json
2. careers.json
3. cycles.json
4. courses.json
5. students.json
6. records.json
7. prerequisites.json
8. enrollments.json
9. academic_history.json
10. advisory_turns.json

Este orden evita referencias a entidades todavía no cargadas.

---

# Respuesta Esperada al Cargar Dataset

```json
{
  "success": true,
  "message": "Dataset demo cargado correctamente",
  "data": {
    "faculties": 2,
    "careers": 4,
    "cycles": 3,
    "courses": 16,
    "students": 8,
    "records": 5,
    "prerequisites": 8,
    "enrollments": 2,
    "history_actions": 4,
    "advisory_turns": 4
  },
  "errors": []
}
```

---

# Errores Esperados

## Referencia inexistente

```json
{
  "success": false,
  "message": "Error de integridad en el dataset",
  "errors": [
    "El curso CUR-999 no existe"
  ]
}
```

## Carnet duplicado

```json
{
  "success": false,
  "message": "Error de integridad en el dataset",
  "errors": [
    "El carnet 2024001 está duplicado"
  ]
}
```

---

# Criterios de Aceptación

El contrato será válido si:

- Todos los archivos tienen estructura clara
- Todos los identificadores son consistentes
- Todas las relaciones están documentadas
- El dataset puede alimentar todas las estructuras de datos
- La carga inicial tiene un orden definido
- Los errores esperados están contemplados

---

# Conclusión

Este contrato define la base formal para construir los archivos reales del dataset demo de EduStruct.

A partir de este documento, la siguiente fase podrá generar los JSON reales en `/datasets` sin improvisar estructura ni romper relaciones.
