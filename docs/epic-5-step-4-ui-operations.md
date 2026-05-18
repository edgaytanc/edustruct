# Épica 5 — Paso 4: Operaciones completas desde UI

## Objetivo

Completar la interacción del Árbol General desde frontend, conectando la vista React Flow con los endpoints Flask ya implementados para el árbol académico.

## Archivos actualizados

```text
frontend/src/api/tree.js
frontend/src/pages/GeneralTreePage.jsx
backend/app/routes/tree.py
backend/app/services/tree_service.py
backend/app/structures/general_tree.py
backend/app/serializers/react_flow_serializer.py
docs/epic-5-step-4-ui-operations.md
```

## Funcionalidades cubiertas

- Cargar dataset demo del pensum académico.
- Insertar nodos por padre.
- Eliminar nodos junto con su subárbol.
- Buscar nodos por ID con resaltado visual.
- Ejecutar recorridos:
  - preorder
  - postorder
  - levelorder
- Mostrar métricas actualizadas:
  - nodos
  - altura
  - niveles
  - hojas
  - máximo de hijos
  - aristas
- Renderizar nodos y aristas con React Flow.
- Mantener sincronización visual después de cada operación.

## Corrección aplicada sobre el frontend

Se corrigió la normalización visual de nodos para evitar reprocesar labels ya renderizados como componentes React. Ahora cada nodo conserva un `rawLabel` interno para mantener estable la visualización después de búsquedas, recorridos y refrescos.

## Decisión técnica

El backend del Paso 3 ya contenía las operaciones necesarias. En este paso se conserva ese código y se refuerza la capa de UI/API sin regresar a placeholders anteriores.

## Validación recomendada

Backend:

```bash
cd backend
python -m compileall app tests
pytest
```

Frontend:

```bash
cd frontend
npm install
npm run build
npm run lint
```

## Git workflow

```bash
git status
git add .
git commit -m "feat(frontend): complete general tree ui operations"
```
