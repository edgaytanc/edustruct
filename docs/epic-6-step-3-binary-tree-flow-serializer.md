# Épica 6 — STEP 3: Serialización React Flow para Árbol Binario

## Objetivo

Extender la capa de serialización visual para representar el árbol binario de búsqueda en React Flow sin contaminar la estructura pura ni la capa HTTP.

## Archivos actualizados

```text
backend/app/serializers/react_flow_serializer.py
backend/app/services/binary_tree_service.py
```

## Archivos creados

```text
backend/tests/serializers/test_react_flow_binary_tree_serializer.py
```

## Contrato visual

Cada nodo serializado contiene:

```json
{
  "id": "50",
  "type": "default",
  "position": { "x": 0, "y": 0 },
  "data": {
    "label": "50",
    "category": "root",
    "metadata": {
      "value": 50,
      "level": 0,
      "parentId": null,
      "direction": null,
      "hasLeft": true,
      "hasRight": true,
      "childrenCount": 2
    }
  }
}
```

Cada arista contiene:

```json
{
  "id": "binary-tree-edge-50-25",
  "source": "50",
  "target": "25",
  "type": "smoothstep",
  "label": "left",
  "animated": false,
  "data": {
    "relationship": "left"
  }
}
```

## Layout

El layout es jerárquico:

- raíz centrada
- hijos izquierdos posicionados hacia la izquierda
- hijos derechos posicionados hacia la derecha
- separación vertical por nivel

## Validación

Pruebas agregadas para:

- árbol vacío
- nodos root/left/right
- aristas con relación left/right
- posiciones horizontales básicas
- metadata necesaria para UI y animación

## Commit sugerido

```bash
git add .
git commit -m "feat(binary-tree): add react flow serializer"
```
