# Demo checklist — Épica 10 Grafos DFS/BFS

## Preparación

- Levantar backend Flask.
- Levantar frontend React.
- Confirmar que la página de Grafos aparece en la navegación.
- Confirmar que el backend responde correctamente.

## Backend

Validar pruebas:

```bash
PYTHONPATH=. pytest -q
```

Resultado esperado:

```bash
417 passed
```

## Frontend

Validar build:

```bash
npm run build
```

Resultado esperado:

```bash
✓ built
```

## Demostración funcional

1. Abrir la página de Grafos.
2. Cargar el demo de prerrequisitos.
3. Explicar que cada nodo representa un curso.
4. Explicar que cada arista representa una relación de prerrequisito.
5. Seleccionar un nodo inicial.
6. Ejecutar DFS.
7. Mostrar que DFS profundiza por una rama antes de volver.
8. Resetear visualización.
9. Ejecutar BFS.
10. Mostrar que BFS recorre por niveles.
11. Comparar el orden de visita DFS vs BFS.
12. Mostrar métricas del grafo.
13. Mostrar grado/conectividad básica del nodo.

## Puntos para defensa oral

- La implementación no usa librerías externas de grafos.
- La estructura usa lista de adyacencia.
- DFS se apoya en exploración profunda.
- BFS se apoya en cola lógica de exploración por niveles.
- React Flow solo visualiza; la lógica real está en Python.
- El backend mantiene separación entre estructura, service, serializer y rutas.

## Cierre

La Épica 10 cubre el requerimiento de Grafos DFS/BFS del proyecto final y refuerza el caso de uso educativo mediante el mapa de prerrequisitos.

