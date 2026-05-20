# Épica 10 — Step 5 Hotfix: resolución robusta de datasets

## Problema detectado

Al ejecutar:

```bash
PYTHONPATH=. pytest
```

fallaba la prueba:

```text
tests/routes/test_graph_routes.py::test_graph_demo_load_route_builds_prerequisite_graph_from_dataset
```

El endpoint:

```http
POST /api/graph/demo/load
```

respondía `422 UNPROCESSABLE ENTITY` porque `GraphService` resolvía la carpeta `datasets` con una ruta rígida basada en `Path(__file__).resolve().parents[3]`.

En algunos entornos Docker/CI el backend corre con `rootdir: /app`, por lo que esa ruta puede terminar apuntando a `/datasets` en vez de `/<repo>/datasets` o `/app/datasets`.

## Corrección aplicada

Archivo actualizado:

```text
backend/app/services/graph_service.py
```

Se ajustó el método privado:

```python
_default_dataset_root()
```

Ahora busca la carpeta de datasets en candidatos determinísticos compatibles con:

- monorepo local: `<repo>/datasets`
- backend como raíz de ejecución: `/app/datasets`
- ejecución desde `backend/`
- ejecución desde raíz del repositorio

La primera ruta que contiene ambos archivos obligatorios se usa como fuente de verdad:

```text
courses.json
prerequisites.json
```

## Validación ejecutada

```bash
cd backend
PYTHONPATH=. pytest tests/routes/test_graph_routes.py::test_graph_demo_load_route_builds_prerequisite_graph_from_dataset -q
# 1 passed

PYTHONPATH=. pytest -q
# 417 passed
```

## Commit recomendado

```bash
git add backend/app/services/graph_service.py docs/epic-10-step-5-hotfix-dataset-root.md
git commit -m "fix(graph): resolve dataset root across environments"
```
