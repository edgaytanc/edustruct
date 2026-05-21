# Épica 12 — Integración visual unificada de estructuras lineales

## Objetivo

Crear una interfaz frontend unificada para demostrar visualmente las estructuras lineales ya integradas al dominio académico en la Épica 11:

- Lista enlazada: estudiantes inscritos por curso.
- Cola FIFO: turnos de asesoría académica.
- Pila LIFO: historial de navegación académica.

Esta épica no reimplementa estructuras de datos en frontend. La lógica principal permanece en Flask y en las estructuras manuales del backend.

## Archivos agregados o modificados

- `frontend/src/api/linearStructures.js`
- `frontend/src/pages/LinearStructuresPage.jsx`
- `frontend/src/router/AppRouter.jsx`
- `frontend/src/components/layout/MainLayout.jsx`
- `frontend/src/pages/HomePage.jsx`
- `docs/epic-12-linear-structures-frontend.md`

## Endpoints consumidos

### Lista

- `GET /api/list/courses`
- `POST /api/list/demo/load-course`
- `GET /api/list/traverse`

### Cola

- `GET /api/queue/advisory-turns`
- `POST /api/queue/demo/load-advisory`
- `GET /api/queue/front`
- `DELETE /api/queue/delete`
- `GET /api/queue/traverse`

### Pila

- `POST /api/stack/demo/load-history`
- `POST /api/stack/navigation/push`
- `DELETE /api/stack/navigation/back`
- `GET /api/stack/peek`
- `GET /api/stack/traverse`

## Decisiones UI

Se creó una sola página en `/linear-structures` con tabs para evitar tres pantallas aisladas. Esta decisión mantiene la exposición compacta y permite comparar directamente las tres estructuras lineales.

La página usa React Flow para mostrar nodos y aristas serializados por el backend. La normalización visual del frontend solo cambia presentación: bordes, etiquetas, marcadores y resaltado de recorrido. No altera el estado de la estructura.

El menú principal se agregó al layout global para facilitar la navegación entre estructuras. En `HomePage.jsx` solo se agregó una tarjeta nueva, respetando el estilo visual existente.

## Explicación de cada estructura

### Lista de inscritos

Representa estudiantes reales inscritos en un curso. El usuario selecciona un curso desde el catálogo expuesto por backend y carga sus inscritos como lista enlazada. La visualización muestra el recorrido desde `HEAD` hasta `TAIL`.

Métricas visibles:

- cantidad
- aristas
- head
- tail

### Cola de asesoría

Representa turnos de atención académica. El primer estudiante cargado queda al frente de la cola y será atendido primero. Se permite consultar `front`, ejecutar `dequeue` y visualizar el recorrido FIFO.

Métricas visibles:

- cantidad
- aristas
- front
- rear

### Pila académica

Representa historial de navegación dentro del sistema académico. El último módulo visitado queda en `TOP`. Se permite cargar historial demo, agregar una navegación, volver atrás y consultar el elemento superior.

Métricas visibles:

- cantidad
- aristas
- top
- política LIFO

## Flujo de usuario

1. Entrar a `/linear-structures` desde el menú o desde la tarjeta del Home.
2. Seleccionar una pestaña: Lista, Cola o Pila.
3. Ejecutar la carga demo correspondiente.
4. Revisar métricas y visualización React Flow.
5. Ejecutar operaciones demostrables:
   - Lista: cargar inscritos y ver recorrido.
   - Cola: consultar front, atender/dequeue y ver recorrido.
   - Pila: cargar historial, agregar navegación, volver atrás, consultar top y ver recorrido.

## Validaciones realizadas

- Se revisaron los archivos actuales antes de modificar:
  - `frontend/src/router/AppRouter.jsx`
  - `frontend/src/components/layout/MainLayout.jsx`
  - `frontend/src/pages/HomePage.jsx`
  - APIs frontend existentes
  - rutas y servicios backend de lista, cola y pila
- Se mantuvo el patrón de APIs basado en Axios.
- Se mantuvo React Flow y Tailwind.
- Se consumieron contratos existentes de Épica 11.
- Se ejecutó `npm run build` en frontend.

## Limitaciones

- La visualización depende del estado en memoria del backend, por lo que al reiniciar el servidor se debe cargar nuevamente la demo.
- La página no crea datos académicos inventados; usa únicamente lo que expone el backend o entradas manuales para simular navegación en pila.

## Cierre Git sugerido

Al iniciar la épica:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-12-linear-structures-frontend
```

Al finalizar:

```bash
git checkout develop
git pull origin develop
git merge --no-ff feature/epic-12-linear-structures-frontend
git push origin develop
```

Eliminar rama temporal:

```bash
git branch -d feature/epic-12-linear-structures-frontend
git push origin --delete feature/epic-12-linear-structures-frontend
```
