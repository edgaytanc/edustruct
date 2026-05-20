# Épica 10 — Step 1: Decisión técnica de representación del grafo

## Objetivo del step

Definir formalmente la representación interna que se usará para implementar el grafo de prerrequisitos de cursos en EduStruct.

La estructura debe permitir demostrar, de forma visual e interactiva:

- Inserción de cursos como nodos.
- Inserción de relaciones de prerrequisito como aristas dirigidas.
- Recorridos DFS y BFS.
- Búsqueda de cursos.
- Métricas básicas del grafo.
- Serialización compatible con React Flow.

---

## Archivos revisados como base

Antes de tomar la decisión se revisaron los documentos y datasets existentes del proyecto:

```text
docs/domain-model.md
docs/demo-dataset-design.md
docs/demo-dataset-contract.md
docs/data-structures-mapping.md
datasets/courses.json
datasets/prerequisites.json
```

También se verificó la arquitectura usada por las épicas anteriores:

```text
backend/app/structures/
backend/app/services/
backend/app/routes/
backend/app/serializers/
backend/tests/
frontend/src/api/
frontend/src/pages/
frontend/src/router/
```

---

## Contexto funcional

El grafo representa el mapa académico de prerrequisitos entre cursos universitarios.

En el dominio de EduStruct, cada curso puede:

- Tener cero o más prerrequisitos.
- Ser prerrequisito de cero o más cursos posteriores.
- Participar en recorridos académicos para mostrar dependencias.
- Visualizarse como nodo dentro de React Flow.

Ejemplo conceptual:

```text
Introducción a la Programación -> Programación I -> Programación II
Programación II -> Programación III
Programación II -> Estructuras de Datos -> Algoritmos -> Inteligencia Artificial
```

El grafo debe ser **dirigido**, porque la relación de prerrequisito tiene dirección académica.

Para EduStruct se usará la dirección:

```text
prerrequisito -> curso habilitado
```

Ejemplo:

```text
CUR-001 -> CUR-005
```

Esto significa:

```text
Introducción a la Programación habilita Programación I
```

Esta dirección es más útil para DFS/BFS porque permite iniciar desde un curso base y visualizar qué cursos desbloquea.

---

## Alternativas evaluadas

Se evaluaron dos representaciones clásicas de grafos:

1. Lista de adyacencia.
2. Matriz de adyacencia.

---

# Alternativa 1: Lista de adyacencia

## Descripción

Cada nodo del grafo mantiene una lista de vecinos conectados por aristas salientes.

Modelo conceptual:

```python
class GraphNode:
    id
    value
    neighbors
```

```python
class Graph:
    adjacency_list
    vertices_count
    edges_count
```

Estructura esperada:

```text
CUR-001 -> [CUR-005]
CUR-005 -> [CUR-009, CUR-011]
CUR-009 -> [CUR-013, CUR-010]
CUR-010 -> [CUR-014]
CUR-014 -> [CUR-016]
```

## Ventajas

- Representa de forma natural grafos dispersos.
- El dataset actual de prerrequisitos tiene pocas aristas respecto al número posible de conexiones.
- Permite insertar nodos y aristas de forma directa.
- DFS y BFS se implementan de forma clara recorriendo vecinos.
- Facilita calcular grado de salida de cada curso.
- Facilita serializar nodos y aristas para React Flow.
- Evita almacenar relaciones inexistentes.
- Es más pedagógica para explicar prerrequisitos en una exposición oral.
- Mantiene bajo acoplamiento con el dataset.
- Es compatible con implementación manual en Python puro.

## Desventajas

- Consultar si existe una arista específica puede requerir revisar la lista de vecinos.
- Si el grafo fuera extremadamente denso, podría ser menos directa que una matriz.
- Requiere controlar duplicados al insertar aristas.

## Compatibilidad con EduStruct

Alta.

El grafo de prerrequisitos no necesita representar todas las combinaciones posibles entre cursos, sino únicamente las dependencias reales.

React Flow trabaja naturalmente con una colección de `nodes` y `edges`, lo cual se alinea con una lista de adyacencia:

```text
adjacency_list -> edges serializables
vertices -> nodes serializables
```

Además, DFS y BFS pueden generar pasos de animación recorriendo cada vecino en orden estable.

---

# Alternativa 2: Matriz de adyacencia

## Descripción

La matriz de adyacencia usa una tabla bidimensional donde cada fila y columna representa un curso.

Si existe una relación entre dos cursos, se marca la celda correspondiente.

Estructura conceptual:

```text
          CUR-001  CUR-005  CUR-009
CUR-001      0        1        0
CUR-005      0        0        1
CUR-009      0        0        0
```

## Ventajas

- Permite consultar existencia de arista en tiempo constante si se conoce el índice de ambos nodos.
- Es fácil de explicar como tabla de conexiones.
- Puede ser útil en grafos densos.

## Desventajas

- Consume más espacio en grafos dispersos.
- Al crecer el número de cursos, la matriz crece cuadráticamente.
- Requiere mantener un índice adicional entre ID de curso y posición en matriz.
- Es menos natural para serializar aristas hacia React Flow.
- DFS y BFS requieren recorrer filas completas, incluyendo conexiones inexistentes.
- Agrega complejidad accidental para el caso académico de prerrequisitos.
- No aporta ventaja visual relevante para esta épica.

## Compatibilidad con EduStruct

Media-baja.

Aunque es implementable, la matriz complica innecesariamente el flujo esperado:

```text
curso -> vecinos -> recorrido -> animación
```

En EduStruct interesa mostrar dependencias reales, no una tabla completa de posibles relaciones. Usarla sería técnicamente defendible, pero pedagógicamente menos limpia. Demasiada matriz para tan pocos prerequisitos; el Excel ya sufrió bastante.

---

## Comparación formal

| Criterio | Lista de adyacencia | Matriz de adyacencia |
|---|---|---|
| Claridad pedagógica | Alta | Media |
| Compatibilidad con prerrequisitos | Alta | Media |
| Compatibilidad con React Flow | Alta | Media |
| Facilidad para DFS/BFS | Alta | Media |
| Inserción de nodo | Simple | Requiere expandir matriz |
| Inserción de arista | Simple | Simple, pero depende de índices |
| Uso de memoria | Eficiente en grafos dispersos | Alto en grafos dispersos |
| Escalabilidad | Alta | Media-baja |
| Complejidad accidental | Baja | Media |
| Mantenibilidad | Alta | Media |
| Implementación manual | Clara | Más mecánica |
| Explicación oral | Directa | Requiere justificar tabla completa |

---

## Decisión técnica

Se selecciona **lista de adyacencia** como representación oficial del grafo para la Épica 10.

---

## Justificación de la decisión

La lista de adyacencia es la opción más adecuada para EduStruct porque el mapa de prerrequisitos es un grafo dirigido y disperso.

Esta representación permite modelar directamente la relación académica:

```text
Curso prerrequisito -> Curso habilitado
```

También simplifica la implementación de DFS y BFS, ya que ambos recorridos trabajan naturalmente sobre vecinos.

La decisión mantiene coherencia con los objetivos del proyecto:

- Implementación manual en Python puro.
- Visualización clara en React Flow.
- Separación estricta entre estructura, servicio, serializer y rutas.
- Métricas simples y defendibles.
- Animación por pasos para reforzar aprendizaje.
- Bajo riesgo de romper compatibilidad con épicas anteriores.

---

## Diseño técnico aprobado para el Step 2

En el siguiente step se implementará el core del grafo en:

```text
backend/app/structures/graph.py
```

Con pruebas en:

```text
backend/tests/structures/test_graph.py
```

La estructura base esperada será:

```python
class GraphNode:
    def __init__(self, node_id, value=None):
        self.id = node_id
        self.value = value
        self.neighbors = []
```

```python
class Graph:
    def __init__(self, directed=True):
        self.directed = directed
        self.adjacency_list = {}
        self.vertices_count = 0
        self.edges_count = 0
```

Operaciones mínimas del core:

```text
add_vertex(node_id, value=None)
add_edge(source_id, target_id)
search(node_id)
dfs(start_id)
bfs(start_id)
get_neighbors(node_id)
degree(node_id)
to_adjacency_list()
metrics()
```

---

## Reglas de implementación para el Step 2

1. No usar librerías externas de grafos.
2. No usar `networkx`.
3. No delegar DFS/BFS a librerías externas.
4. Implementar DFS y BFS manualmente.
5. Usar lista nativa de Python para vecinos.
6. Usar diccionario únicamente como índice interno `id -> GraphNode`, no como sustituto de la estructura completa.
7. Evitar duplicar aristas.
8. Mantener orden estable de vecinos para recorridos predecibles.
9. Levantar errores claros cuando se intente recorrer desde un nodo inexistente.
10. Mantener compatibilidad con serialización posterior a React Flow.

---

## Dataset esperado para pasos posteriores

En pasos posteriores se podrá crear:

```text
datasets/course_graph.json
```

Este archivo deberá derivarse de:

```text
datasets/courses.json
datasets/prerequisites.json
```

Estructura sugerida:

```json
{
  "nodes": [
    {
      "id": "CUR-001",
      "code": "SIS-101",
      "name": "Introducción a la Programación"
    }
  ],
  "edges": [
    {
      "source": "CUR-001",
      "target": "CUR-005",
      "type": "prerequisite"
    }
  ]
}
```

La relación se serializará con dirección:

```text
source = prerequisite_id
target = course_id
```

---

## Impacto esperado en frontend

La lista de adyacencia permitirá exponer una respuesta compatible con React Flow:

```json
{
  "nodes": [],
  "edges": [],
  "metrics": {
    "vertices_count": 0,
    "edges_count": 0
  },
  "traversals": {
    "dfs": [],
    "bfs": []
  }
}
```

Cada nodo podrá mostrar:

```json
{
  "id": "CUR-010",
  "label": "Estructuras de Datos",
  "neighbors": ["CUR-014"],
  "degree": 1
}
```

Cada recorrido podrá generar pasos de animación:

```json
[
  {
    "step": 1,
    "visited": "CUR-001",
    "order": ["CUR-001"]
  }
]
```

---

## Workflow Git recomendado para iniciar la épica

Antes de implementar código del Step 2, se debe trabajar sobre una rama dedicada:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-10-graphs
```

Commit semántico sugerido para este step:

```bash
git add docs/epic-10-step-1-graph-representation-decision.md
git commit -m "docs(graph): define graph representation decision"
```

---

## Criterio de cierre del Step 1

Este step queda completo cuando:

- Se documenta la comparación entre lista de adyacencia y matriz de adyacencia.
- Se selecciona lista de adyacencia como representación oficial.
- Se define la dirección de aristas como `prerequisite_id -> course_id`.
- Se deja preparado el diseño técnico para implementar `graph.py` en el Step 2.
- El usuario valida explícitamente avanzar al Step 2.

---

## Estado

**Step 1 completado.**

Pendiente de validación explícita para iniciar el Step 2.
