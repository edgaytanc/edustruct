# EduStruct — Diseño del Dataset Demo

## Objetivo

Definir un dataset académico coherente, escalable y reutilizable para alimentar todas las estructuras de datos de EduStruct.

El dataset permitirá:

- Simular un entorno universitario real
- Alimentar estructuras de datos
- Ejecutar búsquedas
- Visualizar recorridos
- Validar relaciones académicas
- Mostrar métricas
- Ejecutar pruebas funcionales

---

# Principios del Dataset

## Consistencia

Todas las entidades deben estar relacionadas correctamente.

---

## Escalabilidad

El dataset debe permitir agregar nuevas carreras, cursos y estudiantes sin romper relaciones existentes.

---

## Reutilización

El mismo dataset debe servir para:

- Árboles
- Grafos
- AVL
- Hash
- Listas
- Pilas
- Colas

---

## Claridad

Los nombres y relaciones deben ser comprensibles y fáciles de visualizar.

---

# Estructura General del Dataset

## Jerarquía Académica

Universidad
└── Facultad
    └── Carrera
        └── Ciclo
            └── Curso

---

# 1. Facultades

## Facultad de Ingeniería

### ID
FAC-001

### Carreras asociadas
- Ingeniería en Sistemas
- Ingeniería Industrial

---

## Facultad de Ciencias Económicas

### ID
FAC-002

### Carreras asociadas
- Administración de Empresas
- Contaduría Pública

---

# 2. Carreras

## Ingeniería en Sistemas

### ID
CAR-001

### Facultad
FAC-001

### Ciclos
- Primer Ciclo
- Segundo Ciclo
- Tercer Ciclo

---

## Ingeniería Industrial

### ID
CAR-002

### Facultad
FAC-001

---

## Administración de Empresas

### ID
CAR-003

### Facultad
FAC-002

---

# 3. Ciclos

## Primer Ciclo

### ID
CIC-001

---

## Segundo Ciclo

### ID
CIC-002

---

## Tercer Ciclo

### ID
CIC-003

---

# 4. Cursos

# Primer Ciclo

| ID | Curso |
|---|---|
| CUR-001 | Introducción a la Programación |
| CUR-002 | Matemática I |
| CUR-003 | Lógica de Sistemas |
| CUR-004 | Técnicas de Estudio |

---

# Segundo Ciclo

| ID | Curso |
|---|---|
| CUR-005 | Programación I |
| CUR-006 | Matemática II |
| CUR-007 | Arquitectura de Computadoras |
| CUR-008 | Estadística I |

---

# Tercer Ciclo

| ID | Curso |
|---|---|
| CUR-009 | Programación II |
| CUR-010 | Estructuras de Datos |
| CUR-011 | Bases de Datos |
| CUR-012 | Física I |

---

# Cursos Avanzados

| ID | Curso |
|---|---|
| CUR-013 | Programación III |
| CUR-014 | Algoritmos |
| CUR-015 | Sistemas Operativos |
| CUR-016 | Inteligencia Artificial |

---

# 5. Relaciones de Prerrequisitos

| Curso | Requiere |
|---|---|
| Programación I | Introducción a la Programación |
| Programación II | Programación I |
| Programación III | Programación II |
| Estructuras de Datos | Programación II |
| Algoritmos | Estructuras de Datos |
| Inteligencia Artificial | Algoritmos |
| Bases de Datos | Programación I |
| Sistemas Operativos | Arquitectura de Computadoras |

---

# Representación del Grafo

Introducción a la Programación
    ↓
Programación I
    ↓
Programación II
    ↓
Programación III
    ↓
Estructuras de Datos
    ↓
Algoritmos
    ↓
Inteligencia Artificial

---

# 6. Estudiantes

| Carnet | Nombre |
|---|---|
| 2024001 | Ana López |
| 2024002 | Carlos Pérez |
| 2024003 | María García |
| 2024004 | Luis Ramírez |
| 2024005 | Sofía Hernández |
| 2024006 | Diego Morales |
| 2024007 | Andrea Castillo |
| 2024008 | José Méndez |

---

# 7. Expedientes

| ID Expediente | Carnet | Estado |
|---|---|---|
| EXP-1001 | 2024001 | Activo |
| EXP-1002 | 2024002 | Activo |
| EXP-1003 | 2024003 | Activo |
| EXP-1004 | 2024004 | Suspendido |
| EXP-1005 | 2024005 | Activo |

---

# Información Académica del Expediente

Cada expediente contendrá:

- Cursos aprobados
- Cursos reprobados
- Promedio académico
- Historial de inscripciones
- Historial de acciones

---

# 8. Inscripciones

## Curso: Programación III

### Estudiantes inscritos
- Ana López
- Carlos Pérez
- María García

---

## Curso: Estructuras de Datos

### Estudiantes inscritos
- Luis Ramírez
- Sofía Hernández

---

# 9. Historial Académico

## Ejemplo de historial

Pila de acciones:

1. Inscripción realizada
2. Curso agregado
3. Expediente consultado
4. Prerrequisito validado

La última acción registrada será la primera en salir.

---

# 10. Turnos de Asesoría

## Cola de atención

| Posición | Estudiante | Motivo |
|---|---|---|
| 1 | Ana López | Asignación de curso |
| 2 | Carlos Pérez | Validación de prerrequisitos |
| 3 | María García | Consulta de expediente |
| 4 | Luis Ramírez | Cambio de carrera |

---

# Volumen Inicial del Dataset

| Entidad | Cantidad Aproximada |
|---|---|
| Facultades | 2 |
| Carreras | 4 |
| Ciclos | 3 |
| Cursos | 16 |
| Estudiantes | 8 |
| Expedientes | 5 |
| Relaciones de prerrequisitos | 8 |
| Turnos | 4 |

---

# Relación con las Estructuras

| Estructura | Datos utilizados |
|---|---|
| Árbol General | Facultad → Carrera → Ciclo → Curso |
| Árbol Binario | Reglas de asignación |
| AVL | IDs de estudiantes y cursos |
| Árbol B/B+ | Expedientes |
| Tabla Hash | Carnets |
| Grafo | Prerrequisitos |
| Lista | Inscritos |
| Pila | Historial |
| Cola | Turnos |

---

# Reglas de Integridad

## Regla 1
No puede existir un carnet duplicado.

---

## Regla 2
Todo expediente debe pertenecer a un estudiante existente.

---

## Regla 3
Todo curso debe pertenecer a un ciclo.

---

## Regla 4
Un prerrequisito únicamente puede apuntar a cursos existentes.

---

## Regla 5
No puede existir un ciclo sin carrera asociada.

---

# Futuras Extensiones

El dataset permitirá crecer hacia:

- Más facultades
- Más estudiantes
- Más carreras
- Horarios
- Docentes
- Secciones
- Salones
- Calificaciones
- Créditos académicos

---

# Conclusión

El dataset demo de EduStruct proporciona una base sólida y coherente para implementar todas las estructuras de datos del proyecto.

La información está diseñada para permitir visualizaciones, recorridos, búsquedas, métricas y simulaciones dentro de un entorno educativo realista.
