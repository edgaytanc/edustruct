# Épica 7 — Resumen de implementación AVL

## Resultado

Se implementó el módulo de Árbol AVL dentro de EduStruct, manteniendo la arquitectura cliente-servidor existente:

```text
React + React Flow → API REST Flask → AVL en Python puro
```

## Archivos principales

```text
backend/app/structures/avl_tree.py
backend/app/services/avl_service.py
backend/app/routes/avl.py
backend/app/serializers/react_flow_serializer.py
frontend/src/api/avl.js
frontend/src/pages/AVLPage.jsx
frontend/src/router/AppRouter.jsx
frontend/src/pages/HomePage.jsx
```

## Valor técnico

El AVL permite demostrar balanceo automático mediante rotaciones LL, RR, LR y RL. Esto cubre directamente el criterio de evaluación de Árbol AVL con balanceo y rotaciones visibles.

## Complejidad

| Operación | Complejidad |
|---|---:|
| Búsqueda | O(log n) |
| Inserción | O(log n) |
| Eliminación | O(log n) |
| Rotación simple | O(1) |
| Rotación doble | O(1) |

## Commits sugeridos por step

```bash
git add backend/app/structures/avl_tree.py backend/tests/structures/test_avl_tree.py docs/epic-7-step-1-avl-core.md
git commit -m "feat(avl): implement avl core structure"

git add backend/app/services/avl_service.py backend/app/serializers/react_flow_serializer.py backend/tests/services/test_avl_service.py backend/tests/serializers/test_react_flow_avl_serializer.py docs/epic-7-step-2-avl-service-serializer.md
git commit -m "feat(avl): add avl service and serializer"

git add backend/app/routes/avl.py backend/tests/routes/test_avl_routes.py docs/epic-7-step-3-avl-routes.md
git commit -m "feat(avl): expose avl rest endpoints"

git add frontend/src/api/avl.js frontend/src/pages/AVLPage.jsx frontend/src/router/AppRouter.jsx frontend/src/pages/HomePage.jsx docs/epic-7-step-4-frontend-avl.md
git commit -m "feat(avl): add avl visualization page"

git add docs/epic-7-summary.md docs/epic-7-final-validation.md docs/demo-checklist-epic-7.md docs/epic-7-git-closeout.md
git commit -m "docs(avl): close epic 7 documentation"
```
