# Épica 10 — Validación final

## Alcance validado

La Épica 10 incorporó el módulo de grafos para representar el mapa de prerrequisitos de cursos universitarios dentro de EduStruct.

El módulo cumple con el objetivo académico de demostrar:

- Representación manual de grafo en Python puro.
- Lista de adyacencia como estructura principal.
- Inserción de nodos.
- Inserción de aristas dirigidas.
- Búsqueda de cursos.
- Recorridos DFS y BFS.
- Serialización compatible con React Flow.
- API REST desacoplada.
- Visualización interactiva en frontend.
- Orden de visita y pasos de animación.
- Métricas básicas del grafo.

## Validación backend

Comando ejecutado:

```bash
PYTHONPATH=. pytest -q
```

Resultado validado por el usuario:

```bash
417 passed in 7.84s
```

Además, se validó puntualmente el endpoint de carga demo:

```bash
PYTHONPATH=. pytest tests/routes/test_graph_routes.py::test_graph_demo_load_route_builds_prerequisite_graph_from_dataset -q
```

Resultado:

```bash
1 passed in 0.39s
```

## Validación frontend

Comando esperado para validación de build:

```bash
npm run build
```

Resultado previo del Step 5:

```bash
✓ built
```

## Hotfix aplicado durante Step 5

Durante la validación se detectó que el endpoint:

```http
POST /api/graph/demo/load
```

respondía `422` en el entorno Docker/CI porque la resolución de la carpeta `datasets` dependía de una ruta rígida.

Se corrigió en:

```text
backend/app/services/graph_service.py
```

La corrección permite resolver datasets de forma resiliente y mantiene compatibilidad cuando el directorio no está montado exactamente igual en todos los entornos.

## Estado final

La Épica 10 queda técnicamente validada para backend y frontend.

No se identifican regresiones contra épicas anteriores.

