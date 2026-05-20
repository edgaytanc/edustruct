# Épica 9 — Step 3: Service + serializer de Tabla Hash

## Objetivo

Integrar la estructura pura `HashTable` con la capa de aplicación y con el contrato visual de React Flow, sin acoplar la estructura a Flask ni a componentes de frontend.

## Archivos creados o modificados

```text
backend/app/services/hash_table_service.py
backend/app/serializers/react_flow_serializer.py
backend/tests/services/test_hash_table_service.py
backend/tests/serializers/test_react_flow_hash_table_serializer.py
docs/epic-9-step-3-hash-service-serializer.md
```

## Decisión aplicada

Se mantiene la estrategia definida en el Step 1: **encadenamiento separado**.

La capa de servicio no usa `dict` como almacenamiento principal de la tabla. El almacenamiento real sigue estando en:

```text
backend/app/structures/hash_table.py
```

El service únicamente coordina casos de uso y arma respuestas JSON-friendly.

## Service implementado

Archivo:

```text
backend/app/services/hash_table_service.py
```

Clase principal:

```python
HashTableService
```

Operaciones expuestas:

- `state()`
- `configure(capacity)`
- `insert(key, value)`
- `bulk_insert(entries)`
- `search(key)`
- `delete(key)`
- `metrics()`
- `load_demo()`
- `reset()`

## Validaciones

El service valida:

- capacidad entera
- capacidad mínima de 3
- clave obligatoria
- clave no vacía
- valor obligatorio
- payload de inserción múltiple como lista
- entradas bulk con formato de objeto
- clave duplicada
- eliminación sobre tabla vacía
- eliminación de clave inexistente

Errores usados:

- `ValidationError`
- `DuplicateKeyError`
- `NotFoundError`
- `StructureEmptyError`

## Métricas expuestas

El resultado del service incluye:

- `count`
- `collisions`
- `capacity`
- `loadFactor`
- `maxChainLength`
- `collisionBucketCount`
- `emptyBucketCount`
- `edgesCount`

Se conservan campos compatibles con métricas existentes:

- `height: None`
- `balanceFactor: None`
- `levels: None`

Esto evita romper la forma general usada por árboles, AVL y Árbol B.

## Serializer visual

Archivo modificado:

```text
backend/app/serializers/react_flow_serializer.py
```

Función agregada:

```python
serialize_hash_table(buckets, metrics=None, last_operation=None)
```

El serializer genera:

- nodos de bucket
- nodos de entrada hash
- aristas bucket → primer elemento
- aristas elemento → siguiente elemento
- categorías visuales para colisiones
- metadata de bucket, clave, valor y posición en cadena
- resaltado para la última operación

## Categorías visuales

Buckets:

- `bucket-empty`
- `bucket`
- `bucket-collision`

Entradas:

- `entry`
- `collision`
- `highlighted-entry`
- `highlighted-collision`

## Contrato visual simplificado

Ejemplo de bucket serializado:

```json
{
  "bucketIndex": 0,
  "size": 2,
  "hasCollision": true,
  "items": [
    {
      "key": "2024001",
      "value": {
        "student_id": "STU-001",
        "full_name": "Andrea Morales"
      },
      "chainPosition": 0,
      "collision": false
    },
    {
      "key": "2024010",
      "value": {
        "student_id": "STU-010",
        "full_name": "Luis Hernández"
      },
      "chainPosition": 1,
      "collision": true
    }
  ]
}
```

## Demo incluida en service

`load_demo()` carga carnets de estudiantes diseñados para provocar colisiones controladas con capacidad pequeña.

Contexto educativo:

```text
Tabla hash para búsqueda de estudiantes por carnet universitario
```

## Testing agregado

Pruebas de service:

```text
backend/tests/services/test_hash_table_service.py
```

Validan:

- estado inicial
- configuración de capacidad
- inserción
- inserción con colisión
- duplicados
- validaciones de clave y valor
- inserción múltiple
- búsqueda encontrada/no encontrada
- eliminación
- tabla vacía
- demo con colisiones
- reset

Pruebas de serializer:

```text
backend/tests/serializers/test_react_flow_hash_table_serializer.py
```

Validan:

- buckets vacíos
- cadenas con colisiones
- aristas `head` y `next`
- categorías visuales
- resaltado de última operación
- etiquetas con valores simples y objetos de estudiante

## Validación ejecutada

```bash
PYTHONPATH=. pytest
```

Resultado esperado:

```text
All tests passed
```

## Workflow Git del Step 3

```bash
git add backend/app/services/hash_table_service.py \
        backend/app/serializers/react_flow_serializer.py \
        backend/tests/services/test_hash_table_service.py \
        backend/tests/serializers/test_react_flow_hash_table_serializer.py \
        docs/epic-9-step-3-hash-service-serializer.md

git commit -m "feat(hash): add hash table service and serializer"
```

## Estado

Step 3 cerrado técnicamente. No se avanzó a rutas REST ni frontend. Eso corresponde al Step 4 y Step 5 respectivamente.
