# EduStruct — Cierre Git Épica 8

## Rama de trabajo

La épica se desarrolla en:

```bash
feature/epic-8-btree
```

## Commits semánticos sugeridos

```bash
docs(btree): define btree technical decision
feat(btree): implement btree core structure
feat(btree): add btree service and serializer
feat(btree): expose btree rest endpoints
feat(btree): add btree visualization page
docs(btree): close epic 8 validation
```

## Validación previa al merge

Desde `backend`:

```bash
PYTHONPATH=. pytest
```

Resultado validado:

```text
297 passed
```

Desde `frontend`:

```bash
npm run build
```

Resultado validado:

```text
✓ built successfully
```

## Merge hacia develop

Ejecutar después de confirmar que todos los cambios están commiteados:

```bash
git checkout develop
git pull origin develop
git merge --no-ff feature/epic-8-btree
git push origin develop
```

## Eliminación de rama temporal

Después de validar que `develop` contiene la épica:

```bash
git branch -d feature/epic-8-btree
git push origin --delete feature/epic-8-btree
```

## Nota de control

No eliminar la rama antes de confirmar que:

1. El merge fue exitoso.
2. `develop` fue enviado a remoto.
3. Backend y frontend siguen validando correctamente desde `develop`.
