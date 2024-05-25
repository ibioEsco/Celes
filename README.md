# Api-celes

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)

Es  una API  construida con FastAPI.

## Descripción

Es una Api que permite gestionar ventas de empleados, productos y tiendas. Proporciona endpoints para obtener información sobre ventas y realizar autenticaciones.

## Características

- Autenticación de usuarios con JWT
- Obtener ventas por empleado, producto y tienda
- Obtener promedios de ventas por empleado, producto y tienda

## Configuracion de entorno de FireStore
Configuracion la variable de entorno GOOGLE_APPLICATION_CREDENTIALS para apuntar a tu archivo de credenciales de cuenta de servicio

-   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-file.json"


## Uso
Endpoints disponibles:

- POST /token: Autenticar y obtener un token de acceso
- POST /sales/by_employee/{employee}: Obtener ventas por empleado
- POST /sales/by_product/{product}: Obtener ventas por producto
- POST /sales/by_store/{store}: Obtener ventas por tienda
- POST /sales/total_avg_by_employee/{avg_employee}: Obtener promedio de ventas por empleado
- POST /sales/total_avg_by_product/{avg_product}: Obtener promedio de ventas por producto
- POST /sales/total_avg_by_store/{avg_store}: Obtener promedio de ventas por tienda

## Instalación

sigue estos pasos para configurar y ejecutar el proyecto localmente:

- python3 -m venv venv  -> nos permite instalalar una maquina virtual y asi tener nuestros paquetes instalado en un ambiente aparte
- pip install -r requirements.txt  -> Permite instalar los paquete localmente
- pip install -e .  -> instalacion por medio del archivo setup.py
- pip install google-cloud-firestore -> Asegurece de tener instalado la bibiblioteca de firestore

## Ejecución

- uvicorn app.main:app --reload -> Se ejecuta la aplicacion


## Pruebas
Ejecuta las pruebas utilizando unittest:

- python -m unittest discover -s tests -> con este comando nos permite ejecutar las pruebas


## Contribución
Las contribuciones son bienvenidas. Por favor sigue estos pasos para contribuir:

- Clonar el proyecto https://github.com/ibioEsco/Celes.git
- Crea una rama para tu característica (git checkout -b feature/nueva-caracteristica)
- Realiza los commits necesarios (git commit -m 'Agregar nueva característica')
- Envía tus cambios (git push origin feature/nueva-caracteristica)
- Crea un Pull Request


### Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más información.

### Requisitos previos

- Python 3.9 o superior
- Pipenv (opcional, pero recomendado) o pip

### Contacto

Ibio Antonio Escobar Gomez  - ibiotec30@gmail.com

Enlace al Proyecto: https://github.com/ibioEsco/Celes

