# Épica 11 — Step 3: Cola de turnos de asesoría académica

## Objetivo

Integrar la estructura lineal **Cola** al contexto real del negocio educativo de EduStruct, usando el dataset `datasets/advisory_turns.json` como fuente principal y `datasets/students.json` para resolver la información del estudiante asociado a cada turno.

Este step reemplaza la carga demo hardcodeada por una cola FIFO de turnos académicos reales.

## Contexto funcional

En una universidad, los estudiantes pueden solicitar asesoría académica para casos como:

- asignación de cursos;
- validación de prerrequisitos;
- consulta de expediente;
- cambio de carrera.

Estos casos se atienden en orden de llegada. Por eso la estructura correcta para modelarlos es una **cola FIFO**.

## Datasets utilizados

### `datasets/advisory_turns.json`

Contiene los turnos de asesoría académica:

```json
{
  "id": "TURN-001",
  "student_carnet": "2024001",
  "reason": "Asignación de curso",
  "status": "pending",
  "created_at": "2026-05-05T09:00:00"
}
```

### `datasets/students.json`

Permite resolver el carnet del turno hacia datos reales del estudiante:

```json
{
  "carnet": "2024001",
  "name": "Ana López",
  "email": "ana.lopez@edustruct.edu",
  "status": "active"
}
```

## Archivos modificados

```text
backend/app/utils/dataset_loader.py
backend/app/services/queue_service.py
backend/app/routes/queue.py
backend/tests/services/test_queue_service.py
backend/tests/routes/test_linear_structure_routes.py
backend/tests/services/test_linear_visualization_services.py
backend/tests/routes/test_linear_visualization_routes.py
```

## Endpoints agregados

### Obtener turnos reales

```http
GET /api/queue/advisory-turns
```

Respuesta esperada:

```json
{
  "turns": [
    {
      "id": "TURN-001",
      "studentCarnet": "2024001",
      "studentName": "Ana López",
      "reason": "Asignación de curso",
      "queuePosition": 0,
      "isFront": true
    }
  ],
  "count": 4,
  "context": "Turnos de asesoría académica",
  "sourceDataset": "advisory_turns.json"
}
```

### Cargar cola real de asesoría

```http
POST /api/queue/demo/load-advisory
```

Construye la cola FIFO usando los turnos en el orden del dataset.

Respuesta esperada:

```json
{
  "items": [
    "TURN-001 - 2024001 - Ana López - Asignación de curso",
    "TURN-002 - 2024002 - Carlos Pérez - Validación de prerrequisitos"
  ],
  "size": 4,
  "front": "TURN-001 - 2024001 - Ana López - Asignación de curso",
  "rear": "TURN-004 - 2024004 - Luis Ramírez - Cambio de carrera",
  "queuePolicy": "FIFO"
}
```

## Decisiones técnicas

### 1. No se modificó la estructura `Queue`

La clase `Queue` ya implementa correctamente el comportamiento FIFO sobre la lista enlazada manual del proyecto. Por eso no se modificó la estructura pura.

### 2. La integración de negocio vive en el servicio

La resolución de dataset y la conversión a etiquetas visuales se implementan en `QueueService`, manteniendo separadas las capas:

- `structures`: lógica pura de datos;
- `services`: casos de uso del dominio;
- `routes`: API REST;
- `serializers`: contrato visual React Flow.

### 3. El endpoint `/api/queue/demo/load` se conserva

Para compatibilidad con la API existente, `load_demo()` ahora delega a `load_advisory_turns_demo()`.

## Justificación académica

La cola demuestra claramente:

| Operación | Caso universitario |
|---|---|
| `enqueue` | Un estudiante solicita turno de asesoría |
| `dequeue` | El asesor atiende al siguiente estudiante |
| `front` | Consulta del próximo estudiante a atender |
| `traverse` | Visualización del orden FIFO |

## Validaciones esperadas

```bash
PYTHONPATH=. pytest
```

También debe mantenerse compatible con Docker:

```bash
docker compose up --build
```

## Estado del step

Step preparado para validación local con backend y pruebas automatizadas.
