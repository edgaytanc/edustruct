# Épica 9 — Resumen técnico

## Objetivo

Implementar una tabla hash real con manejo de colisiones para búsqueda eficiente de estudiantes por carnet.

## Decisión técnica

Se eligió **encadenamiento separado** sobre sondeo lineal porque permite explicar visualmente las colisiones como cadenas dentro de buckets. Esta estrategia es más clara para React Flow, más defendible en exposición y más mantenible para el alcance académico del proyecto.

## Implementación

La tabla hash fue implementada manualmente en Python puro mediante:

- lista nativa de buckets;
- nodos `HashEntry` enlazados;
- función hash propia;
- inserción, búsqueda y eliminación;
- conteo de colisiones;
- cálculo de factor de carga;
- exportación serializable por buckets.

No se usa `dict` como almacenamiento principal.

## Integración backend

Se agregó un servicio de aplicación que mantiene separada la lógica de negocio del transporte HTTP. El servicio permite:

- consultar estado;
- configurar capacidad inicial;
- insertar estudiantes por carnet;
- buscar estudiantes por carnet;
- eliminar estudiantes por carnet;
- cargar demo;
- reiniciar la estructura;
- exponer métricas.

## Integración visual

Se extendió el serializer React Flow con `serialize_hash_table`, representando:

- bucket index;
- nodos bucket;
- entradas encadenadas;
- aristas bucket → entrada;
- aristas entry → next;
- metadata de colisión;
- posición en cadena.

## Integración frontend

Se creó una pantalla de tabla hash con:

- controles de insertar, buscar y eliminar;
- carga demo;
- reset;
- configuración de capacidad;
- visualización React Flow;
- panel de buckets;
- métricas visibles;
- resaltado de colisiones.

## Métricas expuestas

- tamaño de tabla;
- capacidad;
- buckets usados;
- buckets con colisiones;
- colisiones totales;
- factor de carga;
- cadena máxima;
- cantidad de aristas visuales.

## Valor para exposición

La épica permite demostrar de forma clara:

- cómo una clave se transforma en índice;
- por qué ocurren colisiones;
- cómo se resuelven con encadenamiento;
- cómo se afecta el factor de carga;
- por qué la búsqueda por carnet encaja naturalmente con tablas hash.
