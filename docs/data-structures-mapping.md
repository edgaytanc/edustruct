# EduStruct — Mapeo Formal de Estructuras de Datos

## Objetivo del Documento

Este documento define cómo se aplicará cada estructura de datos dentro del dominio educativo de EduStruct.

La finalidad es evitar implementaciones forzadas y asegurar que cada estructura tenga una función clara, justificable y útil dentro del sistema.

---

# Resumen General del Mapeo

| Estructura de Datos | Aplicación en EduStruct | Propósito Principal |
|---|---|---|
| Árbol General | Pensum académico | Representar jerarquía académica |
| Árbol Binario | Decisiones académicas | Simular evaluación de condiciones |
| Árbol AVL | Índice por ID | Búsqueda eficiente y balanceada |
| Árbol B/B+ | Expedientes académicos | Simular índice de base de datos |
| Tabla Hash | Búsqueda por carnet | Acceso rápido a estudiantes |
| Grafo | Prerrequisitos | Representar dependencias entre cursos |
| Lista | Estudiantes inscritos | Mantener colecciones ordenadas |
| Pila | Historial académico | Registrar acciones recientes |
| Cola | Turnos de asesoría | Gestionar atención FIFO |

---

# 1. Árbol General — Pensum Académico

## Aplicación

El árbol general representará la jerarquía académica completa:

Facultad → Carrera → Ciclo → Curso

## Justificación

Un pensum académico tiene una estructura naturalmente jerárquica. Una facultad puede contener varias carreras, cada carrera puede contener varios ciclos y cada ciclo puede contener varios cursos.

## Nodos del Árbol

- Facultad
- Carrera
- Ciclo
- Curso

## Operaciones previstas

- Insertar nodo académico
- Buscar curso dentro del pensum
- Recorrer jerarquía completa
- Visualizar niveles del pensum
- Eliminar o actualizar nodos académicos

## Ejemplo

Facultad de Ingeniería
└── Ingeniería en Sistemas
    ├── Primer Ciclo
    │   ├── Introducción a la Programación
    │   └── Matemática I
    └── Segundo Ciclo
        ├── Programación I
        └── Matemática II

---

# 2. Árbol Binario — Decisiones Académicas

## Aplicación

El árbol binario representará decisiones académicas simples.

## Caso de uso

Determinar si un estudiante puede asignarse un curso.

## Justificación

Un árbol binario permite modelar decisiones con dos posibles caminos:

- Sí
- No

Esto encaja con reglas académicas condicionales.

## Ejemplo de decisión

¿El estudiante aprobó Programación II?

- Sí → Puede evaluar asignación de Programación III
- No → No puede asignarse Programación III

## Operaciones previstas

- Insertar decisión
- Evaluar condición
- Recorrer árbol de decisión
- Mostrar camino tomado
- Reiniciar evaluación

---

# 3. Árbol AVL — Índice Balanceado por ID

## Aplicación

El árbol AVL se utilizará como índice balanceado para búsquedas por identificadores.

## Posibles índices

- ID de curso
- ID de estudiante
- ID de expediente

## Justificación

Un AVL mantiene el árbol balanceado automáticamente, permitiendo búsquedas eficientes incluso después de múltiples inserciones y eliminaciones.

## Operaciones previstas

- Insertar registro por ID
- Buscar registro por ID
- Eliminar registro
- Mostrar rotaciones
- Mostrar factor de balance
- Calcular altura

## Métricas visibles

- Altura del árbol
- Factor de balance
- Rotaciones simples
- Rotaciones dobles

---

# 4. Árbol B/B+ — Expedientes Académicos

## Aplicación

El árbol B o B+ se utilizará para simular un índice de expedientes académicos.

## Justificación

Los expedientes funcionan como registros persistentes que normalmente se consultarían desde una base de datos. El árbol B/B+ permite representar cómo se organizan índices para búsquedas eficientes en grandes volúmenes de datos.

## Clave de búsqueda

- ID de expediente

## Operaciones previstas

- Insertar expediente
- Buscar expediente por ID
- Eliminar expediente
- Dividir nodos
- Mostrar niveles del índice
- Visualizar claves ordenadas

## Ejemplo

Expedientes:

- EXP-1001
- EXP-1002
- EXP-1003
- EXP-1004

El árbol agrupará claves por nodos, simulando almacenamiento indexado.

---

# 5. Tabla Hash — Búsqueda por Carnet

## Aplicación

La tabla hash se utilizará para buscar estudiantes mediante su carnet.

## Justificación

El carnet del estudiante es único y funciona muy bien como clave para una tabla hash.

## Clave

- Carnet del estudiante

## Valor

- Información básica del estudiante

## Operaciones previstas

- Insertar estudiante
- Buscar estudiante por carnet
- Eliminar estudiante
- Manejar colisiones
- Mostrar índice calculado
- Mostrar cantidad de colisiones

## Estrategia de colisiones

Se podrá utilizar encadenamiento mediante listas.

## Ejemplo

Carnet: 2024001  
Hash: índice 3  
Valor: estudiante asociado

---

# 6. Grafo — Prerrequisitos de Cursos

## Aplicación

El grafo representará las dependencias académicas entre cursos.

## Justificación

Los prerrequisitos no forman necesariamente una jerarquía simple. Un curso puede depender de varios cursos y un curso puede habilitar varios cursos posteriores. Esto corresponde naturalmente a un grafo dirigido.

## Tipo de grafo

Grafo dirigido.

## Nodos

Cursos.

## Aristas

Relaciones de prerrequisito.

## Ejemplo

Programación I → Programación II → Programación III

## Operaciones previstas

- Agregar curso
- Agregar prerrequisito
- Eliminar relación
- Ejecutar BFS
- Ejecutar DFS
- Verificar si un curso es alcanzable
- Detectar rutas académicas

## Métricas visibles

- Orden DFS
- Orden BFS
- Cantidad de nodos
- Cantidad de aristas

---

# 7. Lista — Estudiantes Inscritos

## Aplicación

La lista representará estudiantes inscritos en un curso.

## Justificación

Una inscripción es una colección de estudiantes asociada a un curso. La lista permite insertar, eliminar y recorrer estudiantes inscritos de forma simple.

## Operaciones previstas

- Agregar estudiante inscrito
- Eliminar estudiante inscrito
- Buscar estudiante dentro del curso
- Listar inscritos
- Contar inscritos

## Ejemplo

Curso: Programación III

Lista de inscritos:

1. Ana López
2. Carlos Pérez
3. María García

---

# 8. Pila — Historial Académico

## Aplicación

La pila representará el historial de acciones recientes dentro del sistema.

## Justificación

Una pila sigue el principio LIFO. Esto permite modelar acciones recientes como deshacer operaciones o consultar el último cambio realizado.

## Ejemplos de acciones

- Estudiante inscrito en curso
- Curso eliminado
- Expediente consultado
- Prerrequisito agregado

## Operaciones previstas

- Push: registrar acción
- Pop: deshacer última acción
- Peek: ver acción reciente
- Limpiar historial

## Caso de uso

Deshacer la última inscripción realizada.

---

# 9. Cola — Turnos de Asesoría

## Aplicación

La cola representará los turnos de asesoría académica.

## Justificación

Los turnos deben atenderse en orden de llegada. Esto corresponde directamente al principio FIFO.

## Operaciones previstas

- Enqueue: agregar turno
- Dequeue: atender siguiente turno
- Peek: ver próximo estudiante
- Mostrar cola completa
- Contar turnos pendientes

## Ejemplo

Turnos pendientes:

1. Estudiante A
2. Estudiante B
3. Estudiante C

El primero en entrar será el primero en ser atendido.

---

# Criterios de Coherencia

Cada estructura cumple una función específica dentro del sistema:

- No se usan estructuras solo por obligación académica
- Cada estructura representa un problema real del dominio educativo
- Las operaciones permiten interacción desde frontend
- Las métricas permiten demostrar comportamiento algorítmico
- El diseño permite crecimiento modular del backend y frontend

---

# Relación con el Frontend

Cada estructura deberá poder visualizarse gráficamente.

## Visualización esperada

| Estructura | Visualización |
|---|---|
| Árbol General | Jerarquía expandible |
| Árbol Binario | Diagrama de decisiones |
| AVL | Árbol balanceado con rotaciones |
| Árbol B/B+ | Nodos con múltiples claves |
| Hash | Tabla con buckets |
| Grafo | Nodos y aristas |
| Lista | Secuencia lineal |
| Pila | Bloques apilados |
| Cola | Fila horizontal |

---

# Relación con el Backend

Cada estructura deberá exponerse mediante endpoints REST.

## Operaciones mínimas comunes

- Crear elemento
- Buscar elemento
- Eliminar elemento
- Consultar estado actual
- Consultar métricas
- Consultar representación visual en JSON

---

# Conclusión

El mapeo formal de estructuras de datos para EduStruct establece una base sólida para la implementación técnica.

Cada estructura tiene una aplicación natural dentro del contexto educativo y permite demostrar conceptos fundamentales de Programación III mediante una aplicación visual, interactiva y justificable.
