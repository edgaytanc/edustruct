# Épica 11 - Step 4: Pila contextual para historial académico

## Objetivo

Integrar la estructura **Pila** al dominio educativo de EduStruct como un historial de navegación académica. La pila deja de representar una demo aislada y pasa a modelar un flujo real de uso dentro de una plataforma universitaria.

## Caso de uso

La pila representa el historial de navegación del estudiante o asesor académico dentro del sistema:

1. Dashboard Académico
2. Pensum Ingeniería en Sistemas
3. Curso CUR-013 - Programación III
4. Prerrequisitos del curso
5. Expediente Estudiantil

Como la pila trabaja con comportamiento **LIFO**, el último módulo consultado queda como `TOP` y es el primero en salir cuando se ejecuta una acción de retroceso.

## Operaciones representadas

| Operación | Endpoint | Contexto educativo |
|---|---|---|
| push | `POST /api/stack/navigation/push` | Registrar una nueva consulta académica |
| pop | `DELETE /api/stack/navigation/back` | Regresar a la vista anterior |
| peek | `GET /api/stack/peek` | Consultar la pantalla actual |
| traverse | `GET /api/stack/traverse` | Mostrar historial desde la vista actual hacia atrás |
| demo | `POST /api/stack/demo/load-history` | Cargar historial académico contextual |

## Endpoints agregados

### Cargar historial académico demo

```http
POST /api/stack/demo/load-history
```

Respuesta esperada:

```json
{
  "items": [
    "Expediente Estudiantil",
    "Prerrequisitos del curso",
    "Curso CUR-013 - Programación III",
    "Pensum Ingeniería en Sistemas",
    "Dashboard Académico"
  ],
  "size": 5,
  "top": "Expediente Estudiantil",
  "navigationPolicy": "LIFO"
}
```

### Navegar a módulo académico

```http
POST /api/stack/navigation/push
```

Payload:

```json
{
  "module": "Curso CUR-013"
}
```

### Retroceder navegación

```http
DELETE /api/stack/navigation/back
```

Respuesta parcial:

```json
{
  "backFrom": "Curso CUR-013",
  "currentModule": "Dashboard Académico",
  "navigationPolicy": "LIFO"
}
```

## Decisiones técnicas

- No se agregó persistencia porque el historial de navegación es una estructura de runtime.
- No se modificó la estructura `Stack`; la implementación manual ya cumple con LIFO.
- Se mantuvo el serializer `serialize_stack`, porque su visualización vertical `TOP -> items` ya representa correctamente una pila.
- El endpoint antiguo `POST /api/stack/demo/load` ahora reutiliza el historial académico contextual para mantener compatibilidad sin sostener demos genéricas.

## Justificación académica

La pila queda asociada a un caso real y defendible: el historial de navegación o deshacer dentro de EduStruct. Esta integración permite explicar:

- Inserción en el tope mediante `push`.
- Eliminación del tope mediante `pop`.
- Consulta de pantalla actual mediante `peek`.
- Política LIFO aplicada a navegación académica.

## Validación esperada

```bash
PYTHONPATH=. pytest
```

También debe mantenerse compatible con Docker:

```bash
docker compose up --build
```
