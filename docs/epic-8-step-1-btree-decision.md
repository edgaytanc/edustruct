# Épica 8 — Step 1: Decisión técnica Árbol B vs Árbol B+

## Objetivo del step

Definir formalmente qué variante de árbol multi-clave se implementará para EduStruct como simulación de índice académico eficiente para expedientes universitarios.

Este step no modifica lógica de backend ni frontend. Solamente deja documentada la decisión arquitectónica antes de implementar la estructura, respetando el flujo incremental usado en las épicas anteriores.

---

## Contexto funcional

EduStruct representa estructuras de datos dentro de un contexto educativo universitario. Para la Épica 8 se necesita simular un índice eficiente de expedientes académicos, donde cada clave puede representar un identificador de expediente, carnet o código académico.

La estructura debe permitir:

- Insertar registros.
- Buscar registros por clave.
- Visualizar nodos con múltiples claves.
- Mostrar splits durante inserciones.
- Mostrar altura y niveles.
- Serializar el árbol para React Flow.
- Defender técnicamente la complejidad y el comportamiento del índice.

---

## Alternativas evaluadas

### Árbol B

Un Árbol B almacena claves y datos asociados en nodos internos y hojas. Sus nodos pueden contener varias claves y varios hijos, manteniendo el árbol balanceado mediante divisiones de nodos cuando se excede la capacidad permitida.

Ventajas para EduStruct:

- Es más directo de implementar y explicar en una exposición académica.
- Permite visualizar claramente la promoción de claves durante un split.
- Cada nodo multi-clave tiene una relación directa con el concepto de página o bloque de índice.
- La búsqueda puede terminar en nodos internos o en hojas, lo que facilita demostrar eficiencia.
- Encaja directamente con el requisito de simular un índice de base de datos.

Desventajas:

- Para recorridos secuenciales masivos, no es tan cómodo como un Árbol B+ porque las hojas no están necesariamente enlazadas.

### Árbol B+

Un Árbol B+ almacena los datos completos normalmente solo en las hojas y usa los nodos internos como índice. Las hojas suelen estar enlazadas para facilitar recorridos secuenciales o consultas por rango.

Ventajas para EduStruct:

- Es más cercano a índices reales usados en muchos motores de bases de datos.
- Mejora recorridos por rango gracias al enlace entre hojas.
- Separa con claridad índice interno y datos finales.

Desventajas:

- Requiere más contratos visuales para distinguir nodos internos, hojas y enlaces horizontales.
- Aumenta la complejidad del serializer y de la interfaz React Flow.
- El objetivo actual se centra en inserción, búsqueda, niveles y splits; no exige consultas por rango ni hojas enlazadas.
- Puede distraer en la defensa oral con detalles adicionales que no aportan directamente al criterio de aceptación.

---

## Decisión

Se implementará un **Árbol B** manual en Python puro.

La decisión se toma porque el Árbol B cubre completamente los criterios de la Épica 8 y permite una visualización más clara de:

- nodos multi-clave;
- promoción de claves;
- split de nodos;
- búsqueda eficiente;
- altura del árbol;
- recorrido por niveles.

Para el alcance actual, un Árbol B es la opción más defendible y menos riesgosa. B+ sería buena opción si el sistema necesitara consultas por rango o navegación secuencial entre hojas, pero eso no forma parte del criterio mínimo de aceptación de esta épica.

---

## Diseño base aprobado

### Nodo

```python
class BTreeNode:
    keys
    children
    leaf
```

### Árbol

```python
class BTree:
    root
    order
```

### Orden inicial recomendado

Se usará orden `4` como valor demo inicial.

Justificación:

- Máximo de claves por nodo: `order - 1 = 3`.
- Máximo de hijos por nodo interno: `order = 4`.
- Permite provocar splits con pocos datos, ideal para demostración visual.
- Mantiene nodos suficientemente compactos para React Flow.

---

## Contrato visual esperado

Cada nodo serializado deberá exponer al frontend una forma equivalente a:

```json
{
  "keys": [10, 20, 30],
  "leaf": false,
  "level": 2
}
```

El serializer deberá transformar esa información al contrato actual de React Flow usado por EduStruct:

```json
{
  "nodes": [],
  "edges": []
}
```

---

## Metadata de splits

Cada split deberá registrar metadata mínima:

```json
{
  "promotedKey": 40,
  "before": {},
  "after": {}
}
```

Esta información será consumida posteriormente por el frontend para explicar visualmente qué clave subió y cómo cambió la estructura.

---

## Alcance del siguiente step

El siguiente step debe implementar el núcleo de la estructura:

- `backend/app/structures/btree.py`
- `backend/tests/structures/test_btree.py`

Debe incluir:

- clase `BTreeNode`;
- clase `BTree`;
- orden configurable;
- inserción manual;
- split de nodos;
- búsqueda;
- recorrido por niveles;
- métricas básicas de altura, niveles y cantidad de claves;
- pruebas unitarias de estructura.

---

## Workflow Git recomendado para este step

Antes de aplicar los cambios del ZIP:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-8-btree
```

Commit semántico sugerido para este step:

```bash
git add docs/epic-8-step-1-btree-decision.md
git commit -m "docs(btree): define epic 8 btree technical decision"
```

---

## Validación del step

Este step queda validado cuando:

- existe la documentación incremental de decisión técnica;
- no se modificó código funcional;
- no se sobrescribió documentación previa;
- queda definido formalmente que EduStruct implementará Árbol B y no B+;
- queda aprobado el orden inicial `4` para la demo.
