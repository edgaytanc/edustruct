# EduStruct — Épica 6 — STEP 5

## Animación visual de recorridos del Árbol Binario

Este paso refina la experiencia visual del árbol binario BST agregando animación progresiva para los recorridos clásicos.

## Archivo actualizado

```text
frontend/src/pages/BinaryTreePage.jsx
```

## Cambios implementados

- Animación paso a paso para recorridos:
  - `preorder`
  - `inorder`
  - `postorder`
  - `levelorder`
- Control de velocidad:
  - lenta
  - normal
  - rápida
- Controles de ejecución:
  - ejecutar
  - pausar
  - continuar
  - reiniciar recorrido
  - limpiar marcas visuales
- Barra de progreso del recorrido.
- Resaltado visual del nodo actual.
- Diferenciación visual entre nodos visitados y nodos pendientes.
- Aristas animadas conforme avanza el recorrido.
- Conservación de la separación de responsabilidades:
  - Backend calcula el recorrido.
  - Frontend anima la secuencia recibida.

## Decisión técnica

La animación no recalcula el árbol en el cliente. El backend sigue siendo la fuente de verdad para:

- estructura del BST
- recorridos
- métricas
- nodos y aristas serializados

El frontend solamente interpreta `traversal.order` y `traversal.steps` para pintar estados visuales temporales.

## Validación manual recomendada

1. Ejecutar backend y frontend.
2. Abrir la página de Árbol Binario.
3. Cargar demo.
4. Ejecutar `inorder` y confirmar que los valores se muestran ordenados.
5. Ejecutar `preorder`, `postorder` y `levelorder`.
6. Probar velocidades lenta, normal y rápida.
7. Pausar y continuar una animación.
8. Reiniciar recorrido.
9. Limpiar marcas visuales.
10. Insertar, buscar y eliminar valores después de animar.

## Commit sugerido

```bash
git add .
git commit -m "feat(binary-tree): animate traversal visualization"
```
