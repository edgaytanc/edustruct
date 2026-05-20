# Épica 9 — Validación final

## Alcance validado

La Épica 9 implementa una tabla hash manual aplicada a la búsqueda de estudiantes por carnet dentro del dominio educativo de EduStruct.

La implementación mantiene la arquitectura del proyecto:

```text
React + Vite + React Flow → API REST Flask → estructuras Python puras
```

## Componentes validados

### Backend

- `backend/app/structures/hash_table.py`
- `backend/app/services/hash_table_service.py`
- `backend/app/routes/hash_table.py`
- `backend/app/serializers/react_flow_serializer.py`

### Frontend

- `frontend/src/api/hashTable.js`
- `frontend/src/pages/HashPage.jsx`
- `frontend/src/router/AppRouter.jsx`
- `frontend/src/pages/HomePage.jsx`

### Pruebas

- `backend/tests/structures/test_hash_table.py`
- `backend/tests/services/test_hash_table_service.py`
- `backend/tests/routes/test_hash_table_routes.py`
- `backend/tests/serializers/test_react_flow_hash_table_serializer.py`

## Validación funcional

| Criterio | Resultado |
|---|---|
| Inserción por carnet | Aprobado |
| Búsqueda por carnet | Aprobado |
| Eliminación por carnet | Aprobado |
| Función hash propia | Aprobado |
| Tamaño inicial configurable | Aprobado |
| Manejo de colisiones | Aprobado |
| Conteo de colisiones | Aprobado |
| Factor de carga | Aprobado |
| Serialización visual por buckets | Aprobado |
| Resaltado de colisiones | Aprobado |
| Frontend integrado | Aprobado |
| Compatibilidad con épicas anteriores | Aprobado |

## Validación técnica

### Backend

Comando ejecutado:

```bash
PYTHONPATH=. pytest
```

Resultado:

```text
368 passed
```

### Frontend

Comando ejecutado:

```bash
npm run build
```

Resultado:

```text
built successfully
```

Observación: durante la instalación de dependencias se reportó una vulnerabilidad moderada existente en dependencias del frontend. No fue introducida por la Épica 9.

## Riesgos revisados

| Riesgo | Estado |
|---|---|
| Usar `dict` como estructura principal | Mitigado: almacenamiento por lista de buckets y nodos enlazados |
| Romper serializers existentes | Mitigado: se agregó `serialize_hash_table` sin alterar contratos previos |
| Duplicar lógica visual de árboles | Mitigado: se reutilizó el patrón de nodos y aristas React Flow |
| Perder trazabilidad de colisiones | Mitigado: cada entrada expone `collision`, `chainPosition` y bucket |
| Crear demo sin colisiones visibles | Mitigado: dataset demo controlado para provocar colisiones |

## Estado final

La Épica 9 queda técnicamente cerrada y lista para exposición universitaria.
