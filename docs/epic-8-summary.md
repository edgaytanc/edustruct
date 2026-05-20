# EduStruct — Resumen Épica 8: Árbol B

## Resultado

Se implementó un **Árbol B** como simulación de índice académico eficiente para expedientes universitarios.

## Decisión técnica

Se eligió Árbol B frente a Árbol B+ por:

- Mayor simplicidad pedagógica.
- Mejor facilidad de explicación.
- Menor complejidad de implementación.
- Visualización más directa en React Flow.
- Suficiente cumplimiento del requerimiento del curso.

## Backend

Se agregó:

- `backend/app/structures/btree.py`
- `backend/app/services/btree_service.py`
- `backend/app/routes/btree.py`

Se extendió:

- `backend/app/serializers/react_flow_serializer.py`

## Frontend

Se agregó:

- `frontend/src/api/btree.js`
- `frontend/src/pages/BTreePage.jsx`

Se extendió:

- `frontend/src/router/AppRouter.jsx`
- `frontend/src/pages/HomePage.jsx`

## Testing

Se agregó cobertura en:

- estructuras
- servicios
- rutas
- serializers

Resultado backend:

```text
297 passed
```

Resultado frontend:

```text
✓ built successfully
```

## Cierre

La épica queda lista para integrarse a `develop` mediante merge controlado y continuar con la siguiente estructura del proyecto.
