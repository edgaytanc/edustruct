# Épica 9 — Cierre Git

## Rama de trabajo

La épica debe desarrollarse en la rama:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-9-hash-table
```

## Commits semánticos sugeridos

```bash
git add docs/epic-9-step-1-hash-collision-strategy.md
git commit -m "feat(hash): define collision strategy"

git add backend/app/structures/hash_table.py backend/tests/structures/test_hash_table.py docs/epic-9-step-2-hash-core.md
git commit -m "feat(hash): implement hash table core"

git add backend/app/services/hash_table_service.py backend/app/serializers/react_flow_serializer.py backend/tests/services/test_hash_table_service.py backend/tests/serializers/test_react_flow_hash_table_serializer.py docs/epic-9-step-3-hash-service-serializer.md
git commit -m "feat(hash): add hash table service and serializer"

git add backend/app/routes/hash_table.py backend/tests/routes/test_hash_table_routes.py docs/epic-9-step-4-hash-routes.md
git commit -m "feat(hash): expose hash table endpoints"

git add frontend/src/api/hashTable.js frontend/src/pages/HashPage.jsx frontend/src/router/AppRouter.jsx frontend/src/pages/HomePage.jsx docs/epic-9-step-5-frontend-hash.md
git commit -m "feat(hash): add hash visualization page"

git add docs/epic-9-final-validation.md docs/epic-9-git-closeout.md docs/epic-9-summary.md docs/demo-checklist-epic-9.md
git commit -m "docs(hash): close epic 9 documentation"
```

## Validación previa al merge

Antes del merge a `develop`, ejecutar:

```bash
cd backend
PYTHONPATH=. pytest

cd ../frontend
npm run build
```

## Merge a develop

```bash
git checkout develop
git pull origin develop
git merge --no-ff feature/epic-9-hash-table
git push origin develop
```

## Eliminación de rama temporal

```bash
git branch -d feature/epic-9-hash-table
git push origin --delete feature/epic-9-hash-table
```

## Nota de control

No eliminar la rama antes de confirmar que `develop` contiene el merge y que el push remoto fue exitoso. Primero se cruza el puente; después se quema, no al revés.
