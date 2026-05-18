# EduStruct — Checklist de Demo Épica 5

## Objetivo de la demo

Demostrar la implementación completa del Árbol General aplicado al pensum académico universitario.

## Preparación previa

### Backend

Desde la raíz del proyecto:

```bash
cd backend
python -m pytest tests/structures/test_general_tree.py
python -m pytest tests/services/test_tree_service.py
python -m pytest tests/routes/test_tree_routes.py
```

### Frontend

```bash
cd frontend
npm install
npm run build
npm run dev
```

### Docker, si se desea validar integrado

```bash
docker compose up --build
```

## Flujo sugerido de demostración

### 1. Presentar el caso educativo

Explicar que el Árbol General representa una jerarquía académica:

```text
Facultad → Carrera → Ciclos → Cursos
```

Puntos clave:

```text
- Cada nodo puede tener múltiples hijos.
- Es una estructura no binaria.
- Sirve para modelar pensum, organización académica o menús jerárquicos.
```

### 2. Mostrar carga del dataset demo

Acción en UI:

```text
Clic en cargar demo
```

Resultado esperado:

```text
Facultad de Ingeniería
Ingeniería en Sistemas
Ciclo 1
Ciclo 2
Matemática I
Introducción a la Programación
Programación I
Matemática II
```

Validar visualmente:

```text
- nodos visibles
- aristas padre-hijo
- distribución por niveles
```

### 3. Mostrar métricas

Explicar métricas esperadas del demo:

```text
Nodos: 8
Aristas: 7
Altura: 3
Niveles: 4
Hojas: 4
Máximo de hijos: 2
```

Interpretación:

```text
Altura 3 significa que el nivel más profundo está en cursos.
Niveles 4 corresponde a Facultad, Carrera, Ciclos y Cursos.
```

### 4. Insertar un nodo

Ejemplo:

```text
id: physics-1
label: Física I
parentId: cycle-1
category: course
```

Resultado esperado:

```text
- Se agrega Física I bajo Ciclo 1.
- Incrementa la cantidad de nodos.
- Incrementa la cantidad de aristas.
- React Flow se actualiza.
```

### 5. Buscar un nodo

Ejemplo:

```text
math-1
```

Resultado esperado:

```text
- El nodo se encuentra.
- Se muestra su nivel.
- La UI lo resalta o muestra el resultado de búsqueda.
```

### 6. Ejecutar recorridos

Probar:

```text
levelorder
preorder
postorder
```

Explicación breve:

```text
levelorder: recorre por niveles usando Queue.
preorder: visita padre antes que hijos.
postorder: visita hijos antes que padre.
```

Punto técnico importante:

```text
El recorrido levelorder reutiliza la cola manual implementada en la Épica 4.
```

### 7. Eliminar un nodo con subárbol

Ejemplo:

```text
cycle-1
```

Resultado esperado:

```text
- Se elimina Ciclo 1.
- También se eliminan sus cursos hijos.
- Disminuye la cantidad de nodos.
- Se actualiza el grafo.
```

Explicación:

```text
Eliminar un nodo de un árbol general elimina el subárbol completo.
```

### 8. Reiniciar árbol

Acción:

```text
Clic en reset
```

Resultado esperado:

```text
- El árbol queda vacío.
- Métricas vuelven a cero.
- No hay nodos ni aristas visibles.
```

## Endpoints para validación rápida

```text
GET    /api/tree/state
POST   /api/tree/demo/load
POST   /api/tree/insert
DELETE /api/tree/delete
GET    /api/tree/search?id=math-1
GET    /api/tree/traverse?type=levelorder
GET    /api/tree/metrics
POST   /api/tree/reset
```

## Comandos Git de cierre

```bash
git status
git add .
git commit -m "test(tree): strengthen general tree test coverage"
git commit -m "docs(epic-5): add general tree demo checklist"
```

Merge hacia `develop` después de validar:

```bash
git checkout develop
git pull origin develop
git merge feature/epic-5-general-tree
git push origin develop
git branch -d feature/epic-5-general-tree
git push origin --delete feature/epic-5-general-tree
```

## Checklist final

```text
[ ] Backend inicia sin errores.
[ ] Frontend inicia sin errores.
[ ] Se carga el demo académico.
[ ] Se visualizan nodos y aristas.
[ ] Se inserta un curso nuevo.
[ ] Se busca un nodo existente.
[ ] Se muestra nodo no encontrado cuando aplica.
[ ] Se ejecuta levelorder.
[ ] Se ejecuta preorder.
[ ] Se ejecuta postorder.
[ ] Se elimina un subárbol.
[ ] Las métricas se actualizan.
[ ] Reset deja el árbol vacío.
[ ] Tests backend pasan.
```
