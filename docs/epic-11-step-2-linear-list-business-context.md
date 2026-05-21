# Épica 11 — Step 2: Lista enlazada con contexto real de inscripciones

## Objetivo

Integrar la estructura de lista enlazada al dominio educativo real de EduStruct mediante la carga de estudiantes inscritos por curso, usando los datasets académicos del proyecto en lugar de valores quemados en código.

La lista deja de representar una demostración genérica y pasa a modelar un caso universitario defendible: **estudiantes inscritos en un curso específico**.

## Contexto de negocio

La estructura lineal `LinkedList` se utiliza para representar el orden de estudiantes inscritos en un curso. Este contexto permite explicar operaciones clásicas de listas dentro de una situación académica real:

| Operación | Significado en el dominio |
| --- | --- |
| Insertar | Inscribir estudiante en la lista del curso |
| Eliminar | Retirar estudiante inscrito |
| Buscar | Localizar estudiante dentro del curso |
| Recorrer | Mostrar todos los inscritos de inicio a fin |
| HEAD | Primer estudiante registrado en la lista |
| TAIL | Último estudiante registrado en la lista |

## Datasets utilizados

Se integran los siguientes archivos:

- `datasets/students.json`
- `datasets/enrollments.json`
- `datasets/courses.json`

La relación se resuelve así:

1. `enrollments.json` define el curso y los carnets inscritos.
2. `students.json` provee la información real del estudiante.
3. `courses.json` agrega metadatos del curso como código y nombre.

Ejemplo para `CUR-013`:

```text
SIS-304 - Programación III
2024001 - Ana López
2024002 - Carlos Pérez
2024003 - María García
```

## Archivos nuevos

### `backend/app/utils/__init__.py`

Inicializa el paquete de utilidades del backend.

### `backend/app/utils/dataset_loader.py`

Centraliza lectura y validación de datasets JSON.

Responsabilidades:

- Resolver la ruta raíz del proyecto.
- Leer archivos dentro de `/datasets`.
- Validar estructura base de JSON.
- Indexar estudiantes por carnet.
- Indexar cursos por id.
- Cargar inscripciones por curso.
- Lanzar `DatasetError` cuando los datasets no son compatibles.

## Archivos modificados

### `backend/app/services/list_service.py`

Se agregan métodos de negocio:

- `get_available_courses()`
- `load_course_enrollments(course_id)`

Además, `load_demo()` ahora carga por defecto `CUR-013`, usando datos reales.

### `backend/app/routes/list_structure.py`

Se agregan endpoints REST:

```http
GET /api/list/courses
POST /api/list/demo/load-course
```

### `backend/tests/services/test_list_service.py`

Se agregan pruebas para:

- cursos disponibles
- carga real de estudiantes por curso
- carga demo basada en dataset real
- curso inexistente
- validación de `courseId`

### `backend/tests/routes/test_linear_structure_routes.py`

Se agregan pruebas para:

- `GET /api/list/courses`
- `POST /api/list/demo/load-course`
- errores `NOT_FOUND`
- errores `VALIDATION_ERROR`

## Contratos REST

### Obtener cursos disponibles

```http
GET /api/list/courses
```

Respuesta esperada:

```json
{
  "success": true,
  "data": {
    "structure": "list",
    "operation": "courses",
    "result": {
      "courses": [
        {
          "courseId": "CUR-013",
          "code": "SIS-304",
          "name": "Programación III",
          "label": "SIS-304 - Programación III",
          "enrolledCount": 3
        }
      ],
      "size": 2,
      "context": "Cursos con estudiantes inscritos disponibles para lista enlazada"
    }
  }
}
```

### Cargar inscripciones de un curso

```http
POST /api/list/demo/load-course
Content-Type: application/json

{
  "courseId": "CUR-013"
}
```

Respuesta esperada:

```json
{
  "success": true,
  "data": {
    "structure": "list",
    "operation": "demo-load-course",
    "result": {
      "items": [
        "2024001 - Ana López",
        "2024002 - Carlos Pérez",
        "2024003 - María García"
      ],
      "size": 3,
      "head": "2024001 - Ana López",
      "tail": "2024003 - María García",
      "courseId": "CUR-013",
      "context": "Lista enlazada de estudiantes inscritos por curso"
    }
  }
}
```

## Validaciones

### `courseId` faltante

```http
400 VALIDATION_ERROR
```

### Curso sin inscripciones

```http
404 NOT_FOUND
```

### Dataset inconsistente

```http
422 DATASET_ERROR
```

## Decisiones técnicas

### No se modificó `LinkedList`

La estructura manual ya cumplía con el objetivo académico:

- nodos propios
- inserción al inicio y final
- eliminación
- búsqueda
- recorrido
- limpieza

El cambio pertenece al servicio porque el problema era de contexto funcional, no de estructura.

### No se agregó persistencia

La épica mantiene el patrón usado por las estructuras visuales anteriores: estado en memoria para demostración interactiva.

### Los arrays de Python solo se usan como frontera

La lógica principal sigue usando `LinkedList`. Las listas nativas aparecen únicamente para:

- leer JSON
- preparar respuestas REST
- serializar hacia React Flow

Esto mantiene la defensa académica del proyecto: la estructura implementada manualmente sigue siendo la protagonista.

## Validación sugerida

Desde `/backend`:

```bash
PYTHONPATH=. pytest
```

Desde `/frontend`:

```bash
npm run build
```

Desde la raíz del proyecto:

```bash
docker compose up --build
```

## Estado del Step

Implementación backend lista para integrarse al frontend en el siguiente paso de la Épica 11.
