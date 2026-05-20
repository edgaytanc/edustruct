# Épica 9 — Step 1: Decisión técnica de estrategia de colisión para Tabla Hash

## Objetivo del step

Definir formalmente la estrategia de manejo de colisiones que se usará en la implementación de la Tabla Hash de EduStruct.

La estructura se aplicará al dominio educativo para búsqueda rápida de estudiantes por carnet, cumpliendo el requerimiento del proyecto de implementar una tabla hash real con manejo visible de colisiones.

---

## Archivos revisados como base

Antes de tomar la decisión se revisaron los documentos y datasets existentes del proyecto:

```text
docs/domain-model.md
docs/demo-dataset-design.md
docs/demo-dataset-contract.md
docs/data-structures-mapping.md
datasets/students.json
```

También se verificó la arquitectura ya utilizada en épicas anteriores:

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

La Tabla Hash tendrá como caso de uso principal la búsqueda de estudiantes por carnet.

Según el dominio actual:

- El estudiante tiene un `carnet` único.
- El carnet se maneja como cadena de texto.
- La tabla hash debe permitir insertar, buscar y eliminar estudiantes.
- La visualización debe mostrar buckets, claves, datos básicos del estudiante y colisiones.
- La implementación debe ser manual en Python puro.
- No se debe usar `dict` como almacenamiento principal.

Ejemplo de clave esperada:

```text
2024001
```

Ejemplo de valor esperado:

```json
{
  "carnet": "2024001",
  "name": "Ana López",
  "career_id": "CAR-001",
  "email": "ana.lopez@edustruct.edu",
  "status": "active"
}
```

---

## Alternativas evaluadas

Se evaluaron dos estrategias clásicas de manejo de colisiones:

1. Encadenamiento separado.
2. Sondeo lineal.

---

# Alternativa 1: Encadenamiento separado

## Descripción

Cada posición de la tabla representa un bucket. Si dos o más claves generan el mismo índice hash, los elementos se almacenan en una lista enlazada dentro de ese bucket.

Estructura conceptual:

```text
bucket[0] -> vacío
bucket[1] -> 2024001 -> 2024012 -> 2024023
bucket[2] -> 2024002
bucket[3] -> vacío
```

Modelo esperado:

```python
class HashEntry:
    key
    value
    next
```

```python
class HashTable:
    buckets
    size
    capacity
    collisions
```

## Ventajas

- Permite mostrar colisiones de forma directa y visual.
- Cada bucket puede representarse claramente en React Flow.
- La colisión se entiende como una cadena dentro del mismo índice.
- La eliminación es más simple que en sondeo abierto.
- No requiere manejar marcas especiales de borrado.
- Es más pedagógica para explicar en exposición oral.
- Evita comportamientos confusos como clustering primario.
- Mantiene separación clara entre índice hash y elementos colisionados.

## Desventajas

- Requiere implementar nodos enlazados adicionales.
- Cada bucket puede tener longitud variable.
- Si la función hash es mala, pueden crecer cadenas largas.

## Compatibilidad con EduStruct

Alta.

El proyecto ya usa visualizaciones por nodos y relaciones en React Flow. El encadenamiento permite representar cada bucket como un contenedor lógico y cada entrada como nodo conectado dentro de la misma fila o columna.

Esto facilita mostrar:

- índice del bucket;
- claves almacenadas;
- estudiantes asociados;
- colisiones resaltadas;
- longitud de cadena por bucket;
- factor de carga;
- conteo total de colisiones.

---

# Alternativa 2: Sondeo lineal

## Descripción

Cuando una clave genera un índice ocupado, la tabla busca la siguiente posición disponible de forma secuencial.

Estructura conceptual:

```text
hash(2024001) -> 1
bucket[1] ocupado
bucket[2] ocupado
bucket[3] disponible -> insertar
```

## Ventajas

- Usa un único arreglo de posiciones.
- No requiere nodos enlazados.
- Puede parecer más simple al inicio.
- Permite explicar direccionamiento abierto.

## Desventajas

- La colisión queda menos explícita visualmente porque el elemento termina en otro índice.
- Requiere diferenciar entre índice original e índice final.
- La eliminación necesita marcas especiales como `deleted` o `tombstone` para no romper búsquedas posteriores.
- Puede generar clustering primario.
- Es menos intuitiva para estudiantes al visualizar buckets.
- Requiere más reglas internas para explicar búsquedas después de eliminaciones.

## Compatibilidad con EduStruct

Media.

Aunque puede implementarse, su visualización exige explicar más conceptos auxiliares:

- posición hash original;
- posición final;
- recorrido de sondeo;
- celdas eliminadas lógicamente;
- celdas ocupadas por desplazamiento.

Esto aumenta complejidad sin aportar más claridad para el objetivo pedagógico de la épica.

---

## Comparación formal

| Criterio | Encadenamiento separado | Sondeo lineal |
|---|---|---|
| Simplicidad pedagógica | Alta | Media |
| Claridad visual de colisiones | Alta | Media |
| Facilidad de implementación | Alta | Media |
| Facilidad de eliminación | Alta | Media-baja |
| Compatibilidad con React Flow | Alta | Media |
| Riesgo de errores | Bajo | Medio |
| Mantenibilidad | Alta | Media |
| Explicación oral | Clara y directa | Requiere más detalles |
| Relación con búsqueda por carnet | Alta | Alta |
| Tiempo de desarrollo | Bajo | Medio |

---

## Decisión técnica

Se selecciona **encadenamiento separado** como estrategia oficial de manejo de colisiones para la Épica 9.

---

## Justificación de la decisión

El encadenamiento separado es la opción más adecuada para EduStruct porque prioriza claridad visual, simplicidad de explicación y mantenibilidad.

La Épica 9 no busca únicamente que la tabla hash funcione; busca que las colisiones sean visibles, defendibles y fáciles de explicar. En ese sentido, el encadenamiento permite mostrar directamente que varias claves comparten el mismo bucket.

Además, se integra mejor con el estilo visual ya usado en árboles y estructuras lineales: nodos conectados, relaciones explícitas y métricas visibles. No obliga a introducir marcas de borrado ni reglas adicionales de sondeo que podrían distraer del objetivo principal.

En resumen: para una exposición universitaria, el encadenamiento separado permite enseñar la colisión sin esconderla debajo de la alfombra algorítmica. Y eso, técnicamente, es lo que se necesita.

---

## Diseño aprobado para próximos steps

### Entrada hash

```python
class HashEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
```

### Tabla hash

```python
class HashTable:
    def __init__(self, capacity=7):
        self.capacity = capacity
        self.buckets = [None] * capacity
        self.size = 0
        self.collisions = 0
```

### Función hash propuesta

La función hash debe ser propia, determinística y explicable.

Propuesta inicial:

```text
sumatoria ponderada de caracteres del carnet módulo capacidad
```

Ejemplo conceptual:

```python
hash = sum((index + 1) * ord(character) for index, character in enumerate(key)) % capacity
```

Esta función es suficientemente clara para exposición y permite provocar colisiones controladas usando una capacidad pequeña en el dataset demo.

---

## Contrato visual esperado

La serialización visual deberá exponer buckets completos:

```json
{
  "bucket_index": 0,
  "items": [
    {
      "key": "2024001",
      "value": {
        "carnet": "2024001",
        "name": "Ana López",
        "career_id": "CAR-001"
      },
      "collision": false
    }
  ]
}
```

Para buckets con más de un elemento, los elementos posteriores deberán marcarse como colisión:

```json
{
  "bucket_index": 3,
  "items": [
    {
      "key": "2024002",
      "collision": false
    },
    {
      "key": "2024011",
      "collision": true
    }
  ]
}
```

---

## Métricas aprobadas

La estructura deberá exponer como mínimo:

```json
{
  "capacity": 7,
  "size": 5,
  "collisions": 2,
  "load_factor": 0.71
}
```

---

## Dataset demo esperado

Se creará posteriormente:

```text
datasets/hash_students.json
```

Este dataset deberá usar estudiantes del dominio educativo y carnets diseñados para provocar colisiones controladas.

La estrategia recomendada será usar una capacidad inicial pequeña, por ejemplo `7`, para que la función hash genere buckets compartidos de manera demostrable.

---

## Archivos que se crearán o modificarán en próximos steps

### Step 2

```text
backend/app/structures/hash_table.py
backend/tests/structures/test_hash_table.py
docs/epic-9-step-2-hash-core.md
```

### Step 3

```text
backend/app/services/hash_table_service.py
backend/app/serializers/react_flow_serializer.py
backend/tests/services/test_hash_table_service.py
backend/tests/serializers/test_react_flow_hash_table_serializer.py
docs/epic-9-step-3-hash-service-serializer.md
```

### Step 4

```text
backend/app/routes/hash_routes.py
backend/tests/routes/test_hash_table_routes.py
docs/epic-9-step-4-hash-routes.md
```

### Step 5

```text
frontend/src/api/hashTable.js
frontend/src/pages/HashPage.jsx
frontend/src/router/AppRouter.jsx
frontend/src/pages/HomePage.jsx
docs/epic-9-step-5-frontend-hash.md
```

---

## Validación del step

Este step no modifica lógica backend ni frontend. Solo agrega documentación técnica incremental.

Validación realizada:

- Se revisó el modelo de dominio.
- Se revisó el contrato de dataset.
- Se revisó el mapeo de estructuras.
- Se verificó que la Tabla Hash está definida para búsqueda por carnet.
- Se seleccionó formalmente encadenamiento separado.
- No se sobrescribió documentación previa.

---

## Workflow Git recomendado para este step

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-9-hash-table
```

Commit semántico recomendado:

```bash
git add docs/epic-9-step-1-hash-collision-strategy.md
git commit -m "feat(hash): define collision strategy"
```

---

## Estado del step

Step 1 queda técnicamente preparado para revisión.

No se debe avanzar al Step 2 hasta recibir validación explícita.
