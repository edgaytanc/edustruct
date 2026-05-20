# Épica 10 — Cierre Git

## Rama de trabajo

La Épica 10 debe trabajarse en la rama:

```bash
feature/epic-10-graphs
```

## Commits semánticos esperados

Durante la épica se recomiendan los siguientes commits:

```bash
docs(graph): define graph representation decision
feat(graph): implement graph core
feat(graph): add graph service and serializer
feat(graph): expose graph routes
feat(graph): add graph visualization page
fix(graph): make demo load resilient without mounted datasets
docs(graph): close epic 10 documentation
```

## Validación antes del merge

Antes de cerrar la rama, ejecutar:

```bash
PYTHONPATH=. pytest -q
```

Resultado validado:

```bash
417 passed
```

También ejecutar en frontend:

```bash
npm run build
```

## Merge hacia develop

Comandos de cierre:

```bash
git checkout develop
git pull origin develop
git merge --no-ff feature/epic-10-graphs
git push origin develop
```

## Eliminación de rama temporal

Luego del merge exitoso:

```bash
git branch -d feature/epic-10-graphs
git push origin --delete feature/epic-10-graphs
```

## Nota de control

No usar `git merge --squash` para este cierre, porque se quiere conservar la trazabilidad incremental de cada step de la épica.

