# EduStruct — Validación Final Épica 6

## Objetivo

Validar que la implementación de Árbol Binario está integrada correctamente antes de cerrar la rama `feature/epic-6-binary-tree`.

## Checklist técnico

### Backend

- [ ] `backend/app/structures/binary_tree.py` existe.
- [ ] `backend/app/services/binary_tree_service.py` existe.
- [ ] `backend/app/routes/binary_tree.py` usa `BinaryTreeService`.
- [ ] `backend/app/routes/__init__.py` registra `binary_tree_bp`.
- [ ] `backend/app/serializers/react_flow_serializer.py` contiene `serialize_binary_tree`.
- [ ] El recorrido `levelorder` usa la cola manual del proyecto.
- [ ] No se usan librerías externas para implementar el árbol.

### Frontend

- [ ] `frontend/src/api/binaryTree.js` existe.
- [ ] `frontend/src/pages/BinaryTreePage.jsx` existe.
- [ ] `frontend/src/router/AppRouter.jsx` registra la ruta del árbol binario.
- [ ] `frontend/src/pages/HomePage.jsx` enlaza hacia la página del árbol binario.
- [ ] React Flow muestra nodos y aristas correctamente.
- [ ] La animación de recorridos resalta nodos en orden.

### Documentación

- [ ] La documentación previa no fue sobrescrita.
- [ ] Se agregaron documentos incrementales de Épica 6.
- [ ] Existe checklist demo para la épica.
- [ ] Existe resumen de cierre.

## Comandos de validación sugeridos

Desde la raíz del proyecto:

```bash
cd backend
python -m pytest
```

Desde la raíz del proyecto:

```bash
cd frontend
npm install
npm run build
```

Con Docker:

```bash
docker compose up --build
```

Validar en navegador:

```text
http://localhost:5173/binary-tree
```

Validar backend:

```text
http://localhost:5000/api/binary-tree/state
```

## Prueba funcional mínima

1. Cargar demo.
2. Ejecutar recorrido inorder.
3. Confirmar que el orden sea ascendente.
4. Insertar un nuevo valor.
5. Buscar el valor insertado.
6. Eliminar una hoja.
7. Ejecutar preorder.
8. Ejecutar postorder.
9. Ejecutar levelorder.
10. Reiniciar el árbol.

## Criterios de aceptación

La Épica 6 se considera cerrada si:

- todos los tests backend pasan;
- el frontend compila;
- el demo visual permite explicar los cuatro recorridos;
- la documentación incremental queda agregada;
- la rama se fusiona a `develop` sin conflictos.
