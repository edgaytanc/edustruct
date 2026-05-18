# Épica 7 — Step 4: Frontend AVL

## Objetivo

Integrar la interfaz visual del Árbol AVL sobre la arquitectura frontend existente de EduStruct, reutilizando el patrón de API client, página React, React Flow, router y HomePage aplicado previamente en el Árbol Binario.

## Archivos creados

```text
frontend/src/api/avl.js
frontend/src/pages/AVLPage.jsx
```

## Archivos actualizados

```text
frontend/src/router/AppRouter.jsx
frontend/src/pages/HomePage.jsx
```

## Funcionalidad implementada

- Cliente API desacoplado para endpoints `/api/avl`.
- Página `AVLPage.jsx` con React Flow.
- Operaciones de usuario:
  - insertar valor
  - eliminar valor
  - buscar valor
  - cargar dataset demo
  - reiniciar árbol
  - ejecutar recorridos
- Visualización de metadata AVL por nodo:
  - altura interna
  - altura visual
  - factor de balance
  - bandera de desbalance
  - pivote de rotación
- Visualización de rotaciones:
  - LL
  - RR
  - LR
  - RL
- Panel de historial de rotaciones registradas.
- Vista comparativa antes/después cuando la operación devuelve snapshot previo.
- Métricas AVL:
  - cantidad de nodos
  - altura
  - niveles
  - balance de raíz
  - cantidad de rotaciones
  - estado balanceado
- Integración de ruta `/avl`.
- Tarjeta de acceso desde `HomePage`.

## Validación ejecutada

```bash
cd frontend
npm install
npm run build
```

Resultado:

```text
✓ built in 1.55s
```

## Nota técnica

El primer intento de build no encontró `vite` porque el ZIP recibido no incluía dependencias instaladas completas en `node_modules`. Se ejecutó `npm install` usando el `package-lock.json` existente y luego el build finalizó correctamente.

## Workflow Git sugerido

```bash
git add frontend/src/api/avl.js \
        frontend/src/pages/AVLPage.jsx \
        frontend/src/router/AppRouter.jsx \
        frontend/src/pages/HomePage.jsx \
        docs/epic-7-step-4-frontend-avl.md

git commit -m "feat(avl): add avl visualization page"
```

## Siguiente paso recomendado

Continuar con Step 5 para checklist/demo final, validación integral backend + frontend, documentación de cierre y preparación del merge hacia `develop`.
