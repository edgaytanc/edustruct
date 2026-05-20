# Épica 11 — Step 2 Hotfix: resolución de datasets en backend

## Problema detectado

Al ejecutar:

```bash
PYTHONPATH=. pytest
```

los nuevos tests del contexto de lista fallaban porque el backend no encontraba:

- `datasets/enrollments.json`
- `datasets/students.json`

El error observado era:

```text
DATASET_ERROR: El archivo de dataset solicitado no existe.
```

## Causa raíz

El backend dentro de Docker trabaja con:

```text
/app
```

porque `docker-compose.yml` monta:

```yaml
./backend:/app
```

Por lo tanto, la carpeta raíz del monorepo no queda disponible dentro del backend y la ruta:

```text
../datasets
```

no siempre existe desde el contenedor.

## Corrección aplicada

### 1. Loader robusto de datasets

Se actualizó:

```text
backend/app/utils/dataset_loader.py
```

Ahora el loader busca datasets en este orden:

1. variable de entorno `DATASETS_DIR`
2. `/datasets`
3. `Path.cwd()/datasets`
4. `Path.cwd().parent/datasets`
5. carpetas padre del archivo `dataset_loader.py`

Esto permite ejecutar correctamente en:

- entorno local
- contenedor Docker
- CI
- pruebas unitarias desde `backend/`

### 2. Montaje explícito de datasets en Docker

Se actualizó:

```text
docker-compose.yml
```

Agregando:

```yaml
environment:
  DATASETS_DIR: /datasets

volumes:
  - ./datasets:/datasets:ro
```

El volumen es de solo lectura porque el backend solo necesita consultar datasets demo, no modificarlos.

## Archivos modificados

```text
backend/app/utils/dataset_loader.py
docker-compose.yml
```

## Validación esperada

Después de aplicar el hotfix:

```bash
PYTHONPATH=. pytest
```

Debe resolver los datasets reales utilizados por la lista enlazada de inscritos.

## Justificación técnica

La estructura `LinkedList` no necesitaba cambios. El error estaba en infraestructura de lectura de datasets, no en la implementación de la lista ni en los servicios de negocio.

Este ajuste mantiene la separación por capas:

```text
structures -> lógica pura
services   -> caso de uso educativo
utils      -> lectura de datasets
routes     -> API REST
```
