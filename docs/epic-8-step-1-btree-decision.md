# Épica 8 — Step 1: Decisión técnica Árbol B vs Árbol B+

## Decisión

Para EduStruct se implementará **Árbol B**.

## Justificación

El requerimiento del proyecto permite implementar Árbol B o Árbol B+. En el contexto educativo universitario de EduStruct, el objetivo principal es demostrar visualmente búsquedas eficientes, múltiples claves por nodo, splits y crecimiento balanceado.

El Árbol B ofrece la mejor relación entre claridad pedagógica, facilidad de implementación y visualización con React Flow. Cada nodo puede mostrar sus claves internas directamente y los splits son fáciles de explicar durante la exposición.

## Comparación

| Criterio | Árbol B | Árbol B+ |
|---|---|---|
| Simplicidad pedagógica | Alta | Media |
| Visualización de claves | Directa en todos los nodos | Requiere distinguir hojas enlazadas |
| Implementación manual | Menor complejidad | Mayor complejidad |
| React Flow | Compatible con nodos multi-clave | Requiere enlaces horizontales de hojas |
| Tiempo de desarrollo | Controlado | Mayor |
| Mantenibilidad | Alta | Media |

## Conclusión

Se elige Árbol B porque cumple el criterio formal del curso y permite defender técnicamente la estructura sin introducir complejidad accidental. La implementación será manual en Python puro, con orden configurable, inserción con split, búsqueda, recorrido por niveles y serialización visual.
