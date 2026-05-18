# EduStruct — Git Closeout Épica 6

## Rama de trabajo

```bash
git checkout feature/epic-6-binary-tree
```

## Validar cambios pendientes

```bash
git status
```

## Commit final de documentación

```bash
git add docs/epic-6-summary.md docs/epic-6-final-validation.md docs/epic-6-git-closeout.md
git commit -m "docs(binary-tree): close epic 6 documentation"
```

## Actualizar develop

```bash
git checkout develop
git pull origin develop
```

## Merge de Épica 6

```bash
git merge --no-ff feature/epic-6-binary-tree
```

## Ejecutar validación post-merge

```bash
cd backend
python -m pytest
```

```bash
cd frontend
npm run build
```

## Publicar develop

```bash
git push origin develop
```

## Eliminar rama temporal local

```bash
git branch -d feature/epic-6-binary-tree
```

## Eliminar rama temporal remota

```bash
git push origin --delete feature/epic-6-binary-tree
```

## Commit semántico usado para cierre

```text
docs(binary-tree): close epic 6 documentation
```

## Nota

La eliminación de la rama debe hacerse únicamente después de confirmar que `develop` contiene todos los cambios y que las validaciones finales pasan correctamente.
