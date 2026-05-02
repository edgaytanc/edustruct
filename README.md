# EduStruct

Visualizador Interactivo de Estructuras de Datos aplicado al contexto educativo.

## Descripción

EduStruct es una aplicación web interactiva que permite visualizar y manipular estructuras de datos como árboles, grafos, tablas hash, listas, pilas y colas dentro de un contexto educativo.

La arquitectura base del proyecto es:

```text
Frontend React + Vite → API REST Flask → Lógica de estructuras en Python
```
## Stack tecnológico
- Backend: Python + Flask
- Frontend: React + Vite
- Estilos: Tailwind CSS
- Visualización futura: React Flow
- Comunicación: API REST con JSON
- Contenedores: Docker + Docker Compose

## Estructura del proyecto

edustruct/
├── backend/
├── frontend/
├── docs/
├── datasets/
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md

## Requisitos
Para ejecución local:

- Python 3.12+
- Node.js 22+
- npm

Para ejecución con Docker:

- Docker
- Docker Compose

## Configuración inicia

Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/edustruct.git
cd edustruct
```
Crear archivos de entorno:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

## Ejecutar backend localmente
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Backend disponible en:
```
http://localhost:5000
```

Endpoint de prueba:
```bash
curl http://localhost:5000/api/health
```

## Ejecutar frontend localmente
En otra terminal:

```bash
cd frontend
npm install
npm run dev
```
Frontend disponible en:
```
http://localhost:5173
```

## Ejecutar todo con Docker

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Servicios disponibles:

`docker compose psFrontend:` http://localhost:5173
`Backend:`  http://localhost:5000
`API test:` http://localhost:5000/api/health


Para detener los contenedores:

```bash
docker compose down
```

## Flujo de ramas
```
main                    → versión estable
develop                 → integración
feature/epica-1-setup   → configuración inicial del proyecto
```


## Estado actual
- Monorepo creado
- Backend Flask funcionando
- Frontend React funcionando
- Comunicación frontend-backend validada
- Docker Compose funcionando