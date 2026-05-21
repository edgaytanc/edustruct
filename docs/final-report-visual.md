# EduStruct — Memoria Técnica del Proyecto

## Programación III
### Visualizador Interactivo de Estructuras de Datos Aplicadas al Dominio Educativo

---

# Evidencias Visuales Integradas

## Dashboard principal

![Home](./images/home.png)

---

## Árbol General

El módulo de árbol general representa el pensum académico mediante una estructura jerárquica de múltiples hijos.

Características visuales implementadas:

- jerarquía Facultad → Carrera → Ciclos → Cursos
- métricas estructurales
- recorridos
- renderizado React Flow
- visualización dinámica

![Árbol General](./images/tree-general.png)

---

## Árbol Binario BST

El árbol binario implementa operaciones clásicas de inserción, búsqueda y eliminación.

Características destacadas:

- recorridos animados
- métricas de altura y niveles
- visualización estructural
- representación JSON del árbol

![BST](./images/bst.png)

---

## Árbol AVL

El módulo AVL implementa balanceo automático mediante rotaciones visibles.

Características destacadas:

- rotaciones LL/LR/RR/RL
- factor de balance
- snapshots estructurales
- rebalanceo dinámico

![AVL](./images/avl.png)

---

## Árbol B

El árbol B simula índices académicos multi-clave para expedientes universitarios.

Características destacadas:

- nodos multi-clave
- splits visibles
- recorridos por nivel
- validación estructural

![Árbol B](./images/btree.png)

---

## Tabla Hash

La tabla hash implementa una función hash manual con manejo explícito de colisiones.

Características destacadas:

- buckets visibles
- encadenamiento separado
- colisiones detectables
- factor de carga

![Hash](./images/hash.png)

---

## Grafos DFS/BFS

El módulo de grafos modela prerrequisitos universitarios mediante un grafo dirigido.

Características destacadas:

- recorridos DFS/BFS
- mapa de prerrequisitos
- componentes
- densidad del grafo

![Grafos](./images/graph.png)

---

## Estructuras Lineales

Integra lista enlazada, cola y pila contextualizadas a escenarios académicos reales.

Casos implementados:

| Estructura | Caso |
|---|---|
| Lista | Inscritos |
| Cola | Asesorías |
| Pila | Historial |

![Estructuras Lineales](./images/linear.png)

---

# Diagramas Técnicos

## Arquitectura General

```mermaid
graph TD

Frontend --> FlaskAPI
FlaskAPI --> Services
Services --> Structures
Structures --> Serializers
Serializers --> ReactFlow
```

---

## Flujo AVL

```mermaid
graph TD

Insert --> ValidateBalance
ValidateBalance --> Rotation
Rotation --> Serialize
Serialize --> Render
```

---

## Hash con colisiones

```mermaid
graph LR

Bucket0 --> Node1
Bucket1 --> Node2 --> Node3
Bucket2 --> Node4 --> Node5
```

---

## DFS vs BFS

```mermaid
graph TD

DFS --> Stack
BFS --> Queue
```

---

# Decisiones Técnicas

## Uso de Flask

Flask fue seleccionado por:

- simplicidad arquitectónica
- modularidad
- facilidad para APIs REST
- desacoplamiento frontend/backend

---

## Uso de React Flow

React Flow permitió:

- renderizado dinámico
- nodos interactivos
- edges visuales
- recorridos animados

---

## Uso de Árbol B

Se eligió Árbol B por:

- claridad pedagógica
- visualización más simple
- representación eficiente de índices académicos

---

## Manejo de colisiones hash

Se implementó encadenamiento separado debido a:

- facilidad de visualización
- claridad académica
- representación explícita de colisiones

---

# Estado Actual del Proyecto

EduStruct cuenta actualmente con:

- frontend desacoplado
- backend modular
- visualización interactiva
- estructuras implementadas manualmente
- métricas estructurales
- recorridos clásicos
- arquitectura extensible

---

# Fin del documento
