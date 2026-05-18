# Épica 7 — Cierre Git

## Rama de trabajo

La épica se trabajó en:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-7-avl-tree
```

## Validación antes del merge

Ejecutar:

```bash
PYTHONPATH=backend pytest backend/tests -q
cd frontend
npm install
npm run build
```

## Merge a develop

Cuando la épica esté revisada y aprobada:

```bash
git checkout develop
git pull origin develop
git merge --no-ff feature/epic-7-avl-tree
git push origin develop
```

## Eliminación de rama temporal

```bash
git branch -d feature/epic-7-avl-tree
git push origin --delete feature/epic-7-avl-tree
```

## Motivo del merge no fast-forward

Se usa `--no-ff` para preservar en el historial que todos los commits pertenecen a la Épica 7. Esto facilita trazabilidad, revisión y rollback si fuera necesario.
