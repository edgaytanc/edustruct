# EduStruct — Resumen de Épica 2

## Épica 2

Definición formal del dominio educativo y modelo funcional.

---

# Objetivo de la Épica

Definir el dominio educativo de EduStruct y establecer la relación formal entre las estructuras de datos y el contexto académico universitario.

La finalidad de esta épica fue construir una base sólida antes de iniciar implementación técnica en backend y frontend.

---

# Estado General

## Resultado

Épica completada correctamente.

## Estado

VALIDADA

## Impacto

La Épica 2 establece:

- El dominio educativo oficial del proyecto
- Las entidades académicas principales
- Las reglas de negocio
- El mapeo formal de estructuras de datos
- El modelo funcional del sistema
- El diseño y contrato del dataset demo
- Los archivos JSON iniciales del proyecto

---

# Documentos Generados

## 1. Modelo Conceptual del Dominio

Ruta:

```text
/docs/domain-model.md
```

Contenido principal:

- Caso de uso
- Entidades
- Relaciones
- Reglas de negocio
- Relación con estructuras

---

## 2. Mapeo Formal de Estructuras

Ruta:

```text
/docs/data-structures-mapping.md
```

Contenido principal:

- Aplicación real de cada estructura
- Operaciones esperadas
- Justificación técnica
- Métricas visuales
- Relación con frontend y backend

---

## 3. Diseño del Dataset Demo

Ruta:

```text
/docs/demo-dataset-design.md
```

Contenido principal:

- Facultades
- Carreras
- Ciclos
- Cursos
- Estudiantes
- Expedientes
- Relaciones académicas
- Turnos y acciones demo

---

## 4. Modelo Funcional

Ruta:

```text
/docs/functional-model.md
```

Contenido principal:

- Módulos del sistema
- Entradas y salidas
- Operaciones por estructura
- Contratos JSON conceptuales
- Responsabilidades frontend/backend

---

## 5. Contrato del Dataset

Ruta:

```text
/docs/demo-dataset-contract.md
```

Contenido principal:

- Estructura formal de archivos JSON
- Validaciones
- Integridad referencial
- Convenciones de IDs
- Orden de carga

---

# Archivos de Dataset Generados

Ubicación:

```text
/datasets
```

Archivos creados:

- faculties.json
- careers.json
- cycles.json
- courses.json
- students.json
- records.json
- prerequisites.json
- enrollments.json
- advisory_turns.json
- academic_history.json

---

# Dominio Educativo Definido

EduStruct fue formalmente definido como:

## Visualizador interactivo de estructuras de datos aplicado a gestión académica universitaria.

---

# Entidades Oficiales del Sistema

| Entidad | Descripción |
|---|---|
| Facultad | Unidad académica principal |
| Carrera | Programa académico |
| Ciclo | Nivel académico |
| Curso | Asignatura del pensum |
| Estudiante | Alumno registrado |
| Expediente | Historial académico |
| Prerrequisito | Dependencia entre cursos |
| Turno de asesoría | Solicitud de atención |

---

# Reglas de Negocio Definidas

## Regla 1

Un curso puede tener cero o más prerrequisitos.

## Regla 2

Todo estudiante tiene carnet único.

## Regla 3

Todo expediente se consulta mediante ID.

## Regla 4

Todo curso pertenece a una jerarquía académica.

## Regla 5

Los turnos se atienden en orden FIFO.

## Regla 6

Un estudiante no puede asignarse cursos sin cumplir prerrequisitos.

---

# Mapeo Oficial de Estructuras

| Estructura | Aplicación |
|---|---|
| Árbol General | Pensum académico |
| Árbol Binario | Decisiones académicas |
| AVL | Índice por ID |
| Árbol B/B+ | Expedientes |
| Tabla Hash | Búsqueda por carnet |
| Grafo | Prerrequisitos |
| Lista | Inscripciones |
| Pila | Historial |
| Cola | Turnos |

---

# Dataset Demo Validado

## Volumen inicial

| Entidad | Cantidad |
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

# Integridad del Dataset

El dataset cumple:

- IDs consistentes
- Relaciones válidas
- Carnets únicos
- Dependencias académicas reales
- Compatibilidad con estructuras de datos

---

# Responsabilidades Arquitectónicas Definidas

## Backend

Responsable de:

- Implementar estructuras desde cero
- Exponer API REST
- Calcular métricas
- Validar reglas de negocio
- Serializar estructuras

## Frontend

Responsable de:

- Visualización gráfica
- Animaciones
- Interacción del usuario
- Consumo de API
- Métricas visuales

---

# Criterios de Aceptación Cumplidos

## Cumplido

✔ Dominio educativo definido formalmente

✔ Relación coherente entre estructuras y problema real

✔ Dataset académico consistente

✔ Contratos de datos documentados

✔ JSON reales creados

✔ Base preparada para implementación técnica

✔ Arquitectura alineada a frontend/backend desacoplados

---

# Riesgos Eliminados

La Épica 2 elimina riesgos importantes:

- Estructuras sin propósito
- Datos inconsistentes
- APIs improvisadas
- Visualizaciones incoherentes
- Relaciones académicas ambiguas
- Modelos rotos entre frontend y backend

---

# Recomendación para la Épica 3

## Próximo paso recomendado

Iniciar implementación técnica de estructuras de datos en backend.

---

# Orden recomendado para Épica 3

## Fase 1

Crear módulo base de estructuras.

Propuesta:

```text
/backend/app/structures
```

---

## Fase 2

Implementar estructuras lineales:

- Lista
- Pila
- Cola

Estas son ideales para validar arquitectura y serialización.

---

## Fase 3

Implementar estructuras jerárquicas:

- Árbol general
- Árbol binario
- AVL

---

## Fase 4

Implementar estructuras avanzadas:

- Árbol B/B+
- Tabla hash
- Grafo

---

## Fase 5

Crear endpoints REST para cada estructura.

---

## Fase 6

Conectar frontend con visualizaciones reales.

---

# Estado Final de la Épica

## Resultado general

Épica 2 finalizada exitosamente.

## Base del sistema

ESTABLE

## Preparado para

Implementación técnica completa de estructuras de datos y visualización interactiva.

---

# Conclusión

La Épica 2 permitió transformar EduStruct de una idea conceptual a una especificación técnica y funcional sólida.

El proyecto ya cuenta con:

- Dominio formal
- Modelo funcional
- Contrato de datos
- Dataset inicial
- Relación clara entre estructuras y contexto educativo

Esto permite avanzar hacia implementación técnica con mucho menor riesgo y mayor coherencia arquitectónica.
