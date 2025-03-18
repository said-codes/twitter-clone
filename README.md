# Django-Vue.js To-Do App

Este proyecto es un clone de twitter que utiliza Django para el backend y Vue.js para el frontend.

## Requisitos previos

Asegúrate de tener instalados los siguientes programas antes de comenzar:
- Python 3.x
- Node.js
- npm (Node Package Manager)
- Virtualenv (opcional, pero recomendado para el entorno de Python)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/said-codes/twitter-clone.git
cd twitter-clone
```

### 2. Configurar el backend (Django)

```bash
cd Backend/src
```

#### a) Crear y activar un entorno virtual

```bash
python -m venv env
source env/bin/activate  # En Windows, usa 'env\Scripts\activate'
```

#### b) Instalar dependencias

```bash
pip install -r requirements.txt
```

#### c) Realizar migraciones y configurar la base de datos

```bash
python manage.py migrate
```

#### d) Ejecutar el servidor de Django

```bash
python manage.py runserver
```

El servidor estará disponible en `http://127.0.0.1:8000/`.

### 3. Configurar el frontend (Vue.js)

En una nueva terminal:

```bash
cd ../../frontend
```

#### a) Instalar dependencias de Vue.js

```bash
npm install
```

#### b) Ejecutar el servidor de desarrollo de Vue.js

```bash
npm run serve
```

El servidor de Vue.js estará disponible en `http://localhost:8080/`.

## Notas adicionales

- Asegúrate de que tanto Django como Vue.js estén ejecutándose simultáneamente.
- Si encuentras problemas con CORS, instala y configura `django-cors-headers` en el backend.
- Para despliegue en producción, se recomienda compilar Vue.js y servir los archivos estáticos desde Django.

## Autor

Proyecto desarrollado por [said-codes](https://github.com/said-codes).

