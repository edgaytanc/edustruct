# Demo checklist — Épica 9 Tabla Hash

## Preparación

- [ ] Ejecutar backend Flask.
- [ ] Ejecutar frontend React.
- [ ] Abrir la pantalla de Tabla Hash desde Home.
- [ ] Confirmar que la visualización inicia vacía o con estado controlado.

## Demo recomendada

1. Cargar demo.
2. Mostrar buckets generados.
3. Identificar buckets con más de un elemento.
4. Explicar que esos elementos tienen colisión porque su hash cae en el mismo índice.
5. Buscar un carnet existente.
6. Mostrar el resultado encontrado y su bucket.
7. Buscar un carnet inexistente.
8. Insertar un nuevo estudiante.
9. Verificar si generó colisión.
10. Eliminar un carnet existente.
11. Confirmar que la cadena se reacomoda correctamente.
12. Revisar métricas actualizadas.

## Puntos técnicos a explicar

- La tabla usa lista de buckets.
- Cada bucket apunta a una cadena de `HashEntry`.
- La función hash transforma el carnet en índice.
- Una colisión ocurre cuando un bucket ya tiene elementos.
- El factor de carga es `size / capacity`.
- La búsqueda promedio es O(1), pero puede degradarse si hay muchas colisiones.

## Preguntas probables del catedrático

### ¿Usaron `dict`?

No. La estructura principal usa lista de buckets y nodos enlazados manuales.

### ¿Por qué encadenamiento?

Porque permite visualizar colisiones con claridad: varias claves viven en el mismo bucket mediante una cadena.

### ¿Qué pasa si dos carnets caen en el mismo índice?

Se agrega una nueva entrada a la cadena de ese bucket y se incrementa el contador de colisiones.

### ¿Qué representa el factor de carga?

Representa qué tan llena está la tabla respecto a su capacidad.

### ¿Por qué aplica al dominio educativo?

Porque el carnet estudiantil funciona como clave única para localizar expedientes o datos básicos del estudiante.

## Validación final de demo

- [ ] Colisiones visibles.
- [ ] Búsqueda por carnet funcional.
- [ ] Inserción funcional.
- [ ] Eliminación funcional.
- [ ] Métricas actualizadas.
- [ ] React Flow estable.
- [ ] Backend sin errores.
- [ ] Frontend construido correctamente.
