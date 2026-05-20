# Épica 9 — Step 2: Core backend de Tabla Hash

## Objetivo del step

Implementar el núcleo de la Tabla Hash de EduStruct en Python puro, manteniendo la decisión formal del Step 1: manejo de colisiones mediante **encadenamiento separado**.

Este step se limita al core de estructura y sus pruebas unitarias. No incluye todavía servicios, serializadores visuales, endpoints REST ni frontend.

---

## Archivos creados

```text
backend/app/structures/hash_table.py
backend/tests/structures/test_hash_table.py
docs/epic-9-step-2-hash-core.md
```

---

## Diseño implementado

### HashEntry

Entrada enlazada usada dentro de cada bucket:

```python
class HashEntry:
    key
    value
    next
```

Cada entrada representa una clave de búsqueda, en este caso el carnet estudiantil, y un valor asociado con datos del estudiante.

### HashTable

Tabla hash manual:

```python
class HashTable:
    buckets
    size
    capacity
    collisions
```

El almacenamiento principal es una lista nativa de Python usada como arreglo de buckets. No se usa `dict` como estructura interna principal.

---

## Función hash

Se implementó una función hash propia, determinística y defendible en exposición:

```text
sumatoria(posición_del_caracter * código_ASCII_del_caracter) % capacidad
```

Ventajas:

- No depende del `hash()` interno de Python.
- Produce el mismo resultado en cada ejecución.
- Es simple de explicar.
- Funciona correctamente con carnets almacenados como texto.
- Permite provocar colisiones de forma controlada para la demo.

---

## Operaciones implementadas

### Inserción

```python
insert(key, value)
```

Comportamiento:

- Normaliza la clave como texto.
- Calcula el bucket con la función hash.
- Inserta directamente si el bucket está vacío.
- Si el bucket ya tiene entradas, recorre la cadena y agrega al final.
- Cuenta una colisión cuando una nueva clave entra en un bucket ocupado.
- Rechaza claves duplicadas con `DUPLICATE_KEY`.

### Búsqueda

```python
search(key)
```

Devuelve un `HashSearchResult` con:

- `found`
- `key`
- `bucket_index`
- `value`
- `comparisons`
- `chain_position`

Esto deja preparado el terreno para la visualización y métricas del Step 3.

### Eliminación

```python
delete(key)
```

Comportamiento:

- Busca la clave dentro del bucket correspondiente.
- Elimina correctamente si está al inicio, en medio o al final de la cadena.
- Conserva el resto de la cadena enlazada.
- Devuelve `True` si eliminó y `False` si la clave no existía.

### Limpieza

```python
clear()
```

Reinicia:

- buckets;
- tamaño;
- contador de colisiones;
- metadata de última operación.

---

## Métricas implementadas

La estructura ya calcula:

```text
size
capacity
collisions
load_factor
max_chain_length
collision_bucket_count
```

Estas métricas son necesarias para cumplir los criterios de aceptación de la épica.

---

## Serialización interna disponible

Aunque el serializer visual formal se implementará en el Step 3, el core ya expone snapshots JSON-friendly:

```python
buckets_snapshot()
to_dict()
```

Cada bucket incluye:

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
        "full_name": "Ana López"
      },
      "chainPosition": 0,
      "collision": false
    }
  ]
}
```

---

## Validaciones cubiertas por pruebas

Las pruebas unitarias validan:

- estado inicial de la tabla;
- capacidad configurable;
- rechazo de capacidad inválida;
- función hash determinística;
- rechazo de claves vacías;
- inserción sin colisión;
- rechazo de claves duplicadas;
- inserción con colisión real mediante encadenamiento;
- búsqueda exitosa;
- búsqueda fallida;
- eliminación de cabeza de cadena;
- eliminación de nodo intermedio/final;
- eliminación de clave inexistente;
- validación de índice de bucket;
- snapshots de buckets;
- serialización completa con `to_dict()`;
- reinicio con `clear()`.

---

## Validación ejecutada

Comando usado desde `backend`:

```bash
PYTHONPATH=. pytest tests/structures/test_hash_table.py
```

Resultado específico del step:

```text
17 passed
```

Validación backend completa adicional:

```bash
PYTHONPATH=. pytest
```

Resultado:

```text
319 passed
```

---

## Workflow Git sugerido para este step

```bash
git checkout develop
git pull origin develop
git checkout feature/epic-9-hash-table

git add backend/app/structures/hash_table.py \
        backend/tests/structures/test_hash_table.py \
        docs/epic-9-step-2-hash-core.md

git commit -m "feat(hash): implement hash table core"
```

---

## Estado del step

Step 2 completado y listo para revisión.

No se debe avanzar al Step 3 hasta recibir validación explícita.
