# Épica 8 — Step 1: Decisión técnica Árbol B vs Árbol B+

## 1. Objetivo del step

Definir formalmente si EduStruct implementará un **Árbol B** o un **Árbol B+** para simular un índice académico eficiente de expedientes universitarios.

Este documento cierra la decisión técnica previa a la implementación de la Épica 8 y debe validarse antes de avanzar al core backend.

---

## 2. Contexto del proyecto

EduStruct es un visualizador interactivo de estructuras de datos aplicado al contexto educativo universitario.

La arquitectura vigente del proyecto es:

```text
React + React Flow → API REST Flask → Estructuras en Python puro
```

La Épica 8 debe representar un índice académico para expedientes universitarios, demostrando:

- búsquedas eficientes;
- múltiples claves por nodo;
- divisiones de nodos o `splits`;
- crecimiento balanceado;
- visualización clara en React Flow;
- métricas como altura y niveles.

---

## 3. Requerimiento formal del curso

El proyecto final exige implementar un **Árbol B o B+** como una de las estructuras de datos obligatorias.

Dentro del contexto educativo de EduStruct, esta estructura se utilizará para simular un índice de búsqueda de expedientes académicos, donde cada clave representa un identificador de expediente.

Ejemplo de claves:

```text
1001, 1002, 1003, 1004, 1005
```

Estas claves representan expedientes universitarios indexados para búsqueda eficiente.

---

## 4. Alternativa 1: Árbol B

Un Árbol B es una estructura de búsqueda balanceada donde cada nodo puede almacenar múltiples claves y múltiples hijos.

### Características principales

- Las claves pueden estar en nodos internos y hojas.
- Todos los nodos hoja quedan al mismo nivel.
- Cada nodo puede contener varias claves ordenadas.
- Las búsquedas pueden terminar en un nodo interno o en una hoja.
- Las inserciones pueden provocar `splits` cuando un nodo excede la capacidad permitida.

### Ventajas para EduStruct

- Es más directo de explicar en una exposición universitaria.
- La estructura visual es más simple que un B+.
- Permite representar múltiples claves por nodo sin añadir enlaces horizontales entre hojas.
- Los `splits` son fáciles de visualizar en React Flow.
- Encaja bien con la arquitectura existente de serializadores de árboles.
- Requiere menos complejidad accidental en frontend.
- Facilita pruebas unitarias de invariantes.

### Desventajas

- No representa tan fielmente los índices modernos de bases de datos como un B+.
- Los recorridos ordenados no son tan naturales como en B+, donde las hojas suelen estar enlazadas.

---

## 5. Alternativa 2: Árbol B+

Un Árbol B+ es una variante del Árbol B donde los datos reales se almacenan normalmente en las hojas y los nodos internos funcionan como índices.

### Características principales

- Los nodos internos contienen claves guía.
- Los registros completos viven en las hojas.
- Las hojas suelen estar enlazadas para recorridos secuenciales.
- Todas las búsquedas reales terminan en hojas.
- Es común en índices de bases de datos y sistemas de archivos.

### Ventajas para EduStruct

- Se parece más a un índice real de base de datos.
- Permite explicar búsquedas por rango de forma más natural.
- Las hojas enlazadas permiten recorridos secuenciales eficientes.

### Desventajas

- Requiere más reglas para explicar correctamente.
- La serialización visual es más compleja.
- React Flow tendría que representar enlaces verticales del árbol y enlaces horizontales entre hojas.
- Aumenta la carga de testing.
- Puede consumir más tiempo de implementación sin aportar mucho más al criterio formal del curso.
- Existe mayor riesgo de introducir errores si se implementa junto con visualizaciones de `splits` y niveles.

---

## 6. Comparación formal

| Criterio | Árbol B | Árbol B+ | Mejor opción para EduStruct |
|---|---|---|---|
| Simplicidad pedagógica | Alta | Media | Árbol B |
| Facilidad visual | Alta | Media | Árbol B |
| Facilidad de implementación | Alta | Media/Baja | Árbol B |
| Facilidad para exposición | Alta | Media | Árbol B |
| Compatibilidad con React Flow | Alta | Media | Árbol B |
| Tiempo de desarrollo | Menor | Mayor | Árbol B |
| Mantenibilidad | Alta | Media | Árbol B |
| Fidelidad a índices reales de BD | Media | Alta | Árbol B+ |
| Búsqueda eficiente | Alta | Alta | Empate |
| Splits visibles | Alta | Alta, pero más compleja | Árbol B |

---

## 7. Decisión técnica

La Épica 8 implementará un **Árbol B**.

No se implementará Árbol B+ en esta épica.

---

## 8. Justificación de la decisión

Se elige **Árbol B** porque cumple completamente el requerimiento formal del curso y se adapta mejor a los objetivos actuales de EduStruct.

La prioridad de esta épica no es construir un motor de base de datos real, sino demostrar correctamente los conceptos de:

- nodos con múltiples claves;
- búsqueda balanceada;
- inserción ordenada;
- división de nodos;
- crecimiento de altura;
- recorrido por niveles;
- visualización clara para defensa oral.

El Árbol B permite cubrir estos puntos con menor complejidad que un B+ y con una representación visual más limpia en React Flow.

En términos prácticos: el B+ es excelente para bases de datos reales, pero para una exposición universitaria visual puede meter demasiado ruido. El Árbol B explica lo esencial sin convertir el frontend en un tablero de conspiración con flechas por todos lados.

---

## 9. Diseño conceptual aprobado

La estructura base será:

```python
class BTreeNode:
    keys
    children
    leaf
```

```python
class BTree:
    root
    order
```

### Orden configurable

El árbol tendrá un `order` configurable.

Regla conceptual:

- máximo de claves por nodo: `order - 1`;
- máximo de hijos por nodo: `order`;
- el `order` mínimo aceptado será `3`.

Ejemplo:

```text
order = 4
máximo de claves por nodo = 3
máximo de hijos por nodo = 4
```

---

## 10. Operaciones que se implementarán en los siguientes steps

### Core backend

Archivo previsto:

```text
backend/app/structures/btree.py
```

Operaciones:

- crear árbol con orden configurable;
- insertar clave;
- dividir nodo lleno;
- buscar clave;
- obtener recorrido por niveles;
- calcular altura;
- obtener métricas;
- exportar estado interno seguro.

### Servicio

Archivo previsto:

```text
backend/app/services/btree_service.py
```

Responsabilidades:

- administrar instancia del árbol;
- validar payloads;
- cargar demo dataset;
- preparar respuestas para rutas;
- no mezclar lógica HTTP con lógica de estructura.

### Serialización React Flow

Archivo a extender:

```text
backend/app/serializers/react_flow_serializer.py
```

Función prevista:

```python
serialize_btree()
```

Cada nodo serializado incluirá:

```json
{
  "keys": [10, 20, 30],
  "leaf": false,
  "level": 2
}
```

### Rutas REST

Archivo previsto:

```text
backend/app/routes/btree.py
```

Endpoints previstos:

```text
GET    /api/btree/state
POST   /api/btree/insert
GET    /api/btree/search?key={key}
GET    /api/btree/traverse?type=levelorder
POST   /api/btree/demo/load
POST   /api/btree/reset
```

### Frontend

Archivos previstos:

```text
frontend/src/api/btree.js
frontend/src/pages/BTreePage.jsx
frontend/src/router/AppRouter.jsx
frontend/src/pages/HomePage.jsx
```

La página debe permitir:

- insertar claves;
- buscar claves;
- cargar demo;
- resetear árbol;
- mostrar nodos multi-clave;
- mostrar splits;
- mostrar altura;
- mostrar niveles;
- mostrar recorrido por niveles.

---

## 11. Dataset demo esperado

El demo debe basarse en expedientes académicos.

Fuente sugerida:

```text
datasets/records.json
```

También puede agregarse un dataset incremental específico si se necesita una secuencia controlada de claves para forzar `splits` visibles.

Archivo previsto si aplica:

```text
datasets/btree_records_demo.json
```

La secuencia demo debe provocar al menos:

- un split de hoja;
- un split que afecte la raíz;
- crecimiento de altura;
- varios niveles visibles.

---

## 12. Testing obligatorio en próximos steps

Se crearán pruebas para:

```text
backend/tests/structures/test_btree.py
backend/tests/services/test_btree_service.py
backend/tests/routes/test_btree_routes.py
backend/tests/serializers/test_react_flow_btree_serializer.py
```

Validaciones mínimas:

- inserciones ordenadas;
- splits correctos;
- búsqueda existente;
- búsqueda inexistente;
- recorrido por niveles;
- altura;
- niveles;
- serialización React Flow;
- invariantes del árbol según orden configurable.

---

## 13. Invariantes esperadas del Árbol B

Para `order = m`:

- cada nodo puede tener como máximo `m - 1` claves;
- cada nodo interno puede tener como máximo `m` hijos;
- las claves dentro de cada nodo están ordenadas;
- todos los hijos mantienen rangos válidos respecto a las claves del padre;
- todos los nodos hoja quedan al mismo nivel;
- la raíz puede tener menos claves que el mínimo normal;
- si la raíz no es hoja, debe tener al menos dos hijos;
- la altura crece únicamente cuando la raíz se divide.

---

## 14. Workflow Git para este step

Antes de iniciar la implementación de la épica:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-8-btree
```

Commit sugerido para este step:

```bash
git add docs/epic-8-step-1-btree-decision.md
git commit -m "docs(btree): define btree technical decision"
```

---

## 15. Estado del step

Estado: **Pendiente de validación del usuario**.

Decisión propuesta: **implementar Árbol B**.

No se debe avanzar al Step 2 hasta recibir validación explícita.

