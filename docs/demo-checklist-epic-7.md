# Demo checklist — Épica 7 Árbol AVL

## Preparación

1. Levantar backend y frontend.
2. Abrir el dashboard principal.
3. Ingresar al módulo Árbol AVL.
4. Cargar demo inicial.

## Flujo recomendado de demostración

### 1. Explicar el problema

- Un árbol binario de búsqueda puede degradarse si los datos entran ordenados.
- AVL mantiene el árbol balanceado automáticamente.
- Cada nodo conserva altura y factor de balance.

### 2. Mostrar carga demo

Acción:

```text
Cargar demo
```

Validar visualmente:

- Nodos renderizados en React Flow.
- Alturas visibles.
- Factor de balance visible.
- Métricas actualizadas.

### 3. Demostrar rotaciones

Usar secuencias típicas:

```text
LL: 30, 20, 10
RR: 10, 20, 30
LR: 30, 10, 20
RL: 10, 30, 20
```

Validar:

- El árbol se rebalancea.
- Se registra el tipo de rotación.
- Se muestra before/after.
- La raíz esperada queda estable.

### 4. Demostrar búsqueda eficiente

Acción:

```text
Buscar un valor existente
Buscar un valor inexistente
```

Validar:

- Resultado claro.
- Nodo resaltado cuando existe.
- Mensaje de no encontrado cuando no existe.

### 5. Demostrar eliminación balanceada

Acción:

```text
Eliminar un nodo que provoque rebalanceo
```

Validar:

- El árbol sigue siendo AVL.
- Se mantienen alturas correctas.
- Se registra rotación si aplica.

### 6. Comparar con BST

Explicación sugerida:

- BST conserva orden, pero no garantiza altura baja.
- AVL paga costo adicional en inserción/eliminación.
- AVL mejora búsquedas al mantener altura O(log n).

## Métricas a mencionar

- Cantidad de nodos.
- Altura del árbol.
- Factor de balance.
- Rotaciones aplicadas.

## Criterios de aceptación demostrables

- El árbol se rebalancea correctamente.
- Las rotaciones son visibles.
- La interfaz muestra metadata de balance.
- La demo deja claro por qué AVL mejora la búsqueda.
