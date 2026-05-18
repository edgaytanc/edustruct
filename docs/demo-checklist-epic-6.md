# EduStruct — Demo Checklist — Épica 6

## Árbol Binario BST y recorridos

### Preparación

```bash
git checkout feature/epic-6-binary-tree
```

Levantar servicios:

```bash
docker compose up --build
```

O ejecución local según entorno del proyecto.

## Backend

Validar endpoints principales:

```text
GET    /api/binary-tree/state
POST   /api/binary-tree/demo/load
POST   /api/binary-tree/insert
DELETE /api/binary-tree/delete
GET    /api/binary-tree/search
GET    /api/binary-tree/traverse?type=inorder
GET    /api/binary-tree/traverse?type=preorder
GET    /api/binary-tree/traverse?type=postorder
GET    /api/binary-tree/traverse?type=levelorder
POST   /api/binary-tree/reset
```

## Frontend

### Operaciones

- Cargar demo.
- Insertar un valor menor a la raíz.
- Insertar un valor mayor a la raíz.
- Buscar un valor existente.
- Buscar un valor inexistente.
- Eliminar hoja.
- Eliminar nodo con un hijo.
- Eliminar nodo con dos hijos.
- Reiniciar árbol.

### Recorridos animados

- Ejecutar `inorder`.
- Verificar que el orden sea ascendente en BST.
- Ejecutar `preorder`.
- Ejecutar `postorder`.
- Ejecutar `levelorder`.
- Cambiar velocidad.
- Pausar animación.
- Continuar animación.
- Reiniciar recorrido.
- Limpiar marcas.

## Explicación técnica para presentación

- El árbol binario se implementó manualmente en Python puro.
- La inserción sigue la propiedad BST: valores menores a la izquierda y mayores a la derecha.
- La eliminación conserva la propiedad BST usando sucesor inorder cuando el nodo tiene dos hijos.
- `inorder` devuelve los valores ordenados.
- `levelorder` reutiliza la cola manual implementada en la Épica 4.
- React Flow visualiza nodos, aristas, niveles y dirección izquierda/derecha.
- La animación se ejecuta en frontend a partir del orden calculado por backend.

## Cierre sugerido de épica

Cuando todos los tests y la demo estén validados:

```bash
git checkout develop
git pull origin develop
git merge feature/epic-6-binary-tree
git push origin develop
git branch -d feature/epic-6-binary-tree
git push origin --delete feature/epic-6-binary-tree
```
