# EduStruct — Checklist demo Épica 8: Árbol B

## Objetivo de la demo

Demostrar que el Árbol B funciona como índice académico eficiente para expedientes universitarios.

## Preparación

1. Levantar backend Flask.
2. Levantar frontend React.
3. Abrir el módulo **Árbol B** desde la pantalla principal.
4. Confirmar que el panel de métricas inicia sin errores.

## Flujo recomendado para exposición

### 1. Explicar decisión técnica

Indicar que se eligió **Árbol B** sobre Árbol B+ porque:

- Es más simple para exposición universitaria.
- Permite visualizar claves internas y hojas en una misma estructura.
- Reduce complejidad frente a punteros entre hojas del B+.
- Cumple el requerimiento formal del curso.
- Encaja mejor con React Flow para nodos multi-clave.

### 2. Configurar orden

Usar orden `4` para que los splits sean visibles rápidamente.

Explicación:

- Orden 4 significa máximo 3 claves por nodo.
- Al insertar una cuarta clave en un nodo, ocurre split.

### 3. Insertar claves manualmente

Secuencia sugerida:

```text
2024008, 2024016, 2024024, 2024032, 2024040
```

Puntos a explicar:

- Las claves se mantienen ordenadas dentro de cada nodo.
- El árbol crece balanceado.
- Los nodos pueden tener múltiples claves.
- Los splits promueven una clave al padre.

### 4. Cargar demo

Usar la opción de demo para cargar expedientes académicos.

Dataset interno usado:

```text
2024008, 2024016, 2024024, 2024032, 2024040, 2024048, 2024056, 2024064, 2024072, 2024080, 2024088
```

Puntos a explicar:

- Simula un índice por número de expediente/carnet.
- Permite búsquedas eficientes sin recorrer todos los expedientes.
- La altura se mantiene baja aunque aumenten las claves.

### 5. Buscar expediente

Buscar una clave existente, por ejemplo:

```text
2024048
```

Luego buscar una inexistente:

```text
2024999
```

Puntos a explicar:

- La búsqueda compara contra rangos de claves.
- Baja solo por el hijo correspondiente.
- La ruta de búsqueda queda expuesta en la respuesta del backend.

### 6. Mostrar métricas

Métricas importantes:

- Altura.
- Niveles.
- Cantidad de claves.
- Cantidad de nodos.
- Cantidad de hojas.
- Cantidad de splits.
- Validez de invariantes.

### 7. Mostrar splits

Explicar que un split ocurre cuando un nodo excede su capacidad máxima.

Para orden 4:

```text
Máximo de claves por nodo = 3
```

Cuando se supera ese límite:

1. Se divide el nodo.
2. La clave media sube al padre.
3. Las claves menores quedan a la izquierda.
4. Las claves mayores quedan a la derecha.
5. Todas las hojas se mantienen al mismo nivel.

## Frase técnica para defensa

El Árbol B implementado simula un índice académico porque permite localizar expedientes por clave manteniendo una altura baja, nodos con múltiples claves y crecimiento balanceado mediante splits controlados. Esto reduce el número de comparaciones frente a una búsqueda lineal y representa de forma visual cómo funcionan índices de bases de datos.

## Validación esperada antes de presentar

Backend:

```bash
cd backend
PYTHONPATH=. pytest
```

Resultado esperado:

```text
297 passed
```

Frontend:

```bash
cd frontend
npm run build
```

Resultado esperado:

```text
✓ built successfully
```
