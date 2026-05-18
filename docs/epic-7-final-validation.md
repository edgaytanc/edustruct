# Épica 7 — Validación final técnica

## Objetivo validado

La Épica 7 implementa un Árbol AVL para demostrar búsqueda eficiente mediante balanceo automático y rotaciones visibles en la interfaz.

## Alcance implementado

### Backend

- `backend/app/structures/avl_tree.py`
  - Nodo AVL con valor, referencias izquierda/derecha y altura.
  - Inserción balanceada.
  - Eliminación balanceada.
  - Cálculo de altura por nodo.
  - Cálculo de factor de balance.
  - Rotaciones LL, RR, LR y RL.
  - Registro de eventos de rotación con estado antes/después.

- `backend/app/services/avl_service.py`
  - Servicio de aplicación para operaciones AVL.
  - Carga de demo.
  - Reset.
  - Búsqueda.
  - Inserción.
  - Eliminación.
  - Métricas.
  - Serialización para visualización.

- `backend/app/routes/avl.py`
  - Endpoints REST para estado, demo, reset, inserción, eliminación, búsqueda, recorridos y métricas.

- `backend/app/serializers/react_flow_serializer.py`
  - Serialización AVL compatible con React Flow.
  - Metadata por nodo: altura, factor de balance y bandera de desbalance.

### Frontend

- `frontend/src/api/avl.js`
  - Cliente API desacoplado para consumir los endpoints AVL.

- `frontend/src/pages/AVLPage.jsx`
  - Página visual e interactiva del Árbol AVL.
  - Inserción, eliminación, búsqueda, demo y reset.
  - Visualización React Flow.
  - Visualización before/after de rotaciones.
  - Métricas de altura, nodos y balance.
  - Historial de rotaciones.
  - Resaltado de nodos relevantes.

- `frontend/src/router/AppRouter.jsx`
  - Ruta agregada para `/avl`.

- `frontend/src/pages/HomePage.jsx`
  - Acceso visual al módulo AVL desde el dashboard.

## Validación backend ejecutada

```bash
cd edustruct
PYTHONPATH=backend pytest backend/tests -q
```

Resultado:

```bash
237 passed in 3.41s
```

## Validación frontend ejecutada

```bash
cd edustruct/frontend
npm install
npm run build
```

Resultado:

```bash
✓ built
```

## Pruebas cubiertas

- Inserción AVL.
- Eliminación AVL.
- Búsqueda.
- Alturas.
- Factores de balance.
- Rotación LL.
- Rotación RR.
- Rotación LR.
- Rotación RL.
- Servicio AVL.
- Serialización React Flow AVL.
- Endpoints REST AVL.
- Compatibilidad con pruebas previas de estructuras lineales, árbol general y árbol binario.

## Estado final

La Épica 7 queda técnicamente integrada sobre la base existente de EduStruct, sin romper compatibilidad con épicas anteriores.
