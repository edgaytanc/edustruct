# EduStruct — Modelo Conceptual del Dominio Educativo

## Objetivo del Dominio

EduStruct es un visualizador interactivo de estructuras de datos aplicado al contexto educativo universitario.

El sistema permitirá representar, consultar y manipular información académica utilizando estructuras de datos reales y justificables dentro de un entorno universitario.

---

# Caso de Uso Principal

## Visualizador interactivo de estructuras para gestión académica

El sistema permitirá:

- Administrar facultades, carreras, ciclos y cursos
- Representar pensum académicos
- Gestionar estudiantes y expedientes
- Simular prerrequisitos académicos
- Modelar turnos de asesoría
- Visualizar estructuras de datos gráficamente
- Ejecutar búsquedas, recorridos y operaciones sobre estructuras

---

# Entidades del Dominio

## Facultad

Representa una unidad académica principal dentro de la universidad.

### Ejemplo
- Facultad de Ingeniería

### Relaciones
- Una facultad tiene múltiples carreras

---

## Carrera

Representa un programa académico.

### Ejemplo
- Ingeniería en Sistemas

### Relaciones
- Pertenece a una facultad
- Contiene múltiples ciclos
- Define un pensum académico

---

## Ciclo

Representa una etapa académica dentro de una carrera.

### Ejemplo
- Primer Ciclo
- Segundo Ciclo

### Relaciones
- Pertenece a una carrera
- Contiene múltiples cursos

---

## Curso

Representa una asignatura del pensum.

### Ejemplo
- Programación III

### Relaciones
- Pertenece a un ciclo
- Puede tener cero o más prerrequisitos
- Puede tener estudiantes inscritos

---

## Estudiante

Representa un alumno registrado en el sistema.

### Atributos clave
- carnet (único)

### Relaciones
- Tiene un expediente
- Puede estar inscrito en múltiples cursos

---

## Expediente

Representa el historial académico del estudiante.

### Contenido
- Cursos aprobados
- Cursos reprobados
- Promedio académico
- Historial de acciones

### Relaciones
- Pertenece a un estudiante
- Se consulta mediante ID

---

## Prerrequisito

Representa la dependencia académica entre cursos.

### Ejemplo
- Programación II → Programación III

### Relaciones
- Un curso puede depender de varios cursos
- Un curso puede habilitar otros cursos

---

## Turno de Asesoría

Representa una solicitud de atención académica.

### Ejemplo
- Solicitud de revisión de prerrequisitos
- Solicitud de inscripción

### Relaciones
- Pertenece a un estudiante
- Se atiende por orden de llegada

---

# Reglas de Negocio

## Regla 1
Un curso puede tener cero o más prerrequisitos.

---

## Regla 2
Un estudiante tiene un carnet único.

---

## Regla 3
Un expediente se consulta por ID.

---

## Regla 4
Todo curso pertenece a una jerarquía académica:

Facultad → Carrera → Ciclo → Curso

---

## Regla 5
Un estudiante únicamente puede asignarse un curso si cumple los prerrequisitos.

---

## Regla 6
Los turnos de asesoría se atienden utilizando FIFO.

---

## Regla 7
El historial académico debe conservar el orden cronológico reciente.

---

# Relación del Dominio con Estructuras de Datos

| Estructura | Aplicación en EduStruct |
|---|---|
| Árbol General | Jerarquía académica del pensum |
| Árbol Binario | Decisiones académicas |
| AVL | Índice balanceado de estudiantes o cursos |
| Árbol B/B+ | Índice de expedientes |
| Tabla Hash | Búsqueda rápida por carnet |
| Grafo | Mapa de prerrequisitos |
| Lista | Estudiantes inscritos |
| Pila | Historial académico |
| Cola | Turnos de asesoría |

---

# Modelo Conceptual de Relaciones

Facultad
└── Carrera
    └── Ciclo
        └── Curso
            ├── Prerrequisitos
            └── Estudiantes

Estudiante
└── Expediente

Turnos
└── Cola de atención

---

# Conclusión

El dominio educativo de EduStruct está diseñado para justificar el uso real de estructuras de datos dentro de un contexto universitario.

Cada estructura tendrá una función concreta dentro del sistema y permitirá demostrar operaciones, recorridos, búsquedas y visualizaciones interactivas alineadas a los objetivos del curso.
